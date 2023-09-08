from dailyprice import DailyPrice
import pandas as pd

conn1=DailyPrice.dataBasePgsConn()
c1=DailyPrice.dataBasePgsCursor(conn1)

data=pd.read_sql("""select * from stock_price where date between '2000-01-01' and '2010-12-31' """,conn1)
data1=pd.read_sql("""select * from stock_price where date between '2000-01-01' and '2010-12-31' """,conn1)

data['open']=data1['close']

print("I am data1 and my length is :- " , len(data))
print(data.head(5))

print("I am data1 and my length is :- " , len(data1))
print(data1.head(5))


    