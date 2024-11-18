import json
import math
import typing



class BuildingData(typing.TypedDict):
    buildingId: str
    floor_area: float
    construction_cost: float
    hazard_probability: float
    inflation_rate: float
    

# Load and parse the JSON data file
def load_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)


# Calculate total projected loss with additional complexity and errors
def calculate_projected_losses(years_out: int, building_data: list[BuildingData]):
    total_loss = 0
    for building in building_data:
        floor_area = building['floor_area']
        construction_cost = building['construction_cost']
        hazard_probability = building['hazard_probability']
        inflation_rate = building['inflation_rate']

        # Calculate future cost
        """
        **Future Cost Calculation:** Calculate the future construction cost by adjusting
        the current cost using the inflation rate as an exponent. This method compounds
        the cost annually, reflecting the cumulative effect of inflation over the specified
        number of years.
        """
        future_cost = construction_cost * (1 + inflation_rate)**years_out

        # Calculate risk-adjusted loss
        """
        **Risk-Adjusted Loss Calculation:** Determine the risk-adjusted loss by modifying
        the future construction cost with the likelihood of experiencing a hazard. For each
        building, multiply its future construction cost by its hazard probability to assess
        the potential financial impact if the hazard were to occur.
        """
        # modifying this to take into account the hazard probability over the number of years
        risk_adjusted_loss = future_cost * (1 - hazard_probability)**years_out

        # Calculate present value of the risk-adjusted loss
        """
        **Discounting to Present Value:** To calculate the present value of the estimated
        future losses, apply a discounting process that reflects the principle that future
        financial losses are less valuable in today's terms. For each building, determine
        the present value by dividing the risk-adjusted cost by the discount rate plus one.
        his method translates the future financial impact into an equivalent amount in
        today's dollars, considering the time value of money.
        """
        discount_rate = 0.05  # Assuming a 5% discount rate
        # modifying this to take into account the discount rate over the years out
        present_value_loss = risk_adjusted_loss / (1 + discount_rate)**years_out

        # Calculate maintenance and total maintenance cost
        maintenance_cost = floor_area * 50  # assuming a flat rate per square meter
        # changing this to assume that the total maintenance costs is annual cost and 
        # should summed over every year
        total_maintenance_cost = maintenance_cost / (1 + discount_rate) * years_out

        # Total loss calculation
        """
        **Total Projected Loss Calculation:** Sum the present values of the estimated
        losses from all buildings to arrive at the total projected financial impact.
        This total provides a comprehensive view of the potential losses across the portfolio,
        combining all individual risk assessments.
        """
        # The requirements do not indicate the total maintenance cost should be included in the
        # total loss, so I am excluding them, but obviously this would be an important discussion
        # point with the stakeholders
        # total_loss += present_value_loss + total_maintenance_cost
        total_loss += present_value_loss

    return total_loss


# Main execution function
def main():
    data = load_data('data.json')
    years_out = 10
    total_projected_loss = calculate_projected_losses(years_out, data)
    print(f"Total Projected Loss: ${total_projected_loss:.2f}")

if __name__ == '__main__':
    main()