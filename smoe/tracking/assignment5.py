import layout
import graphicsDisplay
import trackingTestClasses
import inference

from bustersAgents import BustersAgent

def run_game():
    lay = layout.getLayout('q1/1-ExactObserve')
    gameDisplay = graphicsDisplay.PacmanGraphics(frameTime = 0.1)  # initialize the display of the playing field, needed here for the Pacman agent

    ghosts = [trackingTestClasses.SeededRandomGhostAgent(1)]  # controls the behavior of a random ghost

    mr_pacman = BustersAgent(ghostAgents=ghosts, inference=inference.ExactInference, elapseTimeEnable=False)  # controls the pacman behavior
    game = rules.newGame(lay, mr_pacman, ghostAgents=ghosts, display=gameDisplay, maxMoves=50)  # instantiate a Game instance, see below
    game.run()  # run the game, until Pacman catches a ghost.

run_game()