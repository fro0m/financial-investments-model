from dataclasses import dataclass
from datetime import datetime, date, timedelta
import pandas as pd
from typing import Any, Dict
from dateutil.relativedelta import relativedelta
from math import floor
import numpy as np


number_of_months : int = 100*12 # calculate for 100 years forward
average_days_in_month : float = 30.436875
cumulative_inflation_rate: np.array = np.cumprod(np.full(number_of_months, 1 + 0.09/12)) # let's say that yearly inflation is 9%
cumulative_realty_price_change_monthly_rate: np.array = np.cumprod(np.full(number_of_months, 1 + 0.10/12)) # https://www.perplexity.ai/search/srednii-rost-tseny-zhiloi-nedv-5xtf_BFOTbeLgEYBmmSPKg
cumulative_realty_rent_change_monthly_rate: np.array = np.cumprod(np.full(number_of_months, 1 + 0.04/12)) # https://www.perplexity.ai/search/srednii-rost-tseny-arendy-zhil-lhvgH9HnTGmuhlsJHdI6xg
cumulative_cash_conservative_investment_rate: np.array = np.cumprod(np.full(number_of_months, 1 + 0.13/12)) # basic rate of investment cash to a bank deposit or goverment bonds. This is used to adjust costs as they would be invested in the conservative tools

@dataclass
class AssetBase:
  name: str
  # instant costs means a money amount you need to invest at certain dates
  # it returns a instant costs by end of by_month_end_index
  def instant_costs(self, by_month_end_index=0) -> int:
    pass

  def monthly_costs(self, by_month_end_index=0) -> int :
    pass

  # instant income means money a amount you will get at certain dates
  # it returns a instant income by end of by_month_end_index
  def instant_income(self, by_month_end_index=0) -> int :
    pass

  def monthly_income(self, by_month_end_index=0) -> int :
    pass


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
  taxes_percentage: float
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
  cumulative_cash_conservative_investment_rate: np.array

  def date_ready_to_get_income(self) -> date:
    return self.date_of_getting_keys + relativedelta(months_range=self.renovation_time_months)

  def instant_costs(self, by_month_end_index=0) -> int:
    months_to_renovation_start = floor((self.date_of_getting_keys - date.today()).days / average_days_in_month)
    if months_to_renovation_start < 0: # means that object already ready to use as current date is after date of building the realty
      instant_costs = self.instant_price_rur + self.instant_price_renovation_rur
    elif by_month_end_index > months_to_renovation_start:        
#      instant_costs = self.instant_price_rur * self.cumulative_cash_conservative_investment_rate[by_month_end_index] + self.instant_price_renovation_rur * (self.cumulative_cash_conservative_investment_rate[by_month_end_index] / self.cumulative_cash_conservative_investment_rate[by_month_end_index - months_to_renovation_start])
      instant_costs = self.instant_price_rur + self.instant_price_renovation_rur

    elif by_month_end_index >= 0 and by_month_end_index <= months_to_renovation_start:
      instant_costs =  self.instant_price_rur * self.cumulative_realty_price_change_monthly_rate[by_month_end_index] #* self.cumulative_cash_conservative_investment_rate[by_month_end_index]
    else:
      raise Exception("Logic error occurred")  # logic error
    return instant_costs
  
  def monthly_costs(self, by_month_end_index=0) -> int :
    if by_month_end_index > self.realty_mortgage_principal_and_interest_payments_months:
      realty_mortgage_principal_and_interest_rur = 0
    else:
      realty_mortgage_principal_and_interest_rur = self.realty_mortgage_principal_and_interest_rur

    if by_month_end_index > self.renovation_principal_and_interest_payments_months:
      renovation_principal_and_interest_rur = 0
    else:
      renovation_principal_and_interest_rur = self.renovation_principal_and_interest_rur

    return (self.taxes_percentage * self.monthly_income(by_month_end_index) + renovation_principal_and_interest_rur + \
    realty_mortgage_principal_and_interest_rur + (self.cap_ex_rur + \
    self.property_management_rur + self.insurance_rur + \
    self.additional_monthly_expenses_rur + self.utilities_rur) * self.cumulative_inflation_rate[by_month_end_index]) * self.cumulative_cash_conservative_investment_rate[by_month_end_index]

  def instant_income(self, by_month_end_index=0) -> int :
    return self.realty_object_price_rub * self.cumulative_realty_price_change_monthly_rate[by_month_end_index]

  def monthly_income(self, by_month_end_index=0) -> int :
    return (self.expected_monthly_rent_rur + self.additional_income_rur) * self.vacancy_percentage * self.cumulative_realty_rent_change_monthly_rate[by_month_end_index]


