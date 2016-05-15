from searchAgents import SearchAgent
from searchAgents import PositionSearchProblem
import util
import search
import layout
import pacman
from game import Actions, Directions
from util import Stack, Queue, PriorityQueue
from graphicsDisplay import PacmanGraphics

rules = pacman.ClassicGameRules(0)

from pacmanAgents import GreedyAgent
mr_pacman = GreedyAgent()  # controls the pacman behavior

from ghostAgents import RandomGhost
ghosts = [RandomGhost(1), RandomGhost(2)]  # controls the behavior of two ghosts

gameDisplay = PacmanGraphics()  # initialize the display of the playing field

lay = layout.getLayout('mediumClassic')  # load the layout of the map

game = rules.newGame(lay, mr_pacman, ghosts, gameDisplay, False, False)  # instantiate a Game instance, see below
game.run()  # run the game, until Pacman is caught by a ghost or there is no food left