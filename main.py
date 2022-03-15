""" This module contains the main program of the project. """
from datetime import datetime
from controller import Facade, ReporterUI, PortfolioManagerUI
from colours import Colours
from interface import warningUI, stringOutputUI, OutputUI

# Set start-date of stock price series collection
startPeriod = datetime(2012, 1, 1)
# Set end-date of stock price series collection
endPeriod = datetime(2017, 1, 1)


def main():
    """ Main program which presents the option to calculate model accuracy for three different models:
    1. Random Forest - PSO.
    2. Random Forest.
    3. Adapted Random Forest.
    As well as view the evaluation report of all calculations."""

    while True:

        # Initialisation of lists
        listOfSymbols = []  # Holder variable symbols
        tList = []  # Holder transfer variable for list of ticker
        inputs = []  # holder variable for the amount of stock entries to be made
        # holder variable for the number of stock entries to remove or add.

        col = Colours()
        warning = warningUI(col)
        stringOut = stringOutputUI(col, warning)
        # Instantiating subsystem1 for the facade control class
        reporter = ReporterUI(stringOut, warning, col)
        intOut = OutputUI(col, warning, reporter)
        # Instantiating subsystem2 for the facade control class
        subsystem2 = PortfolioManagerUI(col, warning)
        # Instantiating controller class
        controller = Facade(reporter, subsystem2, intOut,
                            stringOut, col, warning)

        inputs, fName, lName = controller.handleUserMenuRequest()

        if inputs == 0:  # if user wanted to check the report revert back to main menu
            main()

        # unpacking variables
        name = str(fName)
        surname = str(lName)

        # Stock symbol management
        correctSymb, sList, confirmS = controller.sendRequestValidateSymbol(
            tList, inputs, listOfSymbols)

        # unpacking variables
        confirm = int(confirmS)

        if(confirm == 1):

            # Preprocessing module
            xTrain, yTrain, xTest, yTest, targetVARS, exploratoryTraining, exploratoryTesting = controller.orchastrateProcessing(
                sList, correctSymb, startPeriod, endPeriod, confirm)  # loading train and test data.

            # Machine learning module
            mae, rmse = controller.orchastrateEvaluation(
                xTrain, yTrain, xTest, yTest, confirm, targetVARS, exploratoryTraining, exploratoryTesting)  # evaluating classifier

            # Report creation and management
            controller.orchastrateReportProcessing(correctSymb, sList, name,
                                                   surname, rmse, mae, confirm)
        elif confirm == 2:

            # Preprocessing module
            xTrain, yTrain, xTest, yTest, targetVARS, exploratoryTraining, exploratoryTesting = controller.orchastrateProcessing(
                sList, correctSymb, startPeriod, endPeriod, confirm)

            # Machine learning module
            mae, rmse = controller.orchastrateEvaluation(
                xTrain, yTrain, xTest, yTest, confirm, targetVARS, exploratoryTraining, exploratoryTesting)

            # Report creation and management
            controller.orchastrateReportProcessing(correctSymb, sList, name,
                                                   surname, rmse, mae, confirm)

        elif confirm == 3:

            # Preprocessing module
            xTrain, yTrain, xTest, yTest, targetVARS, exploratoryTraining, exploratoryTesting = controller.orchastrateProcessing(
                sList, correctSymb, startPeriod, endPeriod, confirm)

            # Machine learning module
            mae, rmse = controller.orchastrateEvaluation(
                xTrain, yTrain, xTest, yTest, confirm, targetVARS, exploratoryTraining, exploratoryTesting)

            # Report creation and management
            controller.orchastrateReportProcessing(correctSymb, sList, name,
                                                   surname, rmse, mae, confirm)

        elif confirm == 4:

            quitI = controller.sendQuitMessage()
            quitIS = int(quitI)

            if quitIS == 1:  # user wants to go back to main program at this point
                main()


if __name__ == "__main__":

    main()
