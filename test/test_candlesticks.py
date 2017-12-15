import unittest
import pandas as pd


import indicators

def fun(x):
    return x + 1


class MyTest(unittest.TestCase):
    def test(self):
        current_candle_dict = {
            "date": 134567896,
            "low": 330.0,
            "high": 400.0,
            "open": 340.0,
            "close": 390.0,
            "volume": 10000
        }

        previous_candle_dict = {
            "date": 134567896,
            "low": 350.0,
            "high": 380.0,
            "open": 370.0,
            "close": 360.0,
            "volume": 20000
        }

        candles_arr = [current_candle_dict, previous_candle_dict]

        candles = pd.DataFrame(candles_arr)

        indicators.check_engulfing(candles)

        print(candles)

        self.assertEqual(fun(3), 4)
