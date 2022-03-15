"""This module contains the interface class and acts as the control class between the UI class and the use cases. between the user and the program."""
from __future__ import annotations
from abc import ABC, abstractmethod
import re
import sys
import logging
import pandas as pd
from sklearn.preprocessing import StandardScaler
from colours import Colours
from interface import OutputUI, stringOutputUI, warningUI
from reporter import ReportEditor, ReportManager
from processor import Director, ConcreteProcessor
from classifier import RandomForest
from optimiser import Heuristic


class IFacade(ABC):
    """Provides default implementation facade control class"""

    @abstractmethod
    def handleUserMenuRequest(self):
        pass

    @abstractmethod
    def sendRequestValidateSymbol(self, tList, inputs, listOfSymbols) -> int:
        pass

    @abstractmethod
    def orchastrateProcessing(self, sList, correctSymb, startPeriod, endPeriod, confirm) -> pd.DataFrame:
        pass

    @abstractmethod
    def orchastrateReportProcessing(self, correctSymb, tList, name, surname, rmse, mae, confirm) -> int:
        pass

    @abstractmethod
    def sendQuitMessage(self) -> None:
        pass


class Facade(IFacade):
    """ Facade class which coordinates UI and use cases by providing a simple interface for the subsystems invovled.
    Requests are delegated to the appropriate classes and their lifecycle is managed.

    This class receives input from users, and dispays messages and progress made during the program. It also validates inputs and handles errors.

    Methods are convenient shortcuts to sophisticated functionality of the subsystem."""

    def __init__(self, subsystem1: ReporterUI, subsystem2: PortfolioManagerUI, output: OutputUI, stringout: stringOutputUI, col: Colours, warning: warningUI) -> None:
        """Providing the facade with existing subsystem objects"""

        self._col = col
        self._warning = warning
        self._reporter = subsystem1
        self._portfolioManager = subsystem2
        self._intUI = output
        self._stringUI = stringout
        self._scaler = StandardScaler()

    def handleUserMenuRequest(self):
        """ This method is responsible for orchastrating the classes involved during the start up to portfolio management processes."""

        fName = []  # list for first name
        lName = []  # list for last name
        inputs = []  # holder variable for the amount of stock entries to be made

        # Collecting user first name
        fName.append(self._stringUI.nameValidateF())
        name = str(fName[-1])
        # Collecting user last name
        lName.append(self._stringUI.nameValidateL(name))
        surname = str(lName[-1])
        # Collecting user access level
        accessLevel = self._intUI.accessLevelSpecifier()

        # Instantiating Report class
        reportSO = ReportManager(name, surname, self._col)
        counter = 0

        # Calling portfolio menu and passing value by reference
        inputs.append(self._intUI.portManagement(
            name, surname, reportSO, accessLevel, counter))

        inputsI = inputs[-1]
        if isinstance(inputsI, int):

            number = int(inputsI)

            return number, name, surname

        elif not isinstance(inputsI, int):

            number = 0
            return number, name, surname

    def sendRequestValidateSymbol(self, tList, inputs, listOfSymbols) -> int:
        """This method is responsible for orachastrating the process of preprocessing of stock symbols."""

        symbolH = []

        inputI = int(inputs)
        # Validating inputs of stock entries
        tList = self._portfolioManager.validateInput(
            listOfSymbols, inputI)

        # Displaying stock entries
        symbolH.append(self._portfolioManager.symbolSelector(
            tList))
        symbol = symbolH[-1]

        if isinstance(symbol, int):

            number = int(symbol)
            # validating user entry for symbol name
            correctSymbol = self._portfolioManager.validateSymbol(
                number, tList)
            correctSymb = int(correctSymbol)

            # Calling main menu controller and passing value by reference
            confirmS = self._intUI.mainMenu()
            confirm = int(confirmS)

            return correctSymb, tList, confirm

    def orchastrateProcessing(self, sList, correctSymb, startPeriod, endPeriod, confirm) -> pd.DataFrame:
        """This method is responsible for orachastrating the feature engineering process."""

        # Preprocessing module
        director = Director(sList[correctSymb],
                            self._scaler, startPeriod, endPeriod, self._col)
        builder = ConcreteProcessor(self._col)
        director.builder = builder

        if confirm == 1:

            xTrain, yTrain, xTest, yTest, targetVARS, exploratoryTraining, exploratoryTesting = director.processingHandler()

            return xTrain, yTrain, xTest, yTest, targetVARS, exploratoryTraining, exploratoryTesting

        else:

            xTest, yTest = director.processingHandlerRF()

            empty = 0
            emptier = 0
            evenEmptier = 0
            yesEmpty = 0
            moreEmpty = 0

            return xTest, yTest, empty, emptier, evenEmptier, yesEmpty, moreEmpty

    def orchastrateEvaluation(self, xTrain, yTrain, xTest, yTest, confirm, targetVARS, exploratoryTraining, exploratoryTesting) -> float:
        """ This method is repsonsible for orchatsrating the machine learning component of the proggram.
        Returns the mean absolute error and root mean squared error of all three models."""

        # instantiating random forest class
        classifier = RandomForest(
            targetVARS, self._scaler, exploratoryTraining, exploratoryTesting)

        if confirm == 1:

            print("--------------------------------------Optimising Parameters------------------------------------")

            # Run PSO algorithm in order to get list of global best solution
            number = 0
            # initialising with parameter to represent dimension of problem
            pso = Heuristic(number, classifier)
            optimalParam = pso.metaOpt(xTrain, yTrain, classifier)

            print("Evaluating Classifier...")
            mae, rmse = classifier.calculateModelAccuracy(
                optimalParam, xTest, yTest)

            return mae, rmse

        elif confirm == 2:
            # Evaluating base classifier
            mae, rmse = classifier.calculateRandomForest(
                xTrain, yTrain, confirm)

            return mae, rmse

        else:

            # Evaluating base classifier
            mae, rmse = classifier.calculateRandomForest(
                xTrain, yTrain, confirm)

            return mae, rmse

    def orchastrateReportProcessing(self, correctSymb, tList, name, surname, rmse, mae, confirm) -> int:
        """This method is responsible for orchastrating the classes involved in the report management process."""

        # Calling method for displaying results
        self._intUI.displayResults(
            tList[correctSymb], rmse, mae, confirm)

        # Instantiating report handler with initialiser
        reportT = ReportEditor(
            name, surname, mae, rmse, tList[correctSymb], confirm, self._col)

        # writing report documenting the mode of program the result was obtained in
        self._reporter.reportWriter(reportT, name, surname)

    def sendQuitMessage(self) -> None:
        """This method is responsible for handling a user's request to quit."""

        # Quit validation mechanism
        quitConfirmation = self._intUI.quitValidator()

        quitConfirmationI = int(quitConfirmation)
        self._portfolioManager.quitMessage(quitConfirmationI)

        return quitConfirmationI


