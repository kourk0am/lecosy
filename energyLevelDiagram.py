#this assumes you use matplotlib.pyplot

class Level(object):
    """Class to represent an energy level. Contains basic info unique to to level. """
    def __init__(self, energy, degeneracy = 1, label = "", color = "k"):
        self.energy = energy
        self.degeneracy = degeneracy
        self.label = label
        self.color = color



class LevelGroup(object):
    """Group of energy levels that will be plotted with common x coordiate (i.e. on top of each other).
    It contains information that is common to all levels in the group."""
    def __init__(self, startX = 1, length = 1, label = ""):
        self.startX = startX
        self.length = length
        self.label = label
        self.levels = []

    def add_level(self, energy, degeneracy = 1, label = "", color = "k"):
        level = Level(energy, degeneracy = degeneracy, label = label, color = color)
        self.levels.append(level)
        return level


class EnergyLevelDiagram(object):
    """Collection of groups of energy levels. Contains information that is common to all level groups. """
    def __init__(self, levelLength = 1, levelSpacing = 1, fontsize = 10,
                 levelLabelOffsetX = 0, levelLabelOffsetY = 0, groupLabelY = 0,
                 groupLabelOffsetX = 0, yAxisLabel = "Energy (K)"):
        self.levelLength = levelLength
        self.levelSpacing = levelSpacing
        self.fontsize = fontsize
        self.levelLabelOffsetX = levelLabelOffsetX
        self.levelLabelOffsetY = levelLabelOffsetY
        self.yAxisLabel = yAxisLabel
        self.groupLabelY = groupLabelY
        self.groupLabelOffsetX = groupLabelOffsetX
        self.levelGroups = []

    def add_level_group(self, groupLabel):
        """Creates a level group in the diagram. """
        startX = len(self.levelGroups)*(self.levelLength + self.levelSpacing)
        group = LevelGroup(startX = startX, length = self.levelLength, label = groupLabel)
        self.levelGroups.append(group)

    def add_level(self, energy, index = -1, #add the level to the last created group by default
                  degeneracy = 1, label = "", color = "k"):
        """Adds a level to specified group (specified by index). The default is to add level to the
        last created group. """
        group = self.levelGroups[index]
        group.add_level(energy, degeneracy = degeneracy, label = label, color = color)

    def plot_levels(self, ax):
        """Plots the energy level diagram. Needs axes - this is useful when the diagram is to become
        part of larger multiplot. """
        for group in self.levelGroups:
            for level in group.levels:
                #get data to plot the level line
                y = level.energy
                startX = group.startX
                endX = group.startX + group.length
                color = level.color
                #plot the level
                ax.hlines(y, startX, endX, color = color)

                #add level label
                labelX = group.startX + self.levelLabelOffsetX
                labelY = level.energy + self.levelLabelOffsetY
                text = level.label
                fontsize = self.fontsize
                ax.text(labelX, labelY, text, fontsize = fontsize)

            #add group label
            labelX = group.startX + self.groupLabelOffsetX
            labelY = self.groupLabelY
            text = group.label
            fontsize = self.fontsize
            ax.text(labelX, labelY, text, fontsize = fontsize)

        #get rid of axes
        ax.set_ylabel( self.yAxisLabel)
        ax.axes.get_xaxis().set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
