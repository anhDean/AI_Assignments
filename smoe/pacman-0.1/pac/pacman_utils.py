from __future__ import print_function, division

import time
import json
import numpy as np
from IPython.core.display import Javascript, display

GHOST_COLORS = ["red", "green", "#00ffde", "#ffb847", "#0031ff", "white"]
dirdic = {'North': 2, 'South': 1, 'West': 3, 'East': 4, 'Stop': 1}


class NotebookGraphics(object):

    """HTML5 visualization for the IPython notebook

    The display canvas is going to be in the output for the cell where this object is created??
    """

    def __init__(self, sleep_time=.2):
        init_pacman()
        self.mmap = None
        self._sleep_time = sleep_time

    def _setup(self, mmap):
        pass

    def initialize(self, state, isBlue=False):
        print('initialize')
        mmap, _, self.power_beans, ghosts, pacman = parse_layout(str(state.layout), False)

        self.food = np.array(state.food.data, dtype=np.bool)
        food_list = zip(*[x.tolist() for x in np.where(self.food)])

        self.capsules = state.capsules
        if not self.mmap or self.mmap != mmap:
            M, N = len(mmap), len(mmap[0])
            s = "window.GameModule.setupCanvas({}, {})".format(N * 30, M * 30)
            display(Javascript(s))
            self.mmap = mmap
        time.sleep(.1)
        init_canvas(mmap, beans=food_list, power_beans=self.capsules)
        time.sleep(.2)
        self.update(state)
        display(Javascript("window.GameModule.startGame()"))

    def update(self, state):
        pacman_pos = state.agentStates[0].configuration.getPosition()
        pacman_dir = dirdic[state.agentStates[0].configuration.getDirection()]

        pacman_state = pacman_pos + (pacman_dir, )
        place_pacman(*pacman_state)
        # print('pacman state: {}'.format(pacman_state))

        for i, agent_state in enumerate(state.agentStates):
            if i == 0:
                continue
            pos = agent_state.configuration.getPosition()
            # print('agent {} state: {}'.format(i, pos))
            place_ghost(i - 1, pos[0], pos[1], d=0, col=GHOST_COLORS[i - 1],
                        scared=agent_state.scaredTimer > 0,
                        blinking=agent_state.scaredTimer > 5)

        food = np.array(state.food.data, dtype=np.bool)
        food_delta = zip(*[x.tolist() for x in np.where(food != self.food)])
        # print('fooddelta: {}'.format(food_delta))
        for x, y in food_delta:
            display(Javascript("window.GameModule.removeBean({}, {});".format(x, y)))
        self.food = food

        capsules = state.capsules
        removed_capsules = set(self.capsules) - set(capsules)

        for x, y in removed_capsules:
            display(Javascript("window.GameModule.removeBean({}, {});".format(x, y)))

        self.capsules = capsules

        self._pause()

    def _pause(self):
        time.sleep(self._sleep_time)

    def finish(self):
        self._stop()

    def _stop(self):
        display(Javascript("window.GameModule.stopGame();"))


def _iswall(c):
    return c == '%'


def differ(c, d):
    return _iswall(c) != _iswall(d)


def _parse_grid(food, power_beans, ghosts, pacman, c, i, j):
    pos = [i, j]
    if c == 'P':
        pacman.append(pos)
    elif c == '.':
        food.append(pos[::-1])
    elif c == 'o':
        power_beans.append(pos[::-1])
    elif c == 'G':
        ghosts.append(pos)


def parse_layout(layout, verbose=False):
    layout = list(reversed(layout.split('\n')))
    M, N = len(layout), len(layout[0])

    mmap = [[-1] * N for _ in range(M)]
    mmap[0] = [8] * N
    mmap[-1] = [2] * N

    for i in range(M):
        mmap[i][0] = 4
        mmap[i][-1] = 1

    mmap[0][0], mmap[0][-1], mmap[-1][0], mmap[-1][-1] = 0, 0, 0, 0

    beans = []
    power_beans = []
    ghosts = []
    pacman = []

    for i in range(1, N - 1):
        for j in range(1, M - 1):
            if verbose:
                print(layout[i][j], end='')
            c = layout[j][i]
            _parse_grid(beans, power_beans, ghosts, pacman, c, i, j)
            val = sum([differ(c, layout[j][i - 1]) * 1,
                       differ(c, layout[j - 1][i]) * 2,
                       differ(c, layout[j][i + 1]) * 4,
                       differ(c, layout[j + 1][i]) * 8])
            mmap[j][i] = val
        print() if verbose else ''

    return mmap, beans, power_beans, ghosts, pacman


def init_canvas(mmap, beans=[], power_beans=[]):
    M, N = len(mmap), len(mmap[0])
    display(Javascript("window.GameModule.initGame({}, {}, {});".format(N * 30, M * 30, json.dumps(mmap))))
    time.sleep(.2)
    init_food(beans, power_beans)


def place_pacman(x, y, d):
    xx, yy = [u * 30 + 15 for u in (x, y)]
    s = "window.GameModule.placePacman({}, {}, {})".format(xx, yy, d)
    display(Javascript(s))


def place_ghost(i, x, y, col=0, d=0, scared=False, blinking=False):
    xx, yy = [u * 30 + 15 for u in (x, y)]
    s = 'window.GameModule.placeGhost({}, {}, {}, "{}", {}, {}, {})'.format(
        i, xx, yy, col, d, int(scared), int(blinking))
    display(Javascript(s))


def init_food(beans, power_beans):
    s = """
    window.GameModule.setBeans(JSON.parse("{0}"));
    window.GameModule.setPowerBeans(JSON.parse("{1}"));
    """.format(json.dumps(beans), json.dumps(power_beans))
    display(Javascript(s))


tpl = """

(function(window) {
    function setupCanvas(width, height) {

        var canvas = $('#myCanvas')[0];
        if (!(canvas===undefined)) {
            console.log('deleting canvas');
            canvas.parentElement.removeChild(canvas);
        }
        element.html("<canvas width="+width+" height="+height+" id='myCanvas'></canvas>");
        container.show();
    }

    var Game;
    var intervalId;
    function initGame(width, height, obj) {
        require(["../static/GameReduced.js"], function(GGame) {
            Game = GGame;
            Game.setCanvas();
            Game.initCanvas(width, height);
            Game.setMaze(obj);
        });
    };
    function setBeans(b) {
        Game.setBeans(b);
    };
    function setPowerBeans(b) {
        Game.setPowerBeans(b);
    };
    function placePac(x, y, d) {Game.placePacman(x, y, d);};
    function placeGhost(i, x, y, c, d, s, b) {Game.placeGhost(i, x, y, c, d, s, b);};

    function start() {Game.initMaze(); Game.startGame();};
    function stop() {Game.stopGame()};

    function rb(x, y) {Game.removeBean(x, y);};
    window.GameModule = {
        initGame: function (width, height, obj) {
            initGame(width, height, obj);
        },
        setupCanvas: function(w, h){ setupCanvas(w, h); },
        setBeans: function(b){ setBeans(b); },
        setPowerBeans: function(b){ setPowerBeans(b); },
        placePacman: function(x, y, d) {placePac(x, y, d);},
        placeGhost: function(i, x, y, c, d, s, b) {placeGhost(i, x, y, c, d, s ,b);},
        startGame: function() {start();},
        stopGame: function() {stop();},
        removeBean: function(x, y) {rb(x, y);}
    }
})(window);

"""


def init_pacman():
    display(Javascript(tpl))
