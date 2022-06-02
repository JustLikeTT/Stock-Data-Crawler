# -*- coding: utf-8 -*-
"""
Created on Wed May 18 15:35:39 2022

@author: HeJiXiao
"""
import requests
import csv
from os.path import exists
from os import makedirs
from datetime import datetime

class Crawler:
    def __init__(self, root: str = "./data/"):
        self.root = root
        self.URL = r"https://www.twse.com.tw/zh/exchangeReport/STOCK_DAY?"
        # There is no data before 2010-01-04
        self.limitDate = datetime(2010, 1, 4)
        
        if not exists(self.root):
            makedirs(self.root)

    def _downloadCSV(self, stockNo: str, selectDate: datetime):
        ''' 
        Parameters
        ----------
        stockNo : str
            Number of stock.
        date : str
            Which month of the date to be download. 
            The formate of date is "yyyymmdd".

        Returns void
        -------
        Dowload thte csv file of the date of the stock, which the default
        filename is sotckNo + "_" + month.
        '''
        if selectDate < self.limitDate or selectDate > datetime.now():
            print("The date have to be between 2010/01/04 and today.")
            return
        
        filetype = ".csv"
        filename = self.root + stockNo + "_" + selectDate.strftime("%Y%m%d") + filetype
        if exists(filename):
            print("{}.csv has been downloaded.".format(filename))
            return
        
        parameter = {"response": filetype[1:]}
        parameter["date"] = selectDate.strftime("%Y%m%d")
        parameter["stockNo"] = stockNo
        
        with open(filename, "w",  newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            responseText = requests.get(self.url, parameter).text
            reader = csv.reader(responseText.splitlines())
            rows = [row[:-1] for row in list(reader)]
            # the first two lines is meta data, and the last five is comment.
            rows = rows[1:-5]
            writer.writerows(rows)
            
            print("Successfully download {}.".format(filename))
            
    def download(self, stocksNo: list, dates: list):
        for stock in stocksNo:
            for date in dates:
                self._downloadCSV(stock, date)
            
if __name__ == "__main__":
    crawler = Crawler()
    stockNoString = input("請輸入股票代碼(若輸入多個請用空白隔開):")
    dates = input("請輸入起訖的月份(yyyymm)，若輸一個或三個以上則會下載該月份的資料:")
    dates = [datetime(year=date[:4], month=date[4:], day=1) 
             for date in dates.split()]
    
    crawler.download(stockNoString.split(), dates)