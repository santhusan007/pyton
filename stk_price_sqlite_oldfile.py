import sqlite3
import numpy as np
import datetime as dt
import nsepy
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import zipfile
import io
import os

conn = sqlite3.connect(r'D:\pyhton\stock_screener\app.db')
conn.row_factory = sqlite3.Row
# this help to retrive the iteration more like a dictionery
c = conn.cursor()


def rbi_sqlite():
    # getting RBI reference using NSEpy module. details can be found in nsepy_testing file in stock
    rbi_ref = nsepy.get_rbi_ref_history(dt.date.today(), dt.date.today())
    print(rbi_ref)
    c.execute(""" SELECT * FROM currency """)
    rows = c.fetchall()
    cur_dict = {row['cur_symbol']: row['id'] for row in rows}
    for i in range(len(rbi_ref.T)):
        sqlite3.register_adapter(np.int64, lambda val: float(val))
        sqlite3.register_adapter(np.int32, lambda val: float(val))
        date = str(dt.datetime.today().date())
        val = [v for v in cur_dict.values()]
        c.execute("INSERT INTO rbi_exchange(date,cur_id,rate ) VALUES ( ?,?,?)",
                  (date, val[i], rbi_ref.iloc[0][i]))
    conn.commit()


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


def metal_sqlite(cu_df):
    c.execute(""" SELECT * FROM commodities """)
    rows = c.fetchall()
    com_dict = {row['com_sym']: row['id'] for row in rows}
    for i in range(len(cu_df.T)-1):
        sqlite3.register_adapter(np.int64, lambda val: float(val))
        sqlite3.register_adapter(np.int32, lambda val: float(val))
        date = str(cu_df['date'].iloc[0]).split(' ')[0]
        com_val = [v for v in com_dict.values()]
        print(com_val[i], date, cu_df.iloc[0][i+1])
        c.execute("INSERT INTO cu_lme_csp(com_id,date,rate ) VALUES ( ?,?,?)",
                  (com_val[i], date, cu_df.iloc[0][i+1]))
        conn.commit()


def bhavcopy():
    aaj = dt.date.today().strftime('%d%b%Y').upper()
    bhav_url = f'https://archives.nseindia.com/content/historical/EQUITIES/2022/{aaj[2:5]}/cm{aaj}bhav.csv.zip'
    folder_location = r'C:\Users\Admin\Desktop\Python\Pandas\database\stock_screener'
    filename = os.path.join(folder_location, bhav_url.split("/")[-1])
    r = requests.get(bhav_url, stream=True)
    # converting zip content to binary
    z = zipfile.ZipFile(io.BytesIO(r.content))
    # using zip library to read the binary zip adnextract it to destination
    z.extractall(folder_location)

    #df = get_price_list(dt=date.today())
    # df=pd.read_csv('cm03JAN2022bhav.csv')
    # avoiding the '.zip'(last 4 charcters) extesnion
    df = pd.read_csv(filename[:-4])
    return df


def stock_sqlite():
    c.execute(""" SELECT id,symbol,company FROM stocks """)
    rows = c.fetchall()
    # for row in rows:
    # print(row['company'])
    stock_df = bhavcopy()

    stock_dict = {row['symbol']: row['id'] for row in rows}
    len(stock_dict)
    # Extracting 506 stock details from the whole list of bahv copy
    daily_data = stock_df.copy()[(stock_df.copy().SYMBOL.isin(stock_dict.keys())) & (
        (stock_df.copy()['SERIES'] == 'EQ') | (stock_df.copy()['SERIES'] == 'BE'))]
    # converting the stock dict to data frame
    stock_data = pd.DataFrame(stock_dict.items(), columns=['SYMBOL', 'stk_id'])
    # merging to dataframe a
    final_df = pd.merge(daily_data, stock_data)
    final_df.sort_values('stk_id', inplace=True)
    final_df.reset_index(inplace=True)
    final_df.drop(columns='index', inplace=True)
    final_df['date'] = pd.to_datetime(final_df['TIMESTAMP'])
    final_df = final_df[['SYMBOL', 'stk_id', 'date',
                         'OPEN', 'HIGH', 'LOW', 'CLOSE', 'TOTTRDQTY']]

    for i in range(len(final_df)):
        sqlite3.register_adapter(np.int64, lambda val: float(val))
        sqlite3.register_adapter(np.int32, lambda val: float(val))
        c.execute("INSERT INTO stock_price(stock_id,date,open,high,low,close,volume ) VALUES ( ?,?,?,?,?,?,?)", (final_df['stk_id'].iloc[i], str(final_df['date'].iloc[i]).split(
            ' ')[0], final_df['OPEN'].iloc[i], final_df['HIGH'].iloc[i], final_df['LOW'].iloc[i], final_df['CLOSE'].iloc[i], final_df['TOTTRDQTY'].iloc[i]))
    conn.commit()


