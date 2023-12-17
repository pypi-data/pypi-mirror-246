# -*- coding: utf-8 -*-
import datetime
import pandas
import _io
import typing
import warnings

warnings.filterwarnings("ignore")

__all__ = ['read_balance_sheet']


class read_balance_sheet:
    def __init__(
            self,
            io: typing.Union[str, bytes, _io.TextIOWrapper, _io.BufferedReader]
    ) -> None:
        self.File = io
        self.Original_Table = pandas.read_excel(io)
        self.Date = self.__find_date()
        self.Table = self.read_table()

    def read_table(self) -> pandas.DataFrame:
        table = pandas.read_excel(self.File)
        i, j = 0, 0
        while "科目代码" not in table.iloc[i].tolist():
            i += 1
        while "科目代码" != table.iloc[i, j]:
            j += 1
        table = pandas.read_excel(self.File, header=i + 1, index_col=j, na_filter="")
        table["成本-本币"] = table["成本-本币" if "成本-本币" in table.columns else "成本"]
        table["市值-本币"] = table["市值-本币" if "市值-本币" in table.columns else "市值"]
        return table.loc[
            [x for x in table.index if not (x == "科目代码" or x == "")]
        ].fillna("").replace({" ", ""})

    def __find_date(self) -> datetime.date:
        table = self.Original_Table.T.dropna(how="all").T
        x = [y for y in table.iloc[:, 0].tolist() if str(y).__contains__("日期")][0]
        return pandas.to_datetime("".join([y for y in x if 48 <= ord(y) <= 57])).date()

    @staticmethod
    def __change_header(table: pandas.DataFrame) -> pandas.DataFrame:
        table["科目名称"] = ["".join(x.split(" ")) if isinstance(x, str) else x for x in table["科目名称"]]
        table["数量"] = table["数量"].astype(float) if len(table) else table["数量"]
        table["成本-本币"] = table["成本-本币" if "成本-本币" in table.columns else "成本"].astype(float)
        table["市值-本币"] = table["市值-本币" if "市值-本币" in table.columns else "市值"].astype(float)
        return table

    @staticmethod
    def __change_fund_name(name: str) -> str:
        head = name[: -4]
        tail = name[-4:]
        if sum([48 <= ord(x) <= 57 for x in tail]) != 4:
            while 48 <= ord(tail[-1]) <= 57:
                tail = tail[:-1]
        return head + tail

    @property
    def Private_Funds(self) -> pandas.DataFrame:
        table = self.Table[self.Table["停牌信息"] != ""]
        table = table.loc[[x for x in table.index if x.__contains__("1108") or x.__contains__("1109")]]
        table = table.loc[[x for x in table.index if x[: 4] == "1108" or x[: 4] == "1109"]]
        if len(table):
            table = self.__change_header(table)
            table["科目名称"] = [self.__change_fund_name(x) for x in table["科目名称"]]
            table = table.pivot_table(index="科目名称", values=["数量", "成本-本币", "市值-本币"], aggfunc="sum")
            table["单位成本"] = table["成本-本币"] / table["数量"]
        return table

    @property
    def Derivatives(self) -> pandas.DataFrame:
        table = self.Table[self.Table["停牌信息"] != ""]
        table = table.loc[[x for x in table.index if x.__contains__("3102")]]
        table = table.loc[[x for x in table.index if x[: 4] == "3102"]]
        table = self.__change_header(table)
        return table

    @property
    def Stocks(self) -> pandas.DataFrame:
        table = self.Table[self.Table["停牌信息"] != ""]
        table = table.loc[[x for x in table.index if x.__contains__("1102")]]
        table = table.loc[[x for x in table.index if x[: 4] == "1102"]]
        table = self.__change_header(table)
        return table

    @property
    def ETFs(self) -> pandas.DataFrame:
        table = self.Table[self.Table["停牌信息"] != ""]
        table = table.loc[[x for x in table.index if x.__contains__("1105")]]
        table = table.loc[[x for x in table.index if x[: 4] == "1105"]]
        table = self.__change_header(table)
        return table

    @property
    def Shares(self) -> typing.Union[int, float]:
        return self.Table["数量"]["实收资本"]

    @property
    def Scale(self) -> typing.Union[int, float]:
        return self.Table[
            "市值-本币" if "市值-本币" in self.Table.columns else "市值"
        ][
            [x for x in self.Table.index if x.__contains__("资产净值")][0]
        ]

    @property
    def Net_Value(self) -> float:
        return round(self.Scale / self.Shares, 4)

    @property
    def Accumulated_Value(self) -> float:
        return float(self.Table.loc[[x for x in self.Table.index if x.__contains__("累计单位净值")][0], "科目名称"])

    @staticmethod
    def __find_dp(number: typing.Union[int, float]) -> int:
        n = 0
        while round(number, n) != number:
            n += 1
        return n

    @property
    def Properties(self) -> pandas.DataFrame:
        table = self.Table[self.Table["停牌信息"] != ""]
        table = self.__change_header(table)
        table["科目名称"] = [self.__change_fund_name(x) if x.__contains__("基金") else x for x in table["科目名称"]]
        if len(table):
            table = self.__change_header(table)
            table["科目名称"] = [self.__change_fund_name(x) for x in table["科目名称"]]
            table = table.pivot_table(index="科目名称", values=["数量", "成本-本币", "市值-本币"], aggfunc="sum")
            table["单位成本"] = table["成本-本币"] / table["数量"]
        return table

    @property
    def Cash(self) -> typing.Union[int, float]:
        return (
            self.Table["市值-本币"]["1002"] if "1002" in self.Table.index else 0
        ) + (
            self.Table["市值-本币"]["3003"] if "3003" in self.Table.index else 0
        )

    @property
    def Dividends(self) -> pandas.DataFrame:
        table = self.Table.loc[[x for x in self.Table.index if len(x) > 10 and x[:4] == "1203"]]
        table = self.__change_header(table.replace({"": float("nan")}))
        if len(table):
            table["科目名称"] = [self.__change_fund_name(x) for x in table["科目名称"]]
            return table.groupby("科目名称")["市值-本币"].sum()
        else:
            return pandas.DataFrame({"市值-本币": {}})["市值-本币"]
