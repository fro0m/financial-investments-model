import unittest
import sys
import os

# Add the parent directory to the sys.path to fix the import issue
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from financial_plan.cash_flow_calc import RealtyObject, cumulative_inflation_rate, cumulative_realty_price_change_monthly_rate, cumulative_realty_rent_change_monthly_rate
from datetime import date

class TestCashFlowCalc(unittest.TestCase):
    def test_realty_object_instant_costs(self):
        realty_object = RealtyObject(
            name='Test', instant_price_rur=1000000, instant_price_renovation_rur=500000,
            renovation_principal_and_interest_rur=0, renovation_principal_and_interest_payments_months=0,
            realty_mortgage_principal_and_interest_rur=10000, realty_mortgage_principal_and_interest_payments_months=360,
            cap_ex_rur=1000, income_tax_percentage=0.1, property_management_rur=2000, insurance_rur=500,
            additional_monthly_expenses_rur=300, utilities_rur=400, date_of_getting_keys=date(2023, 1, 1),
            renovation_time_months=6, realty_object_price_rub=2000000, expected_monthly_rent_rur=15000,
            additional_income_rur=0, vacancy_percentage=0.9, cumulative_inflation_rate=cumulative_inflation_rate,
            cumulative_realty_price_change_monthly_rate=cumulative_realty_price_change_monthly_rate,
            cumulative_realty_rent_change_monthly_rate=cumulative_realty_rent_change_monthly_rate
        )
        self.assertEqual(realty_object.instant_costs(1), 1500000)

    def test_realty_object_monthly_costs(self):
        realty_object = RealtyObject(
            name='Test', instant_price_rur=1000000, instant_price_renovation_rur=500000,
            renovation_principal_and_interest_rur=0, renovation_principal_and_interest_payments_months=0,
            realty_mortgage_principal_and_interest_rur=10000, realty_mortgage_principal_and_interest_payments_months=360,
            cap_ex_rur=1000, income_tax_percentage=0.1, property_management_rur=2000, insurance_rur=500,
            additional_monthly_expenses_rur=300, utilities_rur=400, date_of_getting_keys=date(2023, 1, 1),
            renovation_time_months=6, realty_object_price_rub=2000000, expected_monthly_rent_rur=15000,
            additional_income_rur=0, vacancy_percentage=0.9, cumulative_inflation_rate=cumulative_inflation_rate,
            cumulative_realty_price_change_monthly_rate=cumulative_realty_price_change_monthly_rate,
            cumulative_realty_rent_change_monthly_rate=cumulative_realty_rent_change_monthly_rate
        )
        self.assertAlmostEqual(realty_object.monthly_costs(1), 15622.25, places=2)

    def test_realty_object_instant_income(self):
        realty_object = RealtyObject(
            name='Test', instant_price_rur=1000000, instant_price_renovation_rur=500000,
            renovation_principal_and_interest_rur=0, renovation_principal_and_interest_payments_months=0,
            realty_mortgage_principal_and_interest_rur=10000, realty_mortgage_principal_and_interest_payments_months=360,
            cap_ex_rur=1000, income_tax_percentage=0.1, property_management_rur=2000, insurance_rur=500,
            additional_monthly_expenses_rur=300, utilities_rur=400, date_of_getting_keys=date(2023, 1, 1),
            renovation_time_months=6, realty_object_price_rub=2000000, expected_monthly_rent_rur=15000,
            additional_income_rur=0, vacancy_percentage=0.9, cumulative_inflation_rate=cumulative_inflation_rate,
            cumulative_realty_price_change_monthly_rate=cumulative_realty_price_change_monthly_rate,
            cumulative_realty_rent_change_monthly_rate=cumulative_realty_rent_change_monthly_rate
        )
        self.assertAlmostEqual(realty_object.instant_income(1), 2033472.22, places=2)

    def test_realty_object_monthly_income(self):
        realty_object = RealtyObject(
            name='Test', instant_price_rur=1000000, instant_price_renovation_rur=500000,
            renovation_principal_and_interest_rur=0, renovation_principal_and_interest_payments_months=0,
            realty_mortgage_principal_and_interest_rur=10000, realty_mortgage_principal_and_interest_payments_months=360,
            cap_ex_rur=1000, income_tax_percentage=0.1, property_management_rur=2000, insurance_rur=500,
            additional_monthly_expenses_rur=300, utilities_rur=400, date_of_getting_keys=date(2023, 1, 1),
            renovation_time_months=6, realty_object_price_rub=2000000, expected_monthly_rent_rur=15000,
            additional_income_rur=0, vacancy_percentage=0.9, cumulative_inflation_rate=cumulative_inflation_rate,
            cumulative_realty_price_change_monthly_rate=cumulative_realty_price_change_monthly_rate,
            cumulative_realty_rent_change_monthly_rate=cumulative_realty_rent_change_monthly_rate
        )
        self.assertAlmostEqual(realty_object.monthly_income(1), 13590.15, places=2)

if __name__ == '__main__':
    unittest.main()