class AbstractPortfolio(ABC):
    """ Colour interface for formatting text and inputs."""

    @abstractmethod
    def quitMessage(self, quitConfirmationI) -> None:
        pass

    @abstractmethod
    def splitOption(self, conf, tList, number) -> int:
        pass

    @abstractmethod
    def validateSymbol(self, number, tList) -> list:
        pass

    @abstractmethod
    def errorHandlingMechanism(self, numero) -> int:
        pass

    @abstractmethod
    def evaluatePortfolio(self, tList) -> list:
        pass

    @abstractmethod
    def additionHelper(self, tList, number) -> list:
        pass

    @abstractmethod
    def validateInput(self, tList, inputs) -> list:
        pass

    @abstractmethod
    def removalHelper(self) -> list:
        pass

    @abstractmethod
    def removalHelpingMechanism(self, tList) -> int:
        pass

    @abstractmethod
    def errorMessageHelper(self, tList, numero) -> int:
        pass

    @abstractmethod
    def symbolSelector(self, tList) -> list:
        pass

    @abstractmethod
    def noAmendments(self, conf, tList) -> int:
        pass

    @abstractmethod
    def addNew(self, tList, adjust) -> int:
        pass

    @abstractmethod
    def removeOld(self, tList) -> int:
        pass

    @abstractmethod
    def amendmentToSymbols(self, conf, tList) -> int:
        pass

    @abstractmethod
    def removeFromList(self, numero, amount, tList):
        pass

    @abstractmethod
    def efficientValidation(self, conf, tList, numberI):
        pass

    @abstractmethod
    def efficientEHM(self):
        pass

    @abstractmethod
    def efficientAdditions(self, tList):
        pass

    @abstractmethod
    def efficientValid(self, tList):
        pass

    @abstractmethod
    def efficientRemovalH(self):
        pass

    @abstractmethod
    def efficientRHM(self):
        pass

    @abstractmethod
    def efficientValid(self, tList):
        pass

    @abstractmethod
    def efficientANN(self, tList, amounts, match1):
        pass

    @abstractmethod
    def efficientAN(self, numero, tList):
        pass

    @abstractmethod
    def efficientATS(self, tList):
        pass


