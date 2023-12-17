# -*- coding: utf-8 -*-
import pyecharts
import typing
from pyecharts import options as opts
import pandas

__all__ = [
    "line_plot",
    "bar_plot",
    "page",
    "opts"
]


class line_plot(pyecharts.charts.Line):
    def __init__(self, table: typing.Union[pandas.DataFrame, pandas.Series], **kwargs):
        super().__init__(init_opts=kwargs.get("InitOpts", opts.InitOpts()))
        super().add_xaxis(table.index.tolist())
        if isinstance(table, pandas.DataFrame):
            for name in table.columns:
                super().add_yaxis(
                    name,
                    table[name].tolist(),
                    itemstyle_opts=kwargs.get("ItemStyleOpts", opts.ItemStyleOpts()),
                    linestyle_opts=kwargs.get("LineStyleOpts", opts.LineStyleOpts(width=2)),
                    areastyle_opts=kwargs.get("AreaStyleOpts", opts.AreaStyleOpts()),
                    label_opts=kwargs.get("LabelOpts", opts.LabelOpts(is_show=False)),
                    stack=kwargs.get("Stack", None)
                )
        elif isinstance(table, pandas.Series):
            super().add_yaxis(
                table.name if table.name else "",
                table.tolist(),
                itemstyle_opts=kwargs.get("ItemStyleOpts", opts.ItemStyleOpts()),
                linestyle_opts=kwargs.get("LineStyleOpts", opts.LineStyleOpts(width=2)),
                areastyle_opts=kwargs.get("AreaStyleOpts", opts.AreaStyleOpts()),
                label_opts=kwargs.get("LabelOpts", opts.LabelOpts(is_show=False)),
                stack=kwargs.get("Stack", None)
            )
        super().set_global_opts(
            title_opts=kwargs.get("TitleOpts", opts.TitleOpts()),
            yaxis_opts=kwargs.get("YaxisOpts", opts.AxisOpts(is_scale=True, splitline_opts=opts.SplitLineOpts(is_show=True))),
            xaxis_opts=kwargs.get("XaxisOpts", opts.AxisOpts(is_scale=True, splitline_opts=opts.SplitLineOpts(is_show=True))),
            datazoom_opts=kwargs.get("DatazoomOpts", opts.DataZoomOpts(type_="inside", range_start=0, range_end=100)),
            tooltip_opts=kwargs.get("TooltipOpts", opts.TooltipOpts(trigger="axis")),
            toolbox_opts=kwargs.get("ToolboxOpts", opts.ToolboxOpts(is_show=False)),
            legend_opts=kwargs.get("LegendOpts", opts.LegendOpts(pos_top="bottom", type_="scroll")),
        )


class bar_plot(pyecharts.charts.Bar):
    def __init__(self, table: typing.Union[pandas.DataFrame, pandas.Series], **kwargs):
        super().__init__(init_opts=kwargs.get("InitOpts", opts.InitOpts()))
        super().add_xaxis(table.index.tolist())
        if isinstance(table, pandas.DataFrame):
            for name in table.columns:
                super().add_yaxis(
                    name,
                    table[name].tolist(),
                    itemstyle_opts=kwargs.get("ItemStyleOpts", opts.ItemStyleOpts()),
                    label_opts=kwargs.get("LabelOpts", opts.LabelOpts(is_show=False)),
                    bar_width=kwargs.get("BarWidth", None),
                    color=kwargs.get("BarColor", None),
                    stack=kwargs.get("Stack", None)
                )
        elif isinstance(table, pandas.Series):
            super().add_yaxis(
                table.name if table.name else "",
                table.tolist(),
                itemstyle_opts=kwargs.get("ItemStyleOpts", opts.ItemStyleOpts()),
                label_opts=kwargs.get("LabelOpts", opts.LabelOpts(is_show=False)),
                bar_width=kwargs.get("BarWidth", None),
                color=kwargs.get("BarColor", None),
            )
        super().set_global_opts(
            title_opts=kwargs.get("TitleOpts", opts.TitleOpts()),
            yaxis_opts=kwargs.get("YaxisOpts", opts.AxisOpts(is_scale=True, splitline_opts=opts.SplitLineOpts(is_show=True))),
            xaxis_opts=kwargs.get("XaxisOpts", opts.AxisOpts(is_scale=True, splitline_opts=opts.SplitLineOpts(is_show=True))),
            datazoom_opts=kwargs.get("DatazoomOpts", opts.DataZoomOpts(type_="inside", range_start=0, range_end=100)),
            tooltip_opts=kwargs.get("TooltipOpts", opts.TooltipOpts(trigger="axis")),
            toolbox_opts=kwargs.get("ToolboxOpts", opts.ToolboxOpts(is_show=False)),
            legend_opts=kwargs.get("LegendOpts", opts.LegendOpts(pos_top="bottom", type_="scroll")),
        )


class page(pyecharts.charts.Page):
    def __init__(self, charts=None, **kwargs):
        super().__init__(layout=kwargs.get("Layout", page.SimplePageLayout))
        if charts is None:
            charts = []
        for chart in charts:
            super().add(chart)
