import pytest
import csv
from power_flow import (
    read_data,
    deficit_calculation,
    total_cost,
    power_flow,
)

# Test data
TEST_CSV = "test_power_data.csv"


# Fixture to create a temporary CSV file for testing
@pytest.fixture
def create_test_csv():
    test_data = [
        {"day": "1", "generation": "100", "demand": "150", "cost_per_kwh": "0.30"},
        {"day": "2", "generation": "200", "demand": "150", "cost_per_kwh": "0.4"},
        {"day": "3", "generation": "50", "demand": "200", "cost_per_kwh": "0.25"},
    ]
    with open(TEST_CSV, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file, fieldnames=["day", "generation", "demand", "cost_per_kwh"]
        )
        writer.writeheader()
        writer.writerows(test_data)
    yield TEST_CSV
    # Clean up the test file after the test
    import os

    os.remove(TEST_CSV)


# Test read_data function
def test_read_data(create_test_csv):
    days, pv_generation, demand, cost_per_kwh = read_data(create_test_csv)
    assert days == [1, 2, 3]
    assert pv_generation == [100.0, 200.0, 50.0]
    assert demand == [150.0, 150.0, 200.0]
    assert cost_per_kwh == [0.30, 0.4, 0.25]


# Test deficit_calculation function
def test_deficit_calculation():
    pv_generation = [100, 200, 50]
    demand = [150, 150, 200]
    deficit = deficit_calculation(pv_generation, demand)
    assert deficit == [50, 0, 150]


# Test total_cost function
def test_total_cost():
    deficit = [50, 0, 150]
    cost_per_kwh = [0.30, 0.4, 0.25]
    daily_costs = total_cost(deficit, cost_per_kwh)
    expected = [
        {"day": 1, "deficit_kwh": 50, "cost_eur": 15.0},
        {"day": 2, "deficit_kwh": 0, "cost_eur": 0.0},
        {"day": 3, "deficit_kwh": 150, "cost_eur": 37.5},
    ]
    assert daily_costs == expected


# Test power_flow function
def test_power_flow(create_test_csv):
    result = power_flow(create_test_csv)
    expected = [
        {"day": 1, "deficit_kwh": 50.0, "cost_eur": 15.0},
        {"day": 2, "deficit_kwh": 0, "cost_eur": 0.0},
        {"day": 3, "deficit_kwh": 150.0, "cost_eur": 37.5},
    ]
    assert result == expected