class PortfolioManagerUI(AbstractPortfolio):

    def __init__(self, cols, warning):
        self._cols = cols
        self._warningUI = warning

    def quitMessage(self, quitConfirmationI):
        """ This method provides the output for the selection of the user during the quit menu."""

        if quitConfirmationI == 0:

            print(self._cols.getBold() + self._cols.getPurple() + "[ALERT]" + self._cols.getEnd(
            ) + " You selected '" + self._cols.getBold() + "1" + self._cols.getEnd() + " - Yes, I wish to quit.")
            print(self._cols.getBold() + self._cols.getRed() +
                  "[TERMINATING]" + self._cols.getEnd() + " Now exiting program...")
            sys.exit()

        else:
            print(self._cols.getBold() + self._cols.getPurple() +
                  "[ALERT]" + self._cols.getEnd() + " You selected '" + self._cols.getBold() + "2" + self._cols.getEnd() + " - No, I want to go back to the main menu.")
            print(self._cols.getBold() + self._cols.getItalic() +
                  "Reverting to start menu..." + self._cols.getEnd())

    def splitOption(self, conf, tList, number):
        """The use of this method was a design decision made in order to refactor the code, and is used during the stock validation process."""

        if conf == 1:
            print()
            print(self._cols.getBold() + self._cols.getPurple() +
                  "[ALERT] " + self._cols.getEnd()+"You selected '" + self._cols.getBold() + str(conf) +
                  self._cols.getEnd() + "' - Yes this is the correct choice.")
            print(self._cols.getBold() + self._cols.getPurple() +
                  "[ALERT]" + self._cols.getEnd() + " Validation Completed.")
            print(self._cols.getBold() + self._cols.getItalic() +
                  "Progressing to main menu..." + self._cols.getEnd())
            return number

        elif conf == 2:

            print()
            print("You said that this was not your intended stock.")
            print("Your portfolio is as follows:")
            numero = len(tList)

            for i in range(numero):
                print(" " + self._cols.getBold() + str(i) + self._cols.getEnd() +
                      " : " + self._cols.getBold() + tList[i] + self._cols.getEnd())

            print()
            print("Please re-specify your intended stock symbol index.")
            numberS = self.errorHandlingMechanism(numero)
            readyNumber = int(numberS)
            print()
            print(self._cols.getBold() + self._cols.getPurple() + "[ALERT]" + self._cols.getEnd() + " You have now selected the stock symbol {" + self._cols.getBold() +
                  tList[readyNumber] + self._cols.getEnd() + "} which was index number -", self._cols.getBold() + str(readyNumber) + self._cols.getEnd())
            print()
            print(self._cols.getBold() + self._cols.getPurple() +
                  "[ALERT]" + self._cols.getEnd() + " Validation completed.")
            print(self._cols.getBold() + self._cols.getItalic() +
                  "Progressing to main menu..." + self._cols.getEnd())

            return readyNumber

    def efficientValidation(self, conf, tList, numberI):
        """The use of this method was a design decision made in order to refactor the code, and is used during the stock validation process."""

        confirmation = self._warningUI.choiceOneTwo()  # function call to input function
        numbers = re.search("[1-2]", confirmation)
        if numbers:
            conf = int(confirmation)
            if conf == 1:
                # function call to confirm validation
                number = self.splitOption(conf, tList, numberI)
                numberL = int(number)
                return numberL
            elif conf == 2:
                # function call to confirm validation
                number = self.splitOption(conf, tList, numberI)
                numberL = int(number)
                return numberL

    def validateSymbol(self, number, tList):
        """ This method validates the inputs of symbols and confirms whether the user has made the right choice or wishes to make changes.
            It returns the validated stock symbol the user wishes to continue with, and/or adds or removes further stock symbols."""

        print("-----------------------------------------------------------------------------------------------")
        print(self._cols.getBold() +
              "STOCK VALIDATION MECHANISM:" + self._cols.getEnd())

        numberI = int(number)
        try:

            print(self._cols.getBold() + self._cols.getPurple() +
                  "[ALERT] " + self._cols.getEnd() + "You selected the stock symbol {" + self._cols.getBold() +
                  tList[numberI] + self._cols.getEnd() + "} which was index number - ", self._cols.getBold() + str(numberI) + self._cols.getEnd())
        except ValueError:
            logging.exception("Index out of range! %s", numberI)
            print(self._cols.getBold() + self._cols.getRed() +
                  "[TERMINATING]" + self._cols.getEnd() + "Now exiting program.")
            sys.exit()

        print("Is the stock you intended to select?")
        print()
        confirmation = self._warningUI.choiceOneTwo(
        )  # function call to input function

        correct = re.search("[1-2]", confirmation)
        outOfRange = re.search("[3-9]", confirmation)
        erroneous = re.search("[^0-9]", confirmation)

        if correct:

            conf = int(confirmation)

            if conf == 1:

                # function call to confirm validation
                number = self.splitOption(conf, tList, numberI)
                numberL = int(number)
                return numberL

            elif conf == 2:

                # function call to confirm validation
                number = self.splitOption(conf, tList, numberI)
                numberL = int(number)
                return numberL

        elif outOfRange:

            error = 0
            while error < 3:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1
                self._warningUI.outOfRange()  # function call to error message

                number = self.efficientValidation(conf, tList, numberI)
                return number
        elif erroneous:
            error = 0
            while error < 3:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                self._warningUI.matchedNotNumber()
                number = self.efficientValidation(conf, tList, numberI)
                return number

        elif confirmation is None:
            error = 0
            while confirmation is None:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call to error message
                self._warningUI.emptyInput()
                number = self.efficientValidation(conf, tList, numberI)
                return number

    def efficientEHM(self):
        """The use of this method was a design decision made in order to refactor the code, and is used during the error handling process."""
        number2 = self._warningUI.inputMessageInteger(
        )  # function call to input function
        numbers = re.search("[0-4]", number2)

        if numbers:
            numberI = int(number2)
            if numberI <= numero:
                return numberI

    def errorHandlingMechanism(self, numero):
        """ This method handles any invalid input to do with numbers.
        Instantiates the warning and col class.
        Returns a validated umber within the specified range."""

        number = self._warningUI.inputMessageInteger()  # function call to input function

        notNumber = re.search("[^0-9]", number)
        correct = re.search("[0-4]", number)
        incorrect = re.search("[5-9]", number)

        if notNumber:

            shutDown = 0  # counter variable

            while shutDown < 3:

                # function call to error validator
                self._warningUI.validateError(shutDown)
                shutDown += 1  # increase counter variable by 1

                # function call for error message
                self._warningUI.matchedNotNumber()
                number = self.efficientEHM()
                return number

        elif correct:
            numberI = int(number)
            if numberI > numero:
                shutDown = 0
                while numberI > numero:

                    # function call to error validator
                    self._warningUI.validateError(shutDown)
                    shutDown += 1  # increase counter variable by 1

                    self._warningUI.outOfRange()
                    number = self.efficientEHM()
                    return number
            else:
                return numberI

        elif incorrect:
            shutDown = 0  # counter variable
            while shutDown < 3:

                # function call to error validator
                self._warningUI.validateError(shutDown)
                shutDown += 1  # increase counter variable by 1

                # function call for error message
                self._warningUI.matchedNotNumber()
                number = self.efficientEHM()
                return number

        elif number is None:
            error = 0
            while number is None:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call to error message
                self._warningUI.emptyInput()
                number = self.efficientEHM()
                return number

    def evaluatePortfolio(self, tList):
        """ This function is responsible for presenting the updated portfolio to the user.
        Returns the index specified by the user of the stock to be evaluated in the ML model."""

        numero = len(tList)

        if numero == 0:

            print(self._cols.getBold() + self._cols.getPurple() +
                  "[ALERT]" + self._cols.getEnd() + " Portfolio is empty.")
            print(self._cols.getBold() + self._cols.getPurple() +
                  "[ALERT]" + self._cols.getEnd() + " Please make more additions before evaluation can ensue.")
            sList = self.additionHelper(tList, 0)
            number = self.evaluatePortfolio(sList)
            return number

        else:
            print(
                "-------------------------------------------------------------------------------------------")
            print(self._cols.getBold() + self._cols.getPurple() +
                  "[ALERT]" + self._cols.getEnd() + " Additions/Removals completed.")
            print("The updated portfolio is as follows:")
            for i in range(numero):
                print(
                    " ", self._cols.getBold() + str(i) + self._cols.getEnd(), " : " + self._cols.getBold() + tList[i] + self._cols.getEnd())  # print the index of all the stocks in the portfolio

            print()
            print("Which stock index number would you like to evaluate?")
            print()
            number = self.errorHandlingMechanism(numero)

            if number > numero - 1:  # if index input is higher than the indices available
                shutDown = 0  # setting counter variable
                while number > numero-1:
                    # function call to error validator
                    self._warningUI.validateError(shutDown)
                    shutDown += 1  # increase counter variable by 1

                    self._warningUI.outOfRange()  # function call for warning message
                    # attempting to get the correct input
                    numb = self.errorHandlingMechanism(numero)

                    if numb <= numero - 1:  # if the index input is within the range of the indices available

                        readyNumber = int(numb)
                        print(self._cols.getBold() + self._cols.getPurple() +
                              "[ALERT]" + self._cols.getEnd() + " You selected", self._cols.getBold() +
                              str(readyNumber) + self._cols.getEnd(),
                              "which is - '" + tList[readyNumber] + "'")
                        print()
                        print(self._cols.getBold() + self._cols.getPurple() +
                              "[ALERT]" + self._cols.getEnd() + " Stock collection completed.")
                        print(self._cols.getBold() + self._cols.getItalic() +
                              "Progressing to stock validation..." + self._cols.getEnd())

                        return readyNumber

            else:
                readyNumber = int(number)
                print(self._cols.getBold() + self._cols.getPurple() +
                      "[ALERT]" + self._cols.getEnd() + " You selected", self._cols.getBold() +
                      str(readyNumber) + self._cols.getEnd(),
                      "which is - '" + tList[readyNumber] + "'")
                print()
                print(self._cols.getBold() + self._cols.getPurple() +
                      "[ALERT]" + self._cols.getEnd() + " Stock collection completed.")
                print(self._cols.getBold() + self._cols.getItalic() +
                      "Progressing to stock validation..." + self._cols.getEnd())

                return readyNumber

    def efficientAdditions(self, tList):
        """The use of this method was a design decision made in order to refactor the code, and is used during the stock collection process."""

        value = self._warningUI.inputMessageInteger()
        correct = re.search("[1-2]", value)

        if correct:
            valueI = int(value)
            if number == 1:

                print()
                print(self._cols.getBold() + self._cols.getPurple() +
                      "[ALERT]" + self._cols.getEnd() + " Input '" + self._cols.getBold() +
                      str(value) + self._cols.getEnd() +
                      "' stock indices you would like to add.")

                # Adding the new entries to the portfolio
                sList = self.validateInput(
                    tList, valueI)

                # function to evaluate updated portfolio
                number = self.evaluatePortfolio(sList)
                numberI = int(number)
                return numberI

            elif number == 0:

                print()
                print(self._cols.getBold() + self._cols.getPurple() + "[ALERT]"+self._cols.getEnd() + " You selected to add '" + self._cols.getBold() + str(value) +
                      self._cols.getEnd() + "' new stock/(s) to the portfolio.")
                # adding the new entries to the portfolio
                sList = self.validateInput(
                    tList, valueI)
                return sList

    def additionHelper(self, tList, number):
        """This function helps with the addition of new stock entries into the portfolio.
        Instantiates the warning and colour class.
        Returns a number representing the index of the stock to be evaluated from the new updated portfolio."""

        print()
        print(self._cols.getBold() + self._cols.getPurple() + "[ALERT]" + self._cols.getEnd() + " The " + self._cols.getBold()+"MAXIMUM" + self._cols.getEnd()+" amount of additions is " +
              self._cols.getBold() + "TWO." + self._cols.getEnd())
        print(self._cols.getBold() + self._cols.getPurple() + "[ALERT]" + self._cols.getEnd() + " The " + self._cols.getBold()+"MINIMUM"+self._cols.getEnd()+" amount of additions is " +
              self._cols.getBold() + "ONE." + self._cols.getEnd())
        print()

        # function call to get the number of additions
        value = self._warningUI.inputMessageInteger()
        correct = re.search("[1-2]", value)
        outOfRange = re.search("[3-9]", value)
        erroneous = re.search("[^0-9]", value)

        if correct:

            valueI = int(value)

            if number == 1:

                print()
                print(self._cols.getBold() + self._cols.getPurple() + "[ALERT]"+self._cols.getEnd() + " You selected to add '" + self._cols.getBold() + str(valueI) +
                      self._cols.getEnd() + "' new stock/(s) to the portfolio.")
                # adding the new entries to the portfolio
                sList = self.validateInput(
                    tList, valueI)

                # function to evaluate updated portfolio
                numberI = self.evaluatePortfolio(sList)
                return numberI

            elif number == 0:

                print()
                print(self._cols.getBold() + self._cols.getPurple() + "[ALERT]"+self._cols.getEnd() + " You selected to add '" + self._cols.getBold() + str(valueI) +
                      self._cols.getEnd() + "' new stock/(s) to the portfolio.")
                # adding the new entries to the portfolio
                sList = self.validateInput(
                    tList, valueI)
                return sList

        elif erroneous:

            error = 0  # set counter variable equal to 4
            while erroneous:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call for error message
                self._warningUI.matchedNotNumber()
                variable = self.efficientAdditions(tList)
                return variable
        elif outOfRange:

            error = 0  # set counter variable equal to 0
            while outOfRange:

                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call for error message
                self._warningUI.integerOutOfRangeSC()
                variable = self.efficientAdditions(tList)
                return variable

        elif value is None:
            error = 0
            while value is None:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call to error message
                self._warningUI.emptyInput()
                variable = self.efficientAdditions(tList)
                return variable

    def efficientValid(self, tList):
        """The use of this method was a design decision made in order to refactor the code, and is used during the stock validation process."""

        stockNameI = self._warningUI.symbolInput()
        number = re.search("[0-9]", stockNameI)
        lowercase = re.search("[a-z]", stockNameI)
        incorrect = re.search("[^a-zA-Z]", stockNameI)

        if lowercase and not number or incorrect:

            new = stockNameI.upper()
            tList.append(new)
            return tList

        elif not number or incorrect and not lowercase:
            tList.append(stockNameI)
            return tList

    def validateInput(self, tList, inputs):
        """ This method validates the user input for the stock symbols taken as string.
  Returns the list object containing all stock symbols entered."""

        print(
            "-------------------------------------------------------------------------------------------")
        print(self._cols.getBold() +
              "STOCK COLLECTION MECHANISM:" + self._cols.getEnd())

        for i in range(0, inputs):

            stockName = self._warningUI.symbolInput()  # function call for input

            # regex search condition to check for presence of number 0-9, or lower case in stock name variable
            incorrect = re.search("[^a-zA-Z]", stockName)
            lowercase = re.search("[a-z]", stockName)
            correct = re.search("[A-Z]", stockName)
            limit = 0  # set counter variable = 0

            # if matched loop until the right values specified
            if incorrect:

                while incorrect:

                    # function call to error validator
                    self._warningUI.validateError(limit)
                    limit += 1  # increase counter variable by 1

                    # function call for error message
                    self._warningUI.matchedNotString()
                    tList = self.efficientValid(tList)

            elif lowercase and not incorrect:

                new = stockName.upper()
                tList.append(new)

            elif correct:
                # if not matched continue as normal
                tList.append(stockName)

            elif stockName is None:
                error = 0
                while stockName is None:
                    # function call to error validator
                    self._warningUI.validateError(error)
                    error += 1  # increase counter variable by 1

                    # function call to error message
                    self._warningUI.emptyInput()
                    tList = self.efficientValid(tList)

        return tList

    def efficientRemovalH(self):
        """The use of this method was a design decision made in order to refactor the code, and is used during the stock removal process."""
        number2 = self._warningUI.inputMessageInteger(
        )  # function call for input

        # regex search condition for presence of integers 1 or 2 ONLY.
        numbers2 = re.search("[1-2]", number2)

        if numbers2:
            numb2 = int(numbers2)
            return numb2

    def removalHelper(self):
        """ This function validates the users integer representing the number of stocks to be removed from the list.
        Instantiates the warning and col class.
        Returns a number which represents a correct value within the specified range."""

        value = 2
        print()
        print(self._cols.getPurple() + self._cols.getBold() +
              "[ALERT]" + self._cols.getEnd() + " Stock portfolio is too small. You can make at least '" + self._cols.getBold() + str(value) + self._cols.getEnd() + "' more additions.")
        print("Make more additions before deleting old stock symbols.")

        number = self._warningUI.inputMessageInteger()  # function call for input

        notNumber = re.search("[^0-9]", number)
        correct = re.search("[1-2]", number)
        incorrect = re.search("[5-9]", number)

        if notNumber:
            shutDown = 0  # counter variable set to 0
            while shutDown < 3:
                # function call to error validator
                self._warningUI.validateError(shutDown)
                shutDown += 1  # increase counter variable by 1

                # function call for error message
                self._warningUI.matchedNotNumber()
                number = self.efficientRemovalH()
                return number

        elif correct:
            numba = int(number)
            return numba

        elif incorrect:

            shutDown = 0  # counter variable
            while shutDown < 3:
                # function call to error validator
                self._warningUI.validateError(shutDown)
                shutDown += 1  # increase counter variable by 1

                # function call for error message
                self._warningUI.integerOutOfRange()
                number = self.efficientRemovalH()
                return number

        elif number is None:
            error = 0
            while number is None:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call to error message
                self._warningUI.emptyInput()
                number = self.efficientRemovalH()
                return number

    def removeFromList(self, numero, amount, tList):
        """The use of this method was a design decision made in order to refactor the code, and is used during the stock removal process."""

        numeroS = len(tList)
        print("The portfolio as it stands is as follows:")
        for i in range(numeroS):
            # print the index of all the stocks in the portfolio
            print(" ", i, " : " + tList[i])

        for i in range(0, amount):

            print(self._cols.getBold() + self._cols.getPurple() + "[ALERT]" + self._cols.getEnd(
            ) + " Input " + self._cols.getBold() + "ONE" + self._cols.getEnd()+" stock index that you would like to remove.")
            print()
            first = self.errorHandlingMechanism(numero)
            stockIndex = int(first)

            if stockIndex <= numero:

                print(self._cols.getBold() + self._cols.getPurple()+"[ALERT]" + self._cols.getEnd()+" Now removing " +
                      self._cols.getBold() + tList[stockIndex] + self._cols.getEnd() + " from the portfolio...")
                tList.pop(stockIndex)

                print()
                print("The portfolio" + self._cols.getBold() + " AFTER" +
                      self._cols.getEnd() + " the removal is now:")
                numeroN = len(tList)
                for j in range(numeroN):
                    # print the index of all the stocks in the portfolio
                    print(" " + str(j) + " : " + tList[j])

            else:
                self.errorMessageHelper(
                    tList, numero)

        return tList

    def efficientRHM(self):
        """The use of this method was a design decision made in order to refactor the code, and is used during the stock removal process."""
        amount1 = self._warningUI.inputMessageInteger()  # collecting user input
        correct = re.search("[1-2]", amount1)
        if correct:
            amount = int(amount1)
            sList = self.removeFromList(
                numberOfSymbols, amount, tList)  # looping the removals
            number = self.evaluatePortfolio(sList)
            return number

    def removalHelpingMechanism(self, tList):
        """ This function is for a segment of the removal process for symbols.
        Instantiates the warning message and col class for use.
        Returns a number to be passed on which represents the stock index for evaluation. """

        numberOfSymbols = len(tList)

        print("-----------------------------------------------------------------------------------")
        print("You selected to 'Remove Old' stocks from the portfolio.")
        print()
        print(self._cols.getBold() + self._cols.getPurple() +
              "[ALERT]" + self._cols.getEnd() + " The"+self._cols.getBold() + " MAXIMUM"+self._cols.getEnd() + " amount of removals permitted is" +
              self._cols.getBold() + " TWO" + self._cols.getEnd() + " stocks.")
        print("How many removals would you like to make?")
        print()
        amount = self._warningUI.inputMessageInteger()
        match = re.search("[^1-2]", amount)
        correct = re.search("[1-2]", amount)
        incorrect = re.search("[3-6]", amount)

        if match:
            error = 0
            while match:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call for error message
                self._warningUI.matchedNotNumber()
                number = self.efficientRHM()
                return number

        elif correct:
            amounts = int(amount)

            print(
                "-----------------------------------------------------------------------------------")

            sList = self.removeFromList(numberOfSymbols, amounts, tList)
            number = self.evaluatePortfolio(sList)
            return number

        elif incorrect:
            error = 0
            while incorrect:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call for error message
                self._warningUI.integerOutOfRangeSC()
                number = self.efficientRHM()
                return number

            return number
        elif amount is None:
            error = 0
            while amount is None:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call to error message
                self._warningUI.emptyInput()
                number = self.efficientRHM()
                return number

    def errorMessageHelper(self, tList, numero):
        """ This function is a helper for the process of error message handling when deleting stock entries."""

        error = 0
        while error < 3:

            # function call to error validator
            self._warningUI.validateError(error)
            error += 1  # increase counter variable by 1

            # function call for error message
            self._warningUI.integerOutOfRangeSP(
            )
            second = self.errorHandlingMechanism(numero)

            if second > numero:

                while second > numero:

                    second = self.errorHandlingMechanism(numero)

                    if second <= numero:
                        print(self._cols.getBold() + self._cols.getPurple() +
                              "[ALERT] " + self._cols.getEnd() + "Now removing " + self._cols.getBold() + tList[stockIndex] + self._cols.getEnd() + " from portfolio...")
                        tList.pop(second)

            elif second <= numero:

                print(self._cols.getBold() + self._cols.getPurple() +
                      "[ALERT] " + self._cols.getEnd() + "Now removing " + self._cols.getBold() + tList[stockIndex] + self._cols.getEnd() + " from portfolio...")
                tList.pop(stockIndex)

    def efficientSS(self):
        """The use of this method was a design decision made in order to refactor the code, and is used during the stock collection process."""
        confirmationI = self._warningUI.inputMessageInteger()
        correct = re.search("[1-2]", confirmationI)
        if correct:
            conf = int(confirmationI)
            if conf == 1:
                number = self.amendmentToSymbols(
                    conf, tList)  # Option 1 - Changes
                return number
            elif conf == 2:
                number = self.noAmendments(
                    conf, tList)  # Option 2 - No changes
                numberI = int(number)
                return numberI

    def symbolSelector(self, tList):
        """ This method enables the user to input the symbols they would like to download and returns a list of the inputs.
            It also controls adding new and removing old symbols to the portfolio."""

        # Displaying stock entries
        numero = len(tList)
        print()
        print(self._cols.getBold() + self._cols.getPurple() +
              "[ALERT] " + self._cols.getEnd() + "The stock symbol/(s) selected were:")

        for i in range(numero):
            print(" " + self._cols.getBold() + str(i) + self._cols.getEnd() + " : " +
                  self._cols.getBold() + tList[i] + self._cols.getEnd())
        print()
        print("Would you like to make any amendments to the list of entries?")
        print("1. Yes, I want to make amendments.")
        print("2. No, I do not want to make any amendments.")
        print()
        confirmation = self._warningUI.inputMessageInteger()
        match = re.search("[^0-9]", confirmation)
        correct = re.search("[1-2]", confirmation)
        erroneous = re.search("[3-9]", confirmation)

        if match:
            error = 0  # set counter variable to zero
            while error < 3:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                self._warningUI.matchedNotNumber()
                number = self.efficientSS()
                return number

        elif correct:
            conf = int(confirmation)
            if conf == 1:  # yes would like to make changes to the portfolio list
                number = self.amendmentToSymbols(conf, tList)
                return number
            elif conf == 2:  # no would not like to make changes to the portfolio list
                numberI = self.noAmendments(conf, tList)
                return numberI

        elif erroneous:
            error = 0  # set counter variable to zero
            while error < 3:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1
                self._warningUI.integerOutOfRangeSC()

                number = self.efficientSS()
                return number
        elif confirmation is None:
            error = 0
            while confirmation is None:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call to error message
                self._warningUI.emptyInput()
                number = self.efficientSS()
                return number

    def noAmendments(self, conf, tList):
        """The use of this method was a design decision made in order to refactor the code, and is used during the stock validation process."""

        print("-------------------------------------------------------------------------------------------")
        print(self._cols.getBold() + self._cols.getPurple() + "[ALERT] " + self._cols.getEnd() + "You selected '" + self._cols.getBold() + str(conf) + self._cols.getEnd() +
              "' - No, I do not want to make any amendments.")
        numero = len(tList)
        print()

        print("Which stock index number would you like to evaluate?")
        for i in range(numero):
            # print the index of all the stocks in the portfolio
            print(" " + self._cols.getBold() + str(i) + self._cols.getEnd() +
                  " : " + self._cols.getBold() + tList[i] + self._cols.getEnd())
        print()
        number = self.errorHandlingMechanism(numero)
        readyNumber = int(number)

        return readyNumber

    def efficientAN(self, numero, tList):
        """The use of this method was a design decision made in order to refactor the code, and is used during the stock validation process."""
        confirmationI = self._warningUI.inputMessageInteger()
        correct = re.search("[1-2]", confirmationI)
        if correct:
            valueI = int(confirmationI)

            for i in range(numero):
                print(" ", self._cols.getBold() + str(i) + self._cols.getEnd(),
                      " : " + self._cols.getBold() + tList[i] + self._cols.getEnd())

            print(self._cols.getBold() + self._cols.getPurple() +
                  "[ALERT] " + self._cols.getEnd() + "Input the " + self._cols.getBold() + confirmationI + self._cols.getEnd() + " stock index(s) you would like to add " + self._cols.getBold() + "SUCCESSIVELY" + self._cols.getEnd() + ".")

            # function call to add new stock entries
            sList = self.validateInput(
                tList, valueI)
            numb = self.evaluatePortfolio(
                sList)
            numbI = int(numb)
            return numbI

    def efficientANN(self, tList, amounts, match1):
        """The use of this method was a design decision made in order to refactor the code, and is a part of the stock collection mechanism."""

        if match1:

            amount1 = int(amounts)
            print()
            for i in range(numero):
                # print the index of each stock int the portfolio
                print(" ", str(i),
                      " : " + tList[i])

            print(self._cols.getBold() + self._cols.getPurple() +
                  "[ALERT]" + self._cols.getEnd() + " Input the '" + self._cols.getBold() + amounts + self._cols.getEnd() + " stock indices you would like to remove. One after the other.")
            print(self._cols.getBold() + self._cols.getBlue() + "[INTEGER]" + self._cols.getEnd() + " Input the" + self._cols.getBold() + self._cols.getBlue() + " NUMBER" +
                  self._cols.getEnd() + " of the stock index you would like to remove." + self._cols.getBold() + " NO HIGHER THAN" + self._cols.getEnd(), numero)

            for i in range(amount1):

                first = self.errorHandlingMechanism(
                    numero)

                stockIndex = int(first)

                if stockIndex <= numero:  # if the stock index number selected is less than the total number of stocks

                    print(self._cols.getBold() + self._cols.getPurple() +
                          "[ALERT]" + self._cols.getEnd() + " Now removing " + self._cols.getBold() + tList[stockIndex] + self._cols.getEnd() + " from portfolio...")
                    tList[stockIndex].pop()

                else:
                    error = 0
                    while error < 3:
                        # function call to error validator
                        self._warningUI.validateError(error)
                        error += 1  # increase counter variable by 1

                        # Function call for error message
                        self._warningUI.integerOutOfRangeSC(
                        )

                        second5 = self.errorHandlingMechanism(
                            numero)

                        secondIndex5 = int(second5)

                        if secondIndex5 <= numero:
                            print(self._cols.getBold() + self._cols.getPurple() +
                                  "[ALERT] " + self._cols.getEnd() + "Now removing " + self._cols.getBold() + tList[secondIndex5] + self._cols.getEnd() + " from portfolio...")
                            tList[secondIndex5].pop()

            numb = self.additionHelper(
                tList, 1)
            return numb

    def addNew(self, tList, adjust):
        """The use of this method was a design decision made in order to refactor the code, and is a part of the stock collection mechanism."""

        numero = len(tList)

        if numero < 4 and numero > 0:

            print()
            print(self._cols.getBold() + self._cols.getPurple() +
                  "[ALERT] " + self._cols.getEnd() + "You selected option '" +
                  self._cols.getBold() + str(adjust) + self._cols.getEnd()+"' - Add new stocks to the list.")
            print(self._cols.getBold() + self._cols.getOrange() + "[REMINDER]" + self._cols.getEnd() + " The maximum amount of additions is " + self._cols.getBold() +
                  "TWO" + self._cols.getEnd() + ".")
            print(self._cols.getBold() + self._cols.getOrange() + "[REMINDER]" + self._cols.getEnd() + " The smallest amount of additions is " +
                  self._cols.getBold() + "ONE"+self._cols.getEnd() + ".")
            print()
            value = self._warningUI.inputMessageInteger()
            correct = re.search("[1-2]", value)
            outOfRange = re.search("[3-9]", value)
            erroneous = re.search("[^0-9]", value)

            if correct:
                valueI = int(value)
                print()
                print(self._cols.getBold() + self._cols.getPurple() +
                      "[ALERT] " + self._cols.getEnd() + "Your selection will ensure at least '" + self._cols.getBold() + str(valueI) + self._cols.getEnd() + "' stock(s) will be added to the portfolio.")
                print(self._cols.getBold() + self._cols.getItalic() +
                      "Progressing to stock collection." + self._cols.getEnd())

                sList = self.validateInput(tList, valueI)
                numb = self.evaluatePortfolio(sList)
                return numb

            elif outOfRange:
                error = 0
                while outOfRange:
                    # function call to error validator
                    self._warningUI.validateError(error)
                    error += 1  # increase counter variable by 1
                    self._warningUI.integerOutOfRangeSC()

                    number = self.efficientAN(numero, tList)
                    return number

            elif erroneous:
                error = 0  # set counter variable
                while outOfRange:
                    # function call to error validator
                    self._warningUI.validateError(error)
                    error += 1  # increase counter variable by 1
                    self._warningUI.matchedNotNumber()

                    number = self.efficientAN(numero, tList)
                    return number
            elif value is None:
                error = 0
                while value is None:
                    # function call to error validator
                    self._warningUI.validateError(error)
                    error += 1  # increase counter variable by 1

                    # function call to error message
                    self._warningUI.emptyInput()
                    number = self.efficientAN(numero, tList)
                    return number

        elif numero > 4:
            print("You selected " + self._cols.getBold() + "1" +
                  self._cols.getEnd() + " - Add new stocks to the list")
            print(self._cols.getBold() + self._cols.getRed() + "[ERROR]" + self._cols.getEnd() + " Portfolio space unavailable. Please" +
                  self._cols.getBold() + " REMOVE" + self._cols.getEnd() + " positions before any new positions can be added.")
            print(self._cols.getBold() + self._cols.getPurple() + "[ALERT]" + self._cols.getEnd() + " The maximum amount of removals permitted is" +
                  self._cols.getBold() + " TWO" + self._cols.getEnd() + " stocks.")
            print("The portfolio is as follows:")
            for i in range(numero):
                print(" ", self._cols.getBold() + str(i) + self._cols.getEnd(),
                      " : " + self._cols.getBold() + tList[i] + self._cols.getEnd())
            print()
            amount = self._warningUI.inputMessageInteger()
            match = re.search("[^0-9]", amount)
            correct = re.search("[1-2]", amounts)
            outOfRange = re.search("[3-9]", amounts)

            if match:
                error = 0
                while error < 3:

                    # function call to error validator
                    self._warningUI.validateError(error)
                    error += 1  # increase counter variable by 1

                    # function call for error message
                    self._warningUI.matchedNotNumber(col)
                    print(self._cols.getBold() + self._cols.getPurple() + "[ALERT]" + self._cols.getEnd() +
                          " The maximum amount of removals permitted is " + self._cols.getBold() + "TWO" + self._cols.getEnd() + " stocks.")
                    number = self.efficientANN(tList)
                    return number

            elif correct:
                num = int(number)
                number = self.efficientANN(tList, amounts, match1)
                return number

            elif outOfRange:
                error1 = 0
                while outOfRange:

                    # function call to error validator
                    self._warningUI.validateError(error)
                    error += 1  # increase counter variable by 1

                    # function call for error message
                    self._warningUI.integerOutOfRangeSP()
                    print(self._cols.getBold() + self._cols.getPurple() +
                          "[ALERT]" + self._cols.getEnd() + " The maximum amount of removals permitted is TWO stocks.")
                    amounts = self._warningUI.inputMessageInteger()
                    # regex search for presence of numbers
                    # regex search for presence of numbers 1 or 2
                    match1 = re.search("[1-2]", amounts)
                    number = self.efficientANN(tList, amounts, match1)
                    return number

            elif erroneous:
                error = 0
                while erroneous:

                    # function call to error validator
                    self._warningUI.validateError(error)
                    error += 1  # increase counter variable by 1

                    # function call for error message
                    self._warningUI.matchedNotNumber()
                    print(self._cols.getBold() + self._cols.getPurple() +
                          "[ALERT]" + self._cols.getEnd() + " The maximum amount of removals permitted is TWO stocks.")
                    amounts = self._warningUI.inputMessageInteger()
                    # regex search for presence of numbers
                    # regex search for presence of numbers 1 or 2
                    match1 = re.search("[1-2]", amounts)
                    number = self.efficientANN(tList, amounts, match1)
                    return number

            elif amount is None:
                error = 0
                while amount is None:
                    # function call to error validator
                    self._warningUI.validateError(error)
                    error += 1  # increase counter variable by 1

                    # function call to error message
                    self._warningUI.emptyInput()
                    amounts = self._warningUI.inputMessageInteger()
                    # regex search for presence of numbers
                    # regex search for presence of numbers 1 or 2
                    match1 = re.search("[1-2]", amounts)
                    number = self.efficientANN(tList, amounts, match1)
                    return number

    def removeOld(self, tList):
        """The use of this method was a design decision made in order to refactor the code, and is a part of the stock collection mechanism."""

        numero = len(tList)

        if numero > 1:

            number = self.removalHelpingMechanism(
                tList)

            return number
        else:
            print()
            print(self._cols.getBold() + self._cols.getPurple() +
                  "[ALERT]" + self._cols.getEnd() + " Portfolio too small to remove stocks")
            print(self._cols.getBold() + self._cols.getPurple() +
                  "[ALERT]" + self._cols.getEnd() + " Additions must be made before deletion can commence.")

            sList = self.additionHelper(tList, 0)

            number = self.removalHelpingMechanism(
                sList)

            return number

    def efficientATS(self, tList):
        """The use of this method was a design decision made in order to refactor the code, and is a part of the stock collection mechanism."""
        number = self._warningUI.inputMessageInteger()
        correct = re.search("[1-2]", number)
        if correct:
            numberI = int(number)
            if numberI == 1:
                numb = self.addNew(tList, numberI)
                return numb
            if numberI == 2:
                numb = self.removeOld(tList)
                return numb

    def amendmentToSymbols(self, conf, tList):
        print("-----------------------------------------------------------------------------------")
        print("MANAGING POSITIONS:")
        print(self._cols.getPurple() + self._cols.getBold()+"[ALERT]"+self._cols.getEnd() + " You selected '" +
              self._cols.getBold() + str(conf) + self._cols.getEnd() + "' - Yes I want to make amendments.")
        print("Would you like to:")
        print("1. Add new stocks to the list?")
        print("2. Remove old stocks from the list?")
        print()

        confirm = self._warningUI.inputMessageInteger()
        correct = re.search("[1-2]", confirm)
        outOfRange = re.search("[3-9]", confirm)
        erroneous = re.search("[^0-9]", confirm)

        if correct:

            adjust = int(confirm)
            if adjust == 1:  # add stocks to the portfolio
                numb = self.addNew(tList, adjust)
                return numb

            elif adjust == 2:  # remove stocks from portfolio
                numb = self.removeOld(tList)
                return numb

        elif outOfRange:
            error = 0
            while outOfRange:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                self._warningUI.integerOutOfRangeSC()
                number = self.efficientATS(tList)
                return number
        elif erroneous:
            error = 0
            while erroneous:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                self._warningUI.matchedNotNumber()
                number = self.efficientATS(tList)
                return number
        elif confirm is None:
            error = 0
            while confirm is None:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call to error message
                self._warningUI.emptyInput()
                number = self.efficientATS(tList)
                return number