def index_price():
    index_aaj = dt.date.today().strftime('%d%m%Y').upper()
    index_url = f'https://archives.nseindia.com/content/indices/ind_close_all_{index_aaj}.csv'
    folder_location = r'C:\Users\Admin\Desktop\Python\Pandas\database\stock_screener'
    filename = os.path.join(folder_location, index_url.split("/")[-1])
    r = requests.get(index_url, stream=True)
    with open(filename, 'wb') as f:
        f.write(r.content)

        index_df = pd.read_csv(filename)
        return index_df
#

# Making a dict for broader Index


def index_sqlite():
    c.execute(""" SELECT * FROM broader_index """)
    rows = c.fetchall()
    bor_dict = {row['indices']: row['id'] for row in rows}
    index_df = index_price()

    df = index_df[index_df['Index Name'].isin(
        ['Nifty 50', 'NIFTY Midcap 100', 'NIFTY Smallcap 100'])].reset_index()
    df['Index Date'] = pd.to_datetime(df['Index Date'], dayfirst=True)
    df.drop(columns='index', inplace=True)
    df = round(df, 2)
    for i in range(len(df)):
        sqlite3.register_adapter(np.int64, lambda val: float(val))
        sqlite3.register_adapter(np.int32, lambda val: float(val))
        broader_id = bor_dict[df['Index Name'].iloc[i]]
        c.execute("INSERT INTO index_price(broader_id,date,open,high,low,close,volume ) VALUES (?,?,?,?,?,?,?)", (broader_id, str(df['Index Date'].iloc[i]).split(' ')[
                  0], df['Open Index Value'].iloc[i], df['High Index Value'].iloc[i], df['Low Index Value'].iloc[i], df['Closing Index Value'].iloc[i], df['Volume'].iloc[i]))
        conn.commit()
    c.execute(""" SELECT * FROM sectorial_index """)
    rows = c.fetchall()
    sect_dict = {row['sector']: row['id'] for row in rows}
    sect_df = index_df[index_df['Index Name'].isin(
        list(sect_dict.keys())[:-1])].reset_index()
    sect_df['Index Date'] = pd.to_datetime(
        sect_df['Index Date'], dayfirst=True)
    sect_df.drop(columns='index', inplace=True)
    stock_data = pd.DataFrame(sect_dict.items(), columns=[
                              'Index Name', 'stk_id'])
    df = pd.merge(sect_df, stock_data)
    df.sort_values('stk_id', inplace=True)
    for i in range(len(df)):
        sqlite3.register_adapter(np.int64, lambda val: float(val))
        sqlite3.register_adapter(np.int32, lambda val: float(val))
        c.execute("INSERT INTO index_price(sectorial_id,date,open,high,low,close,volume ) VALUES (?,?,?,?,?,?,?)", (df['stk_id'].iloc[i], str(df['Index Date'].iloc[i]).split(
            ' ')[0], df['Open Index Value'].iloc[i], df['High Index Value'].iloc[i], df['Low Index Value'].iloc[i], df['Closing Index Value'].iloc[i], df['Volume'].iloc[i]))

    conn.commit()


def main():
    rbi_sqlite()
    stock_sqlite()
    index_sqlite()
    cu_url = 'https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Cu_cash'
    cu_df = dfFromURL(cu_url)
    print(cu_df)
    metal_sqlite(cu_df)


if __name__ == "__main__":
    main()
    conn.close()