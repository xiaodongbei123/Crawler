import os
import sys

from data_parser import Parser
from matplotlib import pyplot as plt
from matplotlib import font_manager

block_map = {
    "静安": ["不夜城", "曹家渡", "大宁", "江宁路", "静安寺", "南京西路", "彭浦", "西藏北路", "阳城", "永和", "闸北公园"]
    }

class Grapher:
    def __init__(self, dataset):
        self.dataset = dataset
        self.parser = Parser(dataset=dataset)
        self.dirname = os.path.dirname(dataset)

    def display_house_num_from_diff_block(self):
        block_dict = {"其它": 0}
        table_list = self.parser.get_table_from_dataset()
        for table in table_list:
            block = self.parser.get_block_from_table(table)
            if block in block_dict:
                block_dict[block] += 1
            elif block not in block_map["静安"]:
                block_dict["其它"] += 1
            else:
                block_dict[block] = 1
        print(block_dict)
        x_labels, y_axis = zip(*sorted(block_dict.items(), key=lambda x: x[0]))
        x_axis = range(1, len(x_labels)+1)

        plt.rcParams['font.sans-serif'] = ['KaiTi']
        plt.rcParams['font.size'] = 13
        plot = plt.bar(x_axis, y_axis)
        plt.xticks(x_axis, x_labels)
        plt.bar_label(plot, label_type="edge")
        plt.show()

    def display_house_unit_price_from_diff_block(self):
        block_dict = {"其它": [0, 0]}
        table_list = self.parser.get_table_from_dataset()
        for table in table_list:
            block = self.parser.get_block_from_table(table)
            unit_price = self.parser.get_unit_price(table)
            if block in block_dict:
                block_dict[block][0] += 1
                block_dict[block][1] += unit_price
            elif block not in block_map["静安"]:
                block_dict["其它"][0] += 1
                block_dict["其它"][1] += unit_price
            else:
                block_dict[block] = [1, unit_price]
        print(block_dict)
        x_labels, y_value = zip(*sorted(block_dict.items(), key=lambda x: x[0]))
        x_axis = range(1, len(x_labels)+1)
        y_axis = [value[1]//value[0] for value in y_value]
        plt.rcParams['font.sans-serif'] = ['KaiTi']
        plt.rcParams['font.size'] = 13
        plot = plt.bar(x_axis, y_axis)
        plt.xticks(x_axis, x_labels)
        plt.bar_label(plot, label_type="edge")
        plt.show()


    def run(self):
        # self.display_house_num_from_diff_block()
        self.display_house_unit_price_from_diff_block()
        self.parser.teardown()

dataset_path = "E:\\WorkSpace\\crawl_script\\data\\shanghai\\20230722175151\\20230722175151.db"
Grapher(dataset=dataset_path).run()