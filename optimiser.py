"""This module is responsible for hyperparameter tuning the 'amount of features' variable on the random forest algorithm."""
from __future__ import annotations
from abc import ABC, abstractmethod
import random
import numpy as np
# ----------------------------------------------------------------------------


class ParticleHelper:  # BASE CLASS

    """Particle helper class which manages all the particles within the swarm."""

    # Private variables

    # acceleration co-efficient on the velocity update equation
    __accelerationCoeff1 = float(1.496180)
    # acceleration co-efficient on the position update equation
    __accelerationCoeff2 = float(1.496180)
    # inertia weight to prevent velocities becoming too large
    __inertiaWeight = float(0.729844)

    # Protected variables

    _sizeOfSwarm = int(30)  # Size of the population (particles in the swarm)
    _maximumGeneration = int(3)  # Maximum number of iterations
    # initial number of derived and base indicators
    _dimensionOfProblem = int(12)

    # Arrays

    particleVelocity = []
    particlePosition = []
    previousBest = []

    def __init__(self, number, forest):
        """ Initialises a swarm of particles subject to the size of the problem, that is
        the number of features to be reduced."""

        self._classifier = forest

        if number == 0:  # initialise first particle any amount of features

            numb = list(random.sample(
                range(1, self._dimensionOfProblem-1), 1))
            numero = numb[-1]

            # Randomly initialise population between 0-12 (12 being n_features)
            self.particlePosition = numero

            # Randomly initialise velocity with 0.01 as maximum velocity constraint
            self.particleVelocity = (
                0.01 * numero)

            # Set the current best as the latest particle
            self.previousBest = self.particlePosition

        elif number == 1:  # small amount of features (small initialisation)

            numb = list(random.sample(
                range(1, self._dimensionOfProblem-8), 1))
            numero = numb[-1]

            # Randomly initialise population between 0-12 (12 being n_features)
            self.particlePosition = numero

            # Randomly initialise velocity with 0.01 as maximum velocity constraint
            self.particleVelocity = (
                0.01 * numero)

            # Set the current best as the latest particle
            self.previousBest = self.particlePosition

        elif number == 2:  # medium sized initialisation

            numb = list(random.sample(
                range(5, self._dimensionOfProblem-4), 1))
            numero = numb[-1]

            # Randomly initialise population between 0-12 (12 being n_features)
            self.particlePosition = numero

            # Randomly initialise velocity with 0.001 as maximum velocity constraint
            self.particleVelocity = (
                0.01 * numero)

            # Set the current best as the latest particle
            self.previousBest = self.particlePosition

        elif number == 3:  # large initialisation

            numb = list(random.sample(range(9, self._dimensionOfProblem), 1))
            numero = numb[-1]

            # Randomly initialise population between 0-12 (12 being n_features)
            self.particlePosition = numero

            # Randomly initialise velocity with 0.001 as maximum velocity constraint
            self.particleVelocity = (
                0.01 * numero)

            # Set the current best as the latest particle
            self.previousBest = self.particlePosition

    def updateParticle(self, globalBest):
        """ Updates each particle contained within a swarm according to the amount of features contained in the raw feature set.
        Particle velocity is used to control the rate at which convergence of particles occurs.
        Particle position is the region within the search space the particle is located in."""

        # velocities constrained within a uniform distribution
        velocity1 = np.random.uniform(0, 1)
        velocity2 = np.random.uniform(0, 1)

        # velocity update equation
        self.particleVelocity = (self.__inertiaWeight * self.particleVelocity) + (self.__accelerationCoeff1 * velocity1 * (globalBest - self.particlePosition)) \
            + (self.__accelerationCoeff2 * velocity2 *
               (self.previousBest - self.particlePosition))

        # position update equation
        self.particlePosition = round(
            (self.particlePosition + self.particleVelocity))

    def _evalBFitness(self, xTrain, yTrain, particle):  # protected helper function
        """Fitness function for particle in swarm  - [Nested 10-fold cross validation]. """

        if particle > 12:

            particle = 12

            # function call from random forest class
            value = self._classifier.calculateFitnessPSO(
                particle, xTrain, yTrain)

        elif particle < 0:
            particle = 1
            # function call from random forest class
            value = self._classifier.calculateFitnessPSO(
                particle, xTrain, yTrain)

        else:
            # function call from random forest class
            value = self._classifier.calculateFitnessPSO(
                particle, xTrain, yTrain)

        return value


