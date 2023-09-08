import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import sqlite3
def dfFromURL(url, tableNumber=1):
        # Parse the HTML as a string
        soup = BeautifulSoup(requests.get(url).content, 'lxml')
        tables = soup.find_all('table')
        # check table number is within number of tables on the page
        assert len(tables) >= tableNumber
        df = pd.read_html(str(tables[tableNumber-1]))[0]
       
        # Dropping the duplicate header for each table
        df.drop_duplicates(keep=False, inplace=True)
        # Removing the '.'  from date (example( 08. January 2021 will convert to 08 january 2021))
        df = df[:1]
        df['date'] = df['date'].apply(lambda x: x[0:2]+x[3:])
        # Removing the zero(0) from the start of date
        df['date'] = np.where((df['date'].str.startswith('0')),
                            df['date'].apply(lambda x: x[1:]), df['date'])
        # changing the stings to proper datetime format
        df['date'] = pd.to_datetime(df['date'], format="%d %B %Y")
        df.rename(columns=({'LME Copper Cash-Settlement': 'csp',
                'LME Copper 3-month': 'fut', 'LME Copper stock': 'stock'}), inplace=True)
        df.sort_values(by='date', inplace=True)
        df.reset_index(inplace=True)
        df.drop(columns='index', inplace=True)
        return df 

url='https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Cu_cash'

df=dfFromURL(url)

def dataBaseSqliteConn(path):
        conn=sqlite3.connect(path)
        conn.row_factory=sqlite3.Row
        #print(conn)
        return conn

def dataBaseSqliteCursor(conn):
        c=conn.cursor()
        #print(c)
        return c

def metal_sqlite(cu_df,c,conn):
        c.execute(""" SELECT * FROM commodities """)
        rows = c.fetchall()
        com_dict = {row['com_sym']: row['id'] for row in rows}
        for i in range(len(cu_df)):
            sqlite3.register_adapter(np.int64, lambda val: float(val))
            sqlite3.register_adapter(np.int32, lambda val: float(val))
            date = str(cu_df['date'].iloc[0]).split(' ')[0]
            com_val = [v for v in com_dict.values()]
            
            c.execute("INSERT INTO cu_lme_csp(com_id,date,Cu_CSP,Cu_Fut,Cu_Stock ) VALUES ( ?,?,?,?,?)",
                    (com_val[i], date, cu_df['csp'],cu_df['fut'],cu_df['stock']))
            conn.commit()