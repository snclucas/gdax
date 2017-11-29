import strategy.strategy_bollinger_bands as boll
import strategy.strategy_macd as macd


available_strategies = {'boll': boll, 'macd': macd}


def run_strategies(strategies, intervals):
    for strategy in strategies:
        if available_strategies[strategy] is not None:
            print(available_strategies[strategy].name() + " " + str(available_strategies[strategy].run(intervals)))

if __name__ == '__main__':
    run_strategies(['boll', 'macd'], [60, 600, 1200, 2400, 3600])
