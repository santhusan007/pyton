from dailyprice import DailyPrice
import sqlite3
import psycopg2
from psycopg2.extensions import register_adapter, AsIs
import numpy as np
import datetime as dt
import pandas_datareader as web
import yfinance as yf

    
path=r'D:\pyhton\stock_screener\app.db' # path for sqlite database
#connection to sqlite database
sqliteconn=DailyPrice.dataBaseSqliteConn(path)
sqlitec=DailyPrice.dataBaseSqliteCursor(sqliteconn)
    
# connection to PG  database
pgconn=DailyPrice.dataBasePgsConn()
pgc=DailyPrice.dataBasePgsCursor(pgconn)   

def priceDownloadSqlite(id:list):
    placeholder= '?' # For SQLite. See DBAPI paramstyle.
    placeholders= ', '.join(placeholder for _ in id)
    query= 'SELECT id,symbol,company FROM stocks where id in (%s)' % placeholders
    sqlitec.execute(query, id)
    rows=sqlitec.fetchall()
    stock_dict = {row['symbol']: row['id'] for row in rows}
    yahoo_symbols=[f'{k}.NS' for k in stock_dict.keys()]
    #stockid=[stock_dict[symbol.split('.')[0]] for symbol in yahoo_symbols]

    start=dt.datetime(2000,1,1)#Change date and this script will download the file from yahoo finance upto the desired date interval
    end=dt.datetime.now()
    for k,v in enumerate (stock_dict):
        s_df=priceFromYahoo(stock_dict,start,end)        
        stock_id=stock_dict[v.split('.')[0]]
        #print(s_df)
    
        for i in  range(len(s_df)):
            sqlite3.register_adapter(np.int64,lambda val:float(val))
            sqlite3.register_adapter(np.int32,lambda val:float(val))
            sqlitec.execute("INSERT INTO stock_price(stock_id,date,open,high,low,close,volume ) VALUES ( ?,?,?,?,?,?,?)",(stock_id,str(s_df.index[i]).split(' ')[0],s_df['Open'].iloc[i],s_df['High'].iloc[i],s_df['Low'].iloc[i],s_df['Close'].iloc[i],s_df['Volume'].iloc[i]))
        print(i,"done")
        sqliteconn.commit() 

def priceDeleteSQlite(id:list):
    placeholder= '?' 
    placeholders= ', '.join(placeholder for _ in id)
    query= 'delete FROM stock_price where id in (%s)' % placeholders
    sqlitec.execute(query, id)
    sqliteconn.commit() 

def priceDeletePGsql(id:list):
    placeholder= '%s' 
    placeholders= ', '.join(placeholder for _ in id)
    query= 'delete FROM stock_price where id in (%s)' % placeholders
    pgc.execute(query, id)
    pgconn.commit() 



def priceInsertPGSql(id:list):
    placeholder= '%s' 
    placeholders= ', '.join(placeholder for _ in id)
    query= 'SELECT id,symbol,company FROM stocks where id in (%s)' % placeholders
    pgc.execute(query, id)
    rows=pgc.fetchall()
    stock_dict = {row['symbol']: row['id'] for row in rows}
    #stockid=[stock_dict[symbol.split('.')[0]] for symbol in yahoo_symbols]
    start=dt.datetime(2000,1,1)#Change date and this script will download the file from yahoo finance upto the desired date interval
    end=dt.datetime.now()
    for k,v in enumerate (stock_dict):
        s_df=priceFromYahoo(stock_dict,start,end)        
        stock_id=stock_dict[v.split('.')[0]]
        print(stock_id)
        for i in  range(len(s_df)):
            register_adapter(np.int64, psycopg2._psycopg.AsIs)
            pgc.execute("INSERT INTO stock_price(stock_id,date,open,high,low,close,volume ) VALUES ( %s,%s,%s,%s,%s,%s,%s)",
            (stock_id,str(s_df.index[i]).split(' ')[0],
            s_df['Open'].iloc[i],s_df['High'].iloc[i],s_df['Low'].iloc[i],
            s_df['Close'].iloc[i],s_df['Volume'].iloc[i]))

        print(i,"done")
        pgconn.commit() 

def priceFromYahoo(stock_dict,startdate,enddate):
    yahoo_symbols=[f'{k}.NS' for k in stock_dict.keys()]
    for index,symbol in enumerate (yahoo_symbols):        
        s_df = round(yf.download(symbol,start=startdate, end=enddate), 2)
        s_df=round(s_df,2)
        return s_df
        
#priceDeleteSQlite([116])        

# priceDownloadSqlite([507])

#priceDeletePGsql([45])

priceInsertPGSql([507])