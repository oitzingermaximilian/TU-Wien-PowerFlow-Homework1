import csv

def read_data(filename):
    days = []
    pv_generation = []
    demand = []
    cost_per_kwh = []
    with open(filename, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        print("Column headers:", reader.fieldnames)
        for row in reader:
            days.append(int(row["day"]))
            pv_generation.append(float(row["generation"]))
            demand.append(float(row["demand"]))
            cost_per_kwh.append(float(row["cost_per_kwh"]))
    return days, pv_generation, demand, cost_per_kwh


def deficit_calculation(pv_generation, demand):
    deficit = []
    for i in range(len(pv_generation)):
        deficit.append(max(0, demand[i] - pv_generation[i]))
    return deficit

def total_cost(deficit, cost_per_kwh):
    daily_costs = []
    for i in range(len(deficit)):
        day = i + 1
        daily_deficit = deficit[i]
        daily_cost = daily_deficit * cost_per_kwh[i]
        daily_costs.append({
            "day": day,
            "deficit_kwh": daily_deficit,
            "cost_eur": round(daily_cost, 2),
        })
    return daily_costs

def power_flow(filename):
    days, pv_generation, demand, cost_per_kwh = read_data(filename)
    deficit = deficit_calculation(pv_generation, demand)
    daily_costs = total_cost(deficit, cost_per_kwh)
    return daily_costs

data = power_flow('power_data.csv')
print(data)