from PySide6.QtCore import (
    Qt,
    QObject,
    Signal,
    QPointF,
    QDateTime,
    QDate,
    QTime,
    QThread,
    QSize,
)
import plotly.graph_objects as go
from PySide6.QtWebEngineWidgets import QWebEngineView
from contextlib import suppress
import finplot as fplt
import pyqtgraph as pg
from PySide6.QtGui import QPainter, QPixmap, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QWidget,
    QMainWindow,
    QLineEdit,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
    QListWidget,
    QDialog,
    QDialogButtonBox,
    QListWidgetItem,
    QStyle,
    QStyleOption,
    QInputDialog,
    QGridLayout,
    QScrollArea,
    QComboBox,
    QAbstractItemView,
    QDateTimeEdit,
    QAbstractSpinBox,
)
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QLineSeries,
    QAbstractAxis,
    QValueAxis,
    QDateTimeAxis,
    QCandlestickSeries,
    QCandlestickSet,
)
import sqlite3
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import yfinance as yf
import pandas as pd
import datetime
from string import punctuation
import pickle
from functools import partial
import time
from threading import Thread
from dateutil.relativedelta import relativedelta
import numpy


# def paintEvent is required to style widgets that inherit QWidget


class Error(QDialog):  # Error Dialog for Invalid Inputs
    def __init__(self, msg):
        super().__init__()
        self.msg = QLabel(msg)
        self.Button = QDialogButtonBox(QDialogButtonBox.Ok)
        self.Button.accepted.connect(self.accept)
        self.setWindowTitle("Error")
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.msg)
        self.layout.addWidget(self.Button)
        self.setLayout(self.layout)


class Loading(QDialog):
    def __init__(self) -> None:
        super().__init__()
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.loadingLabel = QLabel("Please Wait")
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.loadingLabel)
        self.setLayout(self.layout)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(
            QStyle.PE_Widget, o, p, self
        )  ##This function is required to enable stylesheet support For QWidget subclasses


class SuccessDialog(QDialog):  # Success Dialog for Successful Database Creation
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Database Created")
        self.message = QLabel("Session Successfully Created")
        self.Button = QDialogButtonBox(QDialogButtonBox.Ok)
        self.Button.accepted.connect(self.accept)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.Button)
        self.setLayout(self.layout)


class ImportDialog(QDialog):  # Dialog used to input data for data import
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Import Stock Data")
        self.StockName = QLineEdit()
        self.StockName.setPlaceholderText(
            "Enter Yahoo Ticker Symbol to Import Stock Data"
        )
        self.Button = QDialogButtonBox(QDialogButtonBox.Ok)
        self.Button.accepted.connect(self.accept)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.StockName)
        self.layout.addWidget(self.Button)
        self.setLayout(self.layout)


class PortfolioImportDialog(ImportDialog):  # Similar to Import Dialog
    def __init__(self) -> None:
        super().__init__()
        self.BuyPrice = QLineEdit()
        self.BuyPrice.setPlaceholderText("Enter Buy Price")
        self.BuyDate = ReadOnlyDateTime(QDate.currentDate())
        self.BuyDate.setCalendarPopup(True)
        self.BuyDate.setMaximumDate(QDate.currentDate())
        self.Quantity = QLineEdit()
        self.Quantity.setPlaceholderText("Enter Quantity Purchased")
        self.layout.insertWidget(1, self.BuyDate)
        self.layout.insertWidget(1, self.Quantity)
        self.layout.insertWidget(1, self.BuyPrice)


class EntryScreen(QWidget):  # Welcome Screen For User
    def __init__(self):
        super().__init__()

        self.newUserButton = QPushButton("New User")
        self.existingUserButton = QPushButton("Existing User")
        self.layout = QHBoxLayout()
        self.layout.addStretch(2)
        self.layout.addWidget(self.newUserButton, 1)
        self.layout.addStretch(0)
        self.layout.addWidget(self.existingUserButton, 1)
        self.layout.addStretch(2)
        self.setLayout(self.layout)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)


class ButtonGroup(QWidget):  # Used in the UserInputForm and ExistingUsers Class
    def __init__(self):
        super().__init__()
        self.BackButton = QPushButton("Back")
        self.ProceedButton = QPushButton("Proceed")
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.BackButton)
        self.layout.addWidget(self.ProceedButton)
        self.setLayout(self.layout)


class UserInputForm(QWidget):  # User can create a New session Here
    def __init__(self):
        super().__init__()

        self.userInputLabel = QLabel("Enter New Session Name")
        self.userInputLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.buttons = ButtonGroup()
        self.userInputField = QLineEdit()
        self.userInputField.setPlaceholderText("Enter a new Session Name")
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addStretch(2)
        self.layout.addWidget(self.userInputLabel, 0)
        self.layout.addStretch(0)
        self.layout.addWidget(self.userInputField, 1)
        self.layout.addStretch(0)
        self.layout.addWidget(self.buttons, 0)
        self.userInputField.setMaximumWidth(400)
        self.layout.addStretch(2)
        self.setLayout(self.layout)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)


class ExistingUsers(QWidget):  # User can log into an existing Session from here
    def __init__(self):
        super().__init__()

        self.ExistingLabel = QLabel("Existing Sessions")
        self.ExistingLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.List = QListWidget()
        for file in os.listdir(
            "financialModeller\\SessionData"
        ):  # Appends Folders made in SessionData, which resembles the various sessions existing to the list Widget
            self.List.addItem(f"{file}")
        self.layout = QVBoxLayout()
        self.buttons = ButtonGroup()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addStretch(2)
        self.layout.addWidget(self.ExistingLabel)
        self.layout.addStretch(0)
        self.layout.addWidget(self.List)
        self.layout.addStretch(0)
        self.layout.addWidget(self.buttons)
        self.layout.addStretch(2)
        self.List.setMaximumWidth(400)
        self.setLayout(self.layout)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)


class TickerSignal(
    QObject
):  # Signal used to connect Custom Tickers made by the program (to make those widgets clickable)
    signal = Signal()


class Ticker(QWidget):  # Contains imported stock data
    def __init__(
        self,
        tickerSymbol,
        tickerPrice,
        stockData,
        uneditedTickerSymbol,  # Made a mess of tickerSymbol and uneditedTickerSymbol and forgot the distinction between the two, so any reference to these have replace methods appended to them
    ) -> None:
        super().__init__()
        self.setMaximumWidth(100)
        self.stockData = stockData
        self.uneditedTicker = uneditedTickerSymbol
        self.setObjectName("Ticker")
        self.clicked = TickerSignal()
        self.tickerSymbol = QLabel(tickerSymbol)
        self.tickerSymbol.setObjectName("tickerSymbol")
        self.tickerPrice = QLabel(tickerPrice)
        self.tickerPrice.setObjectName("tickerPrice")
        self.deleteButton = QPushButton()
        self.deleteButton.setObjectName("DeleteButton")
        trashIcon = QPixmap("financialModeller\\resources\\trash.png")
        self.deleteButton.setIcon(QIcon(trashIcon))
        self.deleteButton.setMaximumWidth(23)
        self.receivedFrom = self.sender()  # This is how it receives the click event
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tickerSymbol)
        self.layout.addWidget(self.tickerPrice)
        self.layout.addWidget(self.deleteButton)
        self.setLayout(self.layout)

    def updatePrice(self, price):  # Updates Price of the ticker
        self.tickerPrice.setText(str(price))

    def updateData(
        self, data
    ):  # Updates the info about the stock associated with the ticker
        self.stockData = data

    def mousePressEvent(
        self, event
    ):  # MousePress and Release Events ensure the click is made within the ticker and not released outside of it
        if event.button() == Qt.LeftButton:
            self.pressPos = event.position().toTuple()

    def mouseReleaseEvent(self, event):
        if (
            self.pressPos is not None
            and event.button() == Qt.LeftButton
            and event.position().toTuple()[0] <= self.rect().getRect()[2]
            and event.position().toTuple()[1] <= self.rect().getRect()[3]
        ):
            self.clicked.signal.emit()
        self.pressPos = None

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(
            QStyle.PE_Widget, o, p, self
        )  ##This function is required to enable stylesheet support For QWidget subclasses


class PortfolioTicker(
    Ticker
):  # Similar to Ticker, but also consists of profit calculation on latest available data
    def __init__(
        self,
        tickerSymbol,
        tickerPrice,
        stockData,
        priceHistory,
        buyPrice,
        uneditedTickerSymbol,
        holding,
    ):
        super().__init__(
            tickerSymbol,
            tickerPrice,
            stockData,
            uneditedTickerSymbol,
        )
        gainOrLossPercent = round(
            (
                (priceHistory["Close"].iloc[len(priceHistory) - 1] - float(buyPrice))
                / float(buyPrice)
            )
            * 100,
            3,
        )
        gainOrLoss = round(
            (
                (priceHistory["Close"].iloc[len(priceHistory) - 1] - float(buyPrice))
                * 100
            ),
            3,
        )
        self.held = QLabel(f"Held: {holding}")
        self.gainLossPercent = QLabel(f"{gainOrLossPercent}%")
        if float(gainOrLoss) < 0:
            self.gainLoss = QLabel(f"Loss:{gainOrLoss}")
        else:
            self.gainLoss = QLabel(f"Gain:{gainOrLoss}")
        self.layout.removeWidget(self.deleteButton)
        self.layout.insertWidget(2, self.gainLoss)
        self.layout.insertWidget(2, self.gainLossPercent)
        self.layout.insertWidget(2, self.held)

    def updateHolding(self, holding):  # Updates number of shares held
        self.held.setText(f"Held: {str(holding)}")

    def updatePrice(self, price):  # Updates Price of the ticker
        self.tickerPrice.setText(str(round(price, 2)))

    def updateGainLoss(self, priceHistory, buyPrice):  # Updates the Gain/Loss Figures
        gainOrLossPercent = round(
            (
                (priceHistory["Close"].iloc[len(priceHistory) - 1] - float(buyPrice))
                / float(buyPrice)
            )
            * 100,
            3,
        )
        gainOrLoss = round(
            (
                (priceHistory["Close"].iloc[len(priceHistory) - 1] - float(buyPrice))
                * 100
            ),
            3,
        )
        self.gainLossPercent.setText(f"{gainOrLossPercent}%")
        if float(gainOrLoss) < 0:
            self.gainLoss.setText(f"Loss:{gainOrLoss}")
        else:
            self.gainLoss.setText(f"Gain:{gainOrLoss}")

    def deleteTicker(
        self, conn, cur
    ):  # Deletes the ticker, if shares in that ticker == 0
        self.setParent(None)
        cur.execute(
            "DELETE FROM PORTFOLIODATA WHERE stock = ?", (self.tickerSymbol.text(),)
        )
        conn.commit()


class StockList(QWidget):  # container for the individual tickers
    def __init__(self) -> None:
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.addStretch()
        self.setLayout(self.layout)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(
            QStyle.PE_Widget, o, p, self
        )  ##This function is required to enable stylesheet support For QWidget subclasses


class TickerList(
    QWidget
):  # container for the stockList, a search bar and a button to import new stocks
    def __init__(self) -> None:
        super().__init__()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search for a stock")
        self.NoStocks = QPushButton("Please import Stocks")
        self.NoStocks.setFlat(True)
        self.NoStocks.setObjectName("NoStocks")
        self.stockList = StockList()
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.stockList)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.search, 0)
        self.layout.addWidget(self.NoStocks, 0)
        self.layout.addWidget(self.scrollArea, 5)
        self.setLayout(self.layout)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)


class SearchBarWidget(QWidget):  # facilitates filter operations for the tickers
    def __init__(self) -> None:
        super().__init__()
        self.tickerList = TickerList()
        self.popUpButton = QPushButton()
        self.popUpButton.setObjectName("popUpButton")
        menuIcon = QPixmap("financialModeller\\resources\\white-menu-icon.png")
        self.popUpButton.setIcon(QIcon(menuIcon))
        self.popUpButton.setIconSize(QSize(30, 30))
        self.popUpButton.setMinimumHeight(30)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tickerList, 2)
        self.layout.addWidget(self.popUpButton, 1)
        self.setLayout(self.layout)
        self.tickerList.search.textChanged.connect(self.SearchBarFilter)

    def SearchBarFilter(self):  # the function controlling the filter
        self.filter = self.tickerList.search.text()
        CurrentStocks1 = self.tickerList.stockList.children()[1:]
        # print(CurrentStocks1)
        if len(CurrentStocks1) == 0:
            return
        CurrentStocks = [
            (i.tickerSymbol.text(), i) for i in CurrentStocks1
        ]  # Makes a list of lists containing the tickerName associated with the widget and the widget
        for i in CurrentStocks:
            if self.filter.upper() in i[0].upper():
                # print(self.filter, i)
                i[1].show()
            else:
                i[1].hide()


class StackSwitcher(
    QWidget
):  # container for buttons that enable you to switch the infoModule stack
    def __init__(self) -> None:
        super().__init__()
        self.button1 = QPushButton("1")
        self.button2 = QPushButton("2")
        self.button3 = QPushButton("3")
        self.button4 = QPushButton("4")
        self.button5 = QPushButton("5")
        self.button6 = QPushButton("6")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    # def AddButtons(self):
    #    self.layout.addWidget(self.button1)
    #    self.layout.addWidget(self.button2)
    #    self.layout.addWidget(self.button3)
    #    self.layout.addWidget(self.button4)

    def AddButtons(self):  # Adds buttons to the layout
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.layout.addWidget(self.button4)
        self.layout.addWidget(self.button5)

    def deleteButtons(self):  # deletes the added buttons
        count = self.layout.count() - 1
        while count >= 0:
            removeWidget = self.layout.itemAt(count).widget()
            removeWidget.setParent(None)
            count -= 1

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)


class MainMainInfoModule(
    QWidget
):  # container for the stackswitcher buttons and the infoModule
    def __init__(self) -> None:
        super().__init__()
        self.MainInfoModule = MainInfoModule()
        self.stackSwitcher = StackSwitcher()
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.MainInfoModule, 16)
        self.layout.addWidget(self.stackSwitcher, 1)
        self.setLayout(self.layout)


class MainInfoModule(QStackedWidget):  # stack container for the various infoModules
    def __init__(self) -> None:
        super().__init__()
        self.infoModule1 = InfoModule()
        self.infoModule2 = InfoModule()
        self.infoModule2.setObjectName("InfoModule2")
        self.infoModule3 = InfoModule()
        self.infoModule4 = InfoModule()
        self.infoModule5 = InfoModule()
        self.infoModule6 = InfoModule()
        self.infoModule4.setObjectName("InfoModule4")
        self.infoModule5.setObjectName("InfoModule5")
        self.infoModule6.setObjectName("InfoModule6")
        self.addWidget(self.infoModule1)
        self.addWidget(self.infoModule2)
        self.addWidget(self.infoModule3)
        self.addWidget(self.infoModule4)
        self.addWidget(self.infoModule5)
        self.addWidget(self.infoModule6)
        self.setCurrentWidget(self.infoModule1)

    def deleteInfo(self):  # Deletes Info persisting in infoModules
        oldInfo1 = self.infoModule1.layout.count() - 1
        if oldInfo1:
            while oldInfo1 >= 0:
                removeInfo = self.infoModule1.layout.itemAt(oldInfo1).widget()
                removeInfo.setParent(None)
                oldInfo1 -= 1
        oldInfo2 = self.infoModule2.layout.count() - 1
        if oldInfo2:
            while oldInfo2 >= 0:
                removeInfo = self.infoModule2.layout.itemAt(oldInfo2).widget()
                removeInfo.setParent(None)
                oldInfo2 -= 1
        oldInfo3 = self.infoModule3.layout.count() - 1
        if oldInfo3:
            while oldInfo3 >= 0:
                removeInfo = self.infoModule3.layout.itemAt(oldInfo3).widget()
                removeInfo.setParent(None)
                oldInfo3 -= 1
        oldInfo4 = self.infoModule4.layout.count() - 1
        if oldInfo4:
            while oldInfo4 >= 0:
                removeInfo = self.infoModule4.layout.itemAt(oldInfo4).widget()
                removeInfo.setParent(None)
                oldInfo4 -= 1
        oldInfo5 = self.infoModule5.layout.count() - 1
        if oldInfo5:
            while oldInfo5 >= 0:
                removeInfo = self.infoModule5.layout.itemAt(oldInfo5).widget()
                removeInfo.setParent(None)
                oldInfo5 -= 1
        oldInfo6 = self.infoModule6.layout.count() - 1
        if oldInfo6:
            while oldInfo6 >= 0:
                removeInfo = self.infoModule6.layout.itemAt(oldInfo6).widget()
                removeInfo.setParent(None)
                oldInfo6 -= 1


