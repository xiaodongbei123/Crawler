# -*-coding:utf-8-*-
import os
import csv
import sys
import time
import sqlite3
import requests
import threading

from bs4 import BeautifulSoup


cookie = 'lianjia_ssid=5e209159-c1da-4e62-baeb-29b625ab36ba; lianjia_uuid=22d821bf-d961-41dc-9056-077832015e6a; UM_distinctid=1798dfa8d573f3-0f1fc788204352-d7e1938-144000-1798dfa8d589af; _smt_uid=60a76b26.5a4b5a14; sajssdk_2015_cross_new_user=1; _ga=GA1.2.49900641.1621584680; _gid=GA1.2.202969428.1621584680; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1621584691; select_city=110000; CNZZDATA1253477573=831351016-1621580301-|1621580301; CNZZDATA1254525948=1771394630-1621584007-|1621584007; CNZZDATA1255633284=838836188-1621583960-|1621583960; CNZZDATA1255604082=286605892-1621584701-|1621584701; sensorsdata2015jssdkcross={"distinct_id":"1798dfa8ea846c-031a736ce10e4f-d7e1938-1327104-1798dfa8ea9930","$device_id":"1798dfa8ea846c-031a736ce10e4f-d7e1938-1327104-1798dfa8ea9930","props":{"$latest_traffic_source_type":"直接流量","$latest_referrer":"","$latest_referrer_host":"","$latest_search_keyword":"未取到值_直接打开"}}; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1621584801; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiYTAyMjhmMDBmNGUwNThlNDdhODk5OTNlYzdhYzZiZWE0NGMwYmI5MDRhNDhiZTI2OWQzNzUxNTY0YTZlODRmZGViNjQzYzI2YmZhZWNiMDA2MWE5OGIxYzYxNmExNzE0ZmRkNzRkOGJiNmIyZTVlMWVmYTg0NGFhNmM3NmU2Zjk0OWY3ZTAxODI2MzEwMDc1OWEwNDFiNWJmNjUzOTNmMDA1YzFhZDE2OGNhMTE4NjY2ZDc3ODNhZjMxNDZmMzU4ODlhYWViOTgwNjczYjc2YTM0NmY2YjNhOGEyMWNhMTI2MjkxMDg3NGQzN2ZkNGZhYTUwMWYxNTU1NmM4MTVhNjAzYzkzNDZhZmRiOGZmNGUwMjM1NzljZWM5NzUwYWYxODg0MGM1ODQ4Mjk4YTE0N2UwZTg0NGY2ODE4OTAzMzhcIixcImtleV9pZFwiOlwiMVwiLFwic2lnblwiOlwiMDdiMzg3ZTVcIn0iLCJyIjoiaHR0cHM6Ly9iai5saWFuamlhLmNvbS9lcnNob3VmYW5nLyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9; _gat=1; _gat_past=1'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36',
    'Cookie': cookie.encode("utf-8").decode("latin1")
    }
city_map = {
    "上海": ("shanghai", "https://sh.lianjia.com", "https://sh.lianjia.com/ershoufang/"),
    "北京": ("beijing", "https://bj.lianjia.com", "https://bj.lianjia.com/ershoufang/"), 
    "深圳": ("shenzhen", "https://sz.lianjia.com", "https://sz.lianjia.com/ershoufang/"),
    "广州": ("guangzhou", "https://gz.lianjia.com", "https://gz.lianjia.com/ershoufang/"),
    "杭州": ("hangzhou", "https://hz.lianjia.com", "https://hz.lianjia.com/ershoufang/"),
    "成都": ("chengdu", "https://cd.lianjia.com", "https://cd.lianjia.com/ershoufang/"),
    "武汉": ("wuhan", "https://wh.lianjia.com", "https://wh.lianjia.com/ershoufang/"),
    "合肥": ("hefei", "https://hf.lianjia.com", "https://hf.lianjia.com/ershoufang/"),
    "大连": ("dalian", "https://dl.lianjia.com", "https://dl.lianjia.com/ershoufang/")
    }


