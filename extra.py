import csv
class CSV():
    def __init__(self) -> None:
        pass
    def read_csv(self, filename):
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            data = []
            for row in reader:
                 data.append(row[0])
            return data

    def append_csv(self,filename, row):
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(row)

    def remove_csv(self,filename, name):
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            data = []
            for row in reader:
                if row[0] != name:
                    data.append(row)