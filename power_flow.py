import csv

def read_data(filename):
    days = []
    pv_generation = []
    demand = []
    with open(filename, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        print("Column headers:", reader.fieldnames)
        for row in reader:
            days.append(int(row["day"]))
            pv_generation.append(float(row["generation"]))
            demand.append(float(row["demand"]))
    return days, pv_generation, demand


def power_deficit(pv_generation, demand):
    deficit = []
    for i in range(len(pv_generation)):
        deficit.append(max(0,demand[i] - pv_generation[i]))
    return deficit



data = read_data('power_data.csv')
print(data)
deficit = power_deficit(data[1], data[2])
print(deficit)