class Optimiser(ABC):
    """ Interface for all instances where an optimisation algorithm is required."""

    @abstractmethod
    def metaOpt(self, xTrain, yTrain, forest):
        pass


class Heuristic(ParticleHelper, Optimiser):  # DERIVED CLASS

    """ Derived class for particle optimisation. """

    # Initialisation of arrays
    swarmOfParticles = []
    candidateTotal = []

    def __init__(self, number, forest):

        # constructor of super class
        ParticleHelper.__init__(self, number, forest)

    def metaOpt(self, xTrain, yTrain, forest):
        """ Metaheuristic algorithm for hyperparameter tuning. """

        print("Initialising Swarm...")

        for i in range(0, self._sizeOfSwarm):  # mixed initialisation

            if i < (self._sizeOfSwarm-20):  # small init

                number = 1
                # instantiating particle helper class with inbuilt initialiser
                self.swarmOfParticles.append(
                    Heuristic(number, forest))

            elif i > (self._sizeOfSwarm-21) and i < (self._sizeOfSwarm-10):  # medium init

                number = 2
                # instantiating particle helper class with inbuilt initialiser
                self.swarmOfParticles.append(
                    Heuristic(number, forest))

            else:  # large init
                number = 3

                # instantiating particle helper class with inbuilt initialiser
                self.swarmOfParticles.append(
                    Heuristic(number, forest))

        for j in range(0, self._maximumGeneration):
            print("Optimising Swarm: No.", j+1)

            # Global best particle (initialisation)
            globalBest = self.swarmOfParticles[0].particlePosition

            for a in range(0, self._sizeOfSwarm):

                # location of previous best particle
                previousLocation = self.swarmOfParticles[a].previousBest
                # pointer to best particles list
                particle = self.swarmOfParticles[a].particlePosition

                # Update the personal best position (find pbest)
                if self._evalBFitness(xTrain, yTrain, particle) < self._evalBFitness(xTrain, yTrain, previousLocation):
                    self.swarmOfParticles[a].previousBest = particle
                elif self._evalBFitness(xTrain, yTrain, particle) == self._evalBFitness(xTrain, yTrain, previousLocation) and abs(self._evalBFitness(xTrain, yTrain, particle)) < abs(self._evalBFitness(xTrain, yTrain, previousLocation)):
                    self.swarmOfParticles[a].previousBest = particle

            for b in range(0, self._sizeOfSwarm):

                # pointer to list of best particles
                previousLocation = self.swarmOfParticles[b].previousBest

                # Update the GLOBAL best position (find gbest)
                if self._evalBFitness(xTrain, yTrain, previousLocation) < self._evalBFitness(xTrain, yTrain, globalBest):

                    # setting global best to previous best location
                    globalBest = previousLocation
                    self.candidateTotal.append(globalBest)

                elif self._evalBFitness(xTrain, yTrain, previousLocation) == self._evalBFitness(xTrain, yTrain, globalBest) and abs(self._evalBFitness(xTrain, yTrain, previousLocation)) < abs(self._evalBFitness(xTrain, yTrain, globalBest)):

                    # setting global best to previous best location
                    globalBest = previousLocation
                    self.candidateTotal.append(globalBest)

            for c in range(0, self._sizeOfSwarm):

                # Update velocities and position of each particle
                self.swarmOfParticles[c].updateParticle(globalBest)

        # return the position of globalbest (the selected feature subset);
        valuesM = self.candidateTotal[-1]
        values = int(valuesM)
        print(len(self.candidateTotal), "global best solutions found.")
        intVariable = "Optimal feature for classifier is {}".format(values)
        print(intVariable)

        return values
