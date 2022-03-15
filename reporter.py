"""This module contains the Trader class responsible for storing information to be stored in records."""
from __future__ import annotations
from abc import ABC, abstractmethod
import random
import os


class Person(ABC):

    @abstractmethod
    def __init__(self, *args) -> None:
        pass


class SoftwareOperator(Person):
    """Software Operator class responsible for storing all the details with the user of the program.
        """

    _fileName: str = ""

    def __init__(self, *args):
        super(SoftwareOperator, self).__init__(*args)
        self._fName = args[0]
        self._lName = args[1]
        self._col = args[2]


class Trader(Person):  # base class
    """Trader class responsible for storing all the details with the user of the program and the results of their calculations.
        """

    _modelText: str = ""
    _fileName: str = ""

    def __init__(self, *args):
        """Initialisation method which sets all the private and protected variables with values of the user at runtime."""

        super(Trader, self).__init__(self, *args)
        self._fName = args[0]
        self._lName = args[1]
        self._mae = args[2]
        self._rmse = args[3]
        self._traderID = self.assignIdentification(args[0], args[1])
        self._stockID = args[4]
        self._modelNo = args[5]
        self._col = args[6]

    def assignIdentification(self, fName, lName):
        """"Method responsible for generating the trader identification in the form 'AB123'.
            Uses the first characters of the first and last name as 'AB' part of the format.
            Randomly generates 3 integers between the range 0-9 for the '123' segment."""

        number = []

        for randomInteger in random.sample(range(0, 9), 3):
            number.append(randomInteger)

        integer1 = number[0]
        integer2 = number[1]
        integer3 = number[2]
        number.clear()

        charNameF = list(fName[0])
        charNameL = list(lName[0])
        self.__traderID = str(charNameF[0]) + str(charNameL[0]) + \
            str(integer1) + str(integer2) + str(integer3)

        return self.__traderID


class Editor(ABC):
    """ Editor interface for editing reports of traders."""
    @abstractmethod
    def writeReport(self, traderIDN, number) -> None:
        pass

    @abstractmethod
    def clearReport(self, traderID, ) -> None:
        pass

    @abstractmethod
    def viewReport(self, traderID) -> None:
        pass

    @abstractmethod
    def deleteReport(self, traderID) -> None:
        pass


class ReportEditor(Trader, Editor):  # derived class

    rmse = []
    mae = []
    traderID = []
    stockID = []

    def __init__(self, *args):
        Trader.__init__(self, *args)

    def writeReport(self, traderIDN, number):
        """ Method responsible for writing the report containing all the details of the model evaluation for the trader/user.
            Instantiates the interfacer class in order to get the mode of the program used.
            If statements used to either append to an existing file, or create a new file if not existing. """

        fullName = self._fName + " " + self._lName
        self.rmse.append(str(self._rmse))
        self.mae.append(str(self._mae))
        self.traderID.append(str(self._traderID))
        self.stockID.append(str(self._stockID))

        if self._modelNo == 1:
            self._modelText = "Random Forest-PSO"
        elif self._modelNo == 2:
            self._modelText = "Random Forest"
        elif self._modelNo == 3:
            self._modelText = "Random Forest with time series splits"

        traderS = str(traderIDN)

        # condition for whether .txt tag is added or not, based on method of obtaining traderID.
        if number == 1:  # append to existing file
            fileName = traderS + ".txt"

        elif number == 2:  # create new file for writing.
            fileName = traderS + ".txt"

        header = "Account Holder: " + fullName
        space = "-----------------------------------------------"
        body1 = "Stock symbol: " + str(self.stockID[-1])
        body2 = "Model: " + self._modelText
        body3 = "RMSE: " + str(self.rmse[-1])
        body4 = "MAE: " + str(self.mae[-1])

        if os.path.isfile(fileName):
            print("")
            print("Existing report with identification found.")
            print("Appending the new information to this report...")

            # appending the new model and stock evaluation information
            reportInfoA = [space, body1, body2, body3, body4]

            with open(fileName, 'a', encoding='UTF-8') as report:  # writing to file in append mode
                report.write("\n")
                # connects elements inside list of strings
                report.write("\n".join(map(str, reportInfoA)))
            print(self._col.getBold() + self._col.getPurple() +
                  "[ALERT] " + self._col.getEnd() + "New model information appended.")
            print(self._col.getBold() + self._col.getItalic() +
                  "Progressing to start menu..."+self._col.getEnd())

        else:

            if number == 1:
                print()
                print(self._col.getBold() + self._col.getRed() +
                      "[ERROR]"+self._col.getEnd()+" You are attempting to write to file that doesn't exist.")
                print("Writing new report...")
                traderS = self._traderID
                fileName = traderS + ".txt"
            else:
                print()
                print("Writing new report...")

            pageTitle = "Portfolio Report ID: " + traderS

            reportInfoW = [pageTitle, header,
                           space, body1, body2, body3, body4]
            with open(fileName, 'w', encoding='UTF-8') as report:  # writing to file in write mode
                report.write("\n".join(map(str, reportInfoW)))
            print(self._col.getBold() + self._col.getPurple() +
                  "[ALERT]"+self._col.getEnd()+" Report created.")
            print(self._col.getBold() + self._col.getItalic() +
                  "Progressing to start menu..."+self._col.getEnd())

    def clearReport(self, traderID):
        pass

    def viewReport(self, traderID):
        """This method is for outputting the contents of the report to the user.
           Checks if the file exists and if so it prints the detail.
           If file does not exits outputs error message and returns to the main menu."""

        traderS = str(traderID)
        fileName = traderS + ".txt"

        if os.path.isfile(fileName):

            # opening the file in read mode.
            with open(fileName, 'r', encoding='UTF-8') as report:
                # strip the file of any new line characters
                reportInformation = report.read().strip()

                print(
                    "-------------------------------------------------------------------------------------------")
                print(self._col.getBold() +
                      "TRADER REPORT" + self._col.getEnd())
                print(reportInformation)

        else:
            print()
            print(self._col.getBold() + self._col.getRed() + "[ERROR]" +
                  self._col.getEnd() + " Report not found.")
            print(self._col.getBold() + self._col.getPurple() +
                  "[ALERT]" + self._col.getEnd() +
                  " Ensure to calculate stock accuracy with a specified model "+self._col.getBold()+"FIRST" + self._col.getEnd()+" before viewing reports.")
            print(self._col.getBold() + self._col.getItalic() +
                  "Progressing to start menu..." + self._col.getEnd())

    def deleteReport(self, traderID):
        pass


