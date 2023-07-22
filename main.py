import argparse
from crawl import Crawl


area_map = {
    "上海": {"浦东", "闵行", "宝山", "徐汇", "普陀", "杨浦", "长宁", "松江", "嘉定", "黄埔", "静安", "虹口", "青浦", "奉贤", "金山", "崇明"},
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
    def __init__(self):
        pass






if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="I am a happy crawler!")
    parser.add_argument(
        "-c",
        "--city",
        dest="city",
        type=str,
        choices=["北京","上海", "广州", "深圳", "杭州" ],
        default="上海",
        help="Which city that you want to crawl"
        )
    parser.add_argument(
        "-a",
        "--area",
        dest="area",
        type=str,
        default="all",
        choices=["浦东", "闵行", "宝山", "徐汇", "普陀", "杨浦", "长宁", "松江", "嘉定", "黄埔", "静安", "虹口", "青浦", "奉贤", "金山", "崇明"],
        help="Specify area to crawl, default crawl all"
        )
    parser.add_argument(
        "-t",
        "--time_stamp",
        type=str,
        default="",
        help="Specify time stamp to crawl continue, default start new crawl"
        )
