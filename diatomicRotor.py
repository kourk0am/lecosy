from __future__ import division
import numpy as np

class DiatomicRotor(object):
    """This class represents a diatomic molecule (currently known species is HD, normalH2, paraH2, orthoH2
    and generic: this one sets B and g_nuc according to the supplied named arguments)
    Rotational constant B is in Kelvin.
    nuclearDegeneracies g_nuc = [nucDeg for J even, nuc deg for J odd]
    If even or odd J values are not allowed set the corresponding entry to 0,
    eg g_nuc = [3, 0] if odd J levels are not allowed and even ones have degeneracy 3. """

    def __init__(self, species, Jmax = 100,  debug = 0, B = 1, g_nuc = [1,1]):

        assert Jmax >0, "Jmax>0"
        assert type(Jmax) == int, "Jmax must be integer"
        self.Jmax = Jmax
        self.debug = debug

        #dict of known species and their properties
        knownSpecies = {"HD": {"B" : 65.681716, "g_nuc" : [6, 6]},
                        "normalH2": {"B":87.567467, "g_nuc": [1, 3]},
                        "paraH2": {"B":87.567467, "g_nuc": [1, 0]},
                        "orthoH2": {"B":87.567467, "g_nuc": [0, 3]},
                        "generic": {"B": B, "g_nuc": g_nuc}
                                  }
        assert species in knownSpecies, "Unknown species"
        self.species = species

        # set the rotational constant
        self.B = knownSpecies[species]["B"]
        if self.debug > 0:
            print "Known species", self.species,"  Setting rotational constant B =", self.B, "K"

        # set the nuclear degeneracies
        self.g_nuc = knownSpecies[species]["g_nuc"]
        if self.debug > 0:
            print "Known species", self.species,"  Setting nuclear degeneracies to", self.g_nuc

        #determine which rotational levels are available
        self.Jonly = "all"
        if self.g_nuc[0] == 0:
            self.Jonly = "odd"
        if self.g_nuc[1] == 0:
            self.Jonly = "even"

        # generaging all available J values
        if self.Jonly == "all":
            self.allJ = np.array(range(Jmax))
        elif self.Jonly == "even":
            self.allJ = np.array(range(0, Jmax, 2))
        elif self.Jonly == "odd":
            self.allJ = np.array(range(1, Jmax, 2))

        #some arrays to speed up computation of partition sums:
        #np array of nuclear degeneracies of all available leveles
        self.all_g_nuc = [self.nuclearDegeneracy(J) for J in self.allJ]
        self.all_g_nuc = np.array(self.all_g_nuc)

        #np array of rotational degeneracies of all available leveles
        self.all_g_rot = [self.rotationalDegeneracy(J) for J in self.allJ]
        self.all_g_rot = np.array(self.all_g_rot)

        #np array of total degeneracies of all available leveles
        self.all_g = self.all_g_rot*self.all_g_nuc


    def nuclearDegeneracy(self, J):
        """returns nuclear degeneracy of given state"""
        return self.g_nuc[J%2]

    def rotationalDegeneracy(self, J):
        """Returns rotational degeneracy of state with given J. """
        return 2*J +1

    def degeneracy(self,J):
        """Returns degeneracy of given level (nuclear and rotational only)"""
        return self.rotationalDegeneracy(J)*self.nuclearDegeneracy(J)

    def energy(self, J):
        """returns rotational energy of given level"""
        return self.B*J*(J+1)

    def partSum(self, T):
        """returns partition sum for the given species at given temperature"""
        elements = self.all_g*np.exp(-self.energy(self.allJ)/T)
        return elements.sum()

    def population(self, T, J):
        """returns population of given level J at temperature T"""
        return self.degeneracy(J)*np.exp(-self.energy(J)/T)/self.partSum(T)

    def populations(self, T):
        """returns np.array of populations of all levels in self.allJ"""
        pop = []
        for J in self.allJ:
            pop.append(self.population(T,J))
        return np.array(pop)