class ReportManager(SoftwareOperator, Editor):  # derived class

    def __init__(self, *args):
        SoftwareOperator.__init__(self, *args)

    def writeReport(self, traderIDN, number) -> None:
        pass

    def clearReport(self, traderID):
        """This methods clears the contents of the report after validating the presence of the last name in the file.
            outputs an exception in the case of a failed attempt of opening the file."""

        lNameComparison = []
        traderS = str(traderID)
        fileName = traderS + ".txt"

        # opening file in read mode.
        with open(fileName, 'r', encoding='UTF-8') as report:
            lines = report.readlines()
            # line containing the first and last name variables.
            for word in lines:
                if traderS in word:  # if last name is present in this line in the report
                    lNameComparison.append(1)

        if len(lNameComparison) != 0:  # if the lName list is not empty
            try:
                print("")
                print("Clearing the report for",
                      self._fName, self._lName)
                # overwriting the file to erase the contents.
                open(fileName, 'w', encoding='UTF-8').close()
                print(self._col.getBold() + self._col.getPurple() +
                      "[ALERT]" + self._col.getEnd()+" Report contents have been cleared.")
                print(self._col.getBold() + self._col.getItalic() +
                      "Progressing to start menu..." + self._col.getEnd())

            except OSError:
                print(self._col.getBold() +
                      "[EXCEPTION]" + self._col.getEnd() + " Unable to clear the file.")
        else:
            print(self._col.getRed() + self._col.getBold() +
                  "[ERROR]" + self._col.getEnd()+" Trader Identification entered not found.")
            print(self._col.getBold() + self._col.getItalic() +
                  "Progressing to start menu..." + self._col.getEnd())

    def viewReport(self, traderID):
        """This method is for outputting the contents of the report to the user.
           Checks if the file exists and if so it prints the detail.
           If file does not exits outputs error message and returns to the main menu."""

        traderS = str(traderID)
        fileName = traderS + ".txt"

        if os.path.isfile(fileName):

            # opening the file in read mode.
            with open(fileName, 'r', encoding='UTF-8') as report:
                # strip the file of any new line characters
                reportInformation = report.read().strip()

                print(
                    "-------------------------------------------------------------------------------------------")
                print(self._col.getBold() +
                      "TRADER REPORT" + self._col.getEnd())
                print(reportInformation)

        else:
            print()
            print(self._col.getBold() + self._col.getRed() + "[ERROR]" +
                  self._col.getEnd() + " Reports not found.")
            print(self._col.getBold() + self._col.getPurple() +
                  "[ALERT]" + self._col.getEnd() +
                  " Ensure to calculate stock accuracy with a specified model "+self._col.getBold()+"FIRST" + self._col.getEnd()+" before viewing reports.")
            print(self._col.getBold() + self._col.getItalic() +
                  "Progressing to start menu..." + self._col.getEnd())

    def deleteReport(self, traderID):
        """This method is responsible for deleting the specified report."""

        self._fileName = "{}.txt".format(traderID)
        message = self._col.getBold()+self._col.getPurple() + "[ALERT]" + self._col.getEnd() + " Report ID: {} has been successfully deleted.".format(
            traderID)

        if os.path.isfile(self._fileName):  # if file exists with the filename

            # delete the file with the associated filename
            os.remove(self._fileName)
            print(message)
            print(self._col.getBold() + self._col.getItalic() +
                  "Progressing to start menu..." + self._col.getEnd())

        else:
            print("")
            print(self._col.getBold() + self._col.getRed() +
                  "[ERROR] " + self._col.getEnd() + "Reports not found." + self._col.getEnd())
            print(self._col.getBold() + self._col.getRed() +
                  "[ERROR] " + self._col.getEnd() + "Ensure that reports are within the system before attempting deletes.")
            print(self._col.getBold() + self._col.getItalic() +
                  "Progressing to start menu..." + self._col.getEnd())
