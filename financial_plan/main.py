import os
os.environ["QT_QPA_PLATFORM"] = "xcb"

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QUrl, QObject, pyqtSlot
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from cash_flow_calc import RealtyObject, Bond, prepare_data_frame, cumulative_inflation_rate, cumulative_realty_price_change_monthly_rate, cumulative_realty_rent_change_monthly_rate
import pandas as pd
import sys
import numpy as np
from datetime import datetime

class ApplicationManager(QObject):
    def __init__(self):
        super().__init__()
        self.engine = QQmlApplicationEngine()
        self.engine.rootContext().setContextProperty("mainWin", self)
        self.engine.load(QUrl('financial_plan/main.qml'))
        self.realty_objects = []
        self.bonds = []

    @pyqtSlot(str, float, float, float, int, float, int, float, float, float, float, float, float, str, int, float, float, float, float)
    def add_realty_object(self, name, value, instant_price_renovation_rur, renovation_principal_and_interest_rur, renovation_principal_and_interest_payments_months, realty_mortgage_principal_and_interest_rur, realty_mortgage_principal_and_interest_payments_months, cap_ex_rur, income_tax_percentage, property_management_rur, insurance_rur, additional_monthly_expenses_rur, utilities_rur, date_of_getting_keys, renovation_time_months, realty_object_price_rub, expected_monthly_rent_rur, additional_income_rur, vacancy_percentage):
        date_of_getting_keys = datetime.strptime(date_of_getting_keys, "%Y-%m-%d").date()
        self.realty_objects.append(RealtyObject(
            name, value, instant_price_renovation_rur, renovation_principal_and_interest_rur,
            renovation_principal_and_interest_payments_months, realty_mortgage_principal_and_interest_rur,
            realty_mortgage_principal_and_interest_payments_months, cap_ex_rur, income_tax_percentage,
            property_management_rur, insurance_rur, additional_monthly_expenses_rur, utilities_rur,
            date_of_getting_keys, renovation_time_months, realty_object_price_rub, expected_monthly_rent_rur,
            additional_income_rur, vacancy_percentage, cumulative_inflation_rate,
            cumulative_realty_price_change_monthly_rate, cumulative_realty_rent_change_monthly_rate
        ))

    @pyqtSlot(str, int, int, float, int, int, str)
    def add_bond(self, name, face_value, purchase_price, coupon_rate, 
                coupon_frequency, maturity_months, purchase_date):
        purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d").date()
        self.bonds.append(Bond(
            name=name,
            face_value_rur=face_value,
            purchase_price_rur=purchase_price,
            coupon_rate=coupon_rate,
            coupon_frequency_months=coupon_frequency,
            time_to_maturity_months=maturity_months,
            purchase_date=purchase_date
        ))

    @pyqtSlot()
    def plot_realty_objects(self):
        if not self.realty_objects and not self.bonds:
            print("No objects to plot.")
            return

        import matplotlib.pyplot as plt
        plt.matplotlib.use('Qt5Agg')

        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(30, 15))
        axes = axes.flatten()

        all_assets = self.realty_objects + self.bonds
        for asset in all_assets:
            instant_costs = pd.DataFrame.from_dict(prepare_data_frame(
                asset.alltime_instant_costs(), f"{asset.name}_instant_costs"))
            monthly_costs = pd.DataFrame.from_dict(prepare_data_frame(
                asset.alltime_cumulative_monthly_costs(), f"{asset.name}_monthly_costs"))
            instant_income = pd.DataFrame.from_dict(prepare_data_frame(
                asset.alltime_instant_income(), f"{asset.name}_instant_income"))
            monthly_income = pd.DataFrame.from_dict(prepare_data_frame(
                asset.alltime_cumulative_monthly_income(), f"{asset.name}_monthly_income"))

            instant_costs.plot(ax=axes[0], x="months_range", 
                             y=f"{asset.name}_instant_costs", kind="line", fontsize=20)
            monthly_costs.plot(ax=axes[1], x="months_range", 
                             y=f"{asset.name}_monthly_costs", kind="line", fontsize=20)
            instant_income.plot(ax=axes[2], x="months_range", 
                              y=f"{asset.name}_instant_income", kind="line", fontsize=20)
            monthly_income.plot(ax=axes[3], x="months_range", 
                              y=f"{asset.name}_monthly_income", kind="line", fontsize=20)

        axes[0].set_title('Instant Costs', fontsize=20)
        axes[1].set_title('Monthly Costs', fontsize=20)
        axes[2].set_title('Instant Income', fontsize=20)
        axes[3].set_title('Monthly Income', fontsize=20)

        for ax in axes:
            ax.set_xlabel('Months Range', fontsize=20)
            ax.set_ylabel('Value', fontsize=20)
            ax.legend()

        plt.show()

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))
        for asset in all_assets:
            cumulative_result = asset.alltime_instant_income() + \
                              asset.alltime_cumulative_monthly_income() + \
                              asset.alltime_instant_costs() - \
                              asset.alltime_cumulative_monthly_costs()
            cumulative_result_df = pd.DataFrame.from_dict(
                prepare_data_frame(cumulative_result, f"{asset.name}_cumulative_result"))
            cumulative_result_df.plot(ax=ax, x="months_range", 
                                    y=f"{asset.name}_cumulative_result", 
                                    kind="line", fontsize=20)

        ax.set_title('Cumulative Result', fontsize=20)
        ax.set_xlabel('Months Range', fontsize=20)
        ax.set_ylabel('Cumulative Result', fontsize=20)
        ax.legend()
        plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    appManager = ApplicationManager()
    sys.exit(app.exec())