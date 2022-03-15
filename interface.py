"""UI Module responsible for alerting the user of any errors/self._warnings/messages.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
import sys
import re
import glob


class AbstractAlert(ABC):
    """ Abstract self._warning interface for outputs and user inputs."""

    @abstractmethod
    def inputMessageInteger(self) -> str:
        pass

    @abstractmethod
    def fNameMessage(self) -> str:
        pass

    @abstractmethod
    def lNameMessage(self) -> str:
        pass

    @abstractmethod
    def traderIDMessage(self) -> str:
        pass

    @abstractmethod
    def invalidIDMessage(self) -> None:
        pass

    @abstractmethod
    def choiceOneTwo(self) -> str:
        pass

    @abstractmethod
    def quitInput(self) -> str:
        pass

    @abstractmethod
    def symbolInput(self) -> str:
        pass

    @abstractmethod
    def additionInput(self, selectionI) -> str:
        pass

    @abstractmethod
    def matchedNotNumber(self) -> None:
        pass

    @abstractmethod
    def nameRepeat(self) -> None:
        pass

    @abstractmethod
    def outOfRange(self) -> None:
        pass

    @abstractmethod
    def integerOutOfRangeSC(self) -> None:
        pass

    @abstractmethod
    def integerOutOfRangeSP(self) -> None:
        pass

    @abstractmethod
    def shutDownWarning(self) -> None:
        pass

    @abstractmethod
    def quitMessage(self, quitConfirmationI, main) -> None:
        pass

    @abstractmethod
    def validateError(self, error) -> None:
        pass

    @abstractmethod
    def emptyInput(self) -> None:
        pass


class warningUI(AbstractAlert):
    """ This base class is responsible for outputting messages to the user.
            wm stand for self._warning/error messages.
            access by wm.matchedNotNumber
            """

    def __init__(self, cols):

        self._cols = cols

    def inputMessageInteger(self):
        """This methods collects the input in string form to convert into an integer from a user."""

        message = self._cols.getBold() + self._cols.getBlue() + "[INTEGER]" + self._cols.getEnd() + " Enter a" + \
            self._cols.getBold() + self._cols.getBlue() + " NUMBER" + \
            self._cols.getEnd() + " to represent your choice: "
        confirm = input(message)

        return confirm

    def emptyInput(self):
        """This methods alerts the user that an empty input was found."""

        print()
        print(self._cols.getRed() + self._cols.getBold() +
              "[ERROR]" + self._cols.getEnd() + " Empty input detected.")
        print("Ensure to input in the" + self._cols.getBold() + self._cols.getBlue() +
              " REQUIRED" + self._cols.getEnd() + " format for input to be accepted.")

    def fNameMessage(self):
        """This methods collects the input in string form for the first name."""

        name = self._cols.getBold() + self._cols.getYellow() + \
            "[STRING]" + self._cols.getEnd() + " Please enter your first name: "
        fName = input(name)
        return fName

    def lNameMessage(self):
        """This methods collects the input in string form for the last name."""

        name = self._cols.getBold() + self._cols.getYellow() + \
            "[STRING]" + self._cols.getEnd() + " Please enter your last name: "
        lName = input(name)
        return lName

    def traderIDMessage(self):
        """This methods collects the input in string form for the Trader ID."""
        message = self._cols.getBold() + self._cols.getYellow() + \
            "[STRING]" + self._cols.getEnd() + \
            " Please enter the trader identification: "
        traderID = input(message)

        return traderID

    def invalidIDMessage(self):
        """This method alerts the user of invalid input for Trader ID."""
        print(self._cols.getRed() + self._cols.getBold() +
              "[ERROR]" + self._cols.getEnd()+" ID does not match specified format.")

    def choiceOneTwo(self):
        """This methods collects the input in string form for the choice of one or two  (at any stage of the program) to be converted into integer form."""

        message = self._cols.getBold() + self._cols.getBlue() + "[INTEGER]" + self._cols.getEnd() + " Enter [" + self._cols.getBold() + self._cols.getGreen() + "1" + self._cols.getEnd() + "] = " + self._cols.getBold() + \
            "Yes" + self._cols.getEnd() + " | " + "OR" + self._cols.getEnd() + \
            " | Enter [" + self._cols.getBold() + self._cols.getRed() + "2" + \
            self._cols.getEnd() + "] = " + self._cols.getBold() + \
            "No: " + self._cols.getEnd()
        number = input(message)
        return number

    def quitInput(self):
        """This methods collects the input in string form for the choice of one or two to be converted into integer form (for the quit menu)."""

        message = self._cols.getBold() + self._cols.getBlue() + "[INTEGER] " + self._cols.getEnd() + "Enter [" + self._cols.getBold() + self._cols.getGreen() + "1" + self._cols.getEnd() + "] = " + self._cols.getBold() + "Yes, I wish to quit" + \
            self._cols.getEnd() + " | OR | Enter [" + self._cols.getBold() + self._cols.getRed() + "2" + self._cols.getEnd() + \
            "] = " + self._cols.getBold()+"No, I want to go back to the main menu: " + \
            self._cols.getEnd()
        confirm = input(message)
        return confirm

    def symbolInput(self):
        """This methods collects the input in string form for the choice of stock symbol by the user."""
        message = self._cols.getBold() + self._cols.getYellow() + \
            "[STRING]" + self._cols.getEnd() + " Enter the symbol of the stock in" + \
            self._cols.getBold() + " CAPITALS" + self._cols.getEnd()+": "
        stockName = input(message)
        return stockName

    def additionInput(self, selectionI):
        """This methods alerts users of the constraints of portfolio management before collecting the input in string form."""
        print("-------------------------------------------------------------------------------------------")
        print(self._cols.getBold() + self._cols.getPurple()+"[ALERT] " + self._cols.getEnd() + "You selected option '" +
              self._cols.getBold() + str(selectionI) + self._cols.getEnd() + "' - " + self._cols.getBold() + "Add stocks to portfolio." + self._cols.getEnd())
        print()
        print(self._cols.getBold() + self._cols.getOrange() + "[REMINDER]"+self._cols.getEnd() + " You can make a " +
              self._cols.getBold() + "MINIMUM " + self._cols.getEnd() + "of 1 stock addition.")
        print(self._cols.getBold() + self._cols.getOrange() + "[REMINDER]"+self._cols.getEnd() + " You can make a" +
              self._cols.getBold() + " MAXIMUM"+self._cols.getEnd() + " of 5 stock addition.")
        stock = self.inputMessageInteger()

        return stock

    def matchedNotNumber(self):
        """Method is responsible for outputting error message when user provides inputs which is not an integer. """

        print()
        print(self._cols.getRed() + self._cols.getBold() +
              "[ERROR]" + self._cols.getEnd() + " Invalid input.")
        print("DO"+self._cols.getBold() + " NOT" +
              self._cols.getEnd()+" enter "+self._cols.getBold() + "ALPHABETICAL" + self._cols.getEnd()+" or " + self._cols.getBold() + "SPECIAL CHARACTERS"+self._cols.getEnd() + ".")
        print("Ensure only" + self._cols.getBold() + self._cols.getBlue() +
              " INTEGER" + self._cols.getEnd() + " is entered.")

    def nameRepeat(self):
        """This methods alerts the user of duplicated input for name."""
        print()
        print(self._cols.getRed(
        ) + "[ERROR]" + self._cols.getEnd() + " First name cannot be the same as last name.")

    def outOfRange(self):
        """ Method provides error messages when user provides input which isn't within specific integer range."""
        print()
        print(self._cols.getRed() + self._cols.getBold() +
              "[ERROR]" + self._cols.getEnd() + " Not within the specified number limits.")

    def maxFailures(self):
        """ Method exits the program when the user provides input which is incorrect 3 times."""
        print()
        print(self._cols.getRed() + self._cols.getBold() +
              "[FATAL]" + self._cols.getEnd() + " Exceeded maximum error allowance.")
        print(self._cols.getRed() + self._cols.getBold() +
              "[FATAL]" + self._cols.getEnd() + " Exiting program...")
        sys.exit()

    def matchedWhitespace(self):
        """Method provides error messages when user provides input which contains whitespace."""

        print()
        print(self._cols.getRed() + self._cols.getBold() +
              "[ERROR]" + self._cols.getEnd() + " Invalid input.")
        print(self._cols.getBold() + self._cols.getRed() + " DO NOT" +
              self._cols.getEnd() + " enter any whitespace.")

    def matchedNotString(self):
        """Method provides error messages when user provides input which is not alphabetical."""

        print()
        print(self._cols.getBold() + self._cols.getRed() +
              "[ERROR]" + self._cols.getEnd() + " Presence of characters other than alphabet found.")
        print("Ensure alphabetical characters" +
              self._cols.getBold() + self._cols.getRed() + " ONLY" + self._cols.getEnd()+".")
        print("Do" + self._cols.getBold() + self._cols.getRed() + " NOT" + self._cols.getEnd() + " enter" +
              self._cols.getBold() + " ANY NUMERIC" + self._cols.getEnd() + " or" + self._cols.getBold() + " SPECIAL CHARACTERS." + self._cols.getEnd())
        print()

    def integerOutOfRange(self):
        """Method provides error messages when user provides integer input which is not within specified range for
    the stock collection mechanism"""
        print()
        print(self._cols.getRed() + self._cols.getBold() +
              "[ERROR]" + self._cols.getEnd() + " Not within the specified limits.")
        print("Adjust your demands and try again. Must be" +
              self._cols.getBold() + " LESS THAN 6" + self._cols.getEnd() + ".")

    def integerOutOfRangeSC(self):  # for stock collection
        """Method provides error messages when user provides integer input which is not within specified range for
      portfolio additons/removals."""
        print()
        print(self._cols.getRed() + self._cols.getBold() +
              "[ERROR]" + self._cols.getEnd() + " Not within the specified limits.")
        print("Enter an" + self._cols.getBold() + self._cols.getBlue() + " INTEGER" +
              self._cols.getEnd() + " between the range 1-2.")

    def integerOutOfRangeSP(self):  # for stock portfolio
        """Method provides error messages when user provides integer input which exceeds the index value
      in the stock evaluation mechanism"""
        print()
        print(self._cols.getRed() + self._cols.getBold() +
              "[ERROR]" + self._cols.getEnd() + " Index number exceeded stock portfolio.")
        print("You will have" + self._cols.getBold() + self._cols.getRed() +
              " TWO" + self._cols.getEnd() + " more attempts before system shutdown.")

    def shutDownWarning(self):
        """ Method provides self._warning message to user when they are one attempt away from failing the program."""
        print()
        print(self._cols.getBold() + self._cols.getOrange() + "[WARNING]" + self._cols.getEnd() +
              " A further error will" + self._cols.getBold() + " TERMINATE" + self._cols.getEnd() + " the program.")
        print("Ensure to" + self._cols.getBold() + " VALIDATE" +
              self._cols.getEnd() + " your input with caution otherwise the program will fail.")

    def quitMessage(self, quitConfirmationI, main):
        """This methods alerts the result of their selection in the quit menu."""

        if quitConfirmationI == 0:
            print(self._cols.getBold() + self._cols.getPurple() + "[ALERT] " + self._cols.getEnd() + "You have selected '" + self._cols.getBold() +
                  str(quitConfirmationI) + self._cols.getEnd() + "' - Quit program.")
            print(self._cols.getBold() + self._cols.getRed() +
                  "[TERMINATING]" + self._cols.getEnd() + " Now quitting program...")
            exit()

        elif quitConfirmationI == 1:
            print(self._cols.getBold() + self._cols.getPurple() + "[ALERT] " + self._cols.getEnd() + "You have selected '" + self._cols.getBold() +
                  str(quitConfirmationI) + self._cols.getEnd() + "' - Take me back to the " + main + " menu .")

    def validateError(self, error):
        """This methods was a design decision to refactor the code for warning the user of system error limits before eventual shutdown after 3 wrong attempts."""

        if error == 1:
            # function call for error message
            self.shutDownWarning()
        if error == 2:
            # function call for error message
            self.maxFailures()
            exit()


