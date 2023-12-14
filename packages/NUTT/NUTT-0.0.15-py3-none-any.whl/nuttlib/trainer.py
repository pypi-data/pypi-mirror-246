"""Trainer, the main class for training and testing the model."""

from .mat import Mat
import logging



class Trainer:
    def __init__(self, network):
        self.network = network
        self.loss = None

    def train(self, xs: Mat, ys: Mat, eta: float, epochs: int) -> None:
        if not isinstance(xs, Mat) or not isinstance(ys, Mat):
            raise TypeError("xs and ys must be Mats")
        for epoch in range(epochs):
            for x, y in zip(xs.data, ys.data):
                x, y = float(x[0]), float(y[0])
                logging.debug(f"x: {x}\ny: {y}\ntype(x): {type(x)}\ntype(y): {type(y)}")
                ypred = self.network.fwd(x)

                logging.debug(f"ypred: {ypred}\ntype(ypred): {type(ypred)}")
                self.loss = self.network.layers[-1].neurons[0].J(y, ypred)

                self.network.bwd(x, y, eta)

            if epoch % 1000 == 0:
                logging.info(f"epoch {epoch + 1}: loss = {self.loss}")

"""
for epoch in range(epochs):
    z = np.dot(x, w) + b
    ypred = sigmoid(z).flatten()

    loss = J(y, ypred)

    grad = dJ(y, ypred)
    dw = np.dot(x.T, grad) / len(y) # derivative of loss with respect to w
    db = np.mean(grad) # derivative of loss with respect to b

    w -= eta * dw # update w
    b -= eta * db # update b

    if epoch % 1000 == 0:
        print(f"epoch {epoch + 1}: w = {w}, b = {b}, loss = {loss}")

print(f"final loss: {loss}")
"""