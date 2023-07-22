import sqlite3


class Parser:
    def __init__(self, dataset):
        self.dataset = dataset
        self.conn = sqlite3.connect(self.dataset)
        self.cursor = self.conn.cursor()

    def get_all_tabls_from_dataset(self):
        table_list = []
        self.cursor.execute("select name from sqlite_master where type='table' order by name")
        for row in self.cursor.fetchall():
            if row:
                table_list.append(row[0])
        return table_list

    def get_specify_table_from_dataset(self, area):
        table_list = []
        for table in self.get_all_tabls_from_dataset():
            if self.get_area_from_table(table) == area:
                table_list.append(table)
        return table_list

    def get_data_from_table(self, table):
        data_list = []
        self.cursor.execute(f"SELECT * FROM {table}")
        for row in self.cursor.fetchall():
            data_list.append(row)
        return data_list

    def get_area_from_table(self, table):
        return self.get_data_from_table(table)[1][1].strip()

    def get_block_from_table(self, table):
        return self.get_data_from_table(table)[10][1].strip()

    def get_community_from_table(self, table):
        return self.get_data_from_table(table)[9][1].strip()

    def get_total_price(self, table):
        ret = self.get_data_from_table(table)[11][1]
        return int(ret.replace("万", "").replace(",", "").strip())

    def get_unit_price(self, table):
        ret = self.get_data_from_table(table)[12][1]
        return int(ret.replace("元/平", "").replace(",", "").strip())

    def teardown(self):
        self.cursor.close()
        self.conn.close()

    def run(self):
        pass
