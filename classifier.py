""" This module contains the random forest class and methods pertaining to model accuracy calculation. """

from __future__ import annotations
from abc import ABC, abstractmethod
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from numpy import mean
from sklearn.model_selection import TimeSeriesSplit, KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error


class Classifier(ABC):
    """ Random Forest interface for evaluating the three different models."""

    @abstractmethod
    def calculateModelAccuracy(self, featureMax, exploratoryTesting, responseTesting) -> float:
        pass

    @abstractmethod
    def calculateRandomForest(self, exploratoryTesting, responseTesting, confirm) -> float:
        pass

    @abstractmethod
    def featureImp(self, exploratoryTraining, responseTraining, featureMax) -> list:
        pass

    @abstractmethod
    def featureImpSplitTrain(self, featureMax, orderedIndex):
        pass

    @abstractmethod
    def featureImpSplitTest(self, featureMax, orderedIndex):
        pass

    @abstractmethod
    def calculateFitnessPSO(self, featureMax, exploratoryTraining, responseTraining) -> float:
        pass


class RandomForest(Classifier):

    """ Random forest class which contains methods for calculating model accuracies. """

    def __init__(self, targetVARS, scaler, exploratoryTraining, exploratoryTest):
        self._targetVars = targetVARS
        self._scaler = scaler
        self._exploratoryTrain = exploratoryTraining
        self._exploratoryTest = exploratoryTest

    # proposed model RF-PSO
    def calculateModelAccuracy(self, featureMax, exploratoryTesting, responseTesting):
        """ Returns the mean absolute error and root mean squared error of the proposed rf-pso machine learning model."""

        # Fit a fandom forest model to find the optimal features on the RF from hyperparameters of PSO gbest
        model = RandomForestRegressor(
            n_estimators=100, random_state=0, max_features=featureMax)

        # 10-fold cross validation
        fitnessFunct = TimeSeriesSplit(n_splits=10)

        # container variable for accuracy scores
        outerResults = []
        outerResults2 = []

        orderedI = self.featureImp(
            exploratoryTesting, responseTesting, featureMax)

        exploratoryTestingFI = self.featureImpSplitTest(featureMax, orderedI)

        for trainINDEX, testINDEX in fitnessFunct.split(exploratoryTestingFI, responseTesting):

            # Split the data
            xTrain, xTest = exploratoryTestingFI[trainINDEX,
                                                 :], exploratoryTestingFI[testINDEX, :]
            yTrain, yTest = responseTesting[trainINDEX], responseTesting[testINDEX]

            yTestNP = np.ravel(yTest)
            yTrainNP = np.ravel(yTrain)

            model.fit(xTrain, yTrainNP)
            predValues = model.predict(xTest)

            # Evaluate the validation with specified model
            acc = mean_absolute_error(predValues, yTestNP)
            acc2 = mean_squared_error(predValues, yTestNP, squared=False)

            # store results in outer lists
            outerResults.append(acc)
            outerResults2.append(acc2)

        # aggregate results
        averageAccMAE = mean(outerResults)
        averageAccRMSE = mean(outerResults2)

        return averageAccMAE, averageAccRMSE

    def calculateRandomForest(self, exploratoryTesting, responseTesting, confirm):
        # Baseline model RF without time series split
        """ Returns the mean absolute error and root means squared error of the baseline model - random forest classifier. """

        # Fit a fandom forest model to find the optimal features on the RF from hyperparameters of PSO gbest
        model = RandomForestRegressor(
            n_estimators=100, random_state=0)

        if confirm == 3:

            # 10-fold cross validation
            fitnessFunct = TimeSeriesSplit(n_splits=10)

        elif confirm == 2:

            # 10-fold cross validation
            fitnessFunct = KFold(n_splits=10)

        # container variable for accuracy scores
        outerResults = []
        outerResults2 = []

        for trainINDEX, testINDEX in fitnessFunct.split(exploratoryTesting, responseTesting):

            # Split the data
            xTrain, xTest = exploratoryTesting[trainINDEX,
                                               :], exploratoryTesting[testINDEX, :]
            yTrain, yTest = responseTesting[trainINDEX], responseTesting[testINDEX]

            yTestNP = np.ravel(yTest)
            yTrainNP = np.ravel(yTrain)

            model.fit(xTrain, yTrainNP)
            predValues = model.predict(xTest)

            # Evaluate the validation with specified model
            acc = mean_absolute_error(predValues, yTestNP)
            acc2 = mean_squared_error(predValues, yTestNP, squared=False)

            # store results in outer lists
            outerResults.append(acc)
            outerResults2.append(acc2)

        # aggregate results
        averageAccMAE = mean(outerResults)
        averageAccRMSE = mean(outerResults2)

        return averageAccMAE, averageAccRMSE

    def featureImp(self, exploratoryTraining, responseTraining, featureMax):
        """ This method retrievesthe feature importance scores during the training process and returns
        a sorted list by the index in order of increasing importance."""

        # setting the number of features to the solution
        model = RandomForestRegressor(
            n_estimators=100, random_state=0, max_features=featureMax, criterion="mae")

        # 10-fold cross validation
        fitnessFunc = TimeSeriesSplit(n_splits=10)

        for trainINDEX, testINDEX in fitnessFunc.split(exploratoryTraining, responseTraining):

            # Split the data
            xTrain, _ = exploratoryTraining[trainINDEX,
                                            :], exploratoryTraining[testINDEX, :]
            yTrain, _ = responseTraining[trainINDEX], responseTraining[testINDEX]

            yTrainNP = np.ravel(yTrain)

            # fit the model using training data
            model.fit(xTrain, yTrainNP)

            featureImpDict = {}   # dictionary to store index of the important features
            # feature importance, which features are most strongly related
            for idx, value in enumerate(model.feature_importances_):
                featureImpDict[idx] = value

            # sorting the index by increasign importances values
            featureImpList = sorted(featureImpDict, key=featureImpDict.get)

        return featureImpList

    def featureImpSplitTrain(self, featureMax, orderedIndex):
        """ Prepares portfolio holder into the splits required for training and testing of machine learning models."""

        variables = self._targetVars

        j = 0
        # for as long as max features in n_features.
        for _ in range(0, (12-featureMax)):
            number = orderedIndex[j]  # pop the least important feature
            # get the string representation of the variable from the symbol list.
            variable = variables[number]
            # remove the symbol from the dataframe.
            self._exploratoryTrain.drop(variable, axis=1)

            j += 1

        # Standardise and transform data
        xS = self._scaler.fit_transform(self._exploratoryTrain)

        return xS

    def featureImpSplitTest(self, featureMax, orderedIndex):
        """ Prepares portfolio holder into the splits required for training and testing of machine learning models."""

        variables = self._targetVars
        j = 0
        # for as long as max features in n_features.
        for _ in range(0, 12-featureMax):  # for as long as max features in n_features
            number = orderedIndex[j]  # pop the least important feature
            numberI = int(number)
            # get the string representation in the symbol name list
            variable = variables[numberI]
            # remove this from the axis of the labels
            self._exploratoryTest.drop(variable, axis=1)
            j += 1

        # Standardise and transform data
        xS = self._scaler.fit_transform(self._exploratoryTest)

        return xS

    def calculateFitnessPSO(self, featureMax, exploratoryTraining, responseTraining):
        """ Calculates the fitness of the particle's within the swarm optimisation algorithm by returning the mean absolute error.
         """

        # setting the number of features to the solution
        model = RandomForestRegressor(
            n_estimators=100, random_state=0, max_features=featureMax)

        # 10-fold cross validation
        fitnessFunc = TimeSeriesSplit(n_splits=10)

        # container variable for accuracy scores
        outerResults = []

        orderedI = self.featureImp(
            exploratoryTraining, responseTraining, featureMax)

        exploratoryTrainingFI = self.featureImpSplitTrain(featureMax, orderedI)

        for trainINDEX, testINDEX in fitnessFunc.split(exploratoryTrainingFI, responseTraining):

            # Split the data
            xTrain, xTest = exploratoryTrainingFI[trainINDEX,
                                                  :], exploratoryTrainingFI[testINDEX, :]
            yTrain, yTest = responseTraining[trainINDEX], responseTraining[testINDEX]

            yTestNP = np.ravel(yTest)
            yTrainNP = np.ravel(yTrain)

            # fit the model using training data
            model.fit(xTrain, yTrainNP)

            # predict the model using test data
            predValues = model.predict(xTest)

            # Evaluate the validation with specified model
            acc = mean_absolute_error(predValues, yTestNP)

            outerResults.append(acc)  # store results in outer list

        averageAcc = mean(outerResults)  # aggregate results

        return averageAcc
