from data_query import *


def initialization():
    stock_list = pd.read_csv('data.csv', header=None)
    stock_list.columns = [["Ticker", 'Day0', '_Class', 'Est_EPS', 'Act_EPS']]

    stock_dict = dict()
    sp = SNP()
    for ind, row in stock_list.iterrows():
        print(str(ind + 1) + "\t" + row["Ticker"])
        stock_dict[row["Ticker"]] = (
            Stock(row["Ticker"], row["Day0"], row["_Class"], row["Est_EPS"], row["Act_EPS"], sp))

    miss = Group("Miss")
    meet = Group("Meet")
    beat = Group("Beat")
    for key, value in stock_dict.items():
        if value.stock_class == "Miss":
            miss.add_member(value)
        elif value.stock_class == "Meet":
            meet.add_member(value)
        else:
            beat.add_member(value)

    for i in [miss, meet, beat]:
        i.calculation()

    # result = pd.concat([miss.data.caar, meet.data.caar, beat.data.caar], axis=1)
    # result.columns = ["Miss", "Meet", "Beat"]
    group_dict = dict()
    group_dict["Miss"] = miss
    group_dict["Meet"] = meet
    group_dict["Beat"] = beat

    return stock_dict, group_dict
