# -*- coding: utf-8 -*-
import imaplib
import typing
import datetime
import pandas
import os
import numpy
import chardet
import email.parser
import email.header

from ZYYA_Codes.Balance_Sheet import read_balance_sheet
from ZYYA_Codes.utils import get_fridays, get_configs, decode_str
from ZYYA_Codes.utils.pyecharts_plot import *
from ZYYA_Codes.utils import Mongo_Client

__all__ = ["balance_sheet_analysis"]

Configs = get_configs()


class balance_sheet_analysis:
    sheets: typing.Dict[datetime.date, read_balance_sheet]

    def __init__(
            self,
            balance_sheets: typing.Union[
                typing.List[read_balance_sheet],
                typing.Dict[datetime.date, read_balance_sheet]
            ],
            **kwarg
    ):
        if isinstance(balance_sheets, list) and len(balance_sheets) > 0:
            self.sheets = {x.Date: x for x in balance_sheets}
        elif isinstance(balance_sheets, list) and len(balance_sheets) == 0:
            self.sheets = {}
        else:
            self.sheets = balance_sheets

        self.Holdings = self.__get_everyday_holding()
        self.Holdings_Costs = self.__get_everyday_cost().sort_index()
        self.Holdings_Scales = self.__get_everyday_scale().sort_index()
        self.Holdings_Amount = self.__get_everyday_amount().sort_index()
        self.__Fridays = list(set([
                                      min([y for y in self.sheets.keys() if y >= x]) for x in
                                      get_fridays(min(self.Holdings), max(self.Holdings))
                                  ] if len(self.Holdings) else []))
        self.__Fridays.sort()
        self.Transactions = self.__transactions(
            Transactions=pandas.read_excel(kwarg.get("Transactions")) if kwarg.get("Transactions") else None
        ) if len(self.Holdings) else None
        self.Short_Names = {
            x: self.__change_fund_name(x) for x in self.get_all_securities()
        } if len(self.Holdings) else None
        self.__Strategy_File_Route = kwarg.get("Strategy_File_Route", None)

    def get_cash(self):
        return pandas.Series({x: y.Cash for x, y in self.sheets.items()}).sort_index()

    def __strategies(self):
        List = [x for x in self.Short_Names]
        raise ValueError("请将下列产品策略补足：\n" + "\n".join(List))

    def __get_strategies(self):
        try:
            return pandas.read_excel(self.__Strategy_File_Route, index_col=0)["细分策略"].to_dict()
        except:
            raise FileNotFoundError("给定的文件不存在，请重新输入")

    def get_all_securities(self) -> list:
        List = set()
        for y in self.Holdings.values():
            List = List.union(set(y.index.tolist()))
        return list(List)

    @staticmethod
    def __change_fund_name(name: str):
        if name.__contains__("基金"):
            return name.replace(
                "私募基金", ""
            ).replace(
                "私募证券投资基金", ""
            ).replace(
                "私募证券基金", ""
            )
        else:
            return name

    def __get_everyday_holding(self) -> typing.Dict[datetime.date, pandas.DataFrame]:
        return {x: y.Properties for x, y in self.sheets.items()}

    def __get_everyday_cost(self) -> pandas.DataFrame:
        return pandas.DataFrame(
            {x: y["成本-本币"].to_dict() for x, y in self.Holdings.items()}
        ).T.fillna(0)

    def __get_everyday_amount(self) -> pandas.DataFrame:
        return pandas.DataFrame(
            {x: y["数量"].to_dict() for x, y in self.Holdings.items()}
        ).T.fillna(0)

    def __get_everyday_scale(self) -> pandas.DataFrame:
        return pandas.DataFrame(
            {x: y["市值-本币"].to_dict() for x, y in self.Holdings.items()}
        ).T.fillna(0)

    def __subscribes(self) -> pandas.DataFrame:
        change = self.Holdings_Costs.diff().dropna()
        return pandas.DataFrame(
            [[y, x, -change[y][x], "申购"] for x in change.index for y in change.columns if change[y][x] > 0],
            columns=["产品名称", "日期", "发生金额", "类型"]
        )

    def __redeems(self) -> pandas.DataFrame:
        Net_Value = self.Holdings_Scales / self.Holdings_Amount
        change = self.Holdings_Amount.sort_index(ascending=False).diff().dropna(how="all")
        change = change.where(change > 0).fillna(0)
        change *= Net_Value
        change = change.rename(index={x: min([y for y in Net_Value.index if y > x]) for x in change.index}).fillna(0)
        return pandas.DataFrame(
            [[y, x, change[y][x], "赎回"] for x in change.index for y in change.columns if change[y][x] > 0],
            columns=["产品名称", "日期", "发生金额", "类型"]
        )

    def __dividends(self) -> pandas.DataFrame:
        change = pandas.DataFrame({x: y.Dividends for x, y in self.sheets.items()}).fillna(0)
        dividends = pandas.DataFrame(
            [[x, y, change[y][x], "分红"] for x in change.index for y in change.columns if change[y][x] > 0],
            columns=["产品名称", "日期", "发生金额", "类型"]
        ).sort_values(by="日期").set_index("日期").drop_duplicates().reset_index(drop=False)
        return dividends

    def __transactions(self, **kwargs) -> pandas.DataFrame:
        result = pandas.concat(
            [self.__subscribes(), self.__dividends(), self.__redeems(), kwargs.get("Transactions", None)]
        )
        result["日期"] = [pandas.to_datetime(x).date() for x in result["日期"]]
        result["发生金额"] = result["发生金额"].round(2)
        result = result[
            (result["日期"] >= min(self.__Fridays)) & (result["日期"] <= max(self.__Fridays))
            ].sort_values(by="日期").drop_duplicates().reset_index(drop=True)
        return result

    @property
    def Net_Value(self) -> pandas.Series:
        return pandas.Series({x: y.Net_Value for x, y in self.sheets.items()}).sort_index()

    @property
    def Accumulated_Value(self) -> pandas.Series:
        return pandas.Series({x: y.Accumulated_Value for x, y in self.sheets.items()}).sort_index()

    @property
    def Adjusted_Value(self) -> pandas.Series:
        CNV = self.Accumulated_Value
        NV = self.Net_Value
        ANV = [1]
        for x, y in zip(NV.index[: -1], NV.index[1:]):
            ANV.append(ANV[-1] * ((CNV[y] - CNV[x]) / NV[x] + 1))
        return pandas.Series(ANV, index=NV.index).sort_index()

    @property
    def Pct_Change(self) -> pandas.Series:
        result = self.Adjusted_Value[self.__Fridays].sort_index().pct_change().fillna(0)
        result = pandas.DataFrame(result, columns=["周度涨跌幅"])
        return result["周度涨跌幅"].sort_index()

    @property
    def Net_Value_Set(self) -> pandas.DataFrame:
        return pandas.DataFrame(
            {"单位净值": self.Net_Value,
             "累计单位净值": self.Accumulated_Value,
             "复权净值（归一）": self.Adjusted_Value.round(4)}
        ).sort_index()

    @property
    def Scale(self) -> pandas.Series:
        return pandas.Series(
            {x: y.Scale for x, y in self.sheets.items()}
        ).sort_index()

    @property
    def Strategy_Scale(self) -> pandas.DataFrame:
        Strategy = pandas.Series(self.__get_strategies())
        Strategy = Strategy.groupby(Strategy).agg(lambda x: x.index)
        Scales: pandas.DataFrame = self.Holdings_Scales.loc[self.__Fridays]
        result = pandas.DataFrame(
            {x: Scales[Strategy[x]].T.sum().T for x in Strategy.index}
        )
        result["现金"] = result["货币基金"] + self.get_cash() if "货币基金" in result.columns else self.get_cash()
        result = result[[x for x in result.columns if x != "货币基金"]]
        return result.sort_index()

    @property
    def Strategy_Proportion(self) -> pandas.DataFrame:
        Scales = self.Strategy_Scale
        return (
                Scales.T / self.Scale
        )[self.__Fridays].sort_values(by=max(self.__Fridays)).T

    @property
    def Strategy_Profit(self) -> pandas.DataFrame:
        Strategy = pandas.Series(self.__get_strategies())
        Transactions = self.Transactions.copy()
        Transactions["细分策略"] = [Strategy[a] for a in Transactions["产品名称"]]
        Transactions = Transactions[Transactions["细分策略"] != "货币基金"]
        Product_Scale = self.Scale
        Scales: pandas.DataFrame = self.Strategy_Scale.copy()
        Profit = Scales.diff()
        Profit = Profit[[a for a in Profit.columns if a != "现金"]]
        for x, y, z in zip(Transactions["细分策略"], Transactions["日期"], Transactions["发生金额"]):
            Profit.loc[min([a for a in self.__Fridays if a >= y]), x] += z
        for date in Profit.index[1:]:
            Profit.loc[date] /= Product_Scale[max([a for a in self.__Fridays if a <= date])]
        Profit = Profit.fillna(0).replace({float("inf"): 0, float("-inf"): 0})
        Profit = Profit.T.sort_values(by=max(self.__Fridays), ascending=False).T
        return Profit

    @property
    def Strategy_Profit_Cumsum(self) -> pandas.DataFrame:
        Strategy = pandas.Series(self.__get_strategies())
        Transactions = self.Transactions.copy()
        Transactions["细分策略"] = [Strategy[a] for a in Transactions["产品名称"]]
        Transactions = Transactions[Transactions["细分策略"] != "货币基金"]
        Product_Scale = self.Scale
        Scales: pandas.DataFrame = self.Strategy_Scale.copy()
        Profit = Scales.diff()
        Profit = Profit[[a for a in Profit.columns if a != "现金"]]
        for x, y, z in zip(Transactions["细分策略"], Transactions["日期"], Transactions["发生金额"]):
            Profit.loc[min([a for a in self.__Fridays if a >= y]), x] += z
        for date in Profit.index[1:]:
            Profit.loc[date] /= Product_Scale[max([a for a in self.__Fridays if a <= date])]
        Profit = Profit.fillna(0).replace({float("inf"): 0, float("-inf"): 0}).cumsum()
        Profit = Profit.T.sort_values(by=max(self.__Fridays), ascending=False).T
        return Profit

    @property
    def Strategy_NV(self) -> pandas.DataFrame:
        Strategy = pandas.Series(self.__get_strategies())
        Transactions = self.Transactions.copy()
        Transactions["细分策略"] = [Strategy[a] for a in Transactions["产品名称"]]
        Transactions = Transactions[Transactions["细分策略"] != "货币基金"]
        Scales: pandas.DataFrame = self.Strategy_Scale.copy()
        Profit = Scales.diff()
        Profit = Profit[[a for a in Profit.columns if a != "现金"]]
        for x, y, z in zip(Transactions["细分策略"], Transactions["日期"], Transactions["发生金额"]):
            Profit.loc[min([a for a in self.__Fridays if a >= y]), x] += z
        for date in Profit.index[1:]:
            Profit.loc[date] /= Scales.loc[max([a for a in self.__Fridays if a <= date])]
        Profit = Profit.fillna(0).replace({float("inf"): 0, float("-inf"): 0})
        Profit: pandas.DataFrame = numpy.exp(numpy.log(Profit + 1).cumsum()).ffill()
        Profit = Profit.T.sort_values(by=max(self.__Fridays), ascending=False).T.round(4)
        return Profit

    @property
    def Fund_Proportion(self) -> pandas.DataFrame:
        return (
                self.Holdings_Scales.T / self.Scale
        ).sort_values(
            by=max([x for x in self.Holdings])
        ).T.loc[self.__Fridays]

    @property
    def Fund_Profit(self) -> pandas.DataFrame:
        Strategy = self.__get_strategies()
        Product_Scale = self.Scale
        Scales: pandas.DataFrame = self.Holdings_Scales.loc[self.__Fridays]
        Profit = Scales.diff()
        for x, y, z in zip(self.Transactions["产品名称"], self.Transactions["日期"], self.Transactions["发生金额"]):
            Profit.loc[min([a for a in self.__Fridays if a >= y]), x] += z
        Profit = Profit[[x for x in Profit.columns if Strategy.get(x) != "货币基金"]]
        for date in Profit.index[1:]:
            Profit.loc[date] /= Product_Scale[max([a for a in self.__Fridays if a <= date])]
        Profit = Profit.fillna(0).replace({float("inf"): 0, float("-inf"): 0})
        Profit = Profit.T.sort_values(by=max(self.__Fridays), ascending=False).T
        return Profit

    @property
    def Fund_Profit_Cumsum(self) -> pandas.DataFrame:
        Strategy = self.__get_strategies()
        Product_Scale = self.Scale
        Scales: pandas.DataFrame = self.Holdings_Scales.loc[self.__Fridays]
        Profit = Scales.diff()
        for x, y, z in zip(self.Transactions["产品名称"], self.Transactions["日期"], self.Transactions["发生金额"]):
            Profit.loc[min([a for a in self.__Fridays if a >= y]), x] += z
        Profit = Profit[[x for x in Profit.columns if Strategy.get(x) != "货币基金"]]
        for date in Profit.index[1:]:
            Profit.loc[date] /= Product_Scale[max([a for a in self.__Fridays if a <= date])]
        Profit = Profit.fillna(0).replace({float("inf"): 0, float("-inf"): 0}).cumsum()
        Profit = Profit.T.sort_values(by=max(self.__Fridays), ascending=False).T
        return Profit

    @property
    def Fund_NV(self) -> pandas.DataFrame:
        Strategy = self.__get_strategies()
        Scales: pandas.DataFrame = self.Holdings_Scales.loc[self.__Fridays]
        Profit = Scales.diff()
        for x, y, z in zip(self.Transactions["产品名称"], self.Transactions["日期"], self.Transactions["发生金额"]):
            Profit.loc[min([a for a in self.__Fridays if a >= y]), x] += z
        Profit = Profit[[x for x in Profit.columns if Strategy.get(x) != "货币基金"]]
        for date in Profit.index[1:]:
            Profit.loc[date] /= Scales.loc[max([a for a in self.__Fridays if a <= date])]
        Profit = Profit.fillna(0).replace({float("inf"): 0, float("-inf"): 0})
        Profit: pandas.DataFrame = numpy.exp(numpy.log(Profit + 1).cumsum()).ffill()
        Profit = Profit.T.sort_values(by=max(self.__Fridays), ascending=False).T.round(4)
        return Profit

    def Fund_Proportion_by_Strategy(self, strategy):
        Strategy = self.__get_strategies()
        return self.Fund_Proportion[
            [x for x, y in Strategy.items() if y == strategy]
        ].T.sort_values(by=max(self.__Fridays)).T

    def Fund_Profit_by_Strategy(self, strategy) -> pandas.DataFrame:
        Strategy = self.__get_strategies()
        return self.Fund_Profit[
            [x for x, y in Strategy.items() if y == strategy]
        ].T.sort_values(by=max(self.__Fridays), ascending=False).T

    def Fund_Profit_Cumsum_by_Strategy(self, strategy) -> pandas.DataFrame:
        Strategy = self.__get_strategies()
        return self.Fund_Profit_Cumsum[
            [x for x, y in Strategy.items() if y == strategy]
        ].T.sort_values(by=max(self.__Fridays), ascending=False).T

    def Fund_NV_by_Strategy(self, strategy) -> pandas.DataFrame:
        Strategy = self.__get_strategies()
        return self.Fund_NV[
            [x for x, y in Strategy.items() if y == strategy]
        ].T.sort_values(by=max(self.__Fridays), ascending=False).T

    @property
    def __Pct_Change_Plot(self) -> line_plot:
        return line_plot(
            (self.Pct_Change * 100).round(2),
            LineStyleOpts=opts.LineStyleOpts(width=2)
        )

    def Page_Output(self) -> page:
        charts = [
            line_plot(
                self.Net_Value_Set.loc[self.__Fridays],
                LegendOpts=opts.LegendOpts(selected_mode="single"),
                TitleOpts=opts.TitleOpts(title="单位净值")
            ),
            line_plot(
                (self.Scale.loc[self.__Fridays] / 10000).round(2),
                LegendOpts=opts.LegendOpts(is_show=False),
                TitleOpts=opts.TitleOpts(title="资产规模", subtitle="单位：万元"),
                AreaStyleOpts=opts.AreaStyleOpts(opacity=0.5),
                YaxisOpts=opts.AxisOpts(
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    min_=0
                )
            ),
            line_plot(
                (self.Strategy_Proportion.loc[self.__Fridays] * 100).round(2),
                TitleOpts=opts.TitleOpts(title="策略比重", subtitle="单位：%"),
                Stack="1",
                AreaStyleOpts=opts.AreaStyleOpts(opacity=0.5),
                YAxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ),
            bar_plot(
                (self.Strategy_Profit * 100).round(4),
                TitleOpts=opts.TitleOpts(title="策略收益贡献", subtitle="单位：%"),
                Stack="1",
                YAxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ).overlap(self.__Pct_Change_Plot),
            bar_plot(
                (self.Strategy_Profit_Cumsum * 100).round(4),
                TitleOpts=opts.TitleOpts(title="策略累计收益贡献", subtitle="单位：%"),
                Stack="1",
                YAxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ),
            line_plot(
                self.Strategy_NV.round(4),
                TitleOpts=opts.TitleOpts(title="策略单位净值"),
            ),

            line_plot(
                (self.Fund_Proportion.loc[self.__Fridays] * 100).round(2),
                TitleOpts=opts.TitleOpts(title="子基金比重", subtitle="单位：%"),
                Stack="1",
                AreaStyleOpts=opts.AreaStyleOpts(opacity=0.5),
                YAxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ),
            bar_plot(
                (self.Fund_Profit * 100).round(4),
                TitleOpts=opts.TitleOpts(title="子基金收益贡献", subtitle="单位：%"),
                Stack="1",
                YAxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ).overlap(self.__Pct_Change_Plot),
            bar_plot(
                (self.Fund_Profit_Cumsum * 100).round(4),
                TitleOpts=opts.TitleOpts(title="子基金累计收益贡献", subtitle="单位：%"),
                Stack="1",
                YAxisOpts=opts.AxisOpts(
                    type_="value",
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    axislabel_opts=opts.LabelOpts(formatter="{value}%")
                )
            ),
            line_plot(
                self.Fund_NV.round(4),
                TitleOpts=opts.TitleOpts(title="子基金单位净值"),
            )
        ]
        for Strategy in set(self.__get_strategies().values()):
            if Strategy != "货币基金":
                charts += [
                    line_plot(
                        (self.Fund_Proportion_by_Strategy(Strategy) * 100).round(2),
                        TitleOpts=opts.TitleOpts(title="%s 子基金比重" % Strategy, subtitle="单位：%"),
                        Stack="1",
                        AreaStyleOpts=opts.AreaStyleOpts(opacity=0.5)
                    ),
                    bar_plot(
                        (self.Fund_Profit_by_Strategy(Strategy) * 100).round(4),
                        TitleOpts=opts.TitleOpts(title="%s 子基金收益贡献" % Strategy, subtitle="单位：%"),
                        Stack="1"
                    ),
                    bar_plot(
                        (self.Fund_Profit_Cumsum_by_Strategy(Strategy) * 100).round(4),
                        TitleOpts=opts.TitleOpts(title="%s 子基金累计收益贡献" % Strategy, subtitle="单位：%"),
                        Stack="1"
                    ),
                    line_plot(
                        self.Fund_NV_by_Strategy(Strategy).round(4),
                        TitleOpts=opts.TitleOpts(title="%s 子基金单位净值" % Strategy)
                    )
                ]
        return page(charts)


