# -*-coding:utf-8-*-
import os
import csv
import time
import sqlite3
import requests

from bs4 import BeautifulSoup


cookie = 'lianjia_ssid=5e209159-c1da-4e62-baeb-29b625ab36ba; lianjia_uuid=22d821bf-d961-41dc-9056-077832015e6a; UM_distinctid=1798dfa8d573f3-0f1fc788204352-d7e1938-144000-1798dfa8d589af; _smt_uid=60a76b26.5a4b5a14; sajssdk_2015_cross_new_user=1; _ga=GA1.2.49900641.1621584680; _gid=GA1.2.202969428.1621584680; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1621584691; select_city=110000; CNZZDATA1253477573=831351016-1621580301-|1621580301; CNZZDATA1254525948=1771394630-1621584007-|1621584007; CNZZDATA1255633284=838836188-1621583960-|1621583960; CNZZDATA1255604082=286605892-1621584701-|1621584701; sensorsdata2015jssdkcross={"distinct_id":"1798dfa8ea846c-031a736ce10e4f-d7e1938-1327104-1798dfa8ea9930","$device_id":"1798dfa8ea846c-031a736ce10e4f-d7e1938-1327104-1798dfa8ea9930","props":{"$latest_traffic_source_type":"直接流量","$latest_referrer":"","$latest_referrer_host":"","$latest_search_keyword":"未取到值_直接打开"}}; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1621584801; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiYTAyMjhmMDBmNGUwNThlNDdhODk5OTNlYzdhYzZiZWE0NGMwYmI5MDRhNDhiZTI2OWQzNzUxNTY0YTZlODRmZGViNjQzYzI2YmZhZWNiMDA2MWE5OGIxYzYxNmExNzE0ZmRkNzRkOGJiNmIyZTVlMWVmYTg0NGFhNmM3NmU2Zjk0OWY3ZTAxODI2MzEwMDc1OWEwNDFiNWJmNjUzOTNmMDA1YzFhZDE2OGNhMTE4NjY2ZDc3ODNhZjMxNDZmMzU4ODlhYWViOTgwNjczYjc2YTM0NmY2YjNhOGEyMWNhMTI2MjkxMDg3NGQzN2ZkNGZhYTUwMWYxNTU1NmM4MTVhNjAzYzkzNDZhZmRiOGZmNGUwMjM1NzljZWM5NzUwYWYxODg0MGM1ODQ4Mjk4YTE0N2UwZTg0NGY2ODE4OTAzMzhcIixcImtleV9pZFwiOlwiMVwiLFwic2lnblwiOlwiMDdiMzg3ZTVcIn0iLCJyIjoiaHR0cHM6Ly9iai5saWFuamlhLmNvbS9lcnNob3VmYW5nLyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9; _gat=1; _gat_past=1'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
    'Cookie': cookie.encode("utf-8").decode("latin1")
}
city_map = {
    "上海": "shanghai",
    "北京": "beijing",
    "深圳": "shenzhen"
    }


