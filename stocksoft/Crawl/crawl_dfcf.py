import requests
import json
import time
import os

class dfcf_crawl():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.111 Safari/537.36'
        }
        self.stock_info_daily = []


    def get_data(self, stockcode):
        '''
        数据抓取
        :param stockcode:股票编码
        :return:
        '''
        if stockcode[:1] == '6':
            area = '1'
        else:
            area = '0'
        url = 'http://push2.eastmoney.com/api/qt/stock/trends2/get?secid={area}.{code}&' \
              'fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&' \
              'fields2=f51,f52,f53,f54,f55,f56,f57,f58'.format(area=area, code=stockcode)
        res = requests.get(url, headers=self.headers)
        json_data = json.loads(res.text)
        data = json_data.get('data')
        name = data.get('name')
        trends = data.get('trends')
        for trend in trends:
            stock_info = trend.split(',')[:2]
            self.stock_info_daily.append(stock_info)
        self.save_file(stockcode, name, self.stock_info_daily)


    def save_file(self, stockcode, name, data):
        '''
        用于股票数据日常存储
        :param stockcode: 股票编码
        :param name: 股票名称
        :param data: 股票当日数据
        '''
        date = time.strftime("%Y-%m-%d", time.localtime())
        base_path = '../StockFile/{code}_{name}'.format(code=stockcode,name=name)
        file_path = base_path + '/daily/'
        if not os.path.exists(base_path):
            os.mkdir(base_path)
            os.mkdir(file_path)
        with open(file_path + '{date}.txt'.format(date=date),'w') as f:
            f.writelines(str(data))

if __name__ == "__main__":
    test = dfcf_crawl()
    test.get_data('002500')