class Analysis_Results(balance_sheet_analysis):
    def __init__(self, sheets, **kwargs):
        super().__init__(sheets)

    @staticmethod
    def get_balance_sheets(code, name):
        return ...


class balance_sheet_fetch:
    def __init__(self, code: typing.Union[str, None] = None, name: typing.Union[str, None] = None):
        self.__code = code
        self.__name = self.__name_change(name)
        self.__Mongo_Client = Mongo_Client()
        self.__DB_Email = self.__Mongo_Client["CBS数据"]["投研部邮箱"]
        self.__Email_Client = imaplib.IMAP4_SSL("imap.qiye.163.com", 993)
        self.__Email_Client.login(Configs["TYB_Email"]["username"], Configs["TYB_Email"]["password"])

    @property
    def __email_record(self):
        data = pandas.DataFrame(
            [
                x for x in self.__DB_Email.find(
                {
                    "$and": [
                        {"主题": {"$regex": self.__name}},
                        {"主题": {"$regex": "估值表"}}
                    ]
                },
                {"_id": 0, "序号": 1, "附件": 1, "发件时间": 1, "文件夹": 1}
            )
            ]
        ).sort_values(by=["发件时间"], ascending=False)
        data: pandas.DataFrame = data.loc[
            [
                x for x in data.index
                if sum(
                [
                    y.__contains__(self.__code) and (y.__contains__("估值表") or y.__contains__("估值报表")) for y in
                    data["附件"][x]
                ]
            )
            ]
        ]
        data["附件"] = [",".join(x) for x in data["附件"]]
        data["估值表日期"] = [self.__extract_date(x) for x in data["附件"]]
        return data.drop(columns=["发件时间"]).drop_duplicates()

    @staticmethod
    def __name_change(name: str):
        return name.replace(
            "私募", ""
        ).replace(
            "证券", ""
        ).replace(
            "投资", ""
        ).replace(
            "基金", ""
        )

    def __extract_date(self, filename: str):
        filename = filename.replace(self.__name, "").replace(self.__code, "")
        date = "".join([x for x in filename.split(".")[0] if 48 <= ord(x) <= 57])
        return pandas.to_datetime(date).date()

    def fetch_attachment(self, folder, order):
        self.__Email_Client.select(folder)
        _, data = self.__Email_Client.fetch(str(order), "(RFC822)")
        if data[0]:
            try:
                msg_content = data[0][-1].decode(chardet.detect(data[0][-1])['encoding'])
            except:
                try:
                    msg_content = data[0][-1].decode("ISO-8859-1")
                except:
                    msg_content = data[0].decode("ISO-8859-1")
            msg = email.parser.Parser().parsestr(msg_content)
            for item in msg.walk():
                file_name = item.get_param("name")
                if file_name and ("估值表" in decode_str(file_name) or "估值报表" in decode_str(file_name)):
                    h = email.header.Header(file_name)
                    dh = email.header.decode_header(h)
                    filename = dh[0][0]
                    if dh[0][1]:
                        filename = decode_str(str(filename, dh[0][1]))
                        content = item.get_payload(decode=True)
                        self.__insert_balance_sheet(content, filename, self.__extract_date(filename))
                        print("---已下载--- ==> %s" % filename)
                        return content

    def get(self, **kwargs):
        start = pandas.to_datetime(kwargs.get("start", "20000101")).date()
        end = pandas.to_datetime(kwargs.get("end", datetime.date.today())).date()
        downloaded = pandas.DataFrame(
            [
                x for x in self.__Mongo_Client["CBS数据"]["产品估值表"].find(
                {
                    "产品代码": self.__code,
                    "$and": [
                        {"日期": {"$gte": pandas.to_datetime(start)}},
                        {"日期": {"$lte": pandas.to_datetime(end)}}
                    ]
                }
            )
            ]
        )
        to_download = self.__email_record.copy()
        to_download = to_download[
            (to_download["估值表日期"] <= end) & (to_download["估值表日期"] >= start)
            ]
        to_download = to_download.loc[
            [
                x for x in to_download.index
                if pandas.to_datetime(to_download.loc[x, "估值表日期"]) not in downloaded["日期"].tolist()
            ]
        ]
        to_download = to_download.sort_values(by=["文件夹", "序号"]).reset_index(drop=True)
        print(to_download)
        return [
            self.fetch_attachment(x, y) for x, y, z in zip(
                to_download["文件夹"], to_download["序号"], to_download["附件"]
            )
        ] + downloaded["文件内容"].tolist()

    def delete(self, start):
        self.__Mongo_Client["CBS数据"]["产品估值表"].delete_many(
            filter={
                "产品代码": self.__code,
                "日期": {"$gte": pandas.to_datetime(start)}
            }
        )

    def __insert_balance_sheet(
            self,
            content: bytes,
            filename: str,
            date: typing.Union[str, datetime.date, datetime.datetime]
    ):
        Collection = self.__Mongo_Client["CBS数据"]["产品估值表"]
        if Collection.find_one(
                {
                    "文件名称": filename,
                    "日期": pandas.to_datetime(date),
                    "产品代码": self.__code
                }
        ):
            Collection.update_one(
                {
                    "文件名称": filename,
                    "日期": pandas.to_datetime(date),
                    "产品代码": self.__code
                },
                {"$set":
                     {"文件内容": content}
                 }
            )
        else:
            Collection.insert_one(
                {
                    "产品代码": self.__code,
                    "日期": pandas.to_datetime(date),
                    "文件名称": filename,
                    "文件内容": content
                }
            )