class Crawl:
    def __init__(self, city="上海", timestamp=""):
        self.city = city.strip()
        self.current_time = timestamp if timestamp else time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.data_dir = os.path.join(os.path.dirname(__file__),"data", city_map[self.city], self.current_time)
        self.csv_path = os.path.join(self.data_dir, f"{self.current_time}.csv")
        self.download_txt = os.path.join(self.data_dir, f"{self.current_time}.txt")
        self.dataset = os.path.join(self.data_dir, f"{self.current_time}.db")
        self.table_name = self.current_time

    def env_init(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    @staticmethod
    def get_page(url):
        """获取网页原始数据"""
        global headers
        html = requests.get(url, headers=headers).text
        return html

    def get_area_from_url(self, url):
        """获取网页所属区域"""
        html = self.get_page(url)
        soup = BeautifulSoup(html, 'lxml')
        ershoufang = soup.find('div', attrs={'data-role': 'ershoufang'})
        for a in ershoufang.find_all('div')[0].find_all('a'):
            if a.has_attr("class") and "selected" in a.get_attribute_list("class"):
                return a.get_text().strip()
        return ''

    @staticmethod
    def extract_info(html, district):
        """解析网页数据，抽取出房源相关信息"""
        soup = BeautifulSoup(html, 'lxml')
        data = []
        for li in soup.find('ul', class_='sellListContent').find_all('li', class_='LOGCLICKDATA'):  # 遍历所有房源
            try:
                title = li.find('div', class_='title').a.get_text()  # 房源名称
                url = li.find('div', class_='title').a['href']  # 链接，若保存数据至数据库，可作为主键
                residence = li.find('div', class_='positionInfo').get_text().split('-')[0].strip()  # 小区
                region = li.find('div', class_='positionInfo').get_text().split('-')[1].strip()  # 区域
                house_info = li.find('div', class_='houseInfo').get_text()
                # 2室1厅 | 57.91平米 | 南 北 | 简装 | 低楼层(共6层) | 1989年建 | 板楼
                # 部分房源无建成时间信息
                if len(house_info.split(' | ')) == 6:
                    house_type, area, direction, decoration, floor, else_info = house_info.split(' | ')
                    build_time = ''
                elif len(house_info.split(' | ')) == 7:
                    house_type, area, direction, decoration, floor, build_time, else_info = house_info.split(' | ')
                else:
                    continue
                watch = li.find('div', class_='followInfo').get_text().split('/')[0].strip()  # 关注人数
                release_time = li.find('div', class_='followInfo').get_text().split('/')[1].strip()  # 发布时间
                for span in li.find('div', class_='tag').find_all('span'):
                    else_info += '、' + span.get_text()
                total_price = li.find('div', class_='totalPrice').get_text()  # 总价
                univalence = li.find('div', class_='unitPrice').get_text().replace('单价', '')
                data.append([district, title, url, house_type, area, direction, floor, decoration, residence, region,
                            total_price, univalence, build_time, release_time, watch, else_info])
                print(data)
            except Exception as e:
                print('extract_info: ', e)
        return data

    def get_region_urls(self):
        """由于链家每个区域最多只显示100页数据，因此按照城区划分会漏掉较多数据，需获取每个区域链接单独抓取所有数据"""
        host = 'https://sh.lianjia.com'
        esf_url = 'https://sh.lianjia.com/ershoufang/'
        html = self.get_page(esf_url)
        soup = BeautifulSoup(html, 'lxml')
        ershoufang = soup.find('div', attrs={'data-role': 'ershoufang'})
        district_urls = []
        for a in ershoufang.find_all('div')[0].find_all('a'):
            url = host + a['href']
            district_urls.append(url)
        region_urls = set()
        for url in district_urls:
            html = self.get_page(url)
            soup = BeautifulSoup(html, 'lxml')
            ershoufang = soup.find('div', attrs={'data-role': 'ershoufang'})
            for a in ershoufang.find_all('div')[1].find_all('a'):
                region_urls.add(host + a['href'])
        return list(region_urls)

    def save_data_to_dataset(self, info_list):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        # 创建一个名为 my_table 的表，包含两个字段：id 和 value
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name} (id INTEGER PRIMARY KEY, value TEXT)')
        for row_list in info_list:
            for info in row_list:
                cursor.execute(f"INSERT INTO {self.table_name} (value) VALUES (?)", (info,))
        conn.commit() # 提交更改并关闭游标
        cursor.close()
        conn.close() # 关闭数据库连接

    def crawl(self, area='all'):
        fields = [
            '城市', '名称', '链接', '户型', '面积', '朝向', '楼层', '装修',
            '小区', '区域', '总价', '单价', '建成时间', '发布时间', '关注', '其他信息'
        ]
        csvf = open(self.csv_path, 'a', newline='', encoding='gb18030')
        begin_time = time.time()  # 程序开始运行时间
        cnt = 0  # 记录房源数量
        down_urls = []  # 从日志文件中获取已完成的链接
        if os.path.exists(self.download_txt):
            cnt = 0
            print('以下区域已经被爬过:')
            with open(self.download_txt, 'r', encoding='utf-8') as f:
                for line in f.read().splitlines():
                    line = line.strip()
                    if line:
                        cnt += 1
                        print(f'{cnt} {line}')
                        down_urls.append(line)
        # 日志文件，记录已抓取的子区域链接，便于恢复爬虫
        logf = open(self.download_txt, 'a', encoding='utf-8')
        writer = csv.writer(csvf, delimiter=',')  # 以逗号分割
        writer.writerow(fields)
        raw_region_urls = self.get_region_urls()  # 获取所有地区的链接
        region_urls = []
        if area != 'all':
            for region_url in raw_region_urls:
                if area == self.get_area_from_url(region_url):
                    region_urls.append(region_url)
        print('有限区域链接:')
        for num, region_url in enumerate(region_urls):
            print(f'{num} {region_url}')
        for region_url in region_urls:
            if region_url not in down_urls:
                print(cnt, time.time() - begin_time, region_url, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                for page in range(1, 101):
                    try:
                        url = region_url + 'pg%s/' % page  # 构造链接
                        html = self.get_page(url)
                        data = self.extract_info(html, self.city)
                        if data:
                            cnt += len(data)
                            writer.writerows(data)
                            self.save_data_to_dataset(data)
                        else:
                            break  # 若未获取到数据，说明已到达最后一页，退出当前循环
                    except Exception as e:
                        print('爬虫发生错误，可能是已到达最后一页，故退出当前循环，开始获取下一区域数据\n', e)
                        break
                logf.write(region_url + '\n')
        csvf.close()
        logf.close()

    def run(self):
        self.env_init()
        self.crawl(area='静安')


if __name__ == "__main__":
    Crawl().run()
