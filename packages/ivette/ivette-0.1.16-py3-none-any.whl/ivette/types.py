from dataclasses import dataclass

@dataclass
class ThermoData:
    def __init__(self, energy=None, enthalpy=None, entropy=None, gibbs=None, potential=None):
        self.energy = energy
        self.enthalpy = enthalpy
        self.entropy = entropy
        self.gibbs = gibbs
        self.potential = potential
