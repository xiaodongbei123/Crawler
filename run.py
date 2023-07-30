import os
import sys
import time
import argparse

from library.crawler import Crawler
from library.grapher import Grapher


class Runner:
    def __init__(self, city, area, timestamp, database):
        self.city = city
        self.timestamp = timestamp if timestamp else time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.area = area
        self.crawler = Crawler(city=city, timestamp=timestamp, area=area)
        self.database = database
        self.env_setup()

    def env_setup(self):
        current_dir = os.getcwd()
        config_dir = os.path.join(current_dir, "config")
        library_dir = os.path.join(current_dir, "library")
        if config_dir not in sys.path:
            sys.path.append(config_dir)
        if library_dir not in sys.path:
            sys.path.append(library_dir)

    def parse_all_area_data(self, grapher):
        city_database_dir = os.path.dirname(grapher.database_dir)
        grapher.parse_all_area_house_num()
        grapher.parse_house_num_tendency(city_database_dir)
        for area in self.crawler.area_list:
            grapher.parse_specify_area_house_num(area)
            grapher.parse_specify_area_unit_price(area)
            grapher.parse_specify_area_house_num_tendency(city_database_dir, area)

    def parse_specify_area_data(self, grapher, area):
        city_database_dir = os.path.dirname(grapher.database_dir)
        grapher.parse_specify_area_house_num(area)
        grapher.parse_specify_area_unit_price(area)
        grapher.parse_specify_area_house_num_tendency(city_database_dir, area)

    def graph_run(self, database):
        if os.path.exists(database):
            self.grapher = Grapher(database=database, crawl=self.crawler)
            if self.area == "全部区域":
                self.parse_all_area_data(self.grapher)
            else:
                self.parse_specify_area_data(self.grapher, self.area)
            self.grapher.teardown()
        else:
            print(f"{database} is not existed!")

    def run(self):
        if not self.database:
            self.crawler.run()
            self.graph_run(self.crawler.database)
        else:
            self.graph_run(self.database)


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
        "-d",
        "--database",
        dest="database",
        type=str,
        default="",
        help="Specify database to parse, default none"
        )

    args = parser.parse_args()
    Runner(
        city=args.city,
        area=args.area,
        timestamp=args.timestamp,
        database=args.database
        ).run()
