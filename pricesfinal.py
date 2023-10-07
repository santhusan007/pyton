from dailyprice import DailyPrice
#import pandas as pd

if __name__ == "__main__":
    path = r'D:\pyhton\stock_screener\app.db'  # path for sqlite database
    # connection to sqlite database
    conn = DailyPrice.dataBaseSqliteConn(path)
    c = DailyPrice.dataBaseSqliteCursor(conn)

    # connection to sqlite database
    conn1 = DailyPrice.dataBasePgsConn()
    c1 = DailyPrice.dataBasePgsCursor(conn1)

    ##for today's data delta =0 and for all change delta accordingly

    # rbi_ref, cur_dict = DailyPrice.rbi_dict(c, delta=1)
    # DailyPrice.rbiSqlite(c, conn, rbi_ref, cur_dict, delta=1)
    # print("rbi sqlite done")
    # DailyPrice.rbiPgs(c1, conn1, rbi_ref, cur_dict, delta=1)
    # print("rbi postgres done")

    cu_url = 'https://www.westmetall.com/en/markdaten.php?action=table&field=LME_Cu_cash'
    cu_df = DailyPrice.dfFromURL(cu_url)
    DailyPrice.metal_sqlite(cu_df, c, conn)
    print("copper sqqlite done")
    DailyPrice.cu_pgs(cu_df, c1, conn1)
    print("copper pgs done")
    # # https://archives.nseindia.com/content/historical/EQUITIES/2022/JUL/cm12JUL2022bhav.csv.zip
    # datelist =[2,1]
    # # for d in datelist:
    folder_location = r'D:\pyhton\Python\Pandas\database\stock_screener'
    dateFormated = DailyPrice.bavcopyDate(delta=1)
    url = DailyPrice.bhavcopyUrl(dateFormated)
    print(url)
    # downloaad file from nse website
    downloadDf = DailyPrice.bhavcopy(url, folder_location)
    # downloadDf=pd.read_csv(r'D:\pyhton\Python\Pandas\database\stock_screener\cm04JAN2023bhav.csv')
    stockdfsqlite = DailyPrice.stockData(downloadDf,c)  
    # cleaning the file for sqqlite
    # final writing to the database
    DailyPrice.stock_sqlite(stockdfsqlite, c, conn)
    print("stock sqlite done")

    stockdfPgs = DailyPrice.stockData(downloadDf, c1)  # cleaning the file for pgs
    # final writing to the database
    DailyPrice.stock_pgs(stockdfPgs, c1, conn1)
    print("stock postgres done")

    indexdateFormated = DailyPrice.indexdate(delta=1)
    indexurl = DailyPrice.index_url(indexdateFormated)
    indexdata = DailyPrice.indexDf(indexurl, folder_location)
    print(indexurl)

    mainIndex, mainIndexDict = DailyPrice.broaderIndex(indexdata, c)
    sectorIndex = DailyPrice.sectIndex(indexdata, c)
    DailyPrice.index_sqlite(mainIndex, mainIndexDict, c, conn)
    print("index sqqlite done")
    DailyPrice.sector_sqlite(sectorIndex, c, conn)
    print("sector sqqlite done")

    mainIndexpgs, mainIndexDictpgs = DailyPrice.broaderIndex(indexdata, c1)
    sectorIndexpgs = DailyPrice.sectIndex(indexdata, c1)
    DailyPrice.index_pgs(mainIndexpgs, mainIndexDictpgs, c1, conn1)
    print("index pgs done")
    DailyPrice.sector_pgs(sectorIndexpgs, c1, conn1)
    print("sector pgs done")
