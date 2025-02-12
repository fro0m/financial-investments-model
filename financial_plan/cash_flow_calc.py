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

@dataclass
class Bond(AssetBase):
    # Basic bond parameters
    face_value_rur: int  # Nominal value of the bond
    purchase_price_rur: int  # Actual price paid for the bond
    coupon_rate: float  # Annual coupon rate (e.g., 0.07 for 7%)
    coupon_frequency_months: int  # How often coupons are paid (e.g., 6 for semi-annual)
    time_to_maturity_months: int  # Total number of months until maturity
    number_of_bonds: int  # Number of bonds in the stack
    monthly_investment_rur: int  # Monthly investment in new bonds
    purchase_date: date = date.today()  # When the bond was purchased, defaults to today

    def instant_costs(self, by_month_end_index=1) -> int:
        """Initial bond purchase at month 0"""
        if by_month_end_index == 0:
            # Initial investment
            return self.purchase_price_rur * self.number_of_bonds
        return 0

    def monthly_costs(self, by_month_end_index=1) -> int:
        """Monthly investment in new bonds"""
        if by_month_end_index < self.time_to_maturity_months:
            return self.monthly_investment_rur
        return 0

    def instant_income(self, by_month_end_index=1) -> int:
        """Face value received at maturity for bonds held at that point"""
        total_bonds = self.calculate_total_bonds(by_month_end_index)
        
        # Return face value at maturity points
        if by_month_end_index > 0 and by_month_end_index % self.time_to_maturity_months == 0:
            maturing_bonds = self.calculate_maturing_bonds(by_month_end_index)
            return self.face_value_rur * maturing_bonds
        return 0

    def monthly_income(self, by_month_end_index=1) -> int:
        """Coupon payments for all bonds held"""
        total_bonds = self.calculate_total_bonds(by_month_end_index)
        
        # Coupon payments
        if by_month_end_index > 0 and by_month_end_index % self.coupon_frequency_months == 0:
            coupon_amount = self.face_value_rur * self.coupon_rate / (12 / self.coupon_frequency_months)
            return int(coupon_amount * total_bonds)
        return 0

    def calculate_total_bonds(self, by_month_end_index=1) -> int:
        """Calculate total bonds held at a given month including reinvestments"""
        if by_month_end_index == 0:
            return self.number_of_bonds
        
        total_bonds = self.number_of_bonds
        # Add bonds from monthly investments
        if by_month_end_index > 0:
            months_invested = min(by_month_end_index, self.time_to_maturity_months)
            additional_bonds = floor(self.monthly_investment_rur * months_invested / self.purchase_price_rur)
            total_bonds += additional_bonds
        return total_bonds

    def calculate_maturing_bonds(self, by_month_end_index=1) -> int:
        """Calculate number of bonds maturing at a given month"""
        if by_month_end_index % self.time_to_maturity_months == 0:
            # Calculate bonds that were bought time_to_maturity_months ago
            original_maturity = by_month_end_index == self.time_to_maturity_months
            if original_maturity:
                return self.number_of_bonds
            
            # Calculate bonds from monthly investments that are maturing
            months_to_count = self.time_to_maturity_months
            maturing_bonds = floor(self.monthly_investment_rur * months_to_count / self.purchase_price_rur)
            return maturing_bonds
        return 0

def prepare_data_frame(data: np.array, name: str):
  months_range = range(len(data)) # Ensure the range matches the length of data
  return {'months_range': months_range, name: data}