"""Neuron, the basic unit of a neural network."""

from .mat import Mat
from .randomizer import Randomizer
import logging



class Neuron:
    def __init__(self, nInputs: int, bias: float) -> None:
        self.rand = Randomizer()
        self.weights = self.init_weights(nInputs)
        self.bias = bias
        self.output = None
        self.error = None
        self.activation = None

    def init_weights(self, nInputs: int) -> Mat:
        w = [[self.rand.random()] for _ in range(nInputs)]
        return Mat(nInputs, 1, w)

    def update_weights(self, x: float, eta: float, delta: float) -> None:
        grad = self.calc_grad(delta)
        deltaW = eta * x * grad
        for row in range(self.weights.rows):
            for col in range(self.weights.cols):
                self.weights.data[row][col] -= deltaW
        self.bias -= eta * grad

    def calc_grad(self, delta: float) -> float:
        if not isinstance(delta, float):
            raise TypeError(f"delta must be a float\ntype(delta): {type(delta)}: {delta}")
        return delta * self.dSigmoid()

    def sigmoid(self, x: float) -> float:
        return 1 / (1 + self.exp(-x))

    def exp(self, x: float) -> float:
        if x == 0:
            return 1.0
        else:
            term = 1
            result = 1
            for i in range(1, 100):
                term *= x / i
                result += term
            return result

    def dSigmoid(self) -> float:
        s = self.sigmoid(self.output)
        return s * (1 - s)

    def stimulate(self, x: float) -> float: # ^ stroke it, baby
        # if x.shape[0] != self.weights.shape[0] or x.shape[1] != 1:
        #     raise ValueError(f"Inputs must be a col vect of the same dims as the weights\nCol vect dims: {x.shape}\nWeights dims: {self.weights.shape}")
        wSum = x * self.weights
        logging.debug(f"wSum: {wSum}\ntype(wSum): {type(wSum)}")
        wSum = wSum.sum
        wSum += self.bias
        return wSum

    def activate(self, x: float) -> None:
        logging.debug(f"weights: {self.weights}\nx: {x}")
        wSum = self.stimulate(x)
        self.output = self.sigmoid(wSum)

    # def calc_err(self, target: float) -> None:
    #     self.error = 0.5 * ((target - self.output) ** 2) # MSE
    #     return self.error

    def J(self, y: float, ypred: float) -> float: # cross-entropy
        ypred = max(min(ypred, 1 - 1e-15), 1e-15)
        loss = - (y * self.ln(ypred) + (1 - y) * self.ln(1 - ypred))
        return loss

    def dJ(self, y: float, ypred: float) -> float: # derivative of cross-entropy
        if ypred == 0 or ypred == 1:
            ypred = max(min(ypred, 1 - 1e-15), 1e-15)
        return - (y / ypred - (1 - y) / (1 - ypred))

    def ln(self, x: float) -> float:
        if x <= 0:
            raise ValueError(f"x must be positive\nx = {x}")
        else:
            n = 0
            while x > 2:
                x /= 2
                n += 1

            x -= 1
            term = x
            res = term
            i = 2

            while i < 200:
                term *= -x * (i - 1) / i
                res += term
                i += 1

            return res + n * 0.6931471805599453