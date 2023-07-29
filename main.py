import os
import sys
import time
import argparse

from data_crawler import Crawl
from data_grapher import Grapher


area_map = {
    "上海": ["浦东", "闵行", "宝山", "徐汇", "普陀", "杨浦", "长宁", "松江", "嘉定", "黄浦", "静安", "虹口", "青浦", "奉贤", "金山", "崇明"],
    "北京": ["东城", "西城", "朝阳", "海淀", "丰台", "石景山", "通州", "昌平", "大兴", "亦庄开发区", "顺义", "房山", "门头沟", "平谷", "怀柔", "密云", "延庆"],
    "广州": ["天河", "越秀", "荔湾", "海珠", "番禺", "白云", "黄埔", "从化", "增城", "花都", "南沙", "南海", "顺德"],
    "深圳": ["罗湖", "福田", "南山", "盐田", "宝安", "龙岗", "龙华", "光明", "坪山", "大鹏新区"],
    "杭州": ["西湖", "钱塘", "临平", "下城", "拱墅", "上城", "滨江", "余杭", "萧山", "桐庐", "淳安", "建德", "富阳", "临安"],
    "成都": ["锦江", "青羊", "武侯", "高新", "成华", "金牛", "天府新区", "高新西", "双流", "温江", "郫都", "龙泉驿", "新都", "天府新区南区", "青白江", "都江堰", "彭州", "简阳", "新津", "崇州", "大邑", "金堂", "蒲江", "邛崃"],
    "武汉": ["江岸", "江汉", "硚口", "东西湖", "武昌", "青山", "洪山", "汉阳", "东湖高新", "江夏", "蔡甸", "黄陂", "新洲", "沌口开发区", "汉南"],
    "合肥": ["包河", "巢湖市", "庐江县", "空港经济示范区", "蜀山", "庐阳", "瑶海", "政务", "滨湖新区", "经开", "高新", "新站", "肥东", "肥西", "长丰"],
    "大连": ["甘井子", "沙河口", "中山", "西岗", "高新园区", "开发区", "金州", "旅顺口", "普兰店", "瓦房店"]
    }


class Crawler:
    def __init__(self, city, timestamp, area, operation, dataset, dataset_dir):
        self.city = city
        self.timestamp = timestamp if timestamp else time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.area = area
        self.operation = operation
        self.crawler = Crawl(city=city, timestamp=timestamp, area=area)
        self.dataset = dataset
        self.dataset_dir = dataset_dir
        self.env_init()

    def env_init(self):
        if (self.operation == "graph") and ((not self.dataset) or (not self.dataset_dir)):
            print("Operation is graph but dataset or dataset dir is None")
            sys.exit(1)
        if (self.area != "全部区域") and (self.area not in area_map[self.city]):
            print(f"{self.area}是无效的，{self.city}的所有区域为{area_map[self.city]}".replace("[", ": ").replace("]", ""))
            sys.exit(1)

    def display_all_area_data(self, grapher):
        # grapher.display_house_num_from_diff_area()
        # for area in self.crawler.get_all_areas_from_city():
        #     grapher.display_house_num_from_diff_block(area)
        #     grapher.display_house_unit_price_from_diff_block(area)
        # grapher.display_house_num_history(os.path.dirname(grapher.dirname))
        grapher.display_specify_area_house_num_tendency(os.path.dirname(grapher.dirname), "静安")

    def display_specify_area_data(self, grapher, area):
        grapher.display_house_num_from_diff_block(area)
        grapher.display_house_unit_price_from_diff_block(area)

    def graph_run(self, dataset):
        if os.path.exists(dataset):
            self.grapher = Grapher(dataset=dataset)
            if self.area == "全部区域":
                self.display_all_area_data(self.grapher)
            else:
                self.display_specify_area_data(self.grapher, self.area)
            self.grapher.teardown()
        else:
            print(f"{dataset} is not existed!")

    def run(self):
        if self.operation == "crawl":
            self.crawler.run()
            self.graph_run(self.crawler.dataset)
        elif self.operation == "graph":
            self.graph_run(self.dataset)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="I am a happy crawler!")
    parser.add_argument(
        "-c",
        "--city",
        dest="city",
        type=str,
        default="上海",
        choices=["北京","上海", "广州", "深圳", "杭州", "成都", "武汉", "合肥", "大连"],
        help="Which city that you want to crawl"
        )
    parser.add_argument(
        "-a",
        "--area",
        dest="area",
        type=str,
        default="全部区域",
        help="Specify area to crawl, default crawl all area"
        )
    parser.add_argument(
        "-t",
        "--timestamp",
        dest="timestamp",
        type=str,
        default="",
        help="Specify timestamp to crawl continue, default start new crawler"
        )
    parser.add_argument(
        "-o",
        "--operation",
        dest="operation",
        type=str,
        default="crawl",
        choices=["crawl", "graph"],
        help="Specify operation to run, default crawl data"
        )
    parser.add_argument(
        "-d",
        "--dataset",
        dest="dataset",
        type=str,
        default="",
        help="Specify dataset to parse, default skip"
        )
    parser.add_argument(
        "-p",
        "--dataset_dir",
        dest="dataset_dir",
        type=str,
        default="",
        help="Specify dataset dir to parse, default skip"
        )

    args = parser.parse_args()
    Crawler(
        city=args.city,
        area=args.area,
        timestamp=args.timestamp,
        operation=args.operation,
        dataset=args.dataset,
        dataset_dir=args.dataset_dir
        ).run()
