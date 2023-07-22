import argparse

from data_crawler import Crawl


area_map = {
    "上海": {"浦东", "闵行", "宝山", "徐汇", "普陀", "杨浦", "长宁", "松江", "嘉定", "黄浦", "静安", "虹口", "青浦", "奉贤", "金山", "崇明"},
    "北京": {},
    "广州": {},
    "深圳": {},
    "杭州": {},
    "成都": {},
    "武汉": {},
    "合肥": {},
    "大连": {}
    }


class Crawler:
    def __init__(self, city, timestamp, area, operation):
        self.city = city
        self.timestamp = timestamp
        self.area = area
        self.operation = operation
        self.crawler = Crawl(city=city, timestamp=timestamp, area=area)
        
    def run(self):
        if self.operation == "crawl":
            self.crawler.run()






if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="I am a happy crawler!")
    parser.add_argument(
        "-c",
        "--city",
        dest="city",
        type=str,
        default="上海",
        choices=["北京","上海", "广州", "深圳", "杭州" ],
        help="Which city that you want to crawl"
        )
    parser.add_argument(
        "-a",
        "--area",
        dest="area",
        type=str,
        default="全部区域",
        choices=["浦东", "闵行", "宝山", "徐汇", "普陀", "杨浦", "长宁", "松江", "嘉定", "黄埔", "静安", "虹口", "青浦", "奉贤", "金山", "崇明"],
        help="Specify area to crawl, default crawl all"
        )
    parser.add_argument(
        "-t",
        "--timestamp",
        dest="timestamp",
        type=str,
        default="",
        help="Specify timestamp to crawl continue, default start new crawl"
        )
    parser.add_argument(
        "-o",
        "--operation",
        dest="operation",
        type=str,
        default="crawl",
        choices=["crawl", "parse", "graph"],
        help="Specify operation to run, default crawl data"
        )
    args = parser.parse_args()
