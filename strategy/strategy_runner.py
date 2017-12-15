import strategy.strategy_bollinger_bands as boll
import strategy.strategy_macd as macd
import strategy.strategy_candlestick as candlestick

intervals = [60, 120, 1200, 2400]
available_strategies = {'boll': boll, 'macd': macd, 'candlestick': candlestick}


def run_strategies(strategies_in, intervals_in):
    for interval in intervals_in:
        total_score = 0
        print("Interval: " + str(interval))
        for strategy in strategies_in:
            if available_strategies[strategy] is not None:
                result = available_strategies[strategy].run(interval)
                total_score = total_score + result['score']
        print(" Score: " + str(total_score))

if __name__ == '__main__':
    run_strategies(['boll', 'macd', 'candlestick'], [60, 600, 1200, 2400, 3600])
