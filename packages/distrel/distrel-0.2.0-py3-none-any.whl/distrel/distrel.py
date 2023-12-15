"""Main module for the distrel package."""

# Python imports
import logging
import random

# Module imports
import numpy as np
import nevergrad as ng
import torch
import tqdm

logger = logging.getLogger(__name__)


class drn:
    """Distribution Relation Network Class."""

    def __init__(self, gen, calc, properties=None, seed=None):
        """Initialise the distribution relation network (drn) class.

        Args:
           gen (function) : Function to generate the training data.
           calc (function) : Function to calculate the parameter c from the
                neural network input and output.
           properties (list, optional) : A list of 3 dictionaries each
                containing the mean and variance for each distribution.
        """
        if not hasattr(gen, '__call__'):
            logger.critical("gen function has no `__call__` attribute.")
            raise TypeError("Generator must be callable.")
        if not hasattr(calc, '__call__'):
            logger.critical("calc function has no `__call__` attribute.")
            raise TypeError("Calculator must be callable.")

        if seed is not None:
            torch.manual_seed(seed)
            random.seed(seed)
            np.random.seed(seed)

        self._gen = gen
        self._calc = calc
        if properties is not None:
            self.set_properties(properties)

        self.layer1 = torch.nn.Linear(1, 1)
        self.layer2 = torch.nn.Linear(1, 1)
        self.layer3 = torch.nn.Linear(1, 1)
        self.act = torch.nn.LeakyReLU()
        self.net = torch.nn.ModuleList([self.layer1, self.layer2, self.layer3])

        self.criterion = torch.nn.MSELoss()
        self.optim = torch.optim.AdamW
        self.tol = 0
        self.early_stop = False

    def _set_weights(self, biases, weights):
        for i, layer in enumerate((self.layer1, self.layer2, self.layer3)):
            layer.bias = torch.nn.Parameter(self._as_tensor([biases[i]]))
            layer.weight = torch.nn.Parameter(self._as_tensor([[weights[i]]]))

    def _oneshot(self, bias, weights, N):
        self._set_weights(bias, weights)
        a = self.gen(N)
        b = self.forward(a)
        return self.loss(a, b).item()

    def gen(self, *args, **kwargs):
        """Generate the data."""
        out = self._gen(*args, **kwargs)
        out = self._as_tensor(out.reshape(-1, 1))
        out = (out - self.properties[0]["mean"]) / self.properties[0]["var"]
        return out

    def calc(self, *args, **kwargs):
        """Calculate the output."""
        out = self._calc(*args, **kwargs)
        out = out.reshape(-1, 1)
        return self._as_tensor(out)

    def _as_tensor(self, out):
        """Check and format output as tensor."""
        if not isinstance(out, torch.Tensor):
            out = torch.tensor(out, dtype=torch.float32)
        elif out.dtype != torch.float32:
            out = torch.as_tensor(out, dtype=torch.float32)
        return out

    def forward(self, a, deterministic=False):
        """Forward pass of the network."""
        hidden1 = self.act(self.layer1(a))
        mu = self.layer2(hidden1)

        if deterministic:
            return mu
        logvar = self.layer3(hidden1)

        std = torch.exp(logvar)
        eps = torch.randn_like(std)
        return eps.mul(std).add_(mu)

    def predict(self, a):
        """Make a prediction for the network."""
        self.net.eval()
        a = self._as_tensor(a).reshape(-1, 1)
        a = (a - self.properties[0]["mean"]) / self.properties[0]["var"]
        out = self.forward(a)
        return out * self.properties[1]["var"] + self.properties[1]["mean"]

    def _check_properties(self, properties):
        """Check the properties."""
        assert len(properties) == 3

    def set_properties(self, *args):
        """Set the values for the distribution properties."""
        self._check_properties(args)
        props = []
        for p in args:
            metrics = dict()
            for m in list(p.keys()):
                metrics[m] = self._as_tensor(p[m])
            props.append(metrics)

        self.properties = props

    def skew(self, x):
        """Calculate the Fisher-Pearson coefficient of skewness for x."""
        mu = torch.mean(x)
        m2 = torch.mean((x - mu) ** 2)
        m3 = torch.mean((x - mu) ** 3)
        return m3 / (m2 ** (3/2))

    def kurt(self, x):
        """Calculate the Fisher kurtosis of x."""
        m4 = torch.mean((x - torch.mean(x)) ** 4)
        return m4 / (torch.var(x) ** 2) - 3

    def loss(self, a, b):
        """Calculate the loss of the network."""
        c = (
            self.calc(
                a * self.properties[0]["var"] + self.properties[0]["mean"],
                b * self.properties[1]["var"] + self.properties[1]["mean"],
            ) - self.properties[2]["mean"]
        ) / self.properties[2]["var"]

        rtn_loss = torch.zeros(1)
        tol_fail = False
        for i, v in enumerate((b, c)):
            props = self.properties[i]

            mean = torch.mean(v)
            var = torch.var(v)
            skew = self.skew(v)
            kurt = self.kurt(v * props["var"])

            if "mean" in list(props.keys()):
                _loss = self.criterion(mean, torch.zeros_like(mean))
                if not torch.isnan(_loss) and not torch.isinf(_loss):
                    if _loss > self.tol:
                        tol_fail = True
                        rtn_loss += _loss
            if "var" in list(props.keys()):
                _loss = self.criterion(var, torch.ones_like(var))
                if not torch.isnan(_loss) and not torch.isinf(_loss):
                    if _loss > self.tol:
                        tol_fail = True
                        rtn_loss += _loss
            if "skew" in list(props.keys()):
                _loss = self.criterion(skew, props["skew"]) / props["skew"]
                if not torch.isnan(_loss) and not torch.isinf(_loss):
                    if _loss > self.tol:
                        tol_fail = True
                        rtn_loss += _loss
            if "kurt" in list(props.keys()):
                _loss = self.criterion(kurt, props["kurt"]) / props["kurt"]
                if not torch.isnan(_loss) and not torch.isinf(_loss):
                    if _loss > self.tol:
                        tol_fail = True
                        rtn_loss += _loss

        if not tol_fail:
            self.early_stop = True
            if rtn_loss == 0:
                rtn_loss = _loss

        return rtn_loss

    def train(
            self,
            max_epochs=100,
            tol=0,
            progress_bar=False,
            size=10000,
            lr=1e-2,
            require_closure=False,
            optim=None,
            optim_kwargs=None,
            **kwargs,
    ):
        """Trains the network."""
        self.tol = tol
        self.early_stop = False

        self.grad_free_opt(**kwargs)

        if optim is None:
            optim = self.optim(self.net.parameters(), lr=lr)
        else:
            optim_kwargs = dict() if optim_kwargs is None else optim_kwargs
            optim = optim(self.net.parameters(), lr=lr, **optim_kwargs)

        if progress_bar:
            t = tqdm.trange(max_epochs, desc="Loss: ...")
        else:
            t = range(max_epochs)
        for i, _ in enumerate(t):

            a = self.gen(size)

            def closure():
                optim.zero_grad()
                b = self.forward(a)
                loss = self.loss(a, b)
                if loss.requires_grad:
                    loss.backward()
                return loss

            if require_closure:
                optim.step(closure)
                loss = closure()
            else:
                loss = closure()
                optim.step()

            if progress_bar:
                t.set_description(f"Loss: {loss.item():.4}%")
                t.refresh()
            if self.early_stop:
                logger.info(
                    f"Breaking after {i + 1} epochs with loss {loss.item()}"
                )
                if torch.isnan(loss) or torch.isinf(loss):
                    return False
                return True

        return False

    def grad_free_opt(self, N=1000, budget=100):
        """Optimises the drn through gradient free methods."""
        biases = ng.p.Tuple(ng.p.Scalar(), ng.p.Scalar(), ng.p.Scalar())
        weights = ng.p.Tuple(ng.p.Scalar(), ng.p.Scalar(), ng.p.Scalar())
        instru = ng.p.Instrumentation(biases, weights, N)

        optimiser = ng.optimizers.NGOpt(parametrization=instru, budget=budget)
        recommendation = optimiser.minimize(self._oneshot)

        print(recommendation)
        biases, weights = recommendation.value[0][:2]
        self._set_weights(biases, weights)

    def __repr__(self):
        """Text for repr() calls."""
        _repr = (
            "drn with the properties:\n"
            f"gen:\t{self.gen}\n"
            f"calc:\t{self.calc}\n"
            f"properties:\t{self.properties}\n"
        )
        return _repr

    def __str__(self):
        """Text for str() calls."""
        _str = (
            "        _l2_ mu\n"
            "in _l1_/\n"
            "       \_l3_ sigma\n"
            "out ~ N(mu, sigma)\n"
            "---\n"
            f"l1:\n{self.layer1}\n"
            f"Bias: {self.layer1.bias.item()}\nWeight: {self.layer1.weight.item()}\n"
            f"l2:\n{self.layer2}\n"
            f"Bias: {self.layer2.bias.item()}\nWeight: {self.layer2.weight.item()}\n"
            f"l3:\n{self.layer3}\n"
            f"Bias: {self.layer3.bias.item()}\nWeight: {self.layer3.weight.item()}\n"
        )
        return _str
