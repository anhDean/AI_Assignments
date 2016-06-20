
    def observe(self, observation, gameState):
        """
        Updates beliefs based on the distance observation and Pacman's position.

        The noisyDistance is the estimated Manhattan distance to the ghost you
        are tracking.

        The emissionModel below stores the probability of the noisyDistance for
        any true distance you supply. That is, it stores P(noisyDistance |
        TrueDistance).

        self.legalPositions is a list of the possible ghost positions (you
        should only consider positions that are in self.legalPositions).

        A correct implementation will handle the following special case:
          *  When a ghost is captured by Pacman, all beliefs should be updated
             so that the ghost appears in its prison cell, position
             self.getJailPosition()

             You can check if a ghost has been captured by Pacman by
             checking if it has a noisyDistance of None (a noisy distance
             of None will be returned if, and only if, the ghost is
             captured).
        """
        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()
        allPossible = util.Counter()
        "*** YOUR CODE HERE ***"
        # Replace this code with a correct observation update
        # Be sure to handle the "jail" edge case where the ghost is eaten
        # and noisyDistance is None

        if noisyDistance is None:
            allPossible[self.getJailPosition()] = 1.0  # ghost is in jail 100%
            for p in self.legalPositions:
                allPossible[p] = 0.0    # all other Probabilities 0
        else:
            for p in self.legalPositions:
                trueDistance = util.manhattanDistance(p, pacmanPosition)
                prob = emissionModel[trueDistance]
                allPossible[p] = prob*self.beliefs[p]   # update belief of position p
        "*** END YOUR CODE HERE ***"

        allPossible.normalize()
        self.beliefs = allPossible



def elapseTime(self, gameState):
    """
    Update self.beliefs in response to a time step passing from the current
    state.

    The transition model is not entirely stationary: it may depend on
    Pacman's current position (e.g., for DirectionalGhost).  However, this
    is not a problem, as Pacman's current position is known.

    In order to obtain the distribution over new positions for the ghost,
    given its previous position (oldPos) as well as Pacman's current
    position, use this line of code:

      newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))

    Note that you may need to replace "oldPos" with the correct name of the
    variable that you have used to refer to the previous ghost position for
    which you are computing this distribution. You will need to compute
    multiple position distributions for a single update.

    newPosDist is a util.Counter object, where for each position p in
    self.legalPositions,

    newPostDist[p] = Pr( ghost is at position p at time t + 1 | ghost is at position oldPos at time t )

    (and also given Pacman's current position).  You may also find it useful
    to loop over key, value pairs in newPosDist, like:

      for newPos, prob in newPosDist.items():
        ...

    *** GORY DETAIL AHEAD ***

    As an implementation detail (with which you need not concern yourself),
    the line of code at the top of this comment block for obtaining
    newPosDist makes use of two helper methods provided in InferenceModule
    above:

      1) self.setGhostPosition(gameState, ghostPosition)
          This method alters the gameState by placing the ghost we're
          tracking in a particular position.  This altered gameState can be
          used to query what the ghost would do in this position.

      2) self.getPositionDistribution(gameState)
          This method uses the ghost agent to determine what positions the
          ghost will move to from the provided gameState.  The ghost must be
          placed in the gameState with a call to self.setGhostPosition
          above.

    It is worthwhile, however, to understand why these two helper methods
    are used and how they combine to give us a belief distribution over new
    positions after a time update from a particular position.
    """
    "*** YOUR CODE HERE ***"

    allPossible = util.Counter()

    for p in self.legalPositions:
        newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, p))
        for newPos, prob in newPosDist.items():
            allPossible[newPos] += prob* self.beliefs[p]

    allPossible.normalize()
    self.beliefs = allPossible


def chooseAction(self, gameState):
    """
    First computes the most likely position of each ghost that has
    not yet been captured, then chooses an action that brings
    Pacman closer to the closest ghost (according to mazeDistance!).

    To find the mazeDistance between any two positions, use:
      self.distancer.getDistance(pos1, pos2)

    To find the successor position of a position after an action:
      successorPosition = Actions.getSuccessor(position, action)

    livingGhostPositionDistributions, defined below, is a list of
    util.Counter objects equal to the position belief
    distributions for each of the ghosts that are still alive.  It
    is defined based on (these are implementation details about
    which you need not be concerned):

      1) gameState.getLivingGhosts(), a list of booleans, one for each
         agent, indicating whether or not the agent is alive.  Note
         that pacman is always agent 0, so the ghosts are agents 1,
         onwards (just as before).

      2) self.ghostBeliefs, the list of belief distributions for each
         of the ghosts (including ghosts that are not alive).  The
         indices into this list should be 1 less than indices into the
         gameState.getLivingGhosts() list.
    """
    pacmanPosition = gameState.getPacmanPosition()
    legal = [a for a in gameState.getLegalPacmanActions()]
    livingGhosts = gameState.getLivingGhosts()
    livingGhostPositionDistributions = \
        [beliefs for i, beliefs in enumerate(self.ghostBeliefs)
         if livingGhosts[i + 1]]
    "*** YOUR CODE HERE ***"
    newProbs = []
    actions = dict()

    for action in legal:
        successorPosition = Actions.getSuccessor(pacmanPosition, action)
        newProb = max([p[successorPosition] for p in livingGhostPositionDistributions])
        newProbs.append(newProb)
        actions[newProb] = action

    maxProb = max(newProbs)
    greedyAction = actions[maxProb]
    return greedyAction


