"""
Exercise 2

For exercise 2 I created a CLI that accepts simple_loss or complex_loss as a parameter.

Parameters:
years_out: int
    the number of years to calculate the risk over
standard_discount_rate: float
    the standard discount rate to use (default is 0.05)
input: file
    this is the path of the data.json file for reading the building data

Examples:
python -m exercise2_loss_formula simple_loss 8 0.05 --input data.json
python -m exercise2_loss_formula complex_loss 8 0.05 --input data.json

Notes:
I am not 100% confident in the formulas used here.
It is important to note that I would spend a significant amount of time unit testing them
and working with subject matter experts that the formulas are 100% correct.
"""

import argparse
import time
import typing
import json
import math


class BuildingData(typing.TypedDict):
    """data type to describe the data contained for each building in data.json"""
    buildingId: str
    floor_area: float
    construction_cost: float
    hazard_probability: float
    inflation_rate: float


class BuildingLossEstimate(typing.TypedDict):
    loss_estimate: float
    runtime_seconds: float


def main():
    """entry point parses cli input and executes appropriate loss calculation"""
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(required=True)

    simple_loss = commands.add_parser("simple_loss")
    simple_loss.set_defaults(func=_simple_loss)
    simple_loss.add_argument("years_out", type=int)
    simple_loss.add_argument("standard_discount_rate", type=float, default=0.05)
    simple_loss.add_argument("--input", type=argparse.FileType("r"))

    complex_loss = commands.add_parser("complex_loss")
    complex_loss.set_defaults(func=_complex_loss)
    complex_loss.add_argument("years_out", type=int)
    complex_loss.add_argument("standard_discount_rate", type=float, default=0.05)
    complex_loss.add_argument("--input", type=argparse.FileType("r"))

    parsed = vars(parser.parse_args())

    func = parsed.pop("func")
    func(**parsed)


def load_building_data(json_input: typing.IO[str]) -> list[BuildingData]:
    return json.load(json_input)


def _simple_loss(years_out: int, standard_discount_rate: float, input: typing.IO[str]):
    """Simple loss formula from exercise 1"""
    total_start = time.perf_counter()

    load_data_start = time.perf_counter()
    buildings = load_building_data(input)
    load_data_end = time.perf_counter()
    print(f"--- Loading data took {load_data_end - load_data_start} seconds ---")

    loss_estimates: dict[str, BuildingLossEstimate] = {}
    for building_data in buildings:
        start = time.perf_counter()
        future_cost = building_data['construction_cost'] * (1 + building_data['inflation_rate'])**years_out
        risk_adjusted_loss = future_cost * (1 - building_data['hazard_probability'])**years_out
        loss_estimate = risk_adjusted_loss / (1 + standard_discount_rate)**years_out
        end = time.perf_counter()
        loss_estimates[building_data["buildingId"]] = {
            'loss_estimate': loss_estimate,
            'runtime_seconds': end - start,
        }
        
    total_loss = 0
    for building_id, loss_estimate in loss_estimates.items():
        print(f"--- Building ID: {building_id} ---")
        print(f"Over {years_out} years")
        print(f"Standard discount rate of {standard_discount_rate}")
        print(f"Simple loss estimate: {loss_estimate['loss_estimate']}")
        print(f"Took {loss_estimate['runtime_seconds']} seconds to run")
        total_loss += loss_estimate['loss_estimate']

    print(f"--- Total Loss Over All Properties: {total_loss} ---")
    total_end = time.perf_counter()
    print(f"--- Total calculation took {total_end - total_start} seconds ---")


def _complex_loss(years_out: int, standard_discount_rate: float, input: typing.IO[str]):
    """Complex loss formula"""
    total_start = time.perf_counter()

    load_data_start = time.perf_counter()
    buildings = load_building_data(input)
    load_data_end = time.perf_counter()
    print(f"--- Loading data took {load_data_end - load_data_start} seconds ---")

    loss_estimates: dict[str, BuildingLossEstimate] = {}
    for building_data in buildings:
        start = time.perf_counter()
        loss_estimate = (building_data["construction_cost"] * math.exp(building_data['inflation_rate'] * building_data['floor_area'] / 1000) * building_data['hazard_probability']) / ((1 + standard_discount_rate)**years_out)
        end = time.perf_counter()
        loss_estimates[building_data["buildingId"]] = {
            'loss_estimate': loss_estimate,
            'runtime_seconds': end - start,
        }
    
    total_loss = 0
    for building_id, loss_estimate in loss_estimates.items():
        print(f"--- Building ID: {building_id} ---")
        print(f"Over {years_out} years")
        print(f"Standard discount rate of {standard_discount_rate}")
        print(f"Complex loss estimate: {loss_estimate['loss_estimate']}")
        print(f"Took {loss_estimate['runtime_seconds']} seconds to run")
        total_loss += loss_estimate['loss_estimate']

    print(f"--- Total Loss Over All Properties: {total_loss} ---")
    total_end = time.perf_counter()
    print(f"--- Total calculation took {total_end - total_start} seconds ---")


if __name__ == "__main__":
    main()