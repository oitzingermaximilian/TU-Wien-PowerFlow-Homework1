import csv

def read_data(filename):
    """
    Reads data from a CSV file and extracts relevant columns into separate lists.

    This function is designed to parse CSV files with specific columns: "day",
    "generation", "demand", and "cost_per_kwh". The values for each of these
    columns are collected into their respective lists and returned. It assumes
    that the CSV file contains headers matching these column names.

    :param filename: The path to the CSV file to be read.
    :type filename: str

    :return: A tuple containing four lists:
        1. days: List of integers representing the day values from the CSV.
        2. pv_generation: List of floats representing the PV generation values
           from the CSV.
        3. demand: List of floats representing the demand values from the CSV.
        4. cost_per_kwh: List of floats representing the cost per kWh values
           from the CSV.
    :rtype: tuple[list[int], list[float], list[float], list[float]]
    """
    days = []
    pv_generation = []
    demand = []
    cost_per_kwh = []

    with open(filename, "r", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        print("Column headers:", reader.fieldnames)
        for row in reader:
            days.append(int(row["day"]))
            pv_generation.append(float(row["generation"]))
            demand.append(float(row["demand"]))
            cost_per_kwh.append(float(row["cost_per_kwh"]))
    return days, pv_generation, demand, cost_per_kwh


def deficit_calculation(pv_generation, demand):
    """
    Calculate the energy deficit for each time step.

    The function calculates the energy deficit based on the
    difference between the electrical demand and the photovoltaic
    generation at each time step. If the demand exceeds the
    generation, the deficit is calculated as the difference. If
    generation meets or exceeds demand, the deficit is set to zero.

    :param pv_generation: A list representing the photovoltaic
        generation at each time step.
    :param demand: A list representing the electrical demand at
        each time step.
    :return: A list of energy deficit values for each time step,
        where the deficit is zero if generation meets or exceeds
        demand.
    :rtype: list
    """
    deficit = []
    for i in range(len(pv_generation)):
        deficit.append(max(0, demand[i] - pv_generation[i]))
    return deficit


def total_cost(deficit, cost_per_kwh):
    """
    Calculates total daily costs for a given deficit and cost per kilowatt-hour (kWh).
    Each day is represented by its corresponding index in the provided lists. The
    function multiplies the energy deficit for each day by its respective cost per
    kWh to obtain the daily cost and returns a list of dictionaries containing the
    details of each day's deficit, cost, and day index.

    :param deficit: A list of energy deficits in kWh for each day.
    :type deficit: list[float]
    :param cost_per_kwh: A list of costs in euros per kWh corresponding to the same
        days as the deficit array.
    :type cost_per_kwh: list[float]
    :return: A list of dictionaries where each dictionary represents the day-wise
        details, including the day index, the energy deficit in kWh, and the
        calculated cost in euros, rounded to 2 decimal places.
    :rtype: list[dict]
    """
    daily_costs = []
    for i in range(len(deficit)):
        day = i + 1
        daily_deficit = deficit[i]
        daily_cost = daily_deficit * cost_per_kwh[i]
        daily_costs.append(
            {
                "day": day,
                "deficit_kwh": daily_deficit,
                "cost_eur": round(daily_cost, 2),
            }
        )
    return daily_costs


def power_flow(filename):
    """
    Calculates the daily costs based on power flow data from a given file. The function
    reads photovoltaic generation, energy demand, and cost of energy per kilowatt-hour
    from the file, determines the energy deficit, and then computes the daily costs
    based on that deficit.

    :param filename: The path to the file containing power flow data.
    :type filename: str
    :return: The daily energy costs calculated from the power flow data.
    :rtype: list of float
    """
    days, pv_generation, demand, cost_per_kwh = read_data(filename)
    deficit = deficit_calculation(pv_generation, demand)
    daily_costs = total_cost(deficit, cost_per_kwh)
    return daily_costs


data = power_flow("power_data.csv")
print(data)