class AbstractOutput(ABC):
    """ Abstract output interface for integer values"""

    @abstractmethod
    def quitValidator(self) -> int:
        pass

    @abstractmethod
    def quantityOfSymbols(self, selectionI) -> int:
        pass

    @abstractmethod
    def mainMenu(self) -> int:
        pass

    @abstractmethod
    def accessLevelSpecifier(self) -> int:
        pass

    @abstractmethod
    def modeSelection(self, confirm) -> int:
        pass

    @abstractmethod
    def displayResults(self, tList, rmse, mae, confirm) -> None:
        pass

    @abstractmethod
    def reportManagement(self, fName, lName, accessLevel) -> int:
        pass

    @abstractmethod
    def correctOptionMenu(self, fName, lName, reportHandler, accessLevel, selectionI, counter):
        pass

    @abstractmethod
    def portManagement(self, fName, lName, reportHandler, accessLevel, counter):
        pass

    @abstractmethod
    def optionViewer(self, choices) -> None:
        pass


class OutputUI(AbstractOutput):
    """ This derived class inherits the self._warning messages from the base class and is responsible for validating user inputs outputting the integer results of the program to the user."""

    def __init__(self, cols, warning, reportUI):
        self._cols = cols
        self._warningUI = warning
        self._reportUI = reportUI

    def quitValidator(self):
        """ This method validates whether the user wants to quit and terminates the program."""

        print("----------------------------------------------Exit Menu--------------------------------------------")
        print(self._cols.getOrange() + self._cols.getBold() + "[WARNING] " + self._cols.getEnd() +
              "You have selected -" + self._cols.getBold() + " Exit" + self._cols.getEnd()+".")
        print("Are you sure about this?")
        print("1. Yes, I wish to quit.")
        print("2. No, I want to go back to the main menu.")
        print()
        confirm = self._warningUI.inputMessageInteger()

        # regex search condition to check for presence of anything other than a number
        m = re.search("[^0-9]", confirm)
        correct = re.search("[1-2]", confirm)
        outOfRange = re.search("[3-9]", confirm)

        if m:
            counter = 0  # set counter variable = 0
            while m:

                # function call to error validator
                self._warningUI.validateError(counter)
                counter += 1  # increase counter variable by 1

                # function call for error message
                self._warningUI.matchedNotNumber()
                value = self._warningUI.quitInput()  # function call for input function

                # regex search condition to check for presence of anything other than a number
                correct = re.search("[^1-2]", value)

                if correct:
                    valueI = int(value)

                    if valueI == 1:  # exit program
                        return 0
                    elif valueI == 2:  # return to main menu
                        return 1

        elif correct:

            confirmm = int(confirm)

            if confirmm == 1:  # exit program
                return 0

            elif confirmm == 2:  # return to main menu
                return 1
        elif outOfRange:
            counter = 0  # set counter variable
            while outOfRange:
                # function call to error validator
                self._warningUI.validateError(counter)
                counter += 1  # increase counter variable by 1

                # function call for error message
                self._warningUI.integerOutOfRangeSC()
                value = self._warningUI.inputMessageInteger()  # function call for input function
                # regex search condition to check for presence of anything other than a number
                correct = re.search("[1-2]", value)

                if correct:
                    valueI = int(value)
                    if valueI == 1:  # exit program
                        return 0
                    elif valueI == 2:  # return to main menu
                        return 1
        elif confirm is None:
            counter = 0  # set counter variable
            while confirm is None:
                # function call to error validator
                self._warningUI.validateError(counter)
                counter += 1  # increase counter variable by 1

                # function call for error message
                self._warningUI.emptyInput()
                value = self._warningUI.inputMessageInteger()  # function call for input function
                # regex search condition to check for presence of anything other than a number
                correct = re.search("[1-2]", value)

                if correct:
                    valueI = int(value)
                    if valueI == 1:  # exit program
                        return 0
                    elif valueI == 2:  # return to main menu
                        return 1

    def quantityOfSymbols(self, selectionI):
        """This methods collects the quantity of stock symbols th user wants to input within the array which represents the portfolio."""

        stock = self._warningUI.additionInput(selectionI)

        # regex search condition to check for presence of anything other than a number within specified range
        match = re.search("[^0-9]", stock)
        correct = re.search("[1-5]", stock)
        outOfRange = re.search("[6-9]", stock)

        if match:
            error = 0  # set counter variable equal to 0
            while match:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call for error message
                self._warningUI.matchedNotNumber()
                stock = self._warningUI.inputMessageInteger()
                number = re.search("[1-5]", stock)
                if number:

                    stockI = int(stock)

                    print()
                    print(self._cols.getBold() + self._cols.getPurple()+"[ALERT]"+self._cols.getEnd() + " Your selection will ensure at least '", self._cols.getBold() +
                          str(stock) + self._cols.getEnd(), "' stock(s) will be added to the portfolio.")
                    print(self._cols.getBold() + self._cols.getItalic() +
                          "Progressing to stock collection..."+self._cols.getEnd())
                    return stockI

        elif correct:
            stockI = int(stock)
            print()
            print(self._cols.getBold() + self._cols.getPurple()+"[ALERT]"+self._cols.getEnd() + " Your selection will ensure at least '", self._cols.getBold() +
                  str(stock) + self._cols.getEnd(), "' stock(s) will be added to the portfolio.")
            print(self._cols.getBold() + self._cols.getItalic() +
                  "Progressing to stock collection..."+self._cols.getEnd())

            return stockI

        elif outOfRange:
            error = 0  # set counter variable
            while outOfRange:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call for error message
                self._warningUI.integerOutOfRange()
                stock = self._warningUI.inputMessageInteger()
                number = re.search("[1-5]", stock)
                if number:

                    stockI = int(stock)
                    print()
                    print(self._cols.getBold() + self._cols.getPurple()+"[ALERT]"+self._cols.getEnd() + " Your selection will ensure at least '", self._cols.getBold() +
                          stock + self._cols.getEnd(), "' stock(s) will be added to the portfolio.")
                    print(self._cols.getBold() + self._cols.getItalic() +
                          "Progressing to stock collection..."+self._cols.getEnd())
                    return stockI
        elif stock is None:
            counter = 0
            while stock is None:

                # function call to error validator
                self._warningUI.validateError(counter)
                counter += 1  # increase counter variable by 1

                # function call for error message
                self._warningUI.emptyInput()
                stock = self._warningUI.inputMessageInteger()
                number = re.search("[1-5]", stock)
                if number:

                    stockI = int(stock)
                    print()
                    print(self._cols.getBold() + self._cols.getPurple()+"[ALERT]"+self._cols.getEnd() + " Your selection will ensure at least '", self._cols.getBold() +
                          stock + self._cols.getEnd(), "' stock(s) will be added to the portfolio.")
                    print(self._cols.getBold() + self._cols.getItalic() +
                          "Progressing to stock collection..."+self._cols.getEnd())
                    return stockI

    def correctOptionMenu(self, fName, lName, reportHandler, accessLevel, selectionI, counter):
        """This methods was a design decision to refactor the code. It filters the view of the user by the access level and is involved during quantityOfSymbols method."""

        if selectionI == 1:
            if accessLevel == 1:

                number = self.quantityOfSymbols(selectionI)
                numberI = int(number)
                return numberI

            elif accessLevel == 2:
                if counter < 3:
                    message = self._cols.getBold() + self._cols.getPurple() + \
                        "[ALERT]" + self._cols.getEnd() + \
                        " You selected {} - Add stocks to portfolio.".format(
                            selectionI)
                    print(message)
                    print()
                    print(self._cols.getBold() + self._cols.getCyan() + "[ACCESS RESTRICTED]" + self._cols.getEnd(
                    ) + " Users of this type cannot perform this activity.")
                    print("This activity is only available for users with an access level of '" + self._cols.getBold() + self._cols.getLG()+"1" +
                          self._cols.getEnd() + "' - " + self._cols.getBold() + self._cols.getLG() + "[TRADER]" + self._cols.getEnd())
                    # function call to error validator
                    self._warningUI.validateError(counter)
                    counter += 1  # increase counter variable by 1
                    print(self._cols.getBold() + self._cols.getItalic() +
                          "Reverting to portfolio management menu..." + self._cols.getEnd())
                    self.portManagement(
                        fName, lName, reportHandler, accessLevel, counter)

        elif selectionI == 2:

            # report management menu display to user
            number = self.reportManagement(
                fName, lName, accessLevel)

            if number == 6:  # quitting

                print(self._cols.getBold() + self._cols.getRed() +
                      "[TERMINATING]" + self._cols.getEnd()+" Now exiting program...")
                sys.exit()

            if number == 0:  # revert to main menu
                return 0

            # Handler for viewing or clearing report
            self._reportUI.reportSelector(number, reportHandler)

        elif selectionI == 3:

            main = "Portfolio Management"
            # function call to quit validator
            quitConfirmation = self.quitValidator()
            quitConfirmationI = int(quitConfirmation)
            self._warningUI.quitMessage(quitConfirmationI, main)

            if quitConfirmationI == 1:  # user wants to go back to menu at this point

                self.portManagement(
                    fName, lName, reportHandler, accessLevel, counter)

    def portManagement(self, fName, lName, reportHandler, accessLevel, counter):
        """ This method enables the user to manage the portfolio through additions and removals of stock entries."""

        print("-------------------------------------Portfolio Management-----------------------------------------")
        print("Hello,", fName, lName)
        print("Welcome to your portfolio.")
        print("What operation would you like to perform?")
        print("1. Add stocks to portfolio.")
        print("2. Report management")
        print("3. Exit.")
        print()
        selection = self._warningUI.inputMessageInteger()
        correct = re.search("[1-3]", selection)
        outOfRange = re.search("[4-9]", selection)
        erroneous = re.search("[^0-9]", selection)

        if correct:
            selectionI = int(selection)

            number = self.correctOptionMenu(
                fName, lName, reportHandler, accessLevel, selectionI, counter)
            return number

        elif outOfRange:
            error = 0
            while outOfRange:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call to error message
                self._warningUI.outOfRange()
                select = self._warningUI.inputMessageInteger()
                correct = re.search("[1-3]", select)

                if correct:
                    selectionI = int(select)

                    number = self.correctOptionMenu(
                        fName, lName, reportHandler, accessLevel, selectionI, counter)
                    return number

        elif erroneous:
            error = 0
            while erroneous:

                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call to error message
                self._warningUI.matchedNotNumber()
                select = self._warningUI.inputMessageInteger()
                correct = re.search("[1-3]", select)

                if correct:
                    selectionI = int(select)

                    number = self.correctOptionMenu(
                        fName, lName, reportHandler, accessLevel, selectionI, counter)
                    return number
        elif selection is None:
            error = 0  # set counter variable
            while selection is None:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call to error message
                self._warningUI.emptyInput()
                select = self._warningUI.inputMessageInteger()
                correct = re.search("[1-3]", select)

                if correct:
                    selectionI = int(select)

                    number = self.correctOptionMenu(
                        fName, lName, reportHandler, accessLevel, selectionI, counter)
                    return number

    def optionViewer(self, choices):
        """This methods alerts users of their selection of machine model to use for calculation."""
        print(self._cols.getBold()+self._cols.getPurple() + "[ALERT] " + self._cols.getEnd() + "You have selected option '" + self._cols.getBold()+str(choices)+self._cols.getEnd() +
              "' - " + self.modeSelection(choices) + ".")

    def mainMenu(self):
        """This method displays the main menu to the user to decide which mode of program they wish to experience."""

        print("--------------------------------------------Main Menu---------------------------------------------")
        print("What operation would you like to perform on your portfolio?")
        print(
            "1. Evaluate 'Random Forest-PSO' model accuracy.")
        print(
            "2. Evaluate 'Random Forest' model accuracy.")
        print("3. Evaluate 'Random Forest with time series splits' model accuracy.")
        print("4. Exit.")
        print()
        choice = self._warningUI.inputMessageInteger()

        # regex search condition to check for presence of anything other than the number we need
        m = re.search("[^0-9]", choice)
        correct = re.search("[1-4]", choice)
        outOfRange = re.search("[5-9]", choice)

        if m:
            error = 0  # set counter variable = 0
            while m:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call for error message
                self._warningUI.matchedNotNumber()
                choice = self._warningUI.inputMessageInteger()
                # regex search condition to check for presence of anything other than the number we need
                correct = re.search("[1-4]", choice)

                if correct:
                    choices = int(choice)
                    self.optionViewer(choices)
                    if choices < 4:
                        print(self._cols.getBold() + self._cols.getItalic() +
                              "Progressing to data download..." + self._cols.getEnd())
                    elif choices == 4:
                        print(self._cols.getBold() + self._cols.getItalic() +
                              "Progressing to exit menu..." + self._cols.getEnd())
                    return choices

        elif correct:
            choices = int(choice)
            self.optionViewer(choices)
            if choices < 4:
                print(self._cols.getBold() + self._cols.getItalic() +
                      "Progressing to data download..." + self._cols.getEnd())
            elif choices == 4:
                print(self._cols.getBold() + self._cols.getItalic() +
                      "Progressing to exit menu..." + self._cols.getEnd())
            return choices

        elif outOfRange:
            error = 0  # set counter variable = 0
            while outOfRange:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                self._warningUI.outOfRange()  # function call for error message
                choice = self._warningUI.inputMessageInteger()
                # regex search condition to check for presence of anything other than the number we need
                correct = re.search("[1-4]", choice)

                if correct:
                    choices = int(choice)
                    self.optionViewer(choices)
                    if choices < 4:
                        print(self._cols.getBold() + self._cols.getItalic() +
                              "Progressing to data download..." + self._cols.getEnd())
                    elif choices == 4:
                        print(self._cols.getBold() + self._cols.getItalic() +
                              "Progressing to exit menu..." + self._cols.getEnd())
                    return choices
        elif choice is None:
            error = 0  # set counter variable
            while choice is None:

                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call to error message
                self._warningUI.emptyInput()
                choice = self._warningUI.inputMessageInteger()
                # regex search condition to check for presence of anything other than the number we need
                correct = re.search("[1-4]", choice)

                if correct:
                    choices = int(choice)
                    self.optionViewer(choices)
                    if choices < 4:
                        print(self._cols.getBold() + self._cols.getItalic() +
                              "Progressing to data download..." + self._cols.getEnd())
                    elif choices == 4:
                        print(self._cols.getBold() + self._cols.getItalic() +
                              "Progressing to exit menu..." + self._cols.getEnd())
                    return choices

    def accessLevelSpecifier(self):
        """ Function is responsible for handling an input which is outside of the predetermined acceptable range."""

        message = self._cols.getBold() + self._cols.getBlue()+"[INTEGER]" + self._cols.getEnd() + " Enter ["+self._cols.getBold()+self._cols.getGreen()+"1"+self._cols.getEnd() + \
            "] = Trader | "+self._cols.getBold()+"OR"+self._cols.getEnd() + \
            " | Enter ["+self._cols.getBold()+self._cols.getRed() + \
            "2"+self._cols.getEnd()+"] = Software Operator: "
        choice = input(message)

        # regex search condition to check for presence of anything other than the number we need
        m = re.search("[1-2]", choice)
        outOfBound = re.search("[3-9]", choice)
        erroneous = re.search("[^0-9]", choice)

        if m:

            choices = int(choice)
            print()
            print(self._cols.getBold() + self._cols.getPurple() +
                  "[ALERT]" + self._cols.getEnd() + " Personal information collected.")
            print(self._cols.getBold() + self._cols.getItalic() +
                  "Progressing to Portfolio Management..." + self._cols.getEnd())

            return choices

        elif outOfBound:
            error = 0  # set counter variable
            while outOfBound:

                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call for error message
                self._warningUI.integerOutOfRangeSC()
                choiceI = self._warningUI.inputMessageInteger()
                # regex search condition to check for presence of anything other than the number we need
                m = re.search("[1-2]", choiceI)

                if m:  # if matched
                    choices = int(choiceI)
                    print(self._cols.getBold() + self._cols.getPurple() + "[ALERT]" + self._cols.getEnd()+"You now have an access level of '" + str(choices),
                          "' .")
                    return choices

        elif erroneous:

            error = 0  # set counter variable
            while error < 3:

                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call for error message
                self._warningUI.matchedNotNumber()
                choiceI = self._warningUI.inputMessageInteger()
                # regex search condition to check for presence of anything other than the number we need
                m = re.search("[1-2]", choiceI)

                if m:  # if matched
                    choices = int(choiceI)
                    print(self._cols.getBold() + self._cols.getPurple() + "[ALERT]" + self._cols.getEnd()+"You now have an access level of '" + str(choices),
                          "' .")
                    return choices
        elif choice is None:
            error = 0  # set counter variable
            while choice is None:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call to error message
                self._warningUI.emptyInput()

                choiceI = self._warningUI.inputMessageInteger()
                # regex search condition to check for presence of anything other than the number we need
                m = re.search("[1-2]", choiceI)

                if m:  # if matched
                    choices = int(choiceI)
                    print(self._cols.getBold() + self._cols.getPurple() + "[ALERT]" + self._cols.getEnd()+"You now have an access level of '" + str(choices),
                          "' .")
                    return choices

    def modeSelection(self, confirm):
        """This method outputs the mode of program to the user."""

        if confirm == 1:
            model = self._cols.getBold() + "Random Forest-PSO" + self._cols.getEnd()
            return model

        elif confirm == 2:
            model = self._cols.getBold() + "Random Forest" + self._cols.getEnd()
            return model

        elif confirm == 3:
            model = self._cols.getBold() + "Random Forest with time series splits" + \
                self._cols.getEnd()
            return model
        elif confirm == 4:
            message = "Quit the program."
            return message

    def displayResults(self, tList, rmse, mae, confirm):
        """ This methods displays the model results obtained for the selected stock symbol."""

        print("-----------------------------------------Results-------------------------------------------------")
        print(self._cols.getBold() + self._cols.getPurple() +
              "[ALERT]" + self._cols.getEnd() + " Displaying...")
        print("Stock symbol: " + self._cols.getBold() +
              tList + self._cols.getEnd())
        print("Model: " + self.modeSelection(confirm))
        print("RMSE:", self._cols.getBold() + str(rmse) + self._cols.getEnd())
        print("MAE:", self._cols.getBold() + str(mae) + self._cols.getEnd())
        print()
        print(self._cols.getBold() + self._cols.getItalic() +
              "Progressing to report creation..." + self._cols.getEnd())

    def reportManagement(self, fName, lName, accessLevel):
        """This methods is responsible for report management properties of the user within the system, and constrains the view according to the access level of the user."""

        print(self._cols.getBold() + self._cols.getPurple() +
              "[ALERT]" + self._cols.getEnd() + " Portfolio Management completed.")
        print(self._cols.getBold()+self._cols.getItalic() +
              "Progressing to report management..."+self._cols.getEnd())

        if accessLevel == 1:  # trader
            print(
                "--------------------------------Report Management--------------------------------")
            print("Hello", fName, lName + ".")
            print("You have an access level of '" + self._cols.getBold() +
                  str(accessLevel) + self._cols.getEnd() + "' - "+self._cols.getBold()+self._cols.getLG()+"[TRADER]"+self._cols.getEnd())
            print("You now have the option of one of the following:")
            print(self._cols.getBold() + "1" + self._cols.getEnd() +
                  ". View your report information.")
            print(self._cols.getBold() + "2" +
                  self._cols.getEnd() + ". Exit the program.")
            print()
            valid = self._warningUI.inputMessageInteger()
            correct = re.search("[1-2]", valid)
            incorrect = re.search("[3-9]", valid)
            erroneous = re.search("[^0-9]", valid)

            if correct:
                validI = int(valid)
                if validI == 1:  # view report
                    return validI

                elif validI == 2:  # quit program
                    number = self.quitValidator()
                    if number == 0:
                        return 6
                    if number == 1:  # revert to main menu
                        print(self._cols.getBold() + self._cols.getItalic() +
                              "Reverting to start menu...." + self._cols.getEnd())
                        return 0
            if incorrect:

                error = 0  # set counter variable
                while incorrect:

                    # function call to error validator
                    self._warningUI.validateError(error)
                    error += 1  # increase counter variable by 1

                    # function call for error message
                    self._warningUI.outOfRange()
                    confirm = self._warningUI.inputMessageInteger()
                    correct = re.search("[1-2]", confirm)
                    if correct:
                        confirmI = int(confirm)

                        if confirmI == 1:  # view report
                            return confirmI

                        elif confirmI == 2:  # quit program
                            number = self.quitValidator()
                            if number == 0:
                                return 6
                            if number == 1:  # revert to main menu
                                print(self._cols.getBold() + self._cols.getItalic() +
                                      "Reverting to start menu...." + self._cols.getEnd())
                                return 0

            elif erroneous:
                error = 0
                while erroneous:
                    # function call to error validator
                    self._warningUI.validateError(error)
                    error += 1  # increase counter variable by 1

                    # function call to error message
                    self._warningUI.matchedNotNumber()
                    confirm = self._warningUI.inputMessageInteger()
                    correct = re.search("[1-2]", confirm)

                    if correct:
                        confirmI = int(confirm)
                        if confirmI == 1:  # view report
                            return confirmI
                        elif confirmI == 2:  # quit program
                            number = self.quitValidator()
                            if number == 0:
                                return 6
                            if number == 1:  # revert to main menu
                                print(self._cols.getBold() + self._cols.getItalic() +
                                      "Reverting to start menu...." + self._cols.getEnd())
                                return 0
            elif valid is None:
                error = 0  # set counter variable
                while valid is None:

                    # function call to error validator
                    self._warningUI.validateError(error)
                    error += 1  # increase counter variable by 1

                    # function call to error message
                    self._warningUI.emptyInput()
                    confirm = self._warningUI.inputMessageInteger()
                    correct = re.search("[1-2]", confirm)

                    if correct:
                        confirmI = int(confirm)
                        if confirmI == 1:  # view report
                            return confirmI
                        elif confirmI == 2:  # quit program
                            number = self.quitValidator()
                            if number == 0:
                                return 6
                            if number == 1:  # revert to main menu
                                print(self._cols.getBold() + self._cols.getItalic() +
                                      "Reverting to start menu...." + self._cols.getEnd())
                                return 0

        elif accessLevel == 2:  # software operator
            print(
                "--------------------------------Report Management--------------------------------")
            print("Hello", fName, lName + ".")
            print("You have an access level of '" + self._cols.getBold() +
                  str(accessLevel) + self._cols.getEnd() + "' - "+self._cols.getBold()+self._cols.getCyan()+"[SOFTWARE OPERATOR]"+self._cols.getEnd())
            print("You now have the option of one of the following:")
            print(self._cols.getBold() + "1" + self._cols.getEnd() +
                  ". View all available reports.")
            print(self._cols.getBold() + "2" + self._cols.getEnd() +
                  ". Clear information from a report.")
            print(self._cols.getBold() + "3" +
                  self._cols.getEnd()+". Delete a report.")
            print(self._cols.getBold() + "4" +
                  self._cols.getEnd() + ". Exit the program.")
            print()
            valid = self._warningUI.inputMessageInteger()
            correct = re.search("[1-4]", valid)
            incorrect = re.search("[5-9]", valid)
            erroneous = re.search("[^0-9]", valid)

            if correct:

                validI = int(valid)

                if validI == 4:
                    number = self.quitValidator()
                    if number == 0:
                        return 6
                    elif number == 1:
                        print(self._cols.getBold() + self._cols.getItalic() +
                              "Reverting to start menu...." + self._cols.getEnd())
                        return 0
                else:
                    return validI

            elif incorrect:
                error = 0  # set counter variable
                while incorrect:

                    # function call to error validator
                    self._warningUI.validateError(error)
                    error += 1  # increase counter variable by 1

                    # function call for error message
                    self._warningUI.outOfRange()
                    confirm = self._warningUI.inputMessageInteger()
                    correct = re.search("[1-4]", confirm)

                    if correct:
                        confirmI = int(confirm)
                        if confirmI == 4:
                            number = self.quitValidator()
                            if number == 0:
                                return 6
                            elif number == 1:
                                print(self._cols.getBold() + self._cols.getItalic() +
                                      "Reverting to start menu...." + self._cols.getEnd())
                                return 0
                        else:
                            return confirmI

            elif erroneous:
                error = 0
                while erroneous:

                    # function call to error validator
                    self._warningUI.validateError(error)
                    error += 1  # increase counter variable by 1

                    # function call to error message
                    self._warningUI.matchedNotNumber()
                    confirm = self._warningUI.inputMessageInteger()
                    correct = re.search("[1-4]", confirm)

                    if correct:
                        confirmI = int(confirm)
                        if confirmI == 4:
                            number = self.quitValidator()
                            if number == 0:
                                return 6
                            elif number == 1:
                                print(self._cols.getBold() + self._cols.getItalic() +
                                      "Reverting to start menu...." + self._cols.getEnd())
                                return 0
                        else:
                            return confirmI

            elif valid is None:
                error = 0  # set counter variable
                while valid is None:
                    # function call to error validator
                    self._warningUI.validateError(error)
                    error += 1  # increase counter variable by 1

                    # function call to error message
                    self._warningUI.emptyInput()
                    confirm = self._warningUI.inputMessageInteger()
                    correct = re.search("[1-4]", confirm)

                    if correct:
                        confirmI = int(confirm)
                        if confirmI == 4:
                            number = self.quitValidator()
                            if number == 0:
                                return 6
                            elif number == 1:
                                print(self._cols.getBold() + self._cols.getItalic() +
                                      "Reverting to start menu...." + self._cols.getEnd())
                                return 0
                        else:
                            return confirmI