class Crawl:
    def __init__(self, city="上海", timestamp="", area="全部区域"):
        self.city = city.strip()
        self.current_time = timestamp if timestamp else time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.area = area
        self.data_dir = os.path.join(os.path.dirname(__file__), "data", city_map[self.city][0], f"{area}_{self.current_time}")
        self.csv_path = os.path.join(self.data_dir, f"{self.current_time}.csv")
        self.download_txt = os.path.join(self.data_dir, f"{self.current_time}.txt")
        self.dataset = os.path.join(self.data_dir, f"{self.current_time}.db")
        self.table_base_name = "date"
        self.host = city_map[self.city][1]
        self.esf_url = city_map[self.city][2]
        self.get_url_flag = True

    def env_init(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    @staticmethod
    def get_current_time():
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

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

    def get_block_from_url(self, url):
        """获取网页所属板块"""
        if ".html" not in url:
            print(f"{self.get_current_time()} 查找所属板块时必须是二手房详情页")
        html = self.get_page(url)
        soup = BeautifulSoup(html, 'lxml')
        ershoufang = soup.find('div', attrs={'class': 'fl l-txt'})
        info_list = ershoufang.find_all('a')
        if len(info_list) >= 4:
            return ershoufang.find_all('a')[3].get_text().replace('二手房', '')
        return ''

    def get_all_blocks_from_area(self, url, area):
        block_list = []
        html = self.get_page(url)
        soup = BeautifulSoup(html, 'lxml')
        ershoufang = soup.find('div', attrs={'data-role': 'ershoufang'})
        for a in ershoufang.find_all('div')[1].find_all('a'):
            if self.get_area_from_url(self.host + a['href']) == area:
                block_list.append(a.get_text().strip())
        return block_list

    def get_all_areas_from_city(self):
        area_list = []
        html = self.get_page(self.esf_url)
        soup = BeautifulSoup(html, 'lxml')
        ershoufang = soup.find('div', attrs={'data-role': 'ershoufang'})
        for a in ershoufang.find_all('div')[0].find_all('a'):
            if a.get_text != "上海周边":
                area_list.append(a.get_text().strip())
        return area_list

    @staticmethod
    def extract_info(html, district, block):
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
                data.append([district, block, title, url, house_type, area, direction, floor, decoration, residence,
                            region, total_price, univalence, build_time, release_time, watch, else_info])
            except Exception as e:
                print(f'{self.get_current_time()} extract_info: {e}')
        return data

    def get_region_urls(self):
        """由于链家每个区域最多只显示100页数据，因此按照城区划分会漏掉较多数据，需获取每个区域链接单独抓取所有数据"""
        host = self.host
        esf_url = self.esf_url
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
        self.get_url_flag = False
        return list(region_urls)

    # 数据存储到数据库
    def save_data_to_dataset(self, info_list):
        conn = sqlite3.connect(self.dataset)
        cursor = conn.cursor()
        for num, row_list in enumerate(info_list):
            num_str = str(num)
            if len(num_str) == 1:
                num_str = "00" + num_str
            elif len(num_str) == 2:
                num_str = "0" + num_str
            time_stamp = str(time.time()).split(".")
            table_name = self.table_base_name + time_stamp[0] + time_stamp[-1][:4] + num_str
            for info in row_list:
                cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, value TEXT)')
                cursor.execute(f"INSERT INTO {table_name} (value) VALUES (?)", (info,))
        conn.commit()
        cursor.close()
        conn.close()

    def print_setup_process(self):
        cnt = 0
        while self.get_url_flag:
            cnt += 1
            print(" " * 100, end="\r" )
            print(f"{self.get_current_time()} 正在获取所有地区的链接, 请稍等{'.' * (cnt % 7)}", end="\r")
            sys.stdout.flush()
            time.sleep(0.5)

    def crawl(self):
        fields = [
            '城市', '板块', '名称', '链接', '户型', '面积', '朝向', '楼层', '装修',
            '小区', '区域', '总价', '单价', '建成时间', '发布时间', '关注', '其他信息'
            ]
        csvf = open(self.csv_path, 'a', newline='', encoding='gb18030')
        begin_time = time.time()  # 程序开始运行时间
        cnt = 0  # 记录房源所在板块数量
        down_urls = []  # 从日志文件中获取已完成的链接
        if os.path.exists(self.download_txt):
            print(f'{self.get_current_time()} 以下板块已经被爬过:')
            with open(self.download_txt, 'r', encoding='utf-8') as f:
                for line in f.read().splitlines():
                    line = line.strip()
                    if line:
                        cnt += 1
                        print(f'{self.get_current_time()} {cnt}: {line}')
                        down_urls.append(line)
        # 日志文件，记录已抓取的子区域链接，便于恢复爬虫
        logf = open(self.download_txt, 'a', encoding='utf-8')
        writer = csv.writer(csvf, delimiter=',')  # 以逗号分割
        writer.writerow(fields)
        t_print = threading.Thread(target=self.print_setup_process)
        t_print.setDaemon(True)
        t_print.start()
        raw_region_urls = self.get_region_urls()  # 获取所有地区的链接
        region_urls = []
        if self.area != '全部区域':
            for region_url in raw_region_urls:
                if self.area == self.get_area_from_url(region_url):
                    region_urls.append(region_url)
        else:
            for region_url in raw_region_urls:
                if self.get_area_from_url(region_url) != "上海周边":
                    region_urls.append(region_url)
        total_num = len(region_urls)
        for region_url in region_urls:
            if region_url not in down_urls:
                cnt += 1
                current_area = self.get_area_from_url(region_url)
                exe_time = round(int((time.time() - begin_time))/60, 2)
                print(f'{self.get_current_time()} 总板块数: {total_num}, 当前在爬第 {cnt} 个板块, 板块所在区域：{current_area}')
                print(f'{self.get_current_time()} 板块链接: {region_url}, 已执行时间：{exe_time} 分钟')
                for page in range(1, 101):
                    print(f'{self.get_current_time()} 当前在爬第 {page} 页')
                    try:
                        area = self.get_area_from_url(region_url)
                        url = region_url + 'pg%s/' % page  # 构造链接
                        html = self.get_page(url)
                        data = self.extract_info(html, self.city, area)
                        if data:
                            writer.writerows(data)
                            self.save_data_to_dataset(data)
                        else:
                            break  # 若未获取到数据，说明已到达最后一页，退出当前循环
                    except AttributeError:
                        print(f"{self.get_current_time()} 爬虫已到达最后一页，开始获取下一区域数据\n")
                        break
                    except Exception as e:
                        print(f"{self.get_current_time()} 爬虫发生错误: ", e)
                        break
                logf.write(region_url + '\n')
        csvf.close()
        logf.close()
        print(f"{self.get_current_time()} 爬虫结束, 共耗时：{round(int((time.time() - begin_time))/60, 2)} 分钟")

    def run(self):
        self.env_init()
        self.crawl()
