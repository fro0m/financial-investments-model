from dataclasses import dataclass
from datetime import datetime, date, timedelta
import pandas as pd
from typing import Any, Dict
from dateutil.relativedelta import relativedelta
from math import floor
import numpy as np


number_of_months : int = 30*12 # calculate for 100 years forward
average_days_in_month : float = 30.436875
cumulative_inflation_rate: np.array = np.cumprod(np.full(number_of_months, 1 + 0.09/12)) # let's say that yearly inflation is 9%
cumulative_realty_price_change_monthly_rate: np.array = np.cumprod(np.full(number_of_months, 1 + 0.10/12)) # https://www.perplexity.ai/search/srednii-rost-tseny-zhiloi-nedv-5xtf_BFOTbeLgEYBmmSPKg
cumulative_realty_rent_change_monthly_rate: np.array = np.cumprod(np.full(number_of_months, 1 + 0.04/12)) # https://www.perplexity.ai/search/srednii-rost-tseny-arendy-zhil-lhvgH9HnTGmuhlsJHdI6xg

@dataclass
class AssetBase:
  name: str
  # instant costs means a money amount you need to invest by the certain dates
  # it returns a instant costs by end of by_month_end_index
  # by_month_end_index is not inclusive
  def instant_costs(self, by_month_end_index=1) -> int:
    pass

  # calculate montly costs for a specific month
  # by_month_end_index is not inclusive
  def monthly_costs(self, by_month_end_index=1) -> int :
    pass

  # instant income means money a amount you will get by the certain dates
  # it returns a instant income by end of by_month_end_index
  # by_month_end_index is not inclusive
  def instant_income(self, by_month_end_index=1) -> int :
    pass

  # calculate a montly income for a specific month
  # by_month_end_index is not inclusive
  def monthly_income(self, by_month_end_index=1) -> int :
    pass

  def alltime_instant_income(self) -> np.array:
    """
    Calculate the instant income for all months.

    This method computes the instant income for each month over a specified
    number of months and returns the results as a NumPy array.

    Returns:
      np.array: An array containing the instant income for each month.
    """
    result: np.array = np.zeros(number_of_months)
    for current_month in range(number_of_months):
      result[current_month] = self.instant_income(current_month)
    return result

  def alltime_instant_costs(self) -> np.array:
    """
    Calculate the instant costs for all months.

    This method computes the instant costs for each month over a specified
    number of months and returns the results as a NumPy array.

    Returns:
      np.array: An array containing the instant costs for each month.
    """
    result: np.array = np.zeros(number_of_months)
    for current_month in range(number_of_months):
      result[current_month] = self.instant_costs(current_month)
    return result

  def alltime_cumulative_monthly_income(self) -> np.array:
    """
    Calculate the cumulative monthly income for all months.

    This method computes the cumulative monthly income for each month over a specified
    number of months and returns the results as a NumPy array.

    Returns:
      np.array: An array containing the cumulative monthly income for each month.
    """
    result: np.array = np.zeros(number_of_months)
    cumulative_income: int = 0
    for current_month in range(number_of_months):
      cumulative_income += self.monthly_income(current_month)
      result[current_month] = cumulative_income
    return result

  def alltime_cumulative_monthly_costs(self) -> np.array:
    """
    Calculate the cumulative monthly costs for all months.

    This method computes the cumulative monthly costs for each month over a specified
    number of months and returns the results as a NumPy array.

    Returns:
      np.array: An array containing the cumulative monthly costs for each month.
    """
    result: np.array = np.zeros(number_of_months)
    cumulative_costs: int = 0
    for current_month in range(number_of_months):
      cumulative_costs += self.monthly_costs(current_month)
      result[current_month] = cumulative_costs
    return result
  
