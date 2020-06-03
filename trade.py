import datetime
import backtrader as bt



class SelfWealthComm(bt.CommInfoBase):
    params = (
            ('stocklike', True),
            ('commtype', bt.CommInfoBase.COMM_FIXED),
            )

    def _getcommission(self, size, price, pseudoexec):
        return self.p.commission


class BuyAndHold(bt.Strategy):
    params = dict(monthly_cash=5000)

    def start(self):
        self.broker.set_fundmode(fundmode=True, fundstartval=100.0)

        self.cash_start = self.broker.get_cash()
        self.val_start = 100.0

        self.add_timer(
                bt.timer.SESSION_END,
                monthdays=[1],
                monthcarry=True,
        )

    def notify_timer(self, timer, when, *args, **kwargs):
        self.broker.add_cash(self.p.monthly_cash)

        # Buy available cash

        target_value = self.broker.get_value() + self.p.monthly_cash
        self.order_target_value(target=target_value)


    def stop(self):
        self.roi = (self.broker.get_value() / self.val_start) - 1.0
        self.froi = self.broker.get_fundvalue() - self.val_start
        print('ROI: {:.2f}%'.format(100.0 * self.roi))
        print('Fund Value: {:.2f}%'.format(self.froi))


if __name__ == "__main__":
    cerebro = bt.Cerebro()
    cerebro.addstrategy(BuyAndHold)

    comminfo = SelfWealthComm(commission=9.50)
    cerebro.broker.addcommissioninfo(comminfo)

    now = datetime.datetime.now()
    start = now - datetime.timedelta(days=2*365)

    data = bt.feeds.YahooFinanceCSVData(dataname='yfasx.csv', fromdate=start)

    cerebro.adddata(data)
    cerebro.run()
    cerebro.plot()
