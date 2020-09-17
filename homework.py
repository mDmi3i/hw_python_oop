import datetime as dt


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_balance(self):
        return self.limit - self.get_today_stats()

    def get_period_stat(self, date_start=None, date_end=None):
        if date_end is None:
            date_end = dt.date.today()
        if date_start is None:
            date_start = date_end
        return sum(record.amount
                   for record in self.records
                   if (date_start <= record.date
                       <= date_end))

    def get_today_stats(self):
        return self.get_period_stat()

    def get_week_stats(self):
        period = dt.timedelta(days=6)
        start_week = dt.date.today() - period
        return self.get_period_stat(start_week)


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        calories_balance = self.get_balance()
        if calories_balance > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей'
                    f' калорийностью не более {calories_balance} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):

    USD_RATE = 60.00
    EURO_RATE = 70.00
    RUB_RATE = 1

    CURRENCY = {
                'usd': (USD_RATE, 'USD'),
                'eur': (EURO_RATE, 'Euro'),
                'rub': (RUB_RATE, 'руб')
                }

    def get_today_cash_remained(self, currency):
        cash_balance = self.get_balance()

        if cash_balance == 0:
            return 'Денег нет, держись'

        currency_rate, curency_name = self.CURRENCY[currency]
        cash_balance_currency = cash_balance / currency_rate

        if cash_balance < 0:
            cash_balance_currency = abs(cash_balance_currency)
            return ('Денег нет, держись: твой долг - '
                    f'{cash_balance_currency:.2f} '
                    f'{curency_name}')
        return (f'На сегодня осталось {cash_balance_currency:.2f} '
                f'{curency_name}')


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = self.set_now_date(date)

    def set_now_date(self, date):
        if date is None:
            return dt.date.today()
        return dt.datetime.strptime(date, '%d.%m.%Y').date()


if __name__ == '__main__':
    calories_calculator = CaloriesCalculator(1000)
    calories_calculator.add_record(Record(amount=100, comment='чай'))
    calories_calculator.add_record(Record(amount=100, comment='чай'))
    calories_calculator.add_record(Record(amount=3000,
                                          comment='бар в Танин др',
                                          date='08.11.2019'))
    print(calories_calculator.get_calories_remained())

    cash_calculator = CashCalculator(1000)

    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    cash_calculator.add_record(Record(amount=3000, comment='Серёге за обед'))
    cash_calculator.add_record(Record(amount=3000, comment='бар в Танин др',
                               date='08.11.2019'))
    print(cash_calculator.get_today_cash_remained('rub'))
