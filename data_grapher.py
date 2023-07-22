import os
import sys

from data_crawler import Crawl
from data_parser import Parser
from matplotlib import pyplot as plt
from matplotlib import font_manager


city_area_map = {
    "shanghai": {
        "浦东": "pudong",
        "闵行": "minhang",
        "宝山": "baoshan",
        "徐汇": "xuhui",
        "普陀": "putuo",
        "杨浦": "yangpu",
        "长宁": "changning",
        "松江": "songjiang",
        "嘉定": "jiading",
        "黄浦": "huangpu",
        "静安": "jingan",
        "虹口": "hongkou",
        "青浦": "qingpu",
        "奉贤": "fengxian",
        "金山": "jinshan",
        "崇明": "chongming"
        },
    "beijing": {
        "东城": "dongcheng",
        "西城": "xicheng"
        }
    }


class Grapher:
    def __init__(self, dataset):
        self.dataset = dataset
        self.parser = Parser(dataset=dataset)
        self.dirname = os.path.dirname(dataset)
        self.block = self.dirname.split("\\")[-1].split("_")[0]
        self.date = self.dirname.split("\\")[-1].split("_")[-1][:8]
        self.crawl = Crawl()

    def display_house_num_from_diff_block(self, area):
        if area == "上海周边":
            return
        url = f'{self.crawl.esf_url}{city_area_map["shanghai"][area]}/'
        block_list = self.crawl.get_all_blocks_from_area(url=url, area=area)
        block_dict = {"其它": 0}
        table_list = self.parser.get_specify_table_from_dataset(area)
        for table in table_list:
            block = self.parser.get_block_from_table(table)
            if block in block_dict:
                block_dict[block] += 1
            elif block not in block_list:
                block_dict["其它"] += 1
            else:
                block_dict[block] = 1
        print(block_dict)
        x_labels, y_axis = zip(*sorted(block_dict.items(), key=lambda x: x[0]))
        x_axis = range(1, len(x_labels)+1)

        plt.rcParams['font.sans-serif'] = ['KaiTi']
        plt.rcParams['font.size'] = 13
        plt.figure(figsize=(12, 8))
        plot = plt.bar(x_axis, y_axis)
        plt.xticks(x_axis, x_labels)
        plt.title(label=f"{area} {self.date} 挂牌量 {sum(block_dict.values())}")
        plt.bar_label(plot, label_type="edge")
        plt.subplots_adjust(left=0.04, right=0.98)
        plt.savefig(os.path.join(self.dirname, f"{area}_{self.date}_挂牌量"))
        # plt.show()

    def display_house_unit_price_from_diff_block(self, area):
        if area == "上海周边":
            return
        url = f'{self.crawl.esf_url}{city_area_map["shanghai"][area]}/'
        block_list = self.crawl.get_all_blocks_from_area(url=url, area=area)
        block_dict = {"其它": [0, 0]}
        table_list = self.parser.get_specify_table_from_dataset(area)
        for table in table_list:
            block = self.parser.get_block_from_table(table)
            unit_price = self.parser.get_unit_price(table)
            if block in block_dict:
                block_dict[block][0] += 1
                block_dict[block][1] += unit_price
            elif block not in block_list:
                block_dict["其它"][0] += 1
                block_dict["其它"][1] += unit_price
            else:
                block_dict[block] = [1, unit_price]
        print(block_dict)
        x_labels, y_value = zip(*sorted(block_dict.items(), key=lambda x: x[0]))
        x_axis = range(1, len(x_labels)+1)
        y_axis = [value[1]//value[0] if value[0] != 0 else 0 for value in y_value]
        total_num = sum([value[0] for value in y_value])
        total_price = sum([value[1] for value in y_value])

        plt.rcParams['font.sans-serif'] = ['KaiTi']
        plt.rcParams['font.size'] = 13
        plt.figure(figsize=(12, 8))
        plot = plt.bar(x_axis, y_axis)
        plt.xticks(x_axis, x_labels)
        plt.title(label=f"{area} {self.date} 挂牌均价 {total_price//total_num if total_num != 0 else 0}")
        plt.bar_label(plot, label_type="edge")
        plt.subplots_adjust(left=0.04, right=0.98)
        plt.savefig(os.path.join(self.dirname, f"{area}_{self.date}_挂牌均价"))
        # plt.show()

    def display_house_num_from_diff_area(self):
        area_house_map = {"其它": 0}
        area_list = self.crawl.get_all_areas_from_city()
        table_list = self.parser.get_all_tabls_from_dataset()
        for table in table_list:
            area_name = self.parser.get_area_from_table(table)
            if area_name in area_house_map:
                area_house_map[area_name] += 1
            elif area_name in area_list:
                area_house_map[area_name] = 1
            else:
                area_house_map["其它"] += 1
        print(area_house_map)
        x_labels, y_axis = zip(*sorted(area_house_map.items(), key=lambda x: x[0]))
        x_axis = range(1, len(x_labels)+1)

        plt.rcParams['font.sans-serif'] = ['KaiTi']
        plt.rcParams['font.size'] = 13
        plt.figure(figsize=(12, 8))
        plot = plt.bar(x_axis, y_axis)
        plt.xticks(x_axis, x_labels)
        plt.title(label=f"{sum(area_house_map.values())}")
        plt.bar_label(plot, label_type="edge")
        plt.subplots_adjust(left=0.04, right=0.98)
        plt.savefig(os.path.join(self.dirname, f"{self.crawl.city}_{self.date}_挂牌量"))
        # plt.show()

    def run(self):
        pass

    def teardown(self):
        self.parser.teardown()