@dataclass
class RealtyObject(AssetBase):
  # instant expences
  instant_price_rur: int # how much of personal money is going to be invested
  instant_price_renovation_rur: int # how much of personal money is going to be invested

  # mothly expences
  renovation_principal_and_interest_rur: int
  renovation_principal_and_interest_payments_months: int # how many months need to repay a loan
  realty_mortgage_principal_and_interest_rur: int # mortgage payment
  realty_mortgage_principal_and_interest_payments_months: int # how many months need to repay a loan
  cap_ex_rur: int
  income_tax_percentage: float
  property_management_rur: int
  insurance_rur: int
  additional_monthly_expenses_rur: int
  utilities_rur: int # Costs incurred by using utilities such as electricity, water, waste disposal, heating, and sewage

  # timings
  date_of_getting_keys: date
  renovation_time_months: int

  # instant income
  realty_object_price_rub: int

  # monthly income
  expected_monthly_rent_rur: int
  additional_income_rur: int
  vacancy_percentage: float

  # external market data
  cumulative_inflation_rate: np.array
  cumulative_realty_price_change_monthly_rate: np.array
  cumulative_realty_rent_change_monthly_rate: np.array

  def date_ready_to_get_income(self) -> date:
    return self.date_of_getting_keys + relativedelta(months=self.renovation_time_months)

  def instant_costs(self, by_month_end_index=1) -> int:
    
    months_to_renovation_start = floor((self.date_of_getting_keys - date.today()).days / average_days_in_month)
    if months_to_renovation_start < 0: # means that object already ready to use as current date is after date of building the realty
      instant_costs = self.instant_price_rur + self.instant_price_renovation_rur
    elif by_month_end_index > months_to_renovation_start: # means that renovation has started       
      instant_costs = self.instant_price_rur + self.instant_price_renovation_rur
    elif by_month_end_index <= months_to_renovation_start: # means that renovation has not started
      instant_costs = self.instant_price_rur 
    else:
      raise Exception("Logic error occurred")  # logic error

    return instant_costs
  
  def monthly_costs(self, by_month_end_index=1) -> int :
    if by_month_end_index > self.realty_mortgage_principal_and_interest_payments_months:
      realty_mortgage_principal_and_interest_rur = 0 # loan already covered
    else:
      realty_mortgage_principal_and_interest_rur = self.realty_mortgage_principal_and_interest_rur

    if by_month_end_index > self.renovation_principal_and_interest_payments_months:
      renovation_principal_and_interest_rur = 0 # loan already covered
    else:
      renovation_principal_and_interest_rur = self.renovation_principal_and_interest_rur
    
    result_in_current_month = (self.income_tax_percentage * self.monthly_income(by_month_end_index) + renovation_principal_and_interest_rur + \
    realty_mortgage_principal_and_interest_rur + (self.cap_ex_rur + \
    self.property_management_rur + self.insurance_rur + \
    self.additional_monthly_expenses_rur + self.utilities_rur) * cumulative_inflation_rate[by_month_end_index])

    return result_in_current_month

  def instant_income(self, by_month_end_index=1) -> int :
    return self.realty_object_price_rub * self.cumulative_realty_price_change_monthly_rate[by_month_end_index]

  def monthly_income(self, by_month_end_index=1) -> int : 
    return (self.expected_monthly_rent_rur + self.additional_income_rur) * self.vacancy_percentage * \
      self.cumulative_realty_rent_change_monthly_rate[by_month_end_index]


avant_appartment_fifth_percent_mortgage = RealtyObject(name = 'Avant 5 percent mortgage',  instant_price_rur=4000000, instant_price_renovation_rur=2500000, renovation_principal_and_interest_rur=0, renovation_principal_and_interest_payments_months=0, realty_mortgage_principal_and_interest_rur=71796, realty_mortgage_principal_and_interest_payments_months=30*12, cap_ex_rur=5000, income_tax_percentage=0.07, property_management_rur=20000, insurance_rur=0, additional_monthly_expenses_rur=0, utilities_rur=0, date_of_getting_keys=date(2027, 6, 1),  renovation_time_months=3, realty_object_price_rub=22000000, expected_monthly_rent_rur=120000, additional_income_rur=0,vacancy_percentage=0.9, cumulative_inflation_rate=cumulative_inflation_rate, cumulative_realty_price_change_monthly_rate=cumulative_realty_price_change_monthly_rate, cumulative_realty_rent_change_monthly_rate=cumulative_realty_rent_change_monthly_rate)

