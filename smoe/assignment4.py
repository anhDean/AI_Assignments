from Bayes_exercise import Cpt
import random


rain = Cpt('Rain', [[0.9, 0.1],[0.2, 0.8]], ['Cloudy'])

cloudy = Cpt('Cloudy', [[0.6, 0.4]],[])

wetgrass = Cpt('WetGrass', [[0.8, 0.2],
                            [0.4, 0.6],
                            [0.3, 0.7],
                            [0.1, 0.9]], ['Rain', 'Sprinkler'])


conditioned_state = dict(Rain=True, Sprinkler=False)
wetgrass.conditioned(conditioned_state)