avant_appartment_fifth_percent_mortgage = RealtyObject(name = 'Avant 5 percent mortgage',  instant_price_rur=4000000, instant_price_renovation_rur=2500000, renovation_principal_and_interest_rur=0, renovation_principal_and_interest_payments_months=0, realty_mortgage_principal_and_interest_rur=71796, realty_mortgage_principal_and_interest_payments_months=30*12, cap_ex_rur=5000, taxes_percentage=0.07, property_management_rur=20000, insurance_rur=0, additional_monthly_expenses_rur=0, utilities_rur=0, date_of_getting_keys=date(2027, 6, 1),  renovation_time_months=3, realty_object_price_rub=22000000, expected_monthly_rent_rur=120000, additional_income_rur=0,vacancy_percentage=0.9, cumulative_inflation_rate=cumulative_inflation_rate, cumulative_realty_price_change_monthly_rate=cumulative_realty_price_change_monthly_rate, cumulative_realty_rent_change_monthly_rate=cumulative_realty_rent_change_monthly_rate,cumulative_cash_conservative_investment_rate=cumulative_cash_conservative_investment_rate)

avant_appartment = RealtyObject(name = 'Avant',  instant_price_rur=6000000, instant_price_renovation_rur=2500000, renovation_principal_and_interest_rur=0, renovation_principal_and_interest_payments_months=0, realty_mortgage_principal_and_interest_rur=254222, realty_mortgage_principal_and_interest_payments_months=30*12, cap_ex_rur=5000, taxes_percentage=0.07, property_management_rur=20000, insurance_rur=0, additional_monthly_expenses_rur=0, utilities_rur=0, date_of_getting_keys=date(2027, 6, 1),  renovation_time_months=3, realty_object_price_rub=22000000, expected_monthly_rent_rur=120000, additional_income_rur=0,vacancy_percentage=0.9, cumulative_inflation_rate=cumulative_inflation_rate, cumulative_realty_price_change_monthly_rate=cumulative_realty_price_change_monthly_rate, cumulative_realty_rent_change_monthly_rate=cumulative_realty_rent_change_monthly_rate, cumulative_cash_conservative_investment_rate=cumulative_cash_conservative_investment_rate)

def calculate_income(asset: AssetBase, number_of_months = number_of_months):
  months_range = range(number_of_months) # 30 years
  income_from_asset_rub = list()
  last_income_from_asset_rub = 0
  for current_month_index in months_range:
    last_income_from_asset_rub =  asset.instant_income(current_month_index) + asset.monthly_income(current_month_index) -  asset.instant_costs(current_month_index) - asset.monthly_costs(current_month_index)

    income_from_asset_rub.append(last_income_from_asset_rub)
  return {'months_range': months_range, f'{asset.name} income': income_from_asset_rub}

import matplotlib.pyplot as plt

plt.matplotlib.use('Qt5Agg')
number_of_months_to_plot : int = 1000
avant_df = pd.DataFrame.from_dict(calculate_income(avant_appartment, number_of_months_to_plot))
avant_appartment_fifth_percent_mortgage_df = pd.DataFrame.from_dict(calculate_income(avant_appartment_fifth_percent_mortgage, number_of_months_to_plot))

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(8, 6))  # 2 rows, 1 column

# Plot a bar graph
avant_df.plot(ax=axes[0], x="months_range", y="Avant income", kind="line")
avant_appartment_fifth_percent_mortgage_df.plot(ax=axes[1], x="months_range", y="Avant 5 percent mortgage income", kind="line")

plt.show()