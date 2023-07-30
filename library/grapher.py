import os
import sys

from library.crawler import Crawler
from library.parser import Parser
from matplotlib import pyplot as plt
from matplotlib import font_manager


class Grapher:
    def __init__(self, database, crawl):
        self.database = database
        self.parser = Parser(database=database)
        self.database_dir = os.path.dirname(database)
        self.block =self.database_dir.split("\\")[-1].split("_")[0]
        self.date =self.database_dir.split("\\")[-1].split("_")[-1][:8]
        self.crawl = crawl

    def parse_specify_area_house_num(self, area):
        if area not in self.crawl.area_list:
            return
        url = f"{self.crawl.esf_url}{self.crawl.json_info['area'][area]}/"
        block_list = self.crawl.get_all_blocks_from_area(url=url, area=area)
        block_dict = {"其它": 0}
        table_list = self.parser.get_specify_table_from_database(area)
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
        plt.subplots_adjust(left=0.06, right=0.94)
        plt.savefig(os.path.join(self.database_dir, f"{area}_{self.date}_挂牌量"))
        # plt.show()

    def parse_specify_area_unit_price(self, area):
        if area not in self.crawl.area_list:
            return
        url = f"{self.crawl.esf_url}{self.crawl.json_info['area'][area]}/"
        block_list = self.crawl.get_all_blocks_from_area(url=url, area=area)
        block_dict = {"其它": [0, 0]}
        table_list = self.parser.get_specify_table_from_database(area)
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
        plt.subplots_adjust(left=0.06, right=0.94)
        plt.savefig(os.path.join(self.database_dir, f"{area}_{self.date}_挂牌均价"))
        # plt.show()

    def parse_all_area_house_num(self):
        area_house_map = {"其它": 0}
        area_list = self.crawl.area_list
        table_list = self.parser.get_all_tabls_from_database()
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
        plt.title(label=f"{self.crawl.city} {self.date} 挂牌量 {sum(area_house_map.values())}")
        plt.bar_label(plot, label_type="edge")
        plt.subplots_adjust(left=0.06, right=0.94)
        plt.savefig(os.path.join(self.database_dir, f"{self.crawl.city}_{self.date}_挂牌量"))
        # plt.show()

    def get_specify_area_house_num(self, area, database):
        grapher = Grapher(database=database, crawl=self.crawl)
        table_list = grapher.parser.get_specify_table_from_database(area=area)
        date = grapher.date
        grapher.parser.teardown()
        del grapher
        return date, len(table_list)

    def get_all_area_house_num(self, database):
        grapher = Grapher(database=database, crawl=self.crawl)
        table_list = grapher.parser.get_all_tabls_from_database()
        date = grapher.date
        grapher.parser.teardown()
        del grapher
        return date, len(table_list)

    def parse_house_num_tendency(self, dir_path):
        data_list = []
        house_map = {}
        for dir_name in os.listdir(dir_path):
            sub_dir = os.path.join(dir_path, dir_name)
            if not os.path.isdir(sub_dir):
                continue
            for file in os.listdir(sub_dir):
                if ".db" in file:
                    data_list.append(os.path.join(sub_dir, file))
        for file in data_list:
            house_data = self.get_all_area_house_num(file)
            house_map.update({house_data[0]: house_data[1]})
        print(house_map)

        x_labels, y_axis = zip(*sorted(house_map.items(), key=lambda x: int(x[0])))
        x_axis = range(1, len(x_labels)+1)
        plt.rcParams['font.sans-serif'] = ['KaiTi']
        plt.rcParams['font.size'] = 13
        plt.figure(figsize=(12, 8))
        plot = plt.plot(x_axis, y_axis)
        plt.xticks(x_axis, x_labels)
        plt.title(label=f"{self.crawl.city} {self.date} 挂牌量趋势")
        plt.subplots_adjust(left=0.06, right=0.94)
        for x, y in zip(x_axis, y_axis):
            plt.text(x, y, y, ha="center", va="bottom")
        plt.savefig(os.path.join(self.database_dir, f"{self.crawl.city}_{self.date}_挂牌量趋势"))
        # plt.show()

    def parse_specify_area_house_num_tendency(self, dir_path, area):
        data_list = []
        house_map = {}
        for dir_name in os.listdir(dir_path):
            sub_dir = os.path.join(dir_path, dir_name)
            if not os.path.isdir(sub_dir):
                continue
            for file in os.listdir(sub_dir):
                if ".db" in file:
                    data_list.append(os.path.join(sub_dir, file))
        for file in data_list:
            house_data = self.get_specify_area_house_num(area, file)
            house_map.update({house_data[0]: house_data[1]})
        print(house_map)

        x_labels, y_axis = zip(*sorted(house_map.items(), key=lambda x: int(x[0])))
        x_axis = range(1, len(x_labels)+1)
        plt.rcParams['font.sans-serif'] = ['KaiTi']
        plt.rcParams['font.size'] = 13
        plt.figure(figsize=(12, 8))
        plot = plt.plot(x_axis, y_axis)
        plt.xticks(x_axis, x_labels)
        plt.title(label=f"{area} {self.date} 挂牌量趋势")
        plt.subplots_adjust(left=0.06, right=0.94)
        for x, y in zip(x_axis, y_axis):
            plt.text(x, y, y, ha="center", va="bottom")
        plt.savefig(os.path.join(self.database_dir, f"{area}_{self.date}_挂牌量趋势"))
        # plt.show()

    def run(self):
        pass

    def teardown(self):
        self.parser.teardown()