class AbstractString(ABC):

    @abstractmethod
    def nameValidateF(self) -> str:
        pass

    @abstractmethod
    def nameValidateL(self, fName) -> str:
        pass

    @abstractmethod
    def collectID(self, number) -> str:
        pass

    @abstractmethod
    def validateID(self, traderID, number) -> str:
        pass

    @abstractmethod
    def nameValidationMechanism(self, fName) -> str:
        pass

    @abstractmethod
    def lNameValidationMechanism(self, lName, fName) -> str:
        pass

    @abstractmethod
    def identificationVM(self, number) -> str:
        pass


class stringOutputUI(AbstractString):
    """ Derived class for the taes user input for validation and produces string outputs which inherits the base class which has all the error messages."""

    def __init__(self, cols, warning):
        self._cols = cols
        self._warningUI = warning

    def nameValidationMechanism(self, fName):
        """This methods validates the first name input taken during the start up menu."""

        charString = []
        size = len(fName)
        for i in range(0, size):

            if i == 0:
                new = fName[i].upper()
                charString.append(new)
            else:
                new = fName[i].lower()
                charString.append(new)

        name = "".join(charString)
        return name

    def nameValidateF(self):
        """ This method validates the user inputs for first name and returns the validated input."""

        print("----------------------------------------Start Menu----------------------------------------------")
        print("Hello user.")
        print(
            "To best assist you I will need to collect some of your personal information.")

        fName = self._warningUI.fNameMessage()

        notString = re.search("[^a-zA-Z]", fName)

        if notString:

            error = 0  # set counter variable to 0
            while notString:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call for error message
                self._warningUI.matchedNotString()
                fName = self._warningUI.fNameMessage()
                isString = re.search("[a-zA-Z]", fName)

                if isString:

                    name = self.nameValidationMechanism(fName)
                    return name

        elif fName is None:
            error = 0  # set counter variable
            while fName is None:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call to error message
                self._warningUI.emptyInput()

                fName = self._warningUI.fNameMessage()
                isString = re.search("[a-zA-Z]", fName)

                if isString:

                    name = self.nameValidationMechanism(fName)
                    return name

        else:

            name = self.nameValidationMechanism(fName)
            return name

    def lNameValidationMechanism(self, lName, fName):
        """ This method was a design design made in order to refactor the code, and is a part of the lName validation mechanism."""

        charString = []
        size = len(lName)
        for i in range(0, size):

            if i == 0:
                new = lName[i].upper()
                charString.append(new)
            else:
                new = lName[i].lower()
                charString.append(new)

        surname = "".join(charString)

        if surname == fName:
            while surname == fName:
                self._warningUI.nameRepeat()
                surname = self.nameValidateL(fName)
                if not surname == fName:
                    return surname

        elif not surname == fName:

            return surname

    def nameValidateL(self, fName):
        """ This method validates the user inputs for last name and returns the validated input."""

        lName = self._warningUI.lNameMessage()
        notStringLast = re.search("[^a-zA-Z]", lName)

        if notStringLast:

            error = 0  # set counter variable to 0
            while notStringLast:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1

                # function call for error message
                self._warningUI.matchedNotString()
                lName = self._warningUI.lNameMessage()
                isString = re.search("[a-zA-Z]", lName)

                if isString:

                    name = self.lNameValidationMechanism(lName, fName)
                    return name

        elif lName is None:
            error = 0  # set counter variable
            while lName is None:
                # function call to error validator
                self._warningUI.validateError(error)
                error += 1  # increase counter variable by 1
                # function call to error message
                self._warningUI.emptyInput()

                lName = self._warningUI.lNameMessage()
                isString = re.search("[a-zA-Z]", lName)

                if isString:

                    name = self.lNameValidationMechanism(lName, fName)
                    return name

        else:

            name = self.lNameValidationMechanism(lName, fName)
            return name

    def identificationVM(self, number):
        """ This method validates the traderID of the trader in the system against the required format of the credentials."""
        traderIDD = self._warningUI.traderIDMessage()
        correct = re.search("[a-zA-Z0-9]", traderIDD) #if it contains both numbers and alphabetical letters
        if correct and len(traderIDD) == 5: #if in the specified format
            traderID = self.validateID(traderIDD, number) #function call to validate TRADER ID
            traderIDS = str(traderID)
            return traderIDS

    def collectID(self, number):
        """ This method alerts the user of the mode of report management and collect the trader ID from the user of the report which they wish to alter."""

        if number == 1:
            print(self._cols.getBold() + self._cols.getPurple() +
                  "[ALERT] " + self._cols.getEnd() + "You selected '"+self._cols.getBold() + str(number) +
                  self._cols.getEnd()+"' - View your report.")
            print("")
            print("Below are all the reports available for viewing:")

        elif number == 2:
            print(self._cols.getBold() + self._cols.getPurple() + "[ALERT] " + self._cols.getEnd() + "You selected '"+self._cols.getBold() + str(number) +
                  +self._cols.getEnd()+"' - Clear your report.")
            print("")
            print("Below are all the reports available for clearing:")

        elif number == 3:
            print(self._cols.getBold() + self._cols.getPurple() + "[ALERT] " + self._cols.getEnd() + "You selected '"+self._cols.getBold() + str(number) +
                  self._cols.getEnd()+"' - Delete your report.")
            print("")
            print("Below are all the reports available for deleting:")

        elif number == 4:
            print("")
            print("Below are all the reports available for appending:")

        reportFiles = []
        for file in glob.glob("*.txt"):
            betterFile = file.replace(".txt", "")
            reportFiles.append(betterFile)

            size = len(reportFiles)
            for i in range(size):
                print("Trader ID - "+self._cols.getBold() +
                      reportFiles[i] + self._cols.getEnd())

            print()
            print("Your trader identification is in the form '" +
                  self._cols.getBold()+"AB123"+self._cols.getEnd()+"'.")
            print("Ensure there is "+self._cols.getBold()+"NOT" + self._cols.getEnd()+" any presence of "+self._cols.getBold() +
                  "SPECIAL CHARACTERS"+self._cols.getEnd()+" or "+self._cols.getBold()+"WHITESPACE"+self._cols.getEnd()+".")
            traderID = self._warningUI.traderIDMessage()
            erroneous = re.search("[^a-zA-Z0-9]", traderID)

            if ' ' in traderID:
                error = 0
                while ' ' in traderID:  # if whitespace present

                    # function call to error validator
                    self._warningUI.validateError(error)
                    error += 1  # increase counter variable by 1

                    self._warningUI.matchedWhitespace()
                    traderIDD = self._warningUI.traderIDMessage()

                    if ' ' not in traderIDD:  # if whitespace not present
                        traderID = self.validateID(traderIDD, number)
                        traderIDS = str(traderID)
                        return traderIDS

            elif erroneous:
                error = 0  # set counter variable
                while erroneous:
                    # function call to error validator
                    self._warningUI.validateError(error)
                    error += 1  # increase counter variable by 1

                    self._warningUI.invalidIDMessage()
                    traderID = self.identificationVM(number)
                    return traderID

            elif len(traderID) < 5:

                error = 0  # set counter variable
                while len(traderID) < 5:
                    # function call to error validator
                    self._warningUI.validateError(error)
                    error += 1  # increase counter variable by 1
                    self._warningUI.invalidIDMessage()
                    traderID = self.identificationVM(number)
                    return traderID

            elif traderID is None:
                error = 0  # set counter variable
                while traderID is None:
                    # function call to error validator
                    self._warningUI.validateError(error)
                    error += 1  # increase counter variable by 1

                    # function call to error message
                    self._warningUI.emptyInput()
                    traderID = self.identificationVM(number)
                    return traderID

            else:

                traderIDD = self.validateID(traderID, number)
                traderIDS = str(traderIDD)
                return traderIDS

    def validateID(self, traderID, number):
        """ Validates the trader Identification Tag which is used to access/amend reports."""

        # change to character array, split function
        # change into two strings one character and one integer string
        # re.match for first two characters only presence of characters
        # re.match of next four characters only presence of number

        counter = []  # counter holder variable

        if len(counter) == 3:
            # function call for error message
            self._warningUI.maxFailures()

        if len(counter) == 2:
            # function call for error message
            self._warningUI.shutDownWarning()

        # regex condition to split string into two strings
        r = re.compile("([a-zA-Z]+)([0-9]+)")
        m = r.match(traderID)
        charString = m.group(1)  # first group is the character string
        integerString = m.group(2)  # second group is the integer string

        if not charString:  # if empty
            if len(counter) < 3:
                counter.append(0)
                self._warningUI.matchedNotString()  # error message for no strings
                self._warningUI.invalidIDMessage()  # error message for invalid ID
                chec = self.traderIDMessage(self._cols)
                self.validateID(chec, number)

        elif not integerString:  # if empty
            if len(counter) < 3:
                counter.append(0)
                self._warningUI.invalidIDMessage()  # error message for invalid ID
                self._warningUI.matchedNotNumber()  # error message for no integer
                chec = self.traderIDMessage(self._cols)
                self.validateID(chec, number)

        else:

            if 3 <= len(charString):  # more than two alphabetical chars
                if len(counter) < 3:
                    counter.append(0)
                    self._warningUI.invalidIDMessage()  # error message for invalid ID
                    print(self._cols.getYellow() + self._cols.getBold() + "[STRING]" + self._cols.getEnd(), " Ensure no more than" +
                          self._cols.getBold() + " TWO" + self._cols.getEnd() + " alphabetical characters are present.")
                    traderID = self.collectID(number)

            else:
                print(self._cols.getBold() + self._cols.getPurple() +
                      "[ALERT]" + self._cols.getEnd() + " Trader Identification Validated.")
                print(self._cols.getBold() + self._cols.getItalic() +
                      "Progressing to report..." + self._cols.getEnd())
                return traderID
