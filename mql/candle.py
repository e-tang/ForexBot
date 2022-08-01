from typing import Union

from pandas import DataFrame

from . import Base


class Candle(Base):
    time: int
    open: float
    high: float
    low: float
    close: float
    tick_volume: float
    real_volume: float
    spread: float
    ema: float

    def __repr__(self):
        # kwargs = [f"{i}={k}" for i, k in self.__dict__.items()]
        return f"{self.__class__!r}(open={self.open}, ema={self.ema}, close={self.ema})"

    @property
    def mid(self):
        return (self.open + self.close) / 2

    def is_bullish(self):
        return self.close > self.open

    def is_bearish(self):
        return self.open > self.close

    def is_hanging_man(self, ratio=1.5):
        return max((self.open - self.low), (self.high - self.close)) / (self.close - self.open) >= ratio

    def is_bullish_hammer(self, ratio=1.5):
        return max((self.close - self.low), (self.high - self.open)) / (self.open - self.close) >= ratio


class Candles:
    def __init__(self, *, data: DataFrame, candle=Candle):
        self.__data = data.iloc[::-1]
        self.Candle = candle

    def __len__(self):
        return self.__data.shape[0]

    def __contains__(self, item: Candle):
        return item.time in [i[0] for i in self.__data['time'].items()]

    def __getitem__(self, index) -> Union[type(Candle), "Candles"]:
        if isinstance(index, slice):
            cls = self.__class__
            data = self.__data.iloc[index]
            return cls(data=data, candle=self.Candle)

        item = self.__data.iloc[index]
        return self.Candle(**item)

    def __iter__(self):
        return (self.Candle(**row._asdict()) for row in self.__data.itertuples(index=False))

    @property
    def data(self):
        return self.__data
