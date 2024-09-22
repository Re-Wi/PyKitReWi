import csv


class CsvHandler:

    def __init__(self):
        self.csvData = []
        self.runData = []
        self.horizontalHeaderList = []
        self.horizontalHeaderCount = 0
        self.verticalHeaderCount = 0

    # 打开 CSV 文件
    def open_csv(self, filename, mode='r'):
        try:
            return open(filename, mode, newline='')
        except Exception as err:
            print("open_csv -->", err)

    # 关闭 CSV 文件
    def save_csv(self, filename, listData: list):
        if len(listData) <= 0:
            listData = self.csvData
        self.write_csv(filename, listData)

    # 读取 CSV 文件
    def read_csv(self, filename, dropFirstLine=True):
        self.csvData.clear()
        with self.open_csv(filename) as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if dropFirstLine == True:
                    dropFirstLine = False
                    continue
                if len(row) > 3:
                    self.csvData.append(row)
                # print(', '.join(row))

    # 写入 CSV 文件
    def write_csv(self, filename, data):
        try:
            with self.open_csv(filename, 'w') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerows(data)
        except Exception as err:
            print("write_csv -->", err)

    # 新增行到 CSV 文件
    def append_csv(self, filename, data):
        with self.open_csv(filename, 'a') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(data)

    # 从 CSV 文件删除行
    def delete_csv_row(self, filename, row_number):
        rows = []
        with self.open_csv(filename) as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                rows.append(row)

        with self.open_csv(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows([row for index, row in enumerate(rows) if index != row_number])


# 程序入口
if __name__ == '__main__':
    # 测试
    filename = '../data/example.csv'
    data = [
        ['Name', 'Age', 'City'],
        ['John', '25', 'New York'],
        ['Anna', '30', 'London']
    ]
    csvHandler = CsvHandler()
    # 写入数据到 CSV 文件
    csvHandler.write_csv(filename, data)

    # 读取并打印 CSV 文件内容
    print("CSV 文件内容：")
    csvHandler.read_csv(filename)

    # 新增一行数据
    new_data = ['Bob', '35', 'Paris']
    csvHandler.append_csv(filename, new_data)

    # 读取并打印 CSV 文件内容
    print("\n新增一行后的 CSV 文件内容：")
    csvHandler.read_csv(filename)

    # 删除第二行数据
    csvHandler.delete_csv_row(filename, 1)

    # 读取并打印 CSV 文件内容
    print("\n删除第二行后的 CSV 文件内容：")
    csvreader = csvHandler.read_csv(filename)
    print(str(csvreader))
