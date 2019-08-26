from datetime import datetime,timedelta
from vnpy.trader.ui import create_qapp, QtCore
from vnpy.trader.database import database_manager
from vnpy.trader.constant import Exchange, Interval
from vnpy.chart import ChartWidget, VolumeItem, CandleItem
from vnpy.trader.object import BarData
from random import randint
import pandas as pd
"""
"""

if __name__ == "__main__":
    app = create_qapp()

    bars = database_manager.load_bar_data(
        "IF88",
        Exchange.CFFEX,
        interval=Interval.MINUTE,
        start=datetime(2019, 7, 1),
        end=datetime(2019, 7, 17)
    )

    """
    symbol: str
    exchange: Exchange
    datetime: datetime

    interval: Interval = None
    volume: float = 0
    open_interest: float = 0
    open_price: float = 0
    high_price: float = 0
    low_price: float = 0
    close_price: float = 0
    """
    now = datetime.now()
    data = pd.read_msgpack('TXF_1min.msgpack')
    print('Gen minK.')
    for i in range(10000): 
        k = BarData(gateway_name='shioaji',symbol="TXF",exchange=Exchange.SMART  ,datetime=data.index[i])
        k.volume = data.vol[i]
        k.open_interest = 0
        k.open_price = data.open[i]
        k.close_price = data.close[i]
        k.high_price = data.high[i]
        k.low_price =data.low[i]
        bars.append(k)
    print('Over')
    widget = ChartWidget()
    widget.add_plot("candle", hide_x_axis=True)
    widget.add_plot("volume", maximum_height=200)
    widget.add_item(CandleItem, "candle", "candle")
    widget.add_item(VolumeItem, "volume", "volume")
    widget.add_cursor()

    n = 1000
    history = bars[:n]
    new_data = bars[n:]

    widget.update_history(history)

    def update_bar():
        bar = new_data.pop(0)
        widget.update_bar(bar)

    timer = QtCore.QTimer()
    timer.timeout.connect(update_bar)
    timer.start(100)

    widget.show()
    app.exec_()
