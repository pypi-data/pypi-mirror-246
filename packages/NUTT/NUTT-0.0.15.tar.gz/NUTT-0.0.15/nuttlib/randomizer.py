"""This module helps with rand init of weights and biases."""



class Randomizer:
    def __init__(self) -> None:
        pass

    def random(self) -> float:
        with open("/dev/random", "rb") as f:
            rand = int.from_bytes(f.read(8), "big")
        return ((rand / 2**63) - 1) if rand < 2**63 else ((rand - 2**63) / 2**63) # convert to float in range [-1, 1)