# TU-Wien-PowerFlow-Homework1

This is a simply Project that simulates a solarPV plant connected to TU Wien. This project calculates the resulting costs for buying extra electricity since PV can not fullfil demand at all times. The given data in the csv is not accurate and should only illustrate the basic principle. All data was made up in the head.

The power_flow.py script contains four functions:

 - def read_data() processes the data provided in the .csv file.
 - def deficit_calculation() function calculates the energy deficit based on the difference between the electrical demand and the photovoltaic generation at each time step.
 - def total_cost() calculates total daily costs for a given deficit and cost per kilowatt-hour (kWh).
 - def power_flow() calculates the daily costs based on power flow data from a given file. The function reads photovoltaic generation, energy demand, and cost of energy per kilowatt-hour from the file, determines the energy deficit, and then computes the daily costs based on that deficit.
