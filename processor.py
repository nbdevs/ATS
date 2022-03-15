""" Responsible for data extraction, cleaning and loading, as well as feature transformation."""
from __future__ import annotations
from abc import ABC, abstractmethod
import logging
import pandas as pd
import numpy as np
from scipy.stats import mstats
import yfinance as yf
# --------------------------------------------------------------------------------------------------


class Processor(ABC):
    """ Processor interface for creating different forms of stock portfolios for the 3 different models."""

    @abstractmethod
    def downloadData(self, tickerName, startPeriod, endPeriod) -> pd.DataFrame:
        pass

    @abstractmethod
    def createSMA(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def createStochastic(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def createRSI(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def createMACD(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def createRC(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def splitPreparation(self, scaler) -> pd.DataFrame:
        pass

    @abstractmethod
    def splitPreparationRF(self, scaler) -> pd.DataFrame:
        pass


class ConcreteProcessor(Processor):
    """Follows the implementation details provided in the interface in order to build the portfolio in the specified manner needed for the model of choice.
    Class for pre-processing of stock price series."""

    def __init__(self, col) -> pd.DataFrame:
        """Each new instance contains an empty stock portfolio product to build upon."""
        stockPort = pd.DataFrame()  # Create empty pd.DataFrame for portfolio of stock
        self.stockPort = stockPort
        self._col = col

    def downloadData(self, tickerName, startPeriod, endPeriod) -> pd.DataFrame:
        """ Extracts price series data from yahoo finance."""

        # Initialisation of parameters
        dataHolder = []

        print("------------------------------Downloading Portfolio Data--------------------------------------")

        # Print the symbol which is being downloaded
        print(str(" Downloading stock information for ") + tickerName,
              sep=",",
              end=",",
              flush=True,
              )

        try:
            # Load into the list: daily open, close , trading vol, high, low, adjusted close of stocks

            dataHolder = yf.download(
                tickerName, start=startPeriod, end=endPeriod)  # daily interval stock prices

            # Append the individual stock prices
            if len(dataHolder) == 0:
                print("[FATAL] Data unsuccessfully loaded.")

            else:
                dataHolder["STOCK-NAME"] = tickerName
                self.stockPort = self.stockPort.append(
                    dataHolder, sort=False)
                self.stockPort.head()

        except RuntimeError:
            logging.exception("Download failed: %s", tickerName)
            print(self._col.boldFont + self._col.redFont +
                  "FATAL] " + self._col.endFont + "List index out of range.")
            print("Entered number bigger than than contained in portfolio.")
            print("Area of error - symbolCollector()")
            exit()

        print(self._col.boldFont + self._col.purpleFont +
              "[ALERT] " + self._col.endFont + "Portfolio download completed.")
        print(self._col.boldFont + self._col.italicFont +
              "Progressing to feature engineering..." + self._col.endFont)
        return self.stockPort

    # Feature engineer technical indicators for each stock

    # Simple Moving Average 7 day and 21 day and difference between them derived indicator
    def createSMA(self) -> pd.DataFrame:
        """ Creates simple moving average indicator from raw data."""

        self.stockPort["SMA_7"] = self.stockPort.groupby("STOCK-NAME")["Close"].transform(
            lambda x: x.rolling(window=7).mean()
        )
        self.stockPort["SMA_21"] = self.stockPort.groupby("STOCK-NAME")["Close"].transform(
            lambda x: x.rolling(window=21).mean()
        )

        self.stockPort["SMA_RATIO"] = self.stockPort["SMA_7"] / \
            self.stockPort["SMA_21"]

        return self.stockPort

    def createStochastic(self) -> pd.DataFrame:
        """ Creates stochastic technical indicator from raw market data."""

        # Stochastic Oscillators for overbought and oversold and difference between them derived indicator
        self.stockPort["LOWEST_7D"] = self.stockPort.groupby("STOCK-NAME")["Low"].transform(
            lambda x: x.rolling(window=7).min()
        )
        self.stockPort["HIGH_7D"] = self.stockPort.groupby("STOCK-NAME")["High"].transform(
            lambda x: x.rolling(window=21).max()
        )
        self.stockPort["LOWEST_21D"] = self.stockPort.groupby("STOCK-NAME")["Low"].transform(
            lambda x: x.rolling(window=7).min()
        )
        self.stockPort["HIGH_21D"] = self.stockPort.groupby("STOCK-NAME")["High"].transform(
            lambda x: x.rolling(window=21).max()
        )

        self.stockPort["STOCH_7"] = (
            (self.stockPort["Close"] - self.stockPort["LOWEST_7D"])
            / (self.stockPort["HIGH_7D"] - self.stockPort["LOWEST_7D"])
        ) * 100
        self.stockPort["STOCH_21"] = (
            (self.stockPort["Close"] - self.stockPort["LOWEST_21D"])
            / (self.stockPort["HIGH_21D"] - self.stockPort["LOWEST_21D"])
        ) * 100

        self.stockPort["STOCH_%D_7"] = self.stockPort["STOCH_7"].rolling(
            window=7).mean()
        self.stockPort["STOCH_%D_21"] = self.stockPort["STOCH_7"].rolling(
            window=21).mean()
        self.stockPort["STOCH_RATIO"] = self.stockPort["STOCH_%D_7"] / \
            self.stockPort["STOCH_%D_21"]

        return self.stockPort

    def createRSI(self) -> pd.DataFrame:
        """ Creating Relative Strength Index in order to quantify up and down movements in price and speed changes
        Lower and Upper values are set between 7 and 21 for medium term strategies, and the ratio the difference."""

        self.stockPort["Diff"] = self.stockPort.groupby("STOCK-NAME")["Close"].transform(
            lambda x: x.diff()
        )
        self.stockPort["UP"] = self.stockPort["Diff"]
        self.stockPort.loc[(self.stockPort["UP"] < 0), "UP"] = 0

        self.stockPort["DOWN"] = self.stockPort["Diff"]
        self.stockPort.loc[(self.stockPort["DOWN"] > 0), "DOWN"] = 0
        self.stockPort["DOWN"] = abs(self.stockPort["DOWN"])

        self.stockPort["avg_7UP"] = self.stockPort.groupby("STOCK-NAME")["UP"].transform(
            lambda x: x.rolling(window=7).mean()
        )
        self.stockPort["avg_7DOWN"] = self.stockPort.groupby("STOCK-NAME")["DOWN"].transform(
            lambda x: x.rolling(window=7).mean()
        )

        self.stockPort["avg_21UP"] = self.stockPort.groupby("STOCK-NAME")["UP"].transform(
            lambda x: x.rolling(window=21).mean()
        )
        self.stockPort["avg_21DOWN"] = self.stockPort.groupby("STOCK-NAME")["DOWN"].transform(
            lambda x: x.rolling(window=21).mean()
        )

        self.stockPort["RS_7"] = self.stockPort["avg_7UP"] / \
            self.stockPort["avg_7DOWN"]
        self.stockPort["RS_21"] = self.stockPort["avg_21UP"] / \
            self.stockPort["avg_21DOWN"]

        self.stockPort["RSI_7"] = 100 - (100 / (1 + self.stockPort["RS_7"]))
        self.stockPort["RSI_21"] = 100 - \
            (100 / (1 + self.stockPort["RS_21"]))
        self.stockPort["RSI_Ratio"] = self.stockPort["RSI_7"] / \
            self.stockPort["RSI_21"]

        return self.stockPort

    def createMACD(self) -> pd.DataFrame:
        """ Creating Moving Average Convergence Divergence technical indicator from raw market data."""

        # Moving Average Convergence Divergence (MACD)
        self.stockPort["7Ewm"] = self.stockPort.groupby("STOCK-NAME")["Close"].transform(  # Exponential weighted moving average - 7 day
            lambda x: x.ewm(span=7, adjust=False).mean()
        )
        self.stockPort["21Ewm"] = self.stockPort.groupby("STOCK-NAME")["Close"].transform(  # exponential weighted moving average 21 day
            lambda x: x.ewm(span=21, adjust=False).mean()
        )
        self.stockPort["MACD"] = self.stockPort["21Ewm"] - \
            self.stockPort["7Ewm"]

        return self.stockPort

    def createRC(self) -> pd.DataFrame:
        """ Creating rate of change technical indicator from raw market data. """

        # Rate of Change indicator
        self.stockPort["RC"] = self.stockPort.groupby("STOCK-NAME")["Close"].transform(
            lambda x: x.pct_change(periods=21))  # 21 day period taken for a medium term strategy

        return self.stockPort

    def splitPreparation(self, scaler) -> pd.DataFrame:
        """ Prepares portfolio holder into the splits required for training and testing of machine learning models."""

        # Target variables
        targetVariables = [
            "Open",  # Daily open
            "Close",  # Daily close
            "SMA_7",  # 7 day SMA
            "SMA_21",  # 21 day SMA
            "SMA_RATIO",  # SMA ratio 21/7 day
            "STOCH_7",  # Stochastic 7 day
            "STOCH_21",  # Stochastic 21 day
            "STOCH_RATIO",  # Stochastic ratio 21/7 day
            "RSI_7",  # RSI 7 day
            "RSI_21",  # RSI 21 day
            "MACD",  # Moving average convergence divergence
            "RC",  # Rate of change
        ]

        for variable in targetVariables:  # Winsorizing indicators within upper 10 and lower 10 percentile range
            self.stockPort.loc[:, variable] = mstats.winsorize(
                self.stockPort.loc[:, variable], limits=[0.1, 0.1])

        # Converting pd.DataFrame index in order to do time series split
        self.stockPort.index = pd.to_datetime(self.stockPort.index)

        # Training set - 60% of data
        dataForTraining = self.stockPort.loc[:"2015-12-31", ]

        # Test set - 40% of data
        dataForTesting = self.stockPort.loc[:"2016-01-01":]

        # Exploratory variables
        exploratoryTraining = dataForTraining.loc[:, targetVariables]
        # Standardise and transform data
        xS = scaler.fit_transform(exploratoryTraining)

        # Response variable / output / label
        responseTraining = dataForTraining.loc[:, ["Adj Close"]]
        # Standardising and transforming the data,
        # and reshaping to add an additional dimension
        yTrain = scaler.fit_transform(responseTraining.values.reshape(-1, 1))
        # Convert to 1-dimensional array
        yS = np.ravel(yTrain)

        # Separate between X and Y
        exploratoryTesting = dataForTesting.loc[:, targetVariables]
        # Standardise and transform data
        xTS = scaler.fit_transform(exploratoryTesting)

        responseTesting = dataForTesting.loc[:, ["Adj Close"]]
        # Standardising and transforming the data,
        # and reshaping to add an additional dimension
        yTest = scaler.fit_transform(responseTesting.values.reshape(-1, 1))
        # Convert to 1-dimensional array
        yTS = np.ravel(yTest)

        return xS, yS, xTS, yTS, targetVariables, exploratoryTraining, exploratoryTesting

    def splitPreparationRF(self, scaler) -> pd.DataFrame:
        """ Prepares portfolio holder into the splits required for training and testing of machine learning models."""
        # Target variables

        targetVariables = [
            "Open",  # Daily open
            "Close",  # Daily close
            "SMA_7",  # 7 day SMA
            "SMA_21",  # 21 day SMA
            "SMA_RATIO",  # SMA ratio 21/7 day
            "STOCH_7",  # Stochastic 7 day
            "STOCH_21",  # Stochastic 21 day
            "STOCH_RATIO",  # Stochastic ratio 21/7 day
            "RSI_7",  # RSI 7 day
            "RSI_21",  # RSI 21 day
            "MACD",  # Moving average convergence divergence
            "RC",  # Rate of change
        ]

        for variable in targetVariables:  # Winsorizing indicators within upper 10 and lower 10 percentile range
            self.stockPort.loc[:, variable] = mstats.winsorize(
                self.stockPort.loc[:, variable], limits=[0.1, 0.1])

        # Converting pd.DataFrame index in order to do time series split
        self.stockPort.index = pd.to_datetime(self.stockPort.index)

        # Test set - 40% of data
        dataForTesting = self.stockPort.loc[:"2016-01-01":]

        # Separate between X and Y
        exploratoryTesting = dataForTesting.loc[:, targetVariables]
        # Standardise and transform data
        xTS = scaler.fit_transform(exploratoryTesting)

        responseTesting = dataForTesting.loc[:, ["Adj Close"]]
        # Standardising and transforming the data,
        # and reshaping to add an additional dimension
        yTest = scaler.fit_transform(responseTesting.values.reshape(-1, 1))
        # Convert to 1-dimensional array
        yTS = np.ravel(yTest)

        return xTS, yTS


class Director:

    def __init__(self, listOfSymbols, scaler, startPeriod, endPeriod, col) -> pd.DataFrame:
        self._builder = ConcreteProcessor(col)
        self._listOfSymbols = listOfSymbols
        self._scaler = scaler
        self._startPeriod = startPeriod
        self._endPeriod = endPeriod
        self._col = col

    def processingHandler(self) -> pd.DataFrame:
        """ Helper function to action the processing process from start to finish."""

        # Calling methods to create technical indicators
        self._builder.downloadData(self._listOfSymbols,
                                   self._startPeriod, self._endPeriod)

        print("-----------------------------------Feature Engineering-----------------------------------------")
        print("Creating SMA...")
        self._builder.createSMA()
        print("Creating STOCH...")
        self._builder.createStochastic()
        print("Creating RSI...")
        self._builder.createRSI()
        print("Creating MACD...")
        self._builder.createMACD()
        print("Creating RC...")
        self._builder.createRC()
        # Creating training and testing splits
        print("Creating Training/Testing Splits...")
        xS, yS, xTS, yTS, targetVARS, exploratoryTraining, exploratoryTesting = self._builder.splitPreparation(
            self._scaler)
        print(self._col.boldFont + self._col.purpleFont +
              "[ALERT] " + self._col.endFont + "Feature Engineering completed.")
        print(self._col.boldFont + self._col.italicFont +
              "Progressing to Particle optimisation..." + self._col.endFont)

        return xS, yS, xTS, yTS, targetVARS, exploratoryTraining, exploratoryTesting

    def processingHandlerRF(self) -> pd.DataFrame:
        """ Helper function to action the processing process for the random forests from start to finish."""

        # Calling methods to create technical indicators
        self._builder.downloadData(self._listOfSymbols,
                                   self._startPeriod, self._endPeriod)

        print("-----------------------------------Feature Engineering-----------------------------------------")
        print("Creating SMA...")
        self._builder.createSMA()
        print("Creating STOCH...")
        self._builder.createStochastic()
        print("Creating RSI...")
        self._builder.createRSI()
        print("Creating MACD...")
        self._builder.createMACD()
        print("Creating RC...")
        self._builder.createRC()
        # Creating training and testing splits
        print("Creating Training/Testing Splits...")
        xS, yS = self._builder.splitPreparationRF(self._scaler)
        print(self._col.boldFont + self._col.purpleFont +
              "[ALERT] " + self._col.endFont + "Feature Engineering completed.")
        print(self._col.boldFont + self._col.italicFont +
              "Progressing to results..." + self._col.endFont)

        return xS, yS