class AbstractReporter(ABC):
    """Reporter interface for handling user reports."""

    @ abstractmethod
    def clearHandler(self, number, reporter) -> None:
        pass

    @ abstractmethod
    def viewReport(self, reporter, number) -> None:
        pass

    @ abstractmethod
    def reportSelector(self, numberI, reporter) -> None:
        pass

    @ abstractmethod
    def errorHandlerRS(self, numberI, reporter) -> int:
        pass

    @ abstractmethod
    def deleteHandler(self, reporter, number) -> None:
        pass

    @ abstractmethod
    def reportWriter(self, reporter, fName, lName) -> None:
        pass

    @ abstractmethod
    def writeMechanism(self) -> None:
        pass

    @ abstractmethod
    def clearingMechanism(self, numberI, number, reporter) -> None:
        pass


class ReporterUI(AbstractReporter):
    """ This class is used to handle outputting messages to the user throughout the report creation/management/deletion phase. Contains methods for viewing, deleting, writing and clearing reports."""

    def __init__(self, stringOut, warning, cols):
        self._stringOut = stringOut
        self._warningUI = warning
        self._cols = cols

    def clearingMechanism(self, numberI, number, reporter):
        """The use of this method was a design decision made in order to refactor the code, and is used during the report clearing process."""
        traderID = []

        if numberI == 1:  # then clear the report
            print(self._cols.getBold() + self._cols.getPurple()+"[ALERT] " + self._cols.getEnd() + "You selected '" + self._cols.getBold() + str(numberI) + self._cols.getEnd() +
                  "' - 'I wish to clear my model report'.")
            print()

            traderID.append(self._stringOut.collectID(number))
            traderIDC = str(traderID[-1])
            reporter.clearReport(traderIDC)
        if numberI == 2:  # then exit the program to the main menu
            print()
            print(self._cols.getBold() + self._cols.getPurple()+"[ALERT] " + self._cols.getEnd() + "You selected '" + self._cols.getBold() + str(numberI) + self._cols.getEnd() +
                  "' - 'I do not wish to clear my model report'.")
            print(self._cols.getBold() + self._cols.getPurple() +
                  "[ALERT]" + self._cols.getEnd() + " Report integrity intact.")
            print(self._cols.getBold() + self._cols.getItalic() +
                  "Progressing to start up menu..." + self._cols.getEnd())

    def efficientClearing(self, reporter):
        """The use of this method was a design decision made in order to refactor the code, and is used during the report clearing process."""

        number = self._warningUI.choiceOneTwo()
        correct = re.search("[1-2]", number)
        if correct:
            numberI = int(number)
            self.clearingMechanism(numberI, number, reporter)

    def clearHandler(self, number, reporter):
        """This method handles the process of clearing the contents of a report that is within the system."""

        print(
            "-----------------------------------------------------------------------------------")
        print(self._cols.getBold() + self._cols.getPurple() + "[ALERT] " + self._cols.getEnd() + "You selected '", self._cols.getBold() + str(number) + self._cols.getEnd() +
              "' - Clear your report information.")
        print(self._cols.getBold() + self._cols.getOrange() + "[WARNING]"+self._cols.getEnd() +
              " Clearing will delete all the model calculations made thus far.")
        print("Are you happy with this choice?")
        print("1. Yes, I want to clear the contents of a report.")
        print("2. No, I no longer want to clear the contents of a report.")
        print()
        clear = self._warningUI.inputMessageInteger()
        correct = re.search("[1-2]", clear)
        outOfRange = re.search("[3-9]", clear)
        erroneous = re.search("[^0-9]", clear)

        if correct:
            clearI = int(clear)
            self.clearingMechanism(clearI, clear, reporter)

        elif outOfRange:

            error = 0
            while outOfRange:

                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1
                self._warningUI.integerOutOfRangeSC()  # function call to error validator

                self.efficientClearing(reporter)

        elif erroneous:
            error = 0  # set counter variable
            while erroneous:

                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1
                self._warningUI.matchedNotNumber()  # function call to error validator

                self.efficientClearing(reporter)
        elif clear is None:
            error = 0
            while clear is None:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call to error message
                self._warningUI.emptyInput()
                self.efficientClearing(reporter)

    def viewReport(self, reporter, number):
        """Function is responsible for allowing the user to view the report which contains the results of model evaluation."""

        traderID = self._stringOut.collectID(number)
        traderID1 = str(traderID)
        reporter.viewReport(traderID1)

    def errorHandlerRS(self, numberI, reporter):
        """The use of this method was a design decision made in order to refactor the code,, and is used during the report selection process."""
        error = 0
        number = int(numberI)
        while not numberI < 3:

            # function call to error validator
            self._warningUI.validateError(error)
            error += 1  # increase counter variable by 1

            # function call for error message
            self._warningUI.integerOutOfRange()
            # function call for input function
            confirm = self._warningUI.choiceOneTwo()
            correct = re.search("[1-2]", confirm)
            if correct:
                confirmI = int(confirm)
                if confirmI < 3:
                    self._warningUI.reportSelector(confirmI, reporter)

    def deleteHandler(self, reportHandler, number):
        """This method is responsible for deleting reports from the system, and involves a call to the reporter class in the form of "ReportHandler" as a compositional relationship."""

        traderID = self._stringOut.collectID(number)
        traderIDS = str(traderID)
        reportHandler.deleteReport(traderIDS)

    def writeMechanism(self):
        """The use of this method was a design decision made in order to refactor the code,, and is used during the report writing process."""

        confirmation = self._warningUI.choiceOneTwo()
        correct = re.search("[1-2]", confirmation)
        if correct:
            confirmI = int(confirm)
            if confirmI == 1:  # append to an existing report
                number = 1  # variable for appending
                collectNumber = 5  # variable for appending in collect
                # writing report documenting the mode of program the result was obtained in
                traderID = self._stringOut.collectID(
                    collectNumber)
                traderIDS = str(traderID)
                reportHandler.writeReport(traderIDS, number)
            elif confirmI == 2:  # create a new report for writing.
                number = 2
                traderID = reportHandler.assignIdentification(
                    fName, lName)
                # writing report documenting the mode of program the result was obtained in
                traderIDS = str(traderID)
                reportHandler.writeReport(traderIDS, number)

    def reportWriter(self, reportHandler, fName, lName):
        """This method is responsible for writing reports with the contents of model evaluation."""

        print("Do you want to write this information to an existing report?")
        print()
        confirmation = self._warningUI.choiceOneTwo()
        correct = re.search("[1-2]", confirmation)
        outOfRange = re.search("[3-9]", confirmation)
        erroneous = re.search("[^0-9]", confirmation)

        if correct:
            conf = int(confirmation)
            if conf == 1:  # append to existing report
                message = self._cols.getBold() + self._cols.getPurple()+"[ALERT]" + self._cols.getEnd()+" You selected '{}' - Append to an existing report.".format(
                    conf)
                number = 1  # variable for appending
                print(message)
                collectNumber = 4  # variable for appending in collect
                # writing report documenting the mode of program the result was obtained in
                traderID = self._stringOut.collectID(collectNumber)
                traderIDS = str(traderID)
                reportHandler.writeReport(traderIDS, number)
            elif conf == 2:  # create a new report to write to
                message = self._cols.getBold() + self._cols.getPurple()+"[ALERT]" + self._cols.getEnd()+" You selected '{}' - Write a new report.".format(
                    conf)
                print(message)
                number = 2  # variable for writing
                traderID = reportHandler.assignIdentification(fName, lName)
                # writing report documenting the mode of program the result was obtained in
                traderIDS = str(traderID)
                reportHandler.writeReport(traderIDS, number)

        elif outOfRange:
            error = 0
            while outOfRange:

                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1
                self._warningUI.integerOutOfRange()
                self.writeMechanism()  # function call for writing

        elif erroneous:
            error = 0  # set counter variable
            while erroneous:  # while variable is nto an integer

                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1
                # function call to error message
                self._warningUI.matchedNotNumber()
                self.writeMechanism()  # function call for writing

        elif confirmation is None:
            error = 0
            while confirmation is None:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call to error message
                self._warningUI.emptyInput()
                self.writeMechanism()  # function call for writing

    def reportSelector(self, numberI, reportHandler):
        """Controls all the report handling methods.
            Takes an input (integer) to perform different modes report processing such as viewing, clearing and deleting records.
            """

        if numberI == 1:
            # Calling method for viewing report information
            self.viewReport(reportHandler, numberI)
        elif numberI == 2:
            # calling method for clearing report information from storage
            self.clearHandler(numberI, reportHandler)
        elif numberI == 3:
            # calling method for deleting the report
            self.deleteHandler(reportHandler, numberI)

        else:
            self.errorHandlerRS(numberI, reportHandler)
