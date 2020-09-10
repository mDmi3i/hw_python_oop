import datetime as dt


class Calculator:
    
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
       sum = 0
       now = dt.datetime.now()

       for record in self.records:
           if record.date == now.date(): 
                sum = sum + record.amount
       return sum    

    def get_week_stats(self):

       sum = 0
       end_week = dt.datetime.now()
       period = dt.timedelta(days=7)
       start_week = end_week - period 

       for record in self.records:
           if (record.date > start_week.date()) and (record.date <= end_week.date()):
               sum = sum + record.amount
       return sum    


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):

        calories_balance = self.limit - super().get_today_stats()

        if calories_balance > 0:
            
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {calories_balance} кКал') 

        else:

            return('Хватит есть!')        
     

class CashCalculator(Calculator):

    USD_RATE = 60.00
    EURO_RATE = 70.00
    RUB_RATE = 1 

    CURRENCY = {
                'usd':{'rate':USD_RATE , 'name':'USD'},
                'eur':{'rate':EURO_RATE, 'name':'Euro'},
                'rub':{'rate':RUB_RATE, 'name':'руб'}
                }

    def get_today_cash_remained(self,currency):

        cash_balance = self.limit - super().get_today_stats()
        
        if cash_balance == 0:
            return 'Денег нет, держись'

        else:    

            cash_balance_currency = round(cash_balance / self.CURRENCY[currency]['rate'], 2)
         
            if cash_balance < 0:
                return (f'Денег нет, держись: твой долг - {abs(cash_balance_currency)} {self.CURRENCY[currency]["name"]}')

            else:    
                return (f'На сегодня осталось {cash_balance_currency} {self.CURRENCY[currency]["name"]}')


class Record:

    def __init__(self, amount, comment, date = dt.datetime.now()):
        self.amount = amount
        self.comment = comment 

        if type(date) == str:
            date_format = '%d.%m.%Y'
            moment = dt.datetime.strptime(date, date_format)
            self.date = moment.date()
        else:
            self.date = date.date()    
    

calories_calculator = CaloriesCalculator(1000)

calories_calculator.add_record(Record(amount=100, comment="чай"))
calories_calculator.add_record(Record(amount=100, comment="чай"))
calories_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))

print(calories_calculator.get_calories_remained())

cash_calculator = CashCalculator(1000)   

cash_calculator.add_record(Record(amount=145, comment="кофе")) 
cash_calculator.add_record(Record(amount=3000, comment="Серёге за обед"))
cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))
                
print(cash_calculator.get_today_cash_remained("rub"))