class InfoModule(QWidget):  # Used to display data about the ticker
    def __init__(self) -> None:
        super().__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)


class timeFrameButtons(
    QWidget
):  # Buttons to dynamically adjust the chartModule according to timeframes
    def __init__(self) -> None:
        super().__init__()
        self.oneDay = QPushButton("1D")
        self.oneWeek = QPushButton("1W")
        self.oneMonth = QPushButton("1M")
        self.threeMonth = QPushButton("3M")
        self.sixMonth = QPushButton("6M")
        self.oneYear = QPushButton("1Y")
        self.threeYear = QPushButton("3Y")
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

    # def constructChartTypeLayout(self):
    #    self.layout.addWidget(self.lineChart)
    #    self.layout.addWidget(self.pieChart)

    def constructLayout(
        self, inceptionDate
    ):  # adds the buttons according to the available timeframes for the chart
        children = self.layout.count() - 1
        if children:
            while children >= 0:
                removeWidget = self.layout.itemAt(children).widget()
                removeWidget.setParent(None)
                children -= 1
        inceptionDate = datetime.datetime.fromtimestamp(inceptionDate)
        if inceptionDate > datetime.datetime.now() - relativedelta(weeks=1):
            self.layout.addWidget(self.oneDay)
            return
        elif inceptionDate > datetime.datetime.now() - relativedelta(months=1):
            self.layout.addWidget(self.oneDay)
            self.layout.addWidget(self.oneWeek)
            return
        elif inceptionDate > datetime.datetime.now() - relativedelta(months=3):
            self.layout.addWidget(self.oneDay)
            self.layout.addWidget(self.oneWeek)
            self.layout.addWidget(self.oneMonth)
            return
        elif inceptionDate > datetime.datetime.now() - relativedelta(months=6):
            self.layout.addWidget(self.oneDay)
            self.layout.addWidget(self.oneWeek)
            self.layout.addWidget(self.oneMonth)
            self.layout.addWidget(self.threeMonth)
            return
        elif inceptionDate > datetime.datetime.now() - relativedelta(years=1):
            self.layout.addWidget(self.oneDay)
            self.layout.addWidget(self.oneWeek)
            self.layout.addWidget(self.oneMonth)
            self.layout.addWidget(self.threeMonth)
            self.layout.addWidget(self.sixMonth)
            return
        elif inceptionDate > datetime.datetime.now() - relativedelta(years=3):
            self.layout.addWidget(self.oneDay)
            self.layout.addWidget(self.oneWeek)
            self.layout.addWidget(self.oneMonth)
            self.layout.addWidget(self.threeMonth)
            self.layout.addWidget(self.sixMonth)
            self.layout.addWidget(self.oneYear)
            return
        else:
            self.layout.addWidget(self.oneDay)
            self.layout.addWidget(self.oneWeek)
            self.layout.addWidget(self.oneMonth)
            self.layout.addWidget(self.threeMonth)
            self.layout.addWidget(self.sixMonth)
            self.layout.addWidget(self.oneYear)
            self.layout.addWidget(self.threeYear)
            return

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)


class ChartModule(QWidget):  # Consists of the chart to graph price data in candlesticks
    def __init__(self) -> None:
        super().__init__()
        self.web_view = None
        self.stockData = None
        self.w = fplt.foreground = "#eef"
        b = fplt.background = fplt.odd_plot_background = "#242320"
        fplt.candle_bull_color = fplt.volume_bull_color = (
            fplt.candle_bull_body_color
        ) = fplt.volume_bull_body_color = "#57BA46"
        fplt.candle_bear_color = fplt.volume_bear_color = "#810"
        fplt.cross_hair_color = self.w + "a"
        self.plot = fplt.create_plot_widget(self.window())
        self.volumeOverlay = self.plot.overlay()
        self.window().axs = [self.plot]
        self.timeFrameButtons = timeFrameButtons()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.plot.ax_widget)
        self.layout.addWidget(self.timeFrameButtons)
        self.setLayout(self.layout)
        fplt.FinCrossHair(self.plot, color=self.w + "a")
        fplt.add_crosshair_info(self.update_crosshair, ax=self.plot)
        self.hide()

    def update_crosshair(
        self, x, y, xtext, ytext
    ):  # provides information about the plot
        volume = self.stockData.iloc[x].Volume
        ytext = "%s (Close%+.2f, Volume: %d)" % (
            ytext,
            (y - self.stockData.iloc[x].Close),
            volume,
        )
        return xtext, ytext

    def makePortfolioChart(
        self, stockData: pd.DataFrame, tickerName: str
    ):  # Not used Function,similar to updateStockData
        if self.web_view:
            self.web_view.hide()
            self.show()
        fplt._ax_reset(self.plot)
        fplt._ax_reset(self.volumeOverlay)
        self.plot.setTitle(tickerName)
        fplt.plot(
            stockData["Date"], stockData["Value"], ax=self.plot, legend=tickerName
        )
        fplt.plot(
            stockData["Date"],
            stockData["Value"].rolling(25).mean(),
            legend="ma-25",
            ax=self.plot,
        )
        self.volumeOverlay = self.plot.overlay()
        fplt.volume_ocv(
            self.stockData[["Date", "Open", "Close", "Volume"]], ax=self.volumeOverlay
        )
        fplt.show(qt_exec=False)

    def updateStockData(
        self, stockData, tickerName: str
    ):  # redraws the existing chart according to the price data given
        self.show()
        self.stockData = stockData
        # print(self.stockData)
        fplt._ax_reset(self.plot)
        fplt._ax_reset(self.volumeOverlay)
        self.plot.setTitle(tickerName)
        fplt.candlestick_ochl(
            self.stockData[["Date", "Open", "High", "Low", "Close"]], ax=self.plot
        )
        fplt.plot(
            self.stockData["Date"],
            self.stockData["Close"].rolling(25).mean(),
            legend="ma-25",
            ax=self.plot,
        )
        self.volumeOverlay = self.plot.overlay()
        fplt.volume_ocv(
            self.stockData[["Date", "Open", "Close", "Volume"]], ax=self.volumeOverlay
        )
        fplt.show(qt_exec=False)

    def DeleteChart(self):  # delets the current shown chart
        self.plot.setTitle(None)
        fplt._ax_reset(self.plot)
        fplt._ax_reset(self.volumeOverlay)


class ChartAndInfoModule(
    QWidget
):  # Wrapper that contains both the chart and MainInfoModule
    def __init__(self) -> None:
        super().__init__()
        self.chart = ChartModule()
        self.info = MainMainInfoModule()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.chart, 2)
        self.layout.addWidget(self.info, 1)
        self.setLayout(self.layout)


class PopUpMenu(QWidget):  # Pop up Sidebar
    def __init__(self) -> None:
        super().__init__()
        self.showCount = False
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.Screener = QPushButton(text="Stock Screener")
        self.Portfolio = QPushButton(text="Portfolio")
        self.Screener.setMinimumHeight(100)
        self.Portfolio.setMinimumHeight(100)
        self.layout.addWidget(self.Screener, 1)
        self.layout.addWidget(self.Portfolio, 1)
        self.layout.addStretch()

    def updateState(
        self, bool: bool
    ):  # facilitates in handling the hide and show functionality of the sidebar
        self.showCount = bool

    def hideOrShow(self):  # handling the hide and show functionality of the sidebar
        if self.showCount:
            self.hide()
            self.updateState(False)
        else:
            self.show()
            self.updateState(True)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)


class FinancialModule(
    QWidget
):  # Wrapper that contains the tickerlist and the chart and info module, the whole system
    def __init__(self):
        super().__init__()
        self.popUpMenu = PopUpMenu()
        self.SearchModule = SearchBarWidget()
        self.ChartInfoModule = ChartAndInfoModule()
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.popUpMenu)
        self.popUpMenu.hide()
        self.layout.addWidget(self.SearchModule, 1)
        self.layout.addWidget(self.ChartInfoModule, 10)
        self.setLayout(self.layout)


class PortfolioSearchBarWidget(
    SearchBarWidget
):  # Search Bar widget for the portfolio Section
    def __init__(self) -> None:
        super().__init__()
        self.tickerList.NoStocks.setText("Add Stock to Portfolio")
        self.tickerList.NoStocks.clicked.connect(self.ImportStocks)
        self.portfolioOverview = QPushButton()
        self.portfolioOverview.setObjectName("portfolioOverview")
        pieChartIcon = QPixmap(
            "financialModeller\\resources\\pie-chart-2-svgrepo-com.svg"
        )
        self.portfolioOverview.setIcon(QIcon(pieChartIcon))
        self.layout.addWidget(self.portfolioOverview)

    def ImportStocks(self):  # opens a dialog to import stocks
        self.dialog = PortfolioImportDialog()
        self.dialog.exec()


class ReadOnlyDateTime(QDateTimeEdit):  # Redundant func
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, event):
        event.ignore()


class BuySellModule(QWidget):  # Widget that handles the buying/selling of a held stock
    def __init__(self):
        super().__init__()
        self.currentClickedWidget = None
        self.buyOrSell = True
        self.MainLabel = QLabel("Buy/Sell")
        self.stockNameLabel = QLabel("")
        self.averagePriceLabel = QLabel("")
        self.existingShares = QLabel("")
        self.buyOrSellTransac = QComboBox()
        self.buyOrSellTransac.addItems(["Buy", "Sell"])
        self.buyOrSellTransac.setCurrentText("Buy")
        self.buyOrSellTransac.setMaximumWidth(60)
        self.priceLabel = QLabel("Buy Price")
        self.PriceEntry = QLineEdit()
        self.PriceEntry.setMaximumWidth(130)
        self.QuantityLabel = QLabel("Quantity")
        self.QuantityEntry = QLineEdit()
        self.QuantityEntry.setMaximumWidth(130)
        self.dateLabel = QLabel("Date")
        self.DateEntry = ReadOnlyDateTime(QDate.currentDate())
        self.DateEntry.setMaximumDate(QDate.currentDate())
        self.DateEntry.setDisplayFormat("dd/MM/yyyy")
        self.DateEntry.setCalendarPopup(True)
        self.DateEntry.setMaximumWidth(130)
        self.confirmTrade = QPushButton(text="Confirm Trade")
        self.buyOrSellTransac.currentTextChanged.connect(self.text_Changed)
        # self.buyOrSellTransac.setDisabled(True)
        # self.PriceEntry.setDisabled(True)
        # self.QuantityEntry.setDisabled(True)
        # self.confirmTrade.setDisabled(True)
        self.confirmTrade.setObjectName("confirmTradeButton")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.MainLabel, 1, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.stockNameLabel, 2, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.existingShares, 2, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.averagePriceLabel, 2, Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.buyOrSellTransac, 1)
        self.layout.addWidget(self.priceLabel, 2)
        self.layout.addWidget(self.PriceEntry, 1)
        self.layout.addWidget(self.QuantityLabel, 2)
        self.layout.addWidget(self.QuantityEntry, 1)
        self.layout.addWidget(self.dateLabel, 2)
        self.layout.addWidget(self.DateEntry, 1)
        self.layout.addStretch(3)
        self.layout.addWidget(self.confirmTrade, 2, Qt.AlignmentFlag.AlignCenter)
        self.layout.addStretch(5)

    # def EnableLayout(self):
    #    self.buyOrSellTransac.setEnabled(True)
    #    self.PriceEntry.setEnabled(True)
    #    self.QuantityEntry.setEnabled(True)
    #    self.confirmTrade.setEnabled(True)

    def text_Changed(self):  # changes text depending on whether if its a buy/sell
        if self.buyOrSell:
            self.priceLabel.setText("Sell Price")
            self.buyOrSell = False
        else:
            self.priceLabel.setText("Buy Price")
            self.buyOrSell = True

    def updateStockName(
        self, name, widget
    ):  # updates stockName depending on which ticker is clicked
        self.currentClickedWidget = widget
        self.stockNameLabel.setText(name)

    def updateExistingShares(
        self, quantity, averagePrice
    ):  # updates existing shares held in the ticker that is clicked
        self.existingShares.setText(f"Shares held: {quantity}")
        self.averagePriceLabel.setText(f"Average Price: {averagePrice}")

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)


class TransactionList(QWidget):  # Contains the individual transaction classes
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.addStretch()
        self.setLayout(self.layout)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)


class Transaction(QWidget):  # Represents a transaction entry
    def __init__(
        self,
        stockName,
        Transactiontype,
        price,
        quantity,
        profitOrLoss,
        profitOrLossPercent,
    ):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setMaximumHeight(50)
        self.setLayout(self.layout)
        self.stockName = QLabel(stockName)
        self.stockName.setMinimumWidth(60)
        self.transactionType = QLabel(Transactiontype)
        self.price = QLabel(
            f"""Price
{price}"""
        )
        self.quantity = QLabel(
            f"""Quantity
{quantity}"""
        )
        self.layout.addWidget(self.stockName, 1)
        self.layout.addWidget(self.transactionType, 1)
        self.layout.addWidget(self.price, 1)
        self.layout.addWidget(self.quantity, 1)
        if not pd.isna(profitOrLoss):
            self.profitOrLossAndPercent = QLabel(
                f"""Profit/Loss
{str(profitOrLossPercent)}% ({str(profitOrLoss)})"""
            )
            self.layout.addWidget(self.profitOrLossAndPercent, 1)
        else:
            self.layout.addStretch(4)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)


class TransactionModule(QWidget):  # Parent container for the transaction List
    def __init__(self):
        super().__init__()
        self.label = QLabel("Transaction History")
        self.transactionList = TransactionList()
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidget(self.transactionList)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.scrollArea, 6)
        self.setLayout(self.layout)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)


class portfolioPerformance(
    QWidget
):  # Similar to a infoModule, representing gain made by the portfolio, still in work
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.profitLossToday = QLabel("")
        self.averageProfitLossOnTrades = QLabel("")
        self.layout.addWidget(self.profitLossToday, 0, 0, 1, 1)
        self.layout.addWidget(self.averageProfitLossOnTrades, 0, 1, 1, 1)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

    def updatePortfolioPerformance(
        self, portfolioDf, transactionDf, conn
    ):  # updates the performance figures in the widget
        i = 0
        profitLossToday = 0
        while i < len(portfolioDf):
            row = portfolioDf.loc[i]
            dfStock = pd.read_sql(
                f"SELECT * FROM {row['stock'].replace('-','').replace('.','')}", conn
            )
            dfLastRow = dfStock.tail(1)
            dfLastRow.reset_index(inplace=True, drop=True)
            startPrice = row["DCAPrice"]
            dfLatestPrice = dfLastRow["Close"].loc[0]
            profitLossToday += (dfLatestPrice - startPrice) * row["QuantityLeft"]
            i += 1
        transactionDfNotNull = transactionDf[
            transactionDf["ProfitOrLossPercent"].notnull()
        ]
        transactionDfNotNull.reset_index(inplace=True, drop=True)
        i = 0
        averageProfitLossOnTrades = "NA"
        if not transactionDfNotNull.empty:
            averageProfitLossOnTrades = 0
            while i < len(transactionDfNotNull):
                row = transactionDfNotNull.loc[i]
                averageProfitLossOnTrades += row["ProfitOrLossPercent"]
                i += 1
            averageProfitLossOnTrades = averageProfitLossOnTrades / i
            averageProfitLossOnTrades = round(averageProfitLossOnTrades, 3)

        self.profitLossToday.setText(f"Profit/Loss Today: {round(profitLossToday,3)}")
        self.averageProfitLossOnTrades.setText(
            f"Average Profit/Loss on Trades: {averageProfitLossOnTrades}%"
        )

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)