avant_appartment = RealtyObject(name = 'Avant',  instant_price_rur=6000000, instant_price_renovation_rur=2500000, renovation_principal_and_interest_rur=0, renovation_principal_and_interest_payments_months=0, realty_mortgage_principal_and_interest_rur=254222, realty_mortgage_principal_and_interest_payments_months=30*12, cap_ex_rur=5000, income_tax_percentage=0.07, property_management_rur=20000, insurance_rur=0, additional_monthly_expenses_rur=0, utilities_rur=0, date_of_getting_keys=date(2027, 6, 1),  renovation_time_months=3, realty_object_price_rub=22000000, expected_monthly_rent_rur=120000, additional_income_rur=0,vacancy_percentage=0.9, cumulative_inflation_rate=cumulative_inflation_rate, cumulative_realty_price_change_monthly_rate=cumulative_realty_price_change_monthly_rate, cumulative_realty_rent_change_monthly_rate=cumulative_realty_rent_change_monthly_rate)

# def calculate_income(asset: AssetBase, number_of_months = number_of_months):
#   months_range = range(number_of_months) # 30 years
#   income_from_asset_rub = list()
#   last_income_from_asset_rub = 0
#   for current_month_index in months_range:
#     last_income_from_asset_rub =  asset.instant_income(current_month_index) + asset.monthly_income(current_month_index) -  asset.instant_costs(current_month_index) - asset.monthly_costs(current_month_index)

#     income_from_asset_rub.append(last_income_from_asset_rub)
#   return {'months_range': months_range, f'{asset.name} income': income_from_asset_rub}

def prepare_data_frame(data: np.array, name: str):
  months_range = range(len(data)) # Ensure the range matches the length of data
  return {'months_range': months_range, name: data}

import matplotlib.pyplot as plt

plt.matplotlib.use('Qt5Agg')
avant_df_instant_costs = pd.DataFrame.from_dict(prepare_data_frame(avant_appartment.alltime_instant_costs(), "avant_df_instant_costs"))
avant_df_monthly_costs = pd.DataFrame.from_dict(prepare_data_frame(avant_appartment.alltime_cumulative_monthly_costs(), "avant_df_monthly_costs"))
avant_df_instant_income = pd.DataFrame.from_dict(prepare_data_frame(avant_appartment.alltime_instant_income(), "avant_df_instant_income"))
avant_df_monthly_income = pd.DataFrame.from_dict(prepare_data_frame(avant_appartment.alltime_cumulative_monthly_income(), "avant_df_monthly_income"))

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8, 6))
axes = axes.flatten()  # Flatten the 2D array to 1D

# Plot a bar graph
avant_df_instant_costs.plot(ax=axes[0], x="months_range", y="avant_df_instant_costs", kind="line")
avant_df_monthly_costs.plot(ax=axes[1], x="months_range", y="avant_df_monthly_costs", kind="line")
avant_df_instant_income.plot(ax=axes[2], x="months_range", y="avant_df_instant_income", kind="line")
avant_df_monthly_income.plot(ax=axes[3], x="months_range", y="avant_df_monthly_income", kind="line")

plt.show()

avant_df_profitability = pd.DataFrame.from_dict(prepare_data_frame(avant_appartment.alltime_instant_income()+avant_appartment.alltime_cumulative_monthly_income()+avant_appartment.alltime_instant_costs()-avant_appartment.alltime_cumulative_monthly_costs(), "avant_df_profitability"))
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))
avant_df_profitability.plot(ax=ax, x="months_range", y="avant_df_profitability", kind="line")
plt.show()