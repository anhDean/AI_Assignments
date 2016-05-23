from searchAgents import SearchAgent, AStarCornersAgent, AStarFoodSearchAgent, ClosestDotSearchAgent
from searchAgents import PositionSearchProblem
import util
import search
import layout
import pacman
from game import Actions, Directions
from util import Stack, Queue, PriorityQueue
from graphicsDisplay import PacmanGraphics

tiny_corner_layout = layout.getLayout('tinyCorners')
medium_corner_layout = layout.getLayout('mediumCorners')
big_corner_layout = layout.getLayout('bigCorners')
tiny_maze = layout.getLayout('tinymaze')
medium_classic = layout.getLayout('mediumClassic')
test_search = layout.getLayout('testSearch')
tricky_search = layout.getLayout('trickySearch')

rules = pacman.ClassicGameRules(0)
sa = AStarFoodSearchAgent()
gameDisplay = PacmanGraphics(zoom = 0.9, frameTime=0.1)  # visualization
game = rules.newGame(tricky_search, sa, [], gameDisplay, False, False)
game.run()



'''


'''