class portfolioOverview(QWidget):  # makes the pie chart, representing portfolio breakup
    def __init__(self):
        super().__init__()
        self.web_view = None
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.portfolioPerformanceWidget = portfolioPerformance()
        self.portfolioPerformanceWidget.setMinimumHeight(300)
        self.layout.addWidget(self.portfolioPerformanceWidget)

    def makePieChart(self, data):  # makes/updates the pie chart
        i = 0
        labels = []
        quantity = []
        while i < len(data):
            row = data.loc[i]
            labels.append(row["stock"])
            quantity.append(float(row["QuantityLeft"]))
            i += 1
        fig = go.Figure(
            data=[go.Pie(labels=labels, values=quantity)],
        )
        fig.update_layout(
            title_text="Portfolio Distribution",
            paper_bgcolor="#2a282d",
            plot_bgcolor="#2a282d",
            font=dict(color="#ffffff"),
        )
        html = fig.to_html(include_plotlyjs="cdn", full_html=False)
        if self.web_view:
            self.web_view.setParent(None)
        self.web_view = QWebEngineView()
        self.web_view.setHtml(html)
        self.layout.insertWidget(0, self.web_view)


# make an expanding buysell Module that expands after clicking on the stock, originally only transaction list will be shown,and then after clicking it will contract and show the buysell Module
class PortfolioModule(
    QWidget
):  # Parent Container for all the portfolio systems, similar to the FinancialModule
    def __init__(self) -> None:
        super().__init__()
        self.popUpMenuPortfolio = PopUpMenu()
        self.popUpMenuPortfolio.hide()
        self.stocksInPortfolioList = PortfolioSearchBarWidget()
        self.chartModule = ChartModule()
        self.buySellModule = BuySellModule()
        self.buySellModule.setMinimumWidth(300)
        self.transactionModule = TransactionModule()
        self.transactionModule.setMinimumWidth(300)
        self.infoModule = MainMainInfoModule()
        self.portfolioOverview = portfolioOverview()
        self.layout = QGridLayout()
        self.layout.addWidget(
            self.stocksInPortfolioList, 0, 1, 5, 1, Qt.AlignmentFlag.AlignLeft
        )
        self.layout.addWidget(
            self.popUpMenuPortfolio, 0, 0, 5, 1, Qt.AlignmentFlag.AlignLeft
        )
        self.layout.addWidget(
            self.transactionModule, 0, 2, 5, 1, Qt.AlignmentFlag.AlignLeft
        )
        self.layout.addWidget(self.portfolioOverview, 0, 3, 5, 1)
        self.layout.setColumnStretch(1, 0)
        self.layout.setColumnStretch(2, 1)
        self.layout.setColumnStretch(3, 8)

        # We can add upto column number 9 or span a widget upto 8/9 columns for desired layout
        # tests ->
        # self.layout.addWidget(QWidget(), 0, 2, 3, 1, Qt.AlignmentFlag.AlignLeft)
        # self.layout.addWidget(QWidget(), 0, 3, 3, 1, Qt.AlignmentFlag.AlignLeft)
        # self.layout.addWidget(QWidget(), 0, 4, 3, 1, Qt.AlignmentFlag.AlignLeft)
        # self.layout.addWidget(QWidget(), 0, 5, 3, 1, Qt.AlignmentFlag.AlignLeft)
        # self.layout.addWidget(QWidget(), 0, 6, 3, 1, Qt.AlignmentFlag.AlignLeft)
        # self.layout.addWidget(QWidget(), 0, 7, 3, 1, Qt.AlignmentFlag.AlignLeft)
        # self.layout.addWidget(QWidget(), 0, 8, 3, 1, Qt.AlignmentFlag.AlignLeft)
        # self.layout.addWidget(QWidget(), 0, 9, 3, 1, Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.layout)


