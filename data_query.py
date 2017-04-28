import pandas as pd
import numpy as np
import matplotlib.pylab as plt


class Stock:
    def __init__(self, ticker_, day0_, class_, est_EPS_, act_EPS_, ref):
        self.ticker = ticker_
        self.day0 = day0_
        self.stock_class = class_
        self.est_EPS = est_EPS_
        self.act_EPS = act_EPS_
        self.data = self.get_data()
        self.calculate_aar(ref)

    def url(self, before):
        year = int(self.day0[0:4])
        month = str(int(self.day0[5:7]) - 1)
        day = self.day0[8:10]
        if before == 1:
            return "https://ichart.yahoo.com/table.csv?s=" + self.ticker + "&a=" + month + \
                   "&b=" + day + "&c=" + str(year - 1) + "&d=" + month + "&e=" + day + "&f=" + \
                   str(year) + "&g=d&ignore=.csv"
        return "https://ichart.yahoo.com/table.csv?s=" + self.ticker + "&a=" + month + \
               "&b=" + day + "&c=" + str(year) + "&d=" + month + "&e=" + day + "&f=" + \
               str(year + 1) + "&g=d&ignore=.csv"

    def get_data(self):
        df0 = pd.read_csv(self.url(1), nrows=32)
        df0["Date"] = pd.to_datetime(df0["Date"], format="%Y-%m-%d")
        df0 = df0[["Date", "Adj Close"]]
        df0 = df0.sort_values("Date")
        df1 = pd.read_csv(self.url(0))
        df1["Date"] = pd.to_datetime(df1["Date"], format="%Y-%m-%d")
        df1 = df1[["Date", "Adj Close"]]
        df1 = df1.sort_values("Date").head(61)
        df = pd.concat([df0, df1])
        df = df.drop_duplicates().tail(92)
        df["return"] = df["Adj Close"].diff() / df["Adj Close"]
        df = df[["Date", "return"]]
        df = df.drop_duplicates().dropna()
        df = df.reset_index(drop=True)
        return df

    def calculate_aar(self, ref):
        self.data = self.data.merge(ref.data, how='left', on='Date', suffixes=('_stock', '_index'), copy=False)
        self.data["aar"] = self.data["return_stock"] - self.data["return_index"]

    def return_plot(self):
        self.data["Cum_Stock"] = self.data.return_stock.cumsum()
        self.data["Cum_Index"] = self.data.return_index.cumsum()
        plt.style.use("ggplot")
        plt.figure()
        self.data[["Cum_Stock", "Cum_Index"]].plot()
        plt.xlabel("Day#")
        plt.ylabel("Cum_return")
        plt.title(self.ticker)
        plt.savefig("./static/%s.png" % self.ticker)
        plt.close()


class SNP:
    def __init__(self):
        url = "https://ichart.yahoo.com/table.csv?s=%5Egspc&a=0&b=1&c=2015&d=3&e=1&f=2017&g=d&ignore=.csv"
        df = pd.read_csv(url)
        df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
        df = df.sort_values("Date")
        df = df[["Date", "Adj Close"]]
        df["return"] = df["Adj Close"].diff() / df["Adj Close"]
        df = df[["Date", "return"]]
        self.data = df


class Group:
    def __init__(self, class_):
        self.stock_class = class_
        self.member = list()
        self.data = pd.DataFrame(0, index=np.arange(91), columns=["aar", "caar"], dtype=float)

    def add_member(self, a):
        self.member.append(a)

    def calculation(self):
        self.data = pd.DataFrame(0, index=np.arange(91), columns=["aar", "caar"], dtype=float)
        for i in self.member:
            self.data["aar"] += i.data["aar"]
        self.data["aar"] /= len(self.member)
        self.data["caar"] = self.data["aar"].cumsum()

    def get_stocklist(self):
        temp = list()
        for i in self.member:
            temp.append(i.ticker)
        return " ,".join(temp)