class MainWindow(QMainWindow):  # Main Application
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1800, 700)
        self.activeChart = (
            None  # Used to keep track of the current chart active on the MainModule
        )
        self.portfolioActiveChart = None  # Used to keep track of the current chart active on the portfolioModule
        self.central = QStackedWidget()
        self.setCentralWidget(self.central)
        self.setWindowTitle("Charter")
        self.CurrentSessionName = (
            None  # Used to keep track of the current Session logged into
        )
        self.stockData = None
        self.welcomeScreen = EntryScreen()  # Different Modules in the MainWindow
        self.userForm = UserInputForm()  # Different Modules in the MainWindow
        self.existingUsers = ExistingUsers()  # Different Modules in the MainWindow
        self.MainModule = FinancialModule()  # Different Modules in the MainWindow
        self.portfolioModule = PortfolioModule()  # Different Modules in the MainWindow
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("File")
        switchSessions_action = file_menu.addAction("Switch Sessions")
        switchSessions_action.triggered.connect(self.ExistingUserFunc)
        updatePrices_action = file_menu.addAction("Update Prices")
        updatePrices_action.triggered.connect(self.UpdatePrices)
        self.menu.hide()  # Hides the menu bar until the user logs into a session
        self.central.addWidget(self.userForm)
        self.central.addWidget(self.welcomeScreen)
        self.central.addWidget(self.existingUsers)
        self.central.addWidget(self.MainModule)
        self.central.addWidget(self.portfolioModule)
        self.central.setCurrentWidget(self.welcomeScreen)
        self.welcomeScreen.newUserButton.clicked.connect(
            self.NewUserForm
        )  # All these connect the buttons to an existing func
        self.userForm.buttons.BackButton.clicked.connect(
            self.BackButtonFunc
        )  # All these connect the buttons to an existing func
        self.welcomeScreen.existingUserButton.clicked.connect(
            self.ExistingUserFunc
        )  # All these connect the buttons to an existing func
        self.existingUsers.buttons.BackButton.clicked.connect(
            self.BackButtonFunc
        )  # All these connect the buttons to an existing func
        self.userForm.buttons.ProceedButton.clicked.connect(
            self.CreateNewSession
        )  # All these connect the buttons to an existing func
        self.existingUsers.buttons.ProceedButton.clicked.connect(  # All these connect the buttons to an existing func
            self.LoginExistingSession
        )
        # self.MainModule.SearchModule.tickerList.search.textChanged.connect(
        #    self.SearchBarFilter
        # )
        self.MainModule.SearchModule.tickerList.NoStocks.clicked.connect(  # All these connect the buttons to an existing func
            self.importStockData
        )
        self.MainModule.ChartInfoModule.chart.timeFrameButtons.oneDay.clicked.connect(  # All these connect the buttons to an existing func
            partial(self.oneDayChart, "MAIN")
        )
        self.MainModule.ChartInfoModule.chart.timeFrameButtons.oneWeek.clicked.connect(  # All these connect the buttons to an existing func
            partial(self.oneWeekChart, "MAIN")
        )
        self.MainModule.ChartInfoModule.chart.timeFrameButtons.oneMonth.clicked.connect(  # All these connect the buttons to an existing func
            partial(self.oneMonthChart, "MAIN")
        )
        self.MainModule.ChartInfoModule.chart.timeFrameButtons.threeMonth.clicked.connect(  # All these connect the buttons to an existing func
            partial(self.threeMonthChart, "MAIN")
        )
        self.MainModule.ChartInfoModule.chart.timeFrameButtons.sixMonth.clicked.connect(  # All these connect the buttons to an existing func
            partial(self.sixMonthChart, "MAIN")
        )
        self.MainModule.ChartInfoModule.chart.timeFrameButtons.oneYear.clicked.connect(  # All these connect the buttons to an existing func
            partial(self.oneYearChart, "MAIN")
        )
        self.MainModule.ChartInfoModule.chart.timeFrameButtons.threeYear.clicked.connect(  # All these connect the buttons to an existing func
            partial(self.threeYearChart, "MAIN")
        )
        self.MainModule.SearchModule.tickerList.NoStocks.clicked.connect(  # All these connect the buttons to an existing func
            self.importStockData
        )
        self.portfolioModule.chartModule.timeFrameButtons.oneDay.clicked.connect(  # All these connect the buttons to an existing func
            partial(self.oneDayChart, "PORTFOLIO")
        )
        self.portfolioModule.chartModule.timeFrameButtons.oneWeek.clicked.connect(  # All these connect the buttons to an existing func
            partial(self.oneWeekChart, "PORTFOLIO")
        )
        self.portfolioModule.chartModule.timeFrameButtons.oneMonth.clicked.connect(  # All these connect the buttons to an existing func
            partial(self.oneMonthChart, "PORTFOLIO")
        )
        self.portfolioModule.chartModule.timeFrameButtons.threeMonth.clicked.connect(  # All these connect the buttons to an existing func
            partial(self.threeMonthChart, "PORTFOLIO")
        )
        self.portfolioModule.chartModule.timeFrameButtons.sixMonth.clicked.connect(  # All these connect the buttons to an existing func
            partial(self.sixMonthChart, "PORTFOLIO")
        )
        self.portfolioModule.chartModule.timeFrameButtons.oneYear.clicked.connect(  # All these connect the buttons to an existing func
            partial(self.oneYearChart, "PORTFOLIO")
        )
        self.portfolioModule.chartModule.timeFrameButtons.threeYear.clicked.connect(  # All these connect the buttons to an existing func
            partial(self.threeYearChart, "PORTFOLIO")
        )

        self.MainModule.SearchModule.popUpButton.clicked.connect(  # All these connect the buttons to an existing func
            self.MainModule.popUpMenu.hideOrShow
        )
        self.MainModule.popUpMenu.Portfolio.clicked.connect(
            self.PortfolioModuleSwitch
        )  # All these connect the buttons to an existing func
        self.portfolioModule.stocksInPortfolioList.popUpButton.clicked.connect(  # All these connect the buttons to an existing func
            self.portfolioModule.popUpMenuPortfolio.hideOrShow
        )
        self.portfolioModule.popUpMenuPortfolio.Screener.clicked.connect(  # All these connect the buttons to an existing func
            partial(self.central.setCurrentWidget, self.MainModule)
        )
        self.portfolioModule.stocksInPortfolioList.tickerList.NoStocks.clicked.connect(  # All these connect the buttons to an existing func
            self.ImportPortfolioStockData
        )
        self.portfolioModule.buySellModule.confirmTrade.clicked.connect(  # All these connect the buttons to an existing func
            self.BuySellTransaction
        )
        self.portfolioModule.stocksInPortfolioList.portfolioOverview.clicked.connect(  # All these connect the buttons to an existing func
            self.portfolioBreakUp
        )

    def NewUserForm(self):  # sets the current Widget to the UserInputForm
        self.central.setCurrentWidget(self.userForm)

    def BackButtonFunc(self):  # sets the Current Widget the Entry Screen
        self.central.setCurrentWidget(self.welcomeScreen)

    def ExistingUserFunc(
        self,
    ):  # sets the current widget to the existing Users screen
        self.central.setCurrentWidget(self.existingUsers)
        oldStocks = (
            self.MainModule.SearchModule.tickerList.stockList.layout.count() - 2
        )  # (The whole func deals with this)If a user switches sessions after already having logged onto one, deletes the current tickers in the tickerList,across both modules)
        # print(oldStocks)
        while oldStocks >= 0:
            # print(
            #    self.MainModule.SearchModule.tickerList.stockList.layout.itemAt(
            #        oldStocks
            #    )
            # )
            removeWidget = (
                self.MainModule.SearchModule.tickerList.stockList.layout.itemAt(
                    oldStocks
                ).widget()
            )
            removeWidget.setParent(None)
            oldStocks -= 1
        oldPortfolio = (
            self.portfolioModule.stocksInPortfolioList.tickerList.stockList.layout.count()
            - 2
        )
        while oldPortfolio >= 0:
            removePortfolioStock = self.portfolioModule.stocksInPortfolioList.tickerList.stockList.layout.itemAt(
                oldPortfolio
            ).widget()
            removePortfolioStock.setParent(None)
            oldPortfolio -= 1
        oldTransaction = (
            self.portfolioModule.transactionModule.transactionList.layout.count()
        )
        while oldTransaction >= 0:
            if self.portfolioModule.transactionModule.transactionList.layout.itemAt(
                oldTransaction
            ):
                removeTransaction = self.portfolioModule.transactionModule.transactionList.layout.itemAt(
                    oldTransaction
                ).widget()
                try:
                    removeTransaction.setParent(None)
                except:
                    pass
            oldTransaction -= 1
        self.menu.hide()
        self.MainModule.ChartInfoModule.chart.DeleteChart()
        self.MainModule.ChartInfoModule.info.MainInfoModule.deleteInfo()

    def CreateNewSession(
        self,
    ):  # After user fills UserInputForm, makes a new session if all inputs are valid
        if (
            f"{self.userForm.userInputField.text()}"
            not in os.listdir(  # Checks if session already exists or not
                "financialModeller\\SessionData"
            )
        ):
            os.mkdir(
                f"financialModeller\\SessionData\\{self.userForm.userInputField.text()}"
            )
            self.file = f"financialModeller\\SessionData\\{self.userForm.userInputField.text()}\\{self.userForm.userInputField.text()}.db"
            screenerTracker = open(
                f"financialModeller\\SessionData\\{self.userForm.userInputField.text()}\\stocksInScreener.pkl",
                "wb",
            )
            self.portfolioDb = "portfolioData.db"
            self.portfolioFile = f"financialModeller\\SessionData\\{self.userForm.userInputField.text()}\\{self.portfolioDb}"
            self.portfolioConn = sqlite3.connect(self.portfolioFile)
            self.portfolioConnCur = self.portfolioConn.cursor()
            print(self.file)
        else:
            self.dlg = Error(
                "Session Already Exists, Please Enter a different Session Name"
            )
            self.dlg.exec()
            return
        self.CurrentSessionConn = sqlite3.connect(
            self.file
        )  # If session doesnt exist already, makes an sqlite db and switches to the main module,also adds the session name to the existing sessions list
        print("sqlite3 Database Formed")
        self.dlg = SuccessDialog()
        self.dlg.exec()
        self.central.setCurrentWidget(self.MainModule)
        self.menu.show()
        for file in os.listdir("financialModeller\\SessionData"):
            if (
                len(self.existingUsers.List.findItems(file, Qt.MatchFlag.MatchExactly))
                == 0
            ):
                self.existingUsers.List.addItem(file)
        self.CurrentSessionName = self.userForm.userInputField.text()

    def LoginExistingSession(
        self,
    ):  # Logs into a existing session, making a connection to the relevant database
        try:
            self.CurrentSessionName = (
                self.existingUsers.List.selectedItems()[0].text().replace(".db", "")
            )
        except:  # Ensures selection of the a valid session
            errDialog = Error("Please Select a valid Session Name")
            errDialog.exec()
            return
        self.CurrentSession = f"financialModeller\\SessionData\\{self.existingUsers.List.selectedItems()[0].text()}\\{self.existingUsers.List.selectedItems()[0].text()}.db"
        self.CurrentSessionConn = sqlite3.connect(self.CurrentSession)
        self.portfolioSession = f"financialModeller\\SessionData\\{self.existingUsers.List.selectedItems()[0].text()}\\portfolioData.db"
        self.portfolioConn = sqlite3.connect(self.portfolioSession)
        self.portfolioConnCur = self.portfolioConn.cursor()
        self.CurrentSessionCur = self.CurrentSessionConn.cursor()
        # self.CurrentSessionCur.execute(
        #    """SELECT name FROM sqlite_master
        #    WHERE type='table';"""
        # )
        stocksInScreenerFile = open(
            f"financialModeller\\SessionData\\{self.CurrentSessionName}\\stocksInScreener.pkl",
            "rb",
        )
        try:
            existingStocksInScreener = pickle.load(
                stocksInScreenerFile
            )  # helps to keep track of stocks in the screener section, helping in distinguishing between stocks in the screener and stocks in the portfolio
        except:
            existingStocksInScreener = []
        # self.existingTables = self.CurrentSessionCur.fetchall()
        if existingStocksInScreener:
            for stock in existingStocksInScreener:
                if (
                    "Mo" in stock or "Wk" in stock or "Portfolio" in stock
                ):  # if block Not required, but might break, havent tried it out
                    continue
                # print(stock)
                self.priceTable = pd.read_sql_query(
                    f"SELECT * FROM {stock}", self.CurrentSessionConn
                )  # load existing data
                with open(
                    f"financialModeller\\SessionData\\{self.CurrentSessionName}\\{self.CurrentSessionName}-{stock}.pkl",
                    "rb",
                ) as f:
                    self.stockInfo = pickle.load(f)
                self.priceTicker = Ticker(
                    stock,
                    str(
                        round(
                            float(
                                self.priceTable["Close"].iloc[
                                    len(self.priceTable) - 1
                                ]  # Makes Tickers for the existing stocks in screener
                            ),
                            5,
                        )
                    ),
                    self.stockInfo,
                    uneditedTickerSymbol=self.stockInfo["symbol"],
                )
                self.priceTicker.deleteButton.clicked.connect(  # Gives Functionality to the ticker Widget
                    partial(self.DeleteTicker, stock)
                )
                self.priceTicker.clicked.signal.connect(  # Gives Functionality to the ticker Widget
                    partial(self.createInfo, self.stockInfo)
                )
                self.MainModule.SearchModule.tickerList.stockList.layout.insertWidget(  # Inserts the tickers into the tickerList
                    0, self.priceTicker
                )
                # print(self.pricetable)
        print(f"Connection established to {self.CurrentSession}")

        self.central.setCurrentWidget(self.MainModule)
        self.menu.show()

        # The following block does the same thing as the above one, but for the portfolioModule Stocks
        try:
            existingPortfolio = pd.read_sql(
                "SELECT * FROM PORTFOLIODATA", self.portfolioConn
            )
        except:
            return
        i = 0
        while i < len(
            existingPortfolio
        ):  # Iterates through each row in the dataframe, making a portfolio Ticker Widget for each row
            row = existingPortfolio.loc[i]
            priceHistory = pd.read_sql(
                f"SELECT * FROM {row['stock'].replace('-','').replace('.','')}",
                self.CurrentSessionConn,
            )
            stockData = pickle.load(
                open(
                    f"financialModeller\\SessionData\\{self.CurrentSessionName}\\{self.CurrentSessionName}-{row['stock'].replace('-','').replace('.','')}.pkl",
                    "rb",
                )
            )
            currHolding = self.portfolioConnCur.execute(
                "SELECT QuantityLeft FROM PORTFOLIODATA WHERE stock = ?",
                (row["stock"],),
            )
            currHolding = list(currHolding.fetchone())
            self.portfolioTickerObject = PortfolioTicker(
                tickerSymbol=row["stock"],
                buyPrice=row["DCAPrice"],
                stockData=stockData,
                priceHistory=priceHistory,
                uneditedTickerSymbol=stockData["symbol"],
                tickerPrice=str(
                    round(priceHistory["Close"].iloc[len(priceHistory) - 1], 5)
                ),
                holding=currHolding[0],
            )
            self.portfolioTickerObject.clicked.signal.connect(
                partial(
                    self.portfolioTickerClick,
                    stockData["symbol"],
                    stockData,
                    self.portfolioTickerObject,
                )
            )
            self.portfolioModule.stocksInPortfolioList.tickerList.stockList.layout.insertWidget(
                0, self.portfolioTickerObject
            )
            i += 1

        # Appends transactions to the transaction Module if any existing transactions
        self.portfolioConnCur.execute("SELECT * FROM TransactionHistory")
        transactionItems = self.portfolioConnCur.fetchall()
        for item in transactionItems:
            item = list(item)
            transactionItem = Transaction(
                item[0], item[2], str(item[3]), str(item[4]), item[5], item[6]
            )
            self.portfolioModule.transactionModule.transactionList.layout.insertWidget(
                0, transactionItem
            )
        self.UpdatePrices()  # Updates Prices of stocks in the screener/portfolio on Logging into an existing Session
        df = pd.read_sql("SELECT * FROM PORTFOLIODATA", self.portfolioConn)
        df2 = pd.read_sql("SELECT * FROM TransactionHistory", self.portfolioConn)
        if (
            len(df) == 0
        ):  # If never accessed the portfolio Module or a new User, wont make the Pie Chart and the portfolio Performance
            return
        self.portfolioModule.portfolioOverview.makePieChart(df)
        self.portfolioModule.portfolioOverview.portfolioPerformanceWidget.updatePortfolioPerformance(
            df, df2, self.CurrentSessionConn
        )

    def popUpLeftMenu(self):  # handles the show/hide functionality for the sidebar menu
        if not self.MainModule.popUpMenu.showCount:
            self.MainModule.popUpMenu.show()
            self.MainModule.popUpMenu.updateState(True)
        else:
            self.MainModule.popUpMenu.hide()
            self.MainModule.popUpMenu.updateState(False)

    def threadImport(
        self,
    ):  # Might implement threading,would prove too difficult now tho
        t1 = QThread()
        t1.start()

    def importStockData(self):  # handles importing data for new stocks
        self.importDialog = ImportDialog()
        self.importDialog.exec()
        self.searchSymbol = self.importDialog.StockName.text()
        if not self.searchSymbol:  # Error handling for invalid input
            self.error = Error("Either Stock already exists or no input was given")
            self.error.exec()
            return
        tickersExisting = [
            i.tickerSymbol.text()
            for i in self.MainModule.SearchModule.tickerList.stockList.layout.children()
        ]
        if self.searchSymbol in tickersExisting:  # Error handling for invalid input
            self.error = Error("Either Stock already exists or no input was given")
            self.error.exec()
            return
        self.stockData = yf.Ticker(
            self.searchSymbol
        )  # gets stock data from yfinance library
        # print(self.stockData.info)
        # print(self.stockData.history(period="1mo"))
        # print(self.InceptionDate, datetime.datetime.today())
        self.curPrice = self.stockData.history(
            period="1d"
        )  # fetching dataframe for prices
        self.ogStockTicker = self.stockData.ticker

        # Replace methods are used to ensure no sqlite errors

        self.stockTicker = str(self.stockData.ticker).replace(".", "")
        self.stockTicker = self.stockTicker.replace("-", "")
        try:  # Makes stock ticker if proper input was provided, otherwise throws an error
            self.ticker = Ticker(
                self.stockTicker,
                str(round(float(self.curPrice["Close"].iloc[0]), 5)),
                self.stockData.info,
                uneditedTickerSymbol=self.ogStockTicker,
            )
            self.ticker.clicked.signal.connect(
                partial(self.createInfo, self.stockData.info)
            )
            self.ticker.deleteButton.clicked.connect(
                partial(self.DeleteTicker, self.stockTicker)
            )
        except:
            self.ErrorDialog = Error(
                "Stock Not Found, Please Enter Ticker Name as Specified on Yahoo"
            )
            self.ErrorDialog.exec()
            return
        screenerTracker = open(
            f"financialModeller\\SessionData\\{self.CurrentSessionName}\\stocksInScreener.pkl",
            "rb",
        )
        try:  # Appends newly imported stock to stocksInScreener.pkl
            stocksExisting = pickle.load(screenerTracker)
            stocksExisting.append(self.stockTicker)
        except:  # if pkl file does not exist, initialises a list with the stock in it
            stocksExisting = [self.stockTicker]
        screenerTracker = open(
            f"financialModeller\\SessionData\\{self.CurrentSessionName}\\stocksInScreener.pkl",
            "wb",
        )  # Opens/creates the pkl file
        pickle.dump(stocksExisting, screenerTracker)  # saves to the pkl file
        self.stockData.history(period="max").sort_values("Date").to_sql(
            self.stockTicker,
            self.CurrentSessionConn,
            if_exists="replace",
            dtype={"Date": "DATETIME"},
        )  # saves price dataframe to self.currentsessionConn sqlite db
        oneWeekIntervalHistory = self.stockData.history(period="max", interval="1wk")
        oneWeekIntervalHistory.sort_values("Date").to_sql(
            f"{self.stockTicker}OneWk",
            self.CurrentSessionConn,
            if_exists="replace",
            dtype={"Date": "DATETIME"},
        )  # saves price dataframe to self.currentsessionConn sqlite db
        with open(
            f"financialModeller\\SessionData\\{self.CurrentSessionName}\\{self.CurrentSessionName}-{self.stockTicker}.pkl",
            "wb",
        ) as f:
            pickle.dump(
                self.stockData.info, f
            )  # Makes a pkl file for that stock, and saves its info
        self.MainModule.SearchModule.tickerList.stockList.layout.insertWidget(
            0, self.ticker
        )  # Inserts the ticker object created into the tickerList

        df = pd.read_sql(f"SELECT * FROM {self.stockTicker}", self.CurrentSessionConn)
        df.reset_index(inplace=True, drop=True)
        df["Date"] = pd.to_datetime(df["Date"], utc=True)
        self.MainModule.ChartInfoModule.chart.updateStockData(
            df, self.searchSymbol
        )  # Makes the chart
        self.createInfo(self.stockData.info)  # Makes the info

    def createInfo(
        self, stockData
    ):  # adds data to the infoModules when clicked on a ticker, also updates the chart for that ticker, adding the timeframe buttons aswell
        if self.MainModule.ChartInfoModule.info.stackSwitcher.layout.count() != 0:
            self.MainModule.ChartInfoModule.info.stackSwitcher.deleteButtons()  # refreshes the infoModule
        self.MainModule.ChartInfoModule.info.MainInfoModule.deleteInfo()  # refreshes the chartModule
        self.stockInfo = stockData

        # InfoTab 3
        self.MetricLabel = QLabel(
            "<strong>Metrics/Ratios</strong>"
        )  # Making structured labels to represent data
        self.MetricLabel.setObjectName("MetricLabel")
        try:
            self.prevClose = QLabel(
                f"Previous Close:   {self.stockInfo['previousClose']}"
            )
        except:
            self.prevClose = QLabel(f"Previous Close:   NA")
        try:
            self.Open = QLabel(f"Open:   {self.stockInfo['open']}")
        except:
            self.Open = QLabel(f"Open:   NA")
        try:
            self.DaysRange = QLabel(
                f"Days Range:   {self.stockInfo['dayLow']} - {self.stockInfo['dayHigh']}"
            )
        except:
            self.DaysRange = QLabel(f"Days Range:   NA")
        try:
            self.YearRange = QLabel(
                f"Year Range:   {self.stockInfo['fiftyTwoWeekLow']} - {self.stockInfo['fiftyTwoWeekHigh']}"
            )
        except:
            self.YearRange = QLabel(f"Year Range:   NA")
        try:
            self.Volume = QLabel(f"Volume:   {self.stockInfo['volume']}")
        except:
            self.Volume = QLabel(f"Volume:   NA")
        try:
            self.AvgVolume = QLabel(f"Avg. Volume:   {self.stockInfo['averageVolume']}")
        except:
            self.AvgVolume = QLabel(f"Avg. Volume:   NA")
        try:
            self.marketCap = QLabel(f"Market Cap:   {self.stockInfo['marketCap']}")
        except:
            self.marketCap = QLabel(f"Market Cap:   NA")
        try:
            self.Beta = QLabel(f"Beta(5Y Monthly):   {self.stockInfo['beta']}")
        except:
            self.Beta = QLabel(f"Beta(5Y Monthly):   NA")
        try:
            self.pe = QLabel(f"PE Ratio(TTM):   {self.stockInfo['trailingPE']}")
        except:
            self.pe = QLabel(f"PE Ratio(TTM):   NA")
        try:
            self.eps = QLabel(f"EPS(TTM):   {self.stockInfo['trailingEps']}")
        except:
            self.eps = QLabel(f"EPS(TTM):   NA")
        try:
            self.Est = QLabel(
                f"1Y Target Est(Mean Target Price):   {self.stockInfo['targetMeanPrice']}"
            )
        except:
            self.Est = QLabel(f"1Y Target Est(Mean Target Price):   NA")

        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule3.layout.addWidget(
            self.MetricLabel, 0, 0
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule3.layout.addWidget(
            self.prevClose, 1, 0
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule3.layout.addWidget(
            self.Open, 1, 1
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule3.layout.addWidget(
            self.DaysRange, 1, 2
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule3.layout.addWidget(
            self.YearRange, 1, 3
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule3.layout.addWidget(
            self.Volume, 2, 0
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule3.layout.addWidget(
            self.AvgVolume, 2, 1
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule3.layout.addWidget(
            self.marketCap, 2, 2
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule3.layout.addWidget(
            self.Beta, 2, 3
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule3.layout.addWidget(
            self.pe, 3, 0
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule3.layout.addWidget(
            self.eps, 3, 1
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule3.layout.addWidget(
            self.Est, 3, 2
        )

        df = pd.read_sql(
            f"SELECT Date,Open,High,Low,Close,Volume FROM {self.stockInfo['symbol'].replace('.','').replace('-','')}",
            self.CurrentSessionConn,
        )
        df["Date"] = pd.to_datetime(df["Date"], utc=True)
        # print(df)
        df.reset_index(inplace=True, drop=True)
        self.MainModule.ChartInfoModule.chart.updateStockData(  # Inserts price dataframe into the chart
            df, self.stockInfo["symbol"]
        )
        self.activeChart = self.stockInfo["symbol"]
        self.MainModule.ChartInfoModule.info.stackSwitcher.AddButtons()  # Adds Buttons to the stackSwitcher
        self.MainModule.ChartInfoModule.info.stackSwitcher.button1.clicked.connect(
            partial(
                self.switchStack, 1, "main"
            )  # Adds func to the stackSwitching buttons
        )
        self.MainModule.ChartInfoModule.info.stackSwitcher.button2.clicked.connect(
            partial(
                self.switchStack, 2, "main"
            )  # Adds func to the stackSwitching buttons
        )
        self.MainModule.ChartInfoModule.info.stackSwitcher.button3.clicked.connect(
            partial(
                self.switchStack, 3, "main"
            )  # Adds func to the stackSwitching buttons
        )
        self.MainModule.ChartInfoModule.info.stackSwitcher.button4.clicked.connect(
            partial(
                self.switchStack, 4, "main"
            )  # Adds func to the stackSwitching buttons
        )
        self.MainModule.ChartInfoModule.info.stackSwitcher.button5.clicked.connect(
            partial(
                self.switchStack, 5, "main"
            )  # Adds func to the stackSwitching buttons
        )

        # InfoTab 1
        self.About = QLabel("<strong>About</strong>")
        self.About.setObjectName("About")
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule1.layout.setRowStretch(
            0, 1
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule1.layout.setRowStretch(
            1, 3
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule1.layout.addWidget(
            self.About, 0, 0
        )
        try:
            self.stockAbout = QLabel(self.stockInfo["longBusinessSummary"])
        except:
            self.stockAbout = QLabel("Not Available")
        self.stockAbout.setWordWrap(True)
        self.stockAbout.setObjectName("stockAbout")
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule1.layout.addWidget(
            self.stockAbout, 1, 0
        )
        try:
            self.stockWebsite = QLabel(f"Website:   {self.stockInfo["website"]}")
        except:
            self.stockWebsite = QLabel("Website:   NA")
        try:
            self.stockIndustry = QLabel(f"Industry:   {self.stockInfo["industry"]}")
        except:
            self.stockIndustry = QLabel("Industry:   NA")
        try:
            self.stockSector = QLabel(f"Sector:   {self.stockInfo["sector"]}")
        except:
            self.stockSector = QLabel("Sector:   NA")
        try:
            self.stockFullTimeEmployees = QLabel(
                f"Full Time Employees:   {self.stockInfo["fullTimeEmployees"]}"
            )
        except:
            self.stockFullTimeEmployees = QLabel("Full Time Employees:   NA")
        try:
            self.stockType = QLabel(f"Stock Type:   {self.stockInfo["quoteType"]}")
        except:
            self.stockType = QLabel("Stock Type:   NA")
        try:
            self.stockCurrency = QLabel(
                f"Financial Currency:   {self.stockInfo["financialCurrency"]}"
            )
        except:
            self.stockCurrency = QLabel("Financial Currency:   NA")
        try:
            self.stockEnterpriseValue = QLabel(
                f"Enterprise Value:   {self.stockInfo["enterpriseValue"]}"
            )
        except:
            self.stockEnterpriseValue = QLabel("Enterprise Value:   NA")
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule2.layout.addWidget(
            self.stockWebsite, 0, 0
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule2.layout.addWidget(
            self.stockIndustry, 0, 1
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule2.layout.addWidget(
            self.stockSector, 0, 2
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule2.layout.addWidget(
            self.stockFullTimeEmployees, 0, 3
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule2.layout.addWidget(
            self.stockType, 1, 0
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule2.layout.addWidget(
            self.stockCurrency, 1, 1
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule2.layout.addWidget(
            self.stockEnterpriseValue, 1, 2
        )

        # InfoTab4
        self.misc = QLabel("<strong>Miscellaneous</strong>")
        self.misc.setObjectName("Misc")
        try:
            self.profitMargins = QLabel(
                f"Profit Margins:   {self.stockInfo['profitMargins']}"
            )
        except:
            self.profitMargins = QLabel(f"Profit Margins:   NA")
        try:
            self.ReturnOnAssets = QLabel(
                f"Return on Assets:   {self.stockInfo['returnOnAssets']}"
            )
        except:
            self.ReturnOnAssets = QLabel(f"Return on Assets:   NA")
        try:
            self.ReturnOnEquity = QLabel(
                f"Return on Equity:   {self.stockInfo['returnOnEquity']}"
            )
        except:
            self.ReturnOnEquity = QLabel(f"Return on Equity:   NA")
        try:
            self.CurrentRatio = QLabel(
                f"Current Ratio:   {self.stockInfo['currentRatio']}"
            )
        except:
            self.CurrentRatio = QLabel(f"Current Ratio:   NA")
        try:
            self.QuickRatio = QLabel(f"Quick Ratio:   {self.stockInfo['quickRatio']}")
        except:
            self.QuickRatio = QLabel(f"Quick Ratio:   NA")
        try:
            self.PriceToBook = QLabel(
                f"Price To Book:   {self.stockInfo['priceToBook']}"
            )
        except:
            self.PriceToBook = QLabel(f"Price To Book:   NA")
        try:
            self.DebtToEquity = QLabel(
                f"Debt To Equity:   {self.stockInfo['debtToEquity']}"
            )
        except:
            self.DebtToEquity = QLabel(f"Debt To Equity:   NA")
        try:
            self.earningQuaterlyGrowth = QLabel(
                f"Earnings Quaterly Growth:   {self.stockInfo['earningsQuaterlyGrowth']}"
            )
        except:
            self.earningQuaterlyGrowth = QLabel(f"Earnings Quaterly Growth:   NA")
        try:
            self.AnalystOpinion = QLabel(
                f"Analyst Opinion:   {self.stockInfo['recommendationKey'].replace('_',' ').replace('-',' ').upper()}"
            )
        except:
            self.AnalystOpinion = QLabel(f"Analyst Opinion:   NA")

        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule4.layout.addWidget(
            self.misc, 0, 0
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule4.layout.addWidget(
            self.profitMargins, 1, 0
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule4.layout.addWidget(
            self.ReturnOnAssets, 1, 1
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule4.layout.addWidget(
            self.ReturnOnEquity, 1, 2
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule4.layout.addWidget(
            self.CurrentRatio, 2, 0
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule4.layout.addWidget(
            self.QuickRatio, 2, 1
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule4.layout.addWidget(
            self.PriceToBook, 2, 2
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule4.layout.addWidget(
            self.DebtToEquity, 3, 0
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule4.layout.addWidget(
            self.earningQuaterlyGrowth, 3, 1
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule4.layout.addWidget(
            self.AnalystOpinion, 3, 2
        )

        # InfoTab5
        weekOldPrice = pd.read_sql(
            f"SELECT * FROM {self.stockInfo['symbol'].replace('-','').replace('.','')}",
            self.CurrentSessionConn,
        )
        weekOldPrice["Date"] = pd.to_datetime(weekOldPrice["Date"], utc=True)
        oldestPrice = weekOldPrice.iloc[0]
        curPrice = weekOldPrice.iloc[-1]
        monthOldPrice = weekOldPrice
        halfYearOldPrice = weekOldPrice
        yearOldPrice = weekOldPrice
        if (
            len(weekOldPrice)
            == len(
                weekOldPrice.loc[
                    weekOldPrice["Date"]
                    > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                    - relativedelta(days=8)
                ]
            )
            or len(
                weekOldPrice.loc[
                    weekOldPrice["Date"]
                    > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                    - relativedelta(days=8)
                ]
            )
            == 0
        ):
            weekGain = "NA"
        else:
            weekOldPrice = weekOldPrice.loc[
                weekOldPrice["Date"]
                > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                - relativedelta(days=8)
            ]
            weekOldPrice.reset_index(inplace=True, drop=True)
            # print(weekOldPrice)
            weekOldPrice = weekOldPrice.iloc[0]
            weekGain = round(
                ((curPrice["Close"] - weekOldPrice["Close"]) / weekOldPrice["Close"])
                * 100,
                3,
            )
        if (
            len(monthOldPrice)
            == len(
                monthOldPrice.loc[
                    monthOldPrice["Date"]
                    > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                    - relativedelta(days=32)
                ]
            )
            or len(
                monthOldPrice.loc[
                    monthOldPrice["Date"]
                    > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                    - relativedelta(days=32)
                ]
            )
            == 0
        ):
            monthGain = "NA"
        else:
            monthOldPrice = monthOldPrice.loc[
                monthOldPrice["Date"]
                > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                - relativedelta(days=32)
            ]
            monthOldPrice.reset_index(inplace=True, drop=True)
            monthOldPrice = monthOldPrice.iloc[0]
            monthGain = round(
                ((curPrice["Close"] - monthOldPrice["Close"]) / monthOldPrice["Close"])
                * 100,
                3,
            )
        if (
            len(halfYearOldPrice)
            == len(
                halfYearOldPrice.loc[
                    halfYearOldPrice["Date"]
                    > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                    - relativedelta(days=182)
                ]
            )
            or len(
                halfYearOldPrice.loc[
                    halfYearOldPrice["Date"]
                    > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                    - relativedelta(days=182)
                ]
            )
            == 0
        ):
            halfYearGain = "NA"
        else:
            halfYearOldPrice = halfYearOldPrice.loc[
                halfYearOldPrice["Date"]
                > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                - relativedelta(days=182)
            ]
            halfYearOldPrice.reset_index(inplace=True, drop=True)
            halfYearOldPrice = halfYearOldPrice.iloc[0]
            halfYearGain = round(
                (
                    (curPrice["Close"] - halfYearOldPrice["Close"])
                    / halfYearOldPrice["Close"]
                )
                * 100,
                3,
            )
        if (
            len(yearOldPrice)
            == len(
                yearOldPrice.loc[
                    yearOldPrice["Date"]
                    > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                    - relativedelta(years=1)
                ]
            )
            or len(
                yearOldPrice.loc[
                    yearOldPrice["Date"]
                    > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                    - relativedelta(years=1)
                ]
            )
            == 0
        ):
            yearGain = "NA"
        else:
            yearOldPrice = yearOldPrice.loc[
                yearOldPrice["Date"]
                > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                - relativedelta(years=1)
            ]
            yearOldPrice.reset_index(inplace=True, drop=True)
            yearOldPrice = yearOldPrice.iloc[0]
            yearGain = round(
                ((curPrice["Close"] - yearOldPrice["Close"]) / yearOldPrice["Close"])
                * 100,
                3,
            )
        lifetimeGain = round(
            ((curPrice["Close"] - oldestPrice["Close"]) / oldestPrice["Close"]) * 100,
            3,
        )
        tabLabel = QLabel("<strong>Performance</strong>")
        tabLabel.setObjectName("Performance")
        weekGainLabel = QLabel(f"1 Week Gain:   {str(weekGain)}%")
        monthGainLabel = QLabel(f"1 Month Gain:   {str(monthGain)}%")
        halfYearGainLabel = QLabel(f"6 Month Gain:   {str(halfYearGain)}%")
        yearGainLabel = QLabel(f"1 Year Gain:   {str(yearGain)}%")
        lifetimeGainLabel = QLabel(f"Gain since Inception:   {str(lifetimeGain)}%")
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule5.layout.addWidget(
            tabLabel, 0, 0
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule5.layout.addWidget(
            weekGainLabel, 1, 0
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule5.layout.addWidget(
            monthGainLabel, 1, 1
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule5.layout.addWidget(
            halfYearGainLabel, 1, 2
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule5.layout.addWidget(
            yearGainLabel, 2, 0
        )
        self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule5.layout.addWidget(
            lifetimeGainLabel, 2, 1
        )

        self.MainModule.ChartInfoModule.chart.timeFrameButtons.constructLayout(
            self.stockInfo["firstTradeDateEpochUtc"]
        )

    def switchStack(
        self, stackNumber, whichModule
    ):  # Adds functionality to stackSwitcherButtons, depending on the module
        if stackNumber == 1:
            if whichModule.upper() == "MAIN":
                self.MainModule.ChartInfoModule.info.MainInfoModule.setCurrentWidget(
                    self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule1
                )
            elif whichModule.upper() == "PORTFOLIO":
                self.portfolioModule.infoModule.MainInfoModule.setCurrentWidget(
                    self.portfolioModule.infoModule.MainInfoModule.infoModule1
                )
        if stackNumber == 2:
            if whichModule.upper() == "MAIN":
                self.MainModule.ChartInfoModule.info.MainInfoModule.setCurrentWidget(
                    self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule2
                )
            elif whichModule.upper() == "PORTFOLIO":
                self.portfolioModule.infoModule.MainInfoModule.setCurrentWidget(
                    self.portfolioModule.infoModule.MainInfoModule.infoModule2
                )
        if stackNumber == 3:
            if whichModule.upper() == "MAIN":
                self.MainModule.ChartInfoModule.info.MainInfoModule.setCurrentWidget(
                    self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule3
                )
            elif whichModule.upper() == "PORTFOLIO":
                self.portfolioModule.infoModule.MainInfoModule.setCurrentWidget(
                    self.portfolioModule.infoModule.MainInfoModule.infoModule3
                )
        if stackNumber == 4:
            if whichModule.upper() == "MAIN":
                self.MainModule.ChartInfoModule.info.MainInfoModule.setCurrentWidget(
                    self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule4
                )
            elif whichModule.upper() == "PORTFOLIO":
                self.portfolioModule.infoModule.MainInfoModule.setCurrentWidget(
                    self.portfolioModule.infoModule.MainInfoModule.infoModule4
                )
        if stackNumber == 5:
            if whichModule.upper() == "MAIN":
                self.MainModule.ChartInfoModule.info.MainInfoModule.setCurrentWidget(
                    self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule5
                )
            elif whichModule.upper() == "PORTFOLIO":
                self.portfolioModule.infoModule.MainInfoModule.setCurrentWidget(
                    self.portfolioModule.infoModule.MainInfoModule.infoModule5
                )
        if stackNumber == 6:
            if whichModule.upper() == "MAIN":
                self.MainModule.ChartInfoModule.info.MainInfoModule.setCurrentWidget(
                    self.MainModule.ChartInfoModule.info.MainInfoModule.infoModule6
                )
            elif whichModule.upper() == "PORTFOLIO":
                self.portfolioModule.infoModule.MainInfoModule.setCurrentWidget(
                    self.portfolioModule.infoModule.MainInfoModule.infoModule6
                )

    def getChartDataCustomInterval(
        self, interval: str, whichModule
    ):  # func to resample daily data into different period formats
        allowedFrequencies = ["ME", "3ME", "6ME", "YE", "3YE"]
        if interval not in allowedFrequencies:
            raise ValueError(f"Allowed Values are: {allowedFrequencies}")
        if (
            whichModule.upper() == "MAIN"
        ):  # Uses activeChart variables to fetch data for the current active chart and resample that data into diff duration formats
            df = pd.read_sql(
                f"SELECT Date,Open,High,Low,Close,Volume FROM {self.activeChart.replace('.','').replace('-','')}",
                self.CurrentSessionConn,
            )
        elif whichModule.upper() == "PORTFOLIO":
            df = pd.read_sql(
                f"SELECT Date,Open,High,Low,Close,Volume FROM {self.portfolioActiveChart.replace('.','').replace('-','')}",
                self.CurrentSessionConn,
            )
        df["Date"] = pd.to_datetime(df["Date"], utc=True)
        df.set_index("Date", inplace=True)
        # print(df, df.dtypes)
        finishedData = df.resample(interval).agg(
            {
                "Open": "first",
                "High": "max",
                "Low": "min",
                "Close": "last",
                "Volume": "sum",
            }
        )
        finishedData.reset_index(inplace=True)
        if whichModule.upper() == "MAIN":
            self.MainModule.ChartInfoModule.chart.updateStockData(
                finishedData, self.activeChart
            )
        elif whichModule.upper() == "PORTFOLIO":
            self.portfolioModule.chartModule.updateStockData(
                finishedData, self.portfolioActiveChart
            )

    def oneDayChart(
        self, whichModule
    ):  # fetches data from database of daily prices,previously stored, of that stock
        if whichModule.upper() == "MAIN":
            activeChart = self.activeChart.replace(".", "").replace("-", "")
        elif whichModule.upper() == "PORTFOLIO":
            activeChart = self.portfolioActiveChart.replace(".", "").replace("-", "")
        df = pd.read_sql(
            f"SELECT Date,Open,High,Low,Close,Volume FROM {activeChart}",
            self.CurrentSessionConn,
        )
        df.reset_index(inplace=True, drop=True)
        df["Date"] = pd.to_datetime(df["Date"], utc=True)
        if whichModule.upper() == "MAIN":
            self.MainModule.ChartInfoModule.chart.updateStockData(df, self.activeChart)
        elif whichModule.upper() == "PORTFOLIO":
            self.portfolioModule.chartModule.updateStockData(
                df, self.portfolioActiveChart
            )

    def oneWeekChart(
        self, whichModule
    ):  # Similar to oneDayChart, but fetches weekly data
        if whichModule.upper() == "MAIN":
            activeChart = self.activeChart.replace(".", "").replace("-", "")
        elif whichModule.upper() == "PORTFOLIO":
            activeChart = self.portfolioActiveChart.replace(".", "").replace("-", "")
        df = pd.read_sql(
            f"SELECT Date,Open,High,Low,Close,Volume FROM {activeChart}oneWk",
            self.CurrentSessionConn,
        )
        df.reset_index(inplace=True, drop=True)
        df["Date"] = pd.to_datetime(df["Date"], utc=True)
        if whichModule.upper() == "MAIN":
            self.MainModule.ChartInfoModule.chart.updateStockData(df, self.activeChart)
        elif whichModule.upper() == "PORTFOLIO":
            self.portfolioModule.chartModule.updateStockData(
                df, self.portfolioActiveChart
            )

    def oneMonthChart(
        self, whichModule
    ):  # resamples the data with the help of another func explained above
        self.getChartDataCustomInterval("ME", whichModule)

    def threeMonthChart(
        self, whichModule
    ):  # resamples the data with the help of another func explained above
        self.getChartDataCustomInterval("3ME", whichModule)

    def sixMonthChart(
        self, whichModule
    ):  # resamples the data with the help of another func explained above
        self.getChartDataCustomInterval("6ME", whichModule)

    def oneYearChart(
        self, whichModule
    ):  # resamples the data with the help of another func explained above
        self.getChartDataCustomInterval("YE", whichModule)

    def threeYearChart(
        self, whichModule
    ):  # resamples the data with the help of another func explained above
        self.getChartDataCustomInterval("3YE", whichModule)

    def DeleteTicker(
        self, tickName
    ):  # Deletes the ticker, all of its data(if it only exists in one module) on the click of a button
        portfolioTickers = (
            self.portfolioModule.stocksInPortfolioList.tickerList.stockList.layout.count()
            - 2
        )
        tickersInPortfolio = []
        while portfolioTickers >= 0:
            try:
                portfolioWidget = self.portfolioModule.stocksInPortfolioList.tickerList.stockList.layout.itemAt(
                    portfolioTickers
                ).widget()
                tickersInPortfolio.append(portfolioWidget.tickerSymbol.text())
            except:
                portfolioTickers -= 1
                continue
            portfolioTickers -= 1
        # print(tickersInPortfolio)
        if tickName in tickersInPortfolio:
            stocksInScreenerFile = open(
                f"financialModeller\\SessionData\\{self.CurrentSessionName}\\stocksInScreener.pkl",
                "rb",
            )
            stocksExisting = pickle.load(stocksInScreenerFile)
            stocksExisting.remove(tickName)
            pickle.dump(
                stocksExisting,
                open(
                    f"financialModeller\\SessionData\\{self.CurrentSessionName}\\stocksInScreener.pkl",
                    "wb",
                ),
            )
            children = (
                self.MainModule.SearchModule.tickerList.stockList.layout.count() - 2
            )
            while children >= 0:
                try:
                    obj = (
                        self.MainModule.SearchModule.tickerList.stockList.layout.itemAt(
                            children
                        ).widget()
                    )
                    ticker = obj.tickerSymbol.text()
                except:
                    children -= 1
                    continue
                if ticker == tickName:
                    obj.setParent(None)
                    break
                children -= 1
            children = (
                self.MainModule.SearchModule.tickerList.stockList.layout.count() - 2
            )
            if children > 0:
                stockObj = (
                    self.MainModule.SearchModule.tickerList.stockList.layout.itemAt(
                        children
                    ).widget()
                )
                f = open(
                    f"financialModeller\\SessionData\\{self.CurrentSessionName}\\{self.CurrentSessionName}-{stockObj.tickerSymbol.text()}.pkl",
                    "rb",
                )
                stockData = pickle.load(f)
                self.createInfo(stockData)
            # Add functionality for clean slate when all stocks are removed
            else:
                self.portfolioModule.infoModule.MainInfoModule.deleteInfo()
                self.portfolioModule.chartModule.DeleteChart()
            return

        # Up until this point, the code checks for stocks in the portfolioModule, if the stock that is being deleted in the main module also exists in the portfolio module, then no data about the stock is deleted
        # Now, if the stock is only there in the main Module, then all data about the stock is deleted
        children = self.MainModule.SearchModule.tickerList.stockList.layout.count() - 2
        if children >= 0:
            while children >= 0:
                obj = self.MainModule.SearchModule.tickerList.stockList.layout.itemAt(
                    children
                ).widget()
                ticker = obj.tickerSymbol.text()
                if ticker == tickName:
                    obj.setParent(None)
                    os.remove(
                        f"financialModeller\\SessionData\\{self.CurrentSessionName}\\{self.CurrentSessionName}-{ticker}.pkl"
                    )
                    self.CurrentSessionConn.execute(f"DROP TABLE {ticker}")
                    self.CurrentSessionConn.execute(f"DROP TABLE {ticker}OneWk")
                children -= 1
        stocksInScreenerFile = open(
            f"financialModeller\\SessionData\\{self.CurrentSessionName}\\stocksInScreener.pkl",
            "rb",
        )
        stocksExisting = pickle.load(stocksInScreenerFile)
        stocksExisting.remove(tickName)
        pickle.dump(
            stocksExisting,
            open(
                f"financialModeller\\SessionData\\{self.CurrentSessionName}\\stocksInScreener.pkl",
                "wb",
            ),
        )
        children = self.MainModule.SearchModule.tickerList.stockList.layout.count() - 2
        if children > 0:
            stockObj = self.MainModule.SearchModule.tickerList.stockList.layout.itemAt(
                children
            ).widget()
            f = open(
                f"financialModeller\\SessionData\\{self.CurrentSessionName}\\{self.CurrentSessionName}-{stockObj.tickerSymbol.text()}.pkl",
                "rb",
            )
            stockData = pickle.load(f)
            self.createInfo(stockData)
        # Add functionality for clean slate when all stocks are removed
        else:
            self.MainModule.ChartInfoModule.info.MainInfoModule.deleteInfo()
            self.MainModule.ChartInfoModule.chart.DeleteChart()

    def UpdatePrices(self):  # Updates prices of existing Tickers
        print("Updating Prices")
        countStocks = (
            self.MainModule.SearchModule.tickerList.stockList.layout.count() - 2
        )
        portfolioCountStocks = (
            self.portfolioModule.stocksInPortfolioList.tickerList.stockList.layout.count()
        ) - 2
        alreadyUpdatedStocks = []
        while (
            countStocks >= 0
        ):  # Iterates through all the stocks currently in the main module
            updateWidget = (
                self.MainModule.SearchModule.tickerList.stockList.layout.itemAt(
                    countStocks
                ).widget()
            )
            oldestDateDf = pd.read_sql(
                f"SELECT * FROM {updateWidget.tickerSymbol.text()}",
                self.CurrentSessionConn,  # Fetches the latest Date for which data is available for the stock, was using a append clause on a dataframe, but now i just replace the dataframe entirely, so kind of redundant
            )
            oldestDateDf = oldestDateDf.tail(1)
            oldestDateDf.reset_index(inplace=True, drop=True)
            oldestDateDf["Date"] = pd.to_datetime(oldestDateDf["Date"], utc=True)
            oldestDate = oldestDateDf["Date"].loc[0]
            oldestDate = datetime.datetime.date(oldestDate)
            startDate = oldestDate + relativedelta(
                days=1
            )  # Goes 1 day ahead of the latest date, since yf.Ticker.history searches from the start date provided, not exclusive of it.
            if startDate >= datetime.datetime.date(datetime.datetime.today()):
                countStocks -= 1
                continue
            newStockData = yf.Ticker(updateWidget.uneditedTicker)
            alreadyUpdatedStocks.append(updateWidget.tickerSymbol.text())
            priceHistory = newStockData.history(period="max")
            priceHistoryOneWkInterval = newStockData.history(
                interval="1wk", period="max"
            )
            if priceHistory.empty:
                countStocks -= 1  # If price dataframe is empty, skip over, again this was only valid when using the oldest date as a start date, since sometimes it would give an empty dataframe, but now its obsolete, kept in because idk if something might go wrong, still acts as an additional check anyways.
                continue
            # priceHistory = newStockData.history(period="max")
            # priceHistoryOneWkInterval = newStockData.history(
            #    period="max", interval="1wk"
            # )
            # print(priceHistory)
            # updateWidget.tickerPrice.setText(
            #    str(round(float(priceHistory["Close"].iloc[len(priceHistory) - 1]), 5))
            # )
            priceHistory.sort_values("Date").to_sql(
                updateWidget.tickerSymbol.text().replace("-", "").replace(".", ""),
                self.CurrentSessionConn,
                if_exists="replace",
                dtype={"Date": "DATETIME"},
            )  # updates data in the sql
            priceHistoryOneWkInterval.sort_values("Date").to_sql(
                f"{updateWidget.tickerSymbol.text().replace("-", "").replace(".", "")}OneWk",
                self.CurrentSessionConn,
                if_exists="replace",
                dtype={"Date": "DATETIME"},
            )  # updates data in the sql
            with open(
                f"financialModeller\\SessionData\\{self.CurrentSessionName}\\{self.CurrentSessionName}-{updateWidget
                .tickerSymbol.text().replace('-','').replace('.','')}.pkl",
                "wb",
            ) as f:
                pickle.dump(
                    newStockData.info, f
                )  # updates stock info data in the pkl file
            updateWidget.updateData(newStockData.info)
            # print(updateWidget.tickerPrice)
            updateWidget.clicked.signal.connect(
                partial(self.createInfo, newStockData.info)
            )  # connects a click event to the stock containing the new info
            updateWidget.update()
            countStocks -= 1
            priceHistory = pd.read_sql(
                f"SELECT * FROM {updateWidget.tickerSymbol.text()}",
                self.CurrentSessionConn,
            )
            newPrice = priceHistory.tail(1)
            newPrice.reset_index(drop=True, inplace=True)
            newPrice = newPrice["Close"].loc[0]
            updateWidget.updatePrice(
                newPrice
            )  # updates the price on the ticker with the latest available price
            priceHistory["Date"] = pd.to_datetime(priceHistory["Date"], utc=True)
            # print(priceHistory)
            if (
                self.activeChart and newStockData.ticker == self.activeChart
            ):  # If a stock is updated, and the same stocks chart is currently active, it will update that chart aswell
                self.MainModule.ChartInfoModule.chart.updateStockData(
                    priceHistory, self.activeChart
                )
        # print(alreadyUpdatedStocks)
        while (
            portfolioCountStocks >= 0
        ):  # The same process as before but for the portfolio ticker, this has additional parameters such as calculating the new gain/loss value aswell.
            updateWidget = self.portfolioModule.stocksInPortfolioList.tickerList.stockList.layout.itemAt(
                portfolioCountStocks
            ).widget()
            if updateWidget.tickerSymbol.text() in alreadyUpdatedStocks:
                newStockData = pickle.load(
                    open(
                        f"financialModeller\\SessionData\\{self.CurrentSessionName}\\{self.CurrentSessionName}-{updateWidget.tickerSymbol.text()}.pkl",
                        "rb",
                    )
                )
                updateWidget.clicked.signal.connect(
                    partial(
                        self.portfolioTickerClick,
                        updateWidget.tickerSymbol.text(),
                        newStockData,
                        updateWidget,
                    )
                )
                df = pd.read_sql(
                    f"SELECT * FROM {updateWidget.tickerSymbol.text().replace('-','').replace('.','')}",
                    self.CurrentSessionConn,
                )
                latestPrice = df.tail(1)
                latestPrice.reset_index(drop=True, inplace=True)
                latestPrice = latestPrice["Close"].loc[0]
                updateWidget.updatePrice(latestPrice)
                DCAPrice = pd.read_sql(
                    f"SELECT * FROM PORTFOLIODATA WHERE stock = ?",
                    self.portfolioConn,
                    params=[(updateWidget.tickerSymbol.text())],
                )
                DCAPrice.reset_index(drop=True, inplace=True)
                DCAPrice = DCAPrice["DCAPrice"].loc[0]
                updateWidget.updateGainLoss(df, DCAPrice)
                portfolioCountStocks -= 1
                continue
            newStockData = yf.Ticker(updateWidget.uneditedTicker)
            oldestDateDf = pd.read_sql(
                f"SELECT * FROM {updateWidget.tickerSymbol.text().replace('-','').replace('.','')}",
                self.CurrentSessionConn,
            )
            oldestDateDf = oldestDateDf.tail(1)
            oldestDateDf.reset_index(inplace=True, drop=True)
            oldestDateDf["Date"] = pd.to_datetime(oldestDateDf["Date"], utc=True)
            oldestDate = oldestDateDf["Date"].loc[0]
            oldestDate = datetime.datetime.date(oldestDate)
            startDate = oldestDate + relativedelta(days=1)
            if startDate >= datetime.datetime.date(datetime.datetime.today()):
                portfolioCountStocks -= 1
                continue
            priceHistory = newStockData.history(period="max")
            if priceHistory.empty:
                portfolioCountStocks -= 1
                continue
            priceHistoryOneWkInterval = newStockData.history(
                period="max", interval="1wk"
            )
            priceHistory.sort_values("Date").to_sql(
                updateWidget.tickerSymbol.text().replace("-", "").replace(".", ""),
                self.CurrentSessionConn,
                if_exists="replace",
                dtype={"Date": "DATETIME"},
            )
            priceHistoryOneWkInterval.sort_values("Date").to_sql(
                f"{updateWidget.tickerSymbol.text().replace("-", "").replace(".", "")}OneWk",
                self.CurrentSessionConn,
                if_exists="replace",
                dtype={"Date": "DATETIME"},
            )
            with open(
                f"financialModeller\\SessionData\\{self.CurrentSessionName}\\{self.CurrentSessionName}-{updateWidget.tickerSymbol.text().replace("-", "").replace(".", "")}.pkl",
                "wb",
            ) as f:
                pickle.dump(newStockData.info, f)
            # print(updateWidget.tickerPrice)
            updateWidget.clicked.signal.connect(
                partial(
                    self.portfolioTickerClick,
                    updateWidget.tickerSymbol.text(),
                    newStockData.info,
                    updateWidget,
                )
            )
            updateWidget.updatePrice(priceHistory["Close"].iloc[-1])
            DCAPrice = pd.read_sql(
                f"SELECT * FROM PORTFOLIODATA WHERE stock = ?",
                self.portfolioConn,
                params=[(updateWidget.tickerSymbol.text())],
            )
            DCAPrice.reset_index(drop=True, inplace=True)
            DCAPrice = DCAPrice["DCAPrice"].loc[0]
            updateWidget.updateGainLoss(priceHistory, DCAPrice)
            updateWidget.update()
            # Update Chart Also
            # if (
            #    self.portfolioActiveChart
            #    and newStockData.ticker == self.portfolioActiveChart
            # ):
            #    self.portfolioModule.chartModule.updateStockData(
            #        priceHistory, newStockData.ticker
            #    )
            portfolioCountStocks -= 1

    def PortfolioModuleSwitch(
        self,
    ):  # Switches from Financial Module to portfolio Module
        self.central.setCurrentWidget(self.portfolioModule)

    def portfolioBreakUp(
        self,
    ):  # gathers the data and makes the pie chart for portfolio representation
        self.portfolioModule.infoModule.setParent(None)
        self.portfolioModule.chartModule.setParent(
            None
        )  # Updates the layout to remove the infoModule and chartModule, and instead add the portfolioOverview Module
        self.portfolioModule.layout.addWidget(
            self.portfolioModule.portfolioOverview, 0, 3, 5, 1
        )
        try:
            df = pd.read_sql("SELECT * FROM PORTFOLIODATA", self.portfolioConn)
        except:
            Error(
                "Please Add Stocks to portfolio before clicking on this button"
            ).exec()
            return
        self.portfolioModule.portfolioOverview.makePieChart(df)

    def portfolioTickerClick(
        self, stockName, stockData, widget
    ):  # opens the buySellModule,creates tickerInfo and charts for the ticker that is clicked
        self.activeWidget = widget
        self.portfolioActiveChart = stockName
        self.portfolioModule.layout.removeWidget(self.portfolioModule.transactionModule)
        self.portfolioModule.layout.addWidget(
            self.portfolioModule.buySellModule, 0, 2, 3, 1, Qt.AlignmentFlag.AlignLeft
        )
        self.portfolioModule.layout.addWidget(
            self.portfolioModule.transactionModule,
            3,
            2,
            2,
            1,
            Qt.AlignmentFlag.AlignLeft,
        )
        self.portfolioConnCur.execute(
            "SELECT QuantityLeft FROM PORTFOLIODATA WHERE stock = ?", (stockName,)
        )
        quantity = list(self.portfolioConnCur.fetchone())
        self.portfolioConnCur.execute(
            "SELECT DCAPrice FROM PORTFOLIODATA WHERE stock = ?", (stockName,)
        )
        averageBuyPrice = list(self.portfolioConnCur.fetchone())
        averageBuyPrice = str(round(float(averageBuyPrice[0]), 3))
        self.portfolioModule.buySellModule.updateStockName(stockName, self.activeWidget)
        self.portfolioModule.buySellModule.updateExistingShares(
            str(quantity[0]), averageBuyPrice
        )

        # Update Chart Module
        transactionDf = pd.read_sql(
            "SELECT * FROM TransactionHistory WHERE stock = ?",
            self.portfolioConn,
            params=(stockName,),
        )
        portfolioHoldingDf = pd.read_sql(
            "SELECT * FROM PORTFOLIODATA WHERE stock= ?",
            self.portfolioConn,
            params=(stockName,),
        )
        priceDf = pd.read_sql(
            f"SELECT * FROM {stockName.replace('-','').replace('.','')}",
            self.CurrentSessionConn,
        )
        # firstTransaction = (
        #    transactionDf["Price"].iloc[0] * transactionDf["Quantity"].iloc[0]
        # )
        # curValue = (
        #    priceDf["Close"].iloc[-1] * portfolioHoldingDf["QuantityLeft"].iloc[0]
        # )
        # Make dataframe for the same
        priceDf["Date"] = pd.to_datetime(priceDf["Date"], utc=True)
        self.portfolioModule.chartModule.updateStockData(priceDf, stockName)
        self.portfolioModule.chartModule.timeFrameButtons.constructLayout(
            priceDf["Date"].iloc[0].timestamp()
        )

        # Updates Info Module

        if self.portfolioModule.infoModule.stackSwitcher.layout.count() != 0:
            self.portfolioModule.infoModule.stackSwitcher.deleteButtons()
        self.portfolioModule.infoModule.MainInfoModule.deleteInfo()
        self.portfolioModule.infoModule.stackSwitcher.AddButtons()
        self.portfolioModule.infoModule.stackSwitcher.button1.clicked.connect(
            partial(self.switchStack, 1, "portfolio")
        )
        self.portfolioModule.infoModule.stackSwitcher.button2.clicked.connect(
            partial(self.switchStack, 2, "portfolio")
        )
        self.portfolioModule.infoModule.stackSwitcher.button3.clicked.connect(
            partial(self.switchStack, 3, "portfolio")
        )
        self.portfolioModule.infoModule.stackSwitcher.button4.clicked.connect(
            partial(self.switchStack, 4, "portfolio")
        )
        self.portfolioModule.infoModule.stackSwitcher.button5.clicked.connect(
            partial(self.switchStack, 5, "portfolio")
        )
        # self.portfolioModule.infoModule.stackSwitcher.button6.clicked.connect(
        #    partial(self.switchStack, 6, "portfolio")
        # )
        stockInfo = stockData
        self.createNewPortfolioData(stockInfo, stockName)

    def createNewPortfolioData(
        self, stockData, stockName
    ):  # Uses the pkl file to display the data about the stock in the PortfolioModule only in the infoModule
        if self.portfolioModule.infoModule.stackSwitcher.layout.count() != 0:
            self.portfolioModule.infoModule.stackSwitcher.deleteButtons()
        self.portfolioModule.infoModule.MainInfoModule.deleteInfo()
        self.portfolioModule.infoModule.stackSwitcher.AddButtons()
        self.portfolioModule.infoModule.stackSwitcher.button1.clicked.connect(
            partial(self.switchStack, 1, "portfolio")
        )
        self.portfolioModule.infoModule.stackSwitcher.button2.clicked.connect(
            partial(self.switchStack, 2, "portfolio")
        )
        self.portfolioModule.infoModule.stackSwitcher.button3.clicked.connect(
            partial(self.switchStack, 3, "portfolio")
        )
        self.portfolioModule.infoModule.stackSwitcher.button4.clicked.connect(
            partial(self.switchStack, 4, "portfolio")
        )
        self.portfolioModule.infoModule.stackSwitcher.button5.clicked.connect(
            partial(self.switchStack, 5, "portfolio")
        )
        # self.portfolioModule.infoModule.stackSwitcher.button6.clicked.connect(
        #    partial(self.switchStack, 6, "portfolio")
        # )

        # infoTab1
        stockInfo = stockData
        aboutLabel = QLabel("<Strong>About</Strong>")
        try:
            aboutStock = stockInfo["longBusinessSummary"]
        except:
            aboutStock = "NA"
        aboutStockLabel = QLabel(aboutStock)
        aboutLabel.setObjectName("About")
        aboutStockLabel.setObjectName("stockAbout")
        aboutStockLabel.setWordWrap(True)
        self.portfolioModule.infoModule.MainInfoModule.infoModule1.layout.addWidget(
            aboutLabel, 0, 0
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule1.layout.addWidget(
            aboutStockLabel, 1, 0
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule1.layout.setRowStretch(
            0, 1
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule1.layout.setRowStretch(
            1, 3
        )

        # Update the layout to show the info and chart Module
        if self.portfolioModule.portfolioOverview.parent():
            self.portfolioModule.portfolioOverview.setParent(None)
            self.portfolioModule.layout.addWidget(
                self.portfolioModule.infoModule, 3, 3, 2, 1
            )
            self.portfolioModule.layout.addWidget(
                self.portfolioModule.chartModule, 0, 3, 3, 1
            )

        # infoTab2
        try:
            stockWebsite = QLabel(f"Website:   {stockInfo["website"]}")
        except:
            stockWebsite = QLabel("Website:   NA")
        try:
            stockIndustry = QLabel(f"Industry:   {stockInfo["industry"]}")
        except:
            stockIndustry = QLabel("Industry:   NA")
        try:
            stockSector = QLabel(f"Sector:   {stockInfo["sector"]}")
        except:
            stockSector = QLabel("Sector:   NA")
        try:
            stockFullTimeEmployees = QLabel(
                f"Full Time Employees:   {stockInfo["fullTimeEmployees"]}"
            )
        except:
            stockFullTimeEmployees = QLabel("Full Time Employees:   NA")
        try:
            stockType = QLabel(f"Stock Type:   {stockInfo["quoteType"]}")
        except:
            stockType = QLabel("Stock Type:   NA")
        try:
            stockCurrency = QLabel(
                f"Financial Currency:   {stockInfo["financialCurrency"]}"
            )
        except:
            stockCurrency = QLabel("Financial Currency:   NA")
        try:
            stockEnterpriseValue = QLabel(
                f"Enterprise Value:   {stockInfo["enterpriseValue"]}"
            )
        except:
            stockEnterpriseValue = QLabel("Enterprise Value:   NA")
        self.portfolioModule.infoModule.MainInfoModule.infoModule2.layout.addWidget(
            stockWebsite, 0, 0
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule2.layout.addWidget(
            stockIndustry, 0, 1
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule2.layout.addWidget(
            stockSector, 0, 2
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule2.layout.addWidget(
            stockFullTimeEmployees, 0, 3
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule2.layout.addWidget(
            stockType, 1, 0
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule2.layout.addWidget(
            stockCurrency, 1, 1
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule2.layout.addWidget(
            stockEnterpriseValue, 1, 2
        )
        # infoTab3
        MetricLabel = QLabel("<strong>Metrics/Ratios</strong>")
        MetricLabel.setObjectName("MetricLabel")
        try:
            prevClose = QLabel(f"Previous Close:   {stockInfo['previousClose']}")
        except:
            prevClose = QLabel(f"Previous Close:   NA")
        try:
            Open = QLabel(f"Open:   {stockInfo['open']}")
        except:
            Open = QLabel(f"Open:   NA")
        try:
            DaysRange = QLabel(
                f"Days Range:   {stockInfo['dayLow']} - {stockInfo['dayHigh']}"
            )
        except:
            DaysRange = QLabel(f"Days Range:   NA")
        try:
            YearRange = QLabel(
                f"Year Range:   {stockInfo['fiftyTwoWeekLow']} - {stockInfo['fiftyTwoWeekHigh']}"
            )
        except:
            YearRange = QLabel(f"Year Range:   NA")
        try:
            Volume = QLabel(f"Volume:   {stockInfo['volume']}")
        except:
            Volume = QLabel(f"Volume:   NA")
        try:
            AvgVolume = QLabel(f"Avg. Volume:   {stockInfo['averageVolume']}")
        except:
            AvgVolume = QLabel(f"Avg. Volume:   NA")
        try:
            marketCap = QLabel(f"Market Cap:   {stockInfo['marketCap']}")
        except:
            marketCap = QLabel(f"Market Cap:   NA")
        try:
            Beta = QLabel(f"Beta(5Y Monthly):   {stockInfo['beta']}")
        except:
            Beta = QLabel(f"Beta(5Y Monthly):   NA")
        try:
            pe = QLabel(f"PE Ratio(TTM):   {stockInfo['trailingPE']}")
        except:
            pe = QLabel(f"PE Ratio(TTM):   NA")
        try:
            eps = QLabel(f"EPS(TTM):   {stockInfo['trailingEps']}")
        except:
            eps = QLabel(f"EPS(TTM):   NA")
        try:
            Est = QLabel(
                f"1Y Target Est(Mean Target Price):   {stockInfo['targetMeanPrice']}"
            )
        except:
            Est = QLabel(f"1Y Target Est(Mean Target Price):   NA")
        self.portfolioModule.infoModule.MainInfoModule.infoModule3.layout.addWidget(
            MetricLabel, 0, 0
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule3.layout.addWidget(
            prevClose, 1, 0
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule3.layout.addWidget(
            Open, 1, 1
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule3.layout.addWidget(
            DaysRange, 1, 2
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule3.layout.addWidget(
            YearRange, 1, 3
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule3.layout.addWidget(
            Volume, 2, 0
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule3.layout.addWidget(
            AvgVolume, 2, 1
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule3.layout.addWidget(
            marketCap, 2, 2
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule3.layout.addWidget(
            Beta, 2, 3
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule3.layout.addWidget(
            pe, 3, 0
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule3.layout.addWidget(
            eps, 3, 1
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule3.layout.addWidget(
            Est, 3, 2
        )
        # infoTab4
        misc = QLabel("<strong>Miscellaneous</strong>")
        misc.setObjectName("Misc")
        try:
            profitMargins = QLabel(f"Profit Margins:   {stockInfo['profitMargins']}")
        except:
            profitMargins = QLabel(f"Profit Margins:   NA")
        try:
            ReturnOnAssets = QLabel(
                f"Return on Assets:   {stockInfo['returnOnAssets']}"
            )
        except:
            ReturnOnAssets = QLabel(f"Return on Assets:   NA")
        try:
            ReturnOnEquity = QLabel(
                f"Return on Equity:   {stockInfo['returnOnEquity']}"
            )
        except:
            ReturnOnEquity = QLabel(f"Return on Equity:   NA")
        try:
            CurrentRatio = QLabel(f"Current Ratio:   {stockInfo['currentRatio']}")
        except:
            CurrentRatio = QLabel(f"Current Ratio:   NA")
        try:
            QuickRatio = QLabel(f"Quick Ratio:   {stockInfo['quickRatio']}")
        except:
            QuickRatio = QLabel(f"Quick Ratio:   NA")
        try:
            PriceToBook = QLabel(f"Price To Book:   {stockInfo['priceToBook']}")
        except:
            PriceToBook = QLabel(f"Price To Book:   NA")
        try:
            DebtToEquity = QLabel(f"Debt To Equity:   {stockInfo['debtToEquity']}")
        except:
            DebtToEquity = QLabel(f"Debt To Equity:   NA")
        try:
            earningQuaterlyGrowth = QLabel(
                f"Earnings Quaterly Growth:   {stockInfo['earningsQuaterlyGrowth']}"
            )
        except:
            earningQuaterlyGrowth = QLabel(f"Earnings Quaterly Growth:   NA")
        try:
            AnalystOpinion = QLabel(
                f"Analyst Opinion:   {stockInfo['recommendationKey'].replace('_',' ').replace('-',' ').upper()}"
            )
        except:
            AnalystOpinion = QLabel(f"Analyst Opinion:   NA")
        self.portfolioModule.infoModule.MainInfoModule.infoModule4.layout.addWidget(
            misc, 0, 0
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule4.layout.addWidget(
            profitMargins, 1, 0
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule4.layout.addWidget(
            ReturnOnAssets, 1, 1
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule4.layout.addWidget(
            ReturnOnEquity, 1, 2
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule4.layout.addWidget(
            CurrentRatio, 2, 0
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule4.layout.addWidget(
            QuickRatio, 2, 1
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule4.layout.addWidget(
            PriceToBook, 2, 2
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule4.layout.addWidget(
            DebtToEquity, 3, 0
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule4.layout.addWidget(
            earningQuaterlyGrowth, 3, 1
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule4.layout.addWidget(
            AnalystOpinion, 3, 2
        )
        # infoTab5
        weekOldPrice = pd.read_sql(
            f"SELECT * FROM {stockName.replace('-','').replace('.','')}",
            self.CurrentSessionConn,
        )
        weekOldPrice["Date"] = pd.to_datetime(weekOldPrice["Date"], utc=True)
        oldestPrice = weekOldPrice.iloc[0]
        curPrice = weekOldPrice.iloc[-1]
        monthOldPrice = weekOldPrice
        halfYearOldPrice = weekOldPrice
        yearOldPrice = weekOldPrice
        if (
            len(weekOldPrice)
            == len(
                weekOldPrice.loc[
                    weekOldPrice["Date"]
                    > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                    - relativedelta(days=8)
                ]
            )
            or len(
                weekOldPrice.loc[
                    weekOldPrice["Date"]
                    > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                    - relativedelta(days=8)
                ]
            )
            == 0
        ):
            weekGain = "NA"
        else:
            weekOldPrice = weekOldPrice.loc[
                weekOldPrice["Date"]
                > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                - relativedelta(days=8)
            ]
            weekOldPrice.reset_index(inplace=True, drop=True)
            # print(weekOldPrice)
            weekOldPrice = weekOldPrice.iloc[0]
            weekGain = round(
                ((curPrice["Close"] - weekOldPrice["Close"]) / weekOldPrice["Close"])
                * 100,
                3,
            )
        if (
            len(monthOldPrice)
            == len(
                monthOldPrice.loc[
                    monthOldPrice["Date"]
                    > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                    - relativedelta(days=32)
                ]
            )
            or len(
                monthOldPrice.loc[
                    monthOldPrice["Date"]
                    > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                    - relativedelta(days=32)
                ]
            )
            == 0
        ):
            monthGain = "NA"
        else:
            monthOldPrice = monthOldPrice.loc[
                monthOldPrice["Date"]
                > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                - relativedelta(days=32)
            ]
            monthOldPrice.reset_index(inplace=True, drop=True)
            monthOldPrice = monthOldPrice.iloc[0]
            monthGain = round(
                ((curPrice["Close"] - monthOldPrice["Close"]) / monthOldPrice["Close"])
                * 100,
                3,
            )
        if (
            len(halfYearOldPrice)
            == len(
                halfYearOldPrice.loc[
                    halfYearOldPrice["Date"]
                    > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                    - relativedelta(days=182)
                ]
            )
            or len(
                halfYearOldPrice.loc[
                    halfYearOldPrice["Date"]
                    > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                    - relativedelta(days=182)
                ]
            )
            == 0
        ):
            halfYearGain = "NA"
        else:
            halfYearOldPrice = halfYearOldPrice.loc[
                halfYearOldPrice["Date"]
                > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                - relativedelta(days=182)
            ]
            halfYearOldPrice.reset_index(inplace=True, drop=True)
            halfYearOldPrice = halfYearOldPrice.iloc[0]
            halfYearGain = round(
                (
                    (curPrice["Close"] - halfYearOldPrice["Close"])
                    / halfYearOldPrice["Close"]
                )
                * 100,
                3,
            )
        if (
            len(yearOldPrice)
            == len(
                yearOldPrice.loc[
                    yearOldPrice["Date"]
                    > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                    - relativedelta(years=1)
                ]
            )
            or len(
                yearOldPrice.loc[
                    yearOldPrice["Date"]
                    > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                    - relativedelta(years=1)
                ]
            )
            == 0
        ):
            yearGain = "NA"
        else:
            yearOldPrice = yearOldPrice.loc[
                yearOldPrice["Date"]
                > pd.Timestamp(datetime.datetime.now(), tz="UTC")
                - relativedelta(years=1)
            ]
            yearOldPrice.reset_index(inplace=True, drop=True)
            yearOldPrice = yearOldPrice.iloc[0]
            yearGain = round(
                ((curPrice["Close"] - yearOldPrice["Close"]) / yearOldPrice["Close"])
                * 100,
                3,
            )
        lifetimeGain = round(
            ((curPrice["Close"] - oldestPrice["Close"]) / oldestPrice["Close"]) * 100,
            3,
        )

        tabLabel = QLabel("<strong>Performance</strong>")
        tabLabel.setObjectName("Performance")
        weekGainLabel = QLabel(f"1 Week Gain:   {str(weekGain)}%")
        monthGainLabel = QLabel(f"1 Month Gain:   {str(monthGain)}%")
        halfYearGainLabel = QLabel(f"6 Month Gain:   {str(halfYearGain)}%")
        yearGainLabel = QLabel(f"1 Year Gain:   {str(yearGain)}%")
        lifetimeGainLabel = QLabel(f"Gain since Inception:   {str(lifetimeGain)}%")
        self.portfolioModule.infoModule.MainInfoModule.infoModule5.layout.addWidget(
            tabLabel, 0, 0
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule5.layout.addWidget(
            weekGainLabel, 1, 0
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule5.layout.addWidget(
            monthGainLabel, 1, 1
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule5.layout.addWidget(
            halfYearGainLabel, 1, 2
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule5.layout.addWidget(
            yearGainLabel, 2, 0
        )
        self.portfolioModule.infoModule.MainInfoModule.infoModule5.layout.addWidget(
            lifetimeGainLabel, 2, 1
        )

    def BuySellTransaction(self):  # Handles what happens on a buy or a sell
        stockBoughtOrSold = self.portfolioModule.buySellModule.stockNameLabel.text()
        try:
            quantityPurchasedOrSold = float(
                self.portfolioModule.buySellModule.QuantityEntry.text()
            )
        except:
            dialog = Error("Invalid Input")
            dialog.exec()
            return
        boughtOrSold = "Buy"
        date = datetime.datetime.strptime(
            self.portfolioModule.buySellModule.DateEntry.text(), "%d/%m/%Y"
        )
        try:
            price = float(self.portfolioModule.buySellModule.PriceEntry.text())
        except:
            dialog = Error("Invalid Input")
            dialog.exec()
            return
        self.portfolioConnCur.execute(
            "SELECT DCAPrice,QuantityLeft FROM PORTFOLIODATA WHERE stock = ?",
            (stockBoughtOrSold,),
        )
        previousBuyPriceAndQuantity = list(self.portfolioConnCur.fetchone())
        profitOrLoss = numpy.nan
        profitOrLossPercent = numpy.nan
        if self.portfolioModule.buySellModule.buyOrSell:  # If a buy transaction
            averagedBuyPrice = (
                (previousBuyPriceAndQuantity[0] * previousBuyPriceAndQuantity[1])
                + (price * quantityPurchasedOrSold)
            ) / (previousBuyPriceAndQuantity[1] + quantityPurchasedOrSold)
            newStockCount = previousBuyPriceAndQuantity[1] + quantityPurchasedOrSold
        else:  # If a sell transaction
            averagedBuyPrice = previousBuyPriceAndQuantity[0]
            newStockCount = previousBuyPriceAndQuantity[1] - quantityPurchasedOrSold
            if newStockCount < 0:
                errorMsg = Error("Insufficient Shares to proceed with the transaction")
                errorMsg.exec()
                return
            if (
                newStockCount == 0
            ):  # if a stock is completely sold out from the portfolio, proceeds to delete the ticker
                self.portfolioModule.buySellModule.currentClickedWidget.deleteTicker(
                    self.portfolioConn, self.portfolioConnCur
                )
                try:
                    stocksInScreener: list = pickle.load(
                        open(
                            f"financialModeller\\SessionData\\{self.CurrentSessionName}\\stocksInScreener.pkl",
                            "rb",
                        )
                    )
                except:
                    stocksInScreener = []
                if (
                    not self.portfolioModule.buySellModule.currentClickedWidget.tickerSymbol.text()
                    .replace("-", "")
                    .replace("-", "")
                    in stocksInScreener
                ):  # If the stock that is deleted only exists in the portfolio and not in the screener, then deletes all data about the stock
                    self.CurrentSessionConn.execute(
                        f"DROP TABLE {self.portfolioModule.buySellModule.currentClickedWidget.tickerSymbol.text().replace('-','').replace('.','')}"
                    )
                    self.CurrentSessionConn.execute(
                        f"DROP TABLE {self.portfolioModule.buySellModule.currentClickedWidget.tickerSymbol.text().replace('-','').replace('.','')}OneWk"
                    )
                    os.remove(
                        f"financialModeller\\SessionData\\{self.CurrentSessionName}\\{self.CurrentSessionName}-{self.portfolioModule.buySellModule.currentClickedWidget.tickerSymbol.text().replace('-','').replace('.','')}.pkl"
                    )
                nextTicker = (
                    self.portfolioModule.stocksInPortfolioList.tickerList.stockList.layout.count()
                    - 2
                )  # Uses this to display info about the next stock in the portfolio
                if (
                    nextTicker < 0
                ):  # if no next stock, it makes everything a blank slate
                    self.portfolioModule.chartModule.DeleteChart()
                    self.portfolioModule.buySellModule.setParent(None)
                    self.portfolioModule.transactionModule.setParent(None)
                    self.portfolioModule.layout.addWidget(
                        self.portfolioModule.transactionModule, 0, 2, 5, 1
                    )
                    self.portfolioModule.infoModule.MainInfoModule.deleteInfo()
                    self.portfolioModule.infoModule.stackSwitcher.deleteButtons()
                else:
                    nextTickerWidget = self.portfolioModule.stocksInPortfolioList.tickerList.stockList.layout.itemAt(
                        nextTicker
                    ).widget()
                    nextTicker = (
                        nextTickerWidget.tickerSymbol.text()
                        .replace("-", "")
                        .replace(".", "")
                    )
                    stockDataDf = pd.read_sql(
                        f"SELECT * FROM {nextTicker}", self.CurrentSessionConn
                    )
                    stockDataDf["Date"] = pd.to_datetime(stockDataDf["Date"], utc=True)
                    self.portfolioModule.chartModule.updateStockData(
                        stockData=stockDataDf, tickerName=nextTicker
                    )
                    self.createNewPortfolioData(
                        pickle.load(
                            open(
                                f"financialModeller\\SessionData\\{self.CurrentSessionName}\\{self.CurrentSessionName}-{nextTicker}.pkl",
                                "rb",
                            )
                        ),
                        nextTicker,
                    )
                    self.portfolioModule.buySellModule.updateStockName(
                        nextTicker, nextTickerWidget
                    )
                    nextTickerDf = pd.read_sql(
                        "SELECT * FROM PORTFOLIODATA WHERE stock = ?",
                        self.portfolioConn,
                        params=[(nextTicker)],
                    )
                    nextTickerDf.reset_index(drop=True, inplace=True)
                    self.portfolioModule.buySellModule.updateExistingShares(
                        str(nextTickerDf["QuantityLeft"].loc[0]),
                        str(nextTickerDf["DCAPrice"].loc[0]),
                    )
                # delete that ticker
            boughtOrSold = "Sell"
            profitOrLoss = round(price - averagedBuyPrice, 3)
            profitOrLossPercent = round((profitOrLoss / averagedBuyPrice) * 100, 3)
        averagedBuyPrice = round(averagedBuyPrice, 3)
        self.portfolioConnCur.execute(
            "update PORTFOLIODATA SET DCAPrice = ?, QuantityLeft = ? WHERE stock = ?",
            (
                averagedBuyPrice,
                newStockCount,
                stockBoughtOrSold,
            ),
        )  # deletes the entry for that stock in PORTFOLIODATA if QuantityLeft == 0,otherwise just updates it
        self.portfolioConn.commit()
        # print(averagedBuyPrice)
        if newStockCount != 0:
            self.portfolioModule.buySellModule.updateExistingShares(
                str(newStockCount), averagedBuyPrice
            )
        transaction = pd.DataFrame(
            columns=[
                "stock",
                "Date",
                "BoughtOrSold",
                "Price",
                "Quantity",
                "ProfitOrLoss",
                "ProfitOrLossPercent",
            ]
        )
        TransactionList = [
            stockBoughtOrSold,
            date,
            boughtOrSold,
            price,
            quantityPurchasedOrSold,
            profitOrLoss,
            profitOrLossPercent,
        ]  # Makes a new transaction Entry and appends it to the already existing TransactionHistory Table
        transaction.loc[-1] = TransactionList
        transaction.to_sql(
            "TransactionHistory", self.portfolioConn, if_exists="append", index=False
        )
        transactionItem = Transaction(
            stockBoughtOrSold,
            boughtOrSold,
            price,
            quantityPurchasedOrSold,
            profitOrLoss,
            profitOrLossPercent,
        )  # Makes a new Transaction Object and inserts it into the Layout
        self.portfolioModule.transactionModule.transactionList.layout.insertWidget(
            0, transactionItem
        )
        stocksInPortfolio = (
            self.portfolioModule.stocksInPortfolioList.tickerList.stockList.layout.count()
            - 2
        )
        while stocksInPortfolio >= 0:
            tickerobj = self.portfolioModule.stocksInPortfolioList.tickerList.stockList.layout.itemAt(
                stocksInPortfolio
            ).widget()
            if tickerobj.tickerSymbol.text() == stockBoughtOrSold:
                priceHistory = pd.read_sql(
                    f"SELECT * FROM {stockBoughtOrSold.replace('-','').replace('.','')}",
                    self.CurrentSessionConn,
                )
                DCAPrice = pd.read_sql(
                    f"SELECT * FROM PORTFOLIODATA WHERE stock = ?",
                    self.portfolioConn,
                    params=[(stockBoughtOrSold)],
                )
                DCAPrice.reset_index(drop=True, inplace=True)
                DCAPrice = DCAPrice["DCAPrice"].loc[0]
                tickerobj.updateHolding(newStockCount)
                tickerobj.updateGainLoss(priceHistory, DCAPrice)
            stocksInPortfolio -= 1  # Updates Gain/Loss and holding for the stock that is bought or sold, kinda wasteful to use a loop, couldve just saved a reference for the widget before hand, but maybe ill implement that later
        df = pd.read_sql("SELECT * FROM PORTFOLIODATA", self.portfolioConn)
        df2 = pd.read_sql("SELECT * FROM TransactionHistory", self.portfolioConn)
        self.portfolioModule.portfolioOverview.makePieChart(df)
        self.portfolioModule.portfolioOverview.portfolioPerformanceWidget.updatePortfolioPerformance(
            df, df2, self.CurrentSessionConn
        )

    def ImportPortfolioStockData(
        self,
    ):  # Same as ImportStockData, but also makes a transaction Entry
        stockName = self.portfolioModule.stocksInPortfolioList.dialog.StockName.text()
        buyDate = self.portfolioModule.stocksInPortfolioList.dialog.BuyDate.text()
        try:
            buyPrice = float(
                self.portfolioModule.stocksInPortfolioList.dialog.BuyPrice.text()
            )
        except:
            dialog = Error("Either Stock already exists or no input was given")
            dialog.exec()
            return
        try:
            buyQuantity = float(
                self.portfolioModule.stocksInPortfolioList.dialog.Quantity.text()
            )
        except:
            dialog = Error("Either Stock already exists or no input was given")
            dialog.exec()
            return
        if not stockName:
            return
        children = (
            self.portfolioModule.stocksInPortfolioList.tickerList.stockList.layout.count()
        ) - 2
        stocksExisting = []
        while children >= 0:
            stocksExisting.append(
                self.portfolioModule.stocksInPortfolioList.tickerList.stockList.layout.itemAt(
                    children
                )
                .widget()
                .tickerSymbol.text()
            )
            children -= 1
        noSpecialCharName = stockName.replace(".", "").replace("-", "")
        if stockName in stocksExisting:
            dialog = Error("Either Stock already exists or no input was given")
            dialog.exec()
            return
        stocksInScreener = open(
            f"financialModeller\\SessionData\\{self.CurrentSessionName}\\stocksInScreener.pkl",
            "rb",
        )
        try:
            stocksInScreener = pickle.load(stocksInScreener)
        except:
            stocksInScreener = []
        try:
            stockData = yf.Ticker(stockName)
        except:
            return
        if noSpecialCharName not in stocksInScreener:
            pickleFile = open(
                f"financialModeller\\SessionData\\{self.CurrentSessionName}\\{self.CurrentSessionName}-{noSpecialCharName}.pkl",
                "wb",
            )
            pickle.dump(stockData.info, pickleFile)
            # else: had made a distinction before for memory saving i guess, where it only saves 1wk data if stock already exists in the screener, but i need that one wk data anyways
            priceHistoryWk = stockData.history(period="max", interval="1wk")
            priceHistoryWk.sort_values("Date").to_sql(
                f"{noSpecialCharName}OneWk",
                self.CurrentSessionConn,
                if_exists="replace",
                dtype={"Date": "DATETIME"},
            )
        priceHistory = stockData.history(period="max", interval="1d")
        priceHistory.sort_values("Date").to_sql(
            f"{noSpecialCharName}",
            self.CurrentSessionConn,
            if_exists="replace",
            dtype={"Date": "DATETIME"},
        )
        newTicker = PortfolioTicker(
            tickerSymbol=stockName,
            tickerPrice=str(
                round(priceHistory["Close"].iloc[len(priceHistory) - 1], 5)
            ),
            stockData=stockData.info,
            uneditedTickerSymbol=stockName,
            buyPrice=self.portfolioModule.stocksInPortfolioList.dialog.BuyPrice.text(),
            priceHistory=priceHistory,
            holding=str(buyQuantity),
        )
        newTicker.clicked.signal.connect(
            partial(self.portfolioTickerClick, stockName, stockData.info, newTicker)
        )
        self.portfolioModule.stocksInPortfolioList.tickerList.stockList.layout.insertWidget(
            0, newTicker
        )
        portfoliostocksAdded = pd.DataFrame(
            columns=[
                "stock",
                "BuyDate",
                "DCAPrice",
                "QuantityLeft",
            ]
        )
        valueList = [
            stockName,
            datetime.datetime.strptime(buyDate, "%d-%m-%Y"),
            float(buyPrice),
            float(buyQuantity),
        ]
        transaction = pd.DataFrame(
            columns=[
                "stock",
                "Date",
                "BoughtOrSold",
                "Price",
                "Quantity",
                "ProfitOrLoss",
                "ProfitOrLossPercent",
            ]
        )
        transactionList = [
            stockName,
            datetime.datetime.strptime(buyDate, "%d-%m-%Y"),
            "Buy",
            float(buyPrice),
            float(buyQuantity),
            numpy.nan,
            numpy.nan,
        ]
        # print(valueList)
        portfoliostocksAdded.loc[-1] = valueList
        transaction.loc[-1] = transactionList
        portfoliostocksAdded.to_sql(
            "PORTFOLIODATA", self.portfolioConn, if_exists="append", index=False
        )
        transaction.to_sql(
            "TransactionHistory", self.portfolioConn, if_exists="append", index=False
        )
        transactionItem = Transaction(
            stockName, "Buy", str(buyPrice), str(buyQuantity), numpy.nan, numpy.nan
        )
        self.portfolioModule.transactionModule.transactionList.layout.insertWidget(
            0, transactionItem
        )
        df = pd.read_sql("SELECT * FROM PORTFOLIODATA", self.portfolioConn)
        df2 = pd.read_sql("SELECT * FROM TransactionHistory", self.portfolioConn)
        self.portfolioModule.portfolioOverview.makePieChart(df)
        self.portfolioModule.portfolioOverview.portfolioPerformanceWidget.updatePortfolioPerformance(
            df, df2, self.CurrentSessionConn
        )


app = QApplication()
window = MainWindow()
window.show()
with open("financialModeller\\styleSheet.qss") as f:
    _style = f.read()
    app.setStyleSheet(_style)
app.exec()
