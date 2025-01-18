import os
os.environ["QT_QPA_PLATFORM"] = "xcb"

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QUrl, QObject, pyqtSlot
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from cash_flow_calc import RealtyObject, prepare_data_frame, cumulative_inflation_rate, cumulative_realty_price_change_monthly_rate, cumulative_realty_rent_change_monthly_rate
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

    @pyqtSlot()
    def plot_realty_objects(self):
        if not self.realty_objects:
            print("No realty objects to plot.")
            return

        import matplotlib.pyplot as plt
        plt.matplotlib.use('Qt5Agg')

        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(30, 15))
        axes = axes.flatten()  # Flatten the 2D array to 1D

        for realty_object in self.realty_objects:
            instant_costs = pd.DataFrame.from_dict(prepare_data_frame(realty_object.alltime_instant_costs(), f"{realty_object.name}_instant_costs"))
            monthly_costs = pd.DataFrame.from_dict(prepare_data_frame(realty_object.alltime_cumulative_monthly_costs(), f"{realty_object.name}_monthly_costs"))
            instant_income = pd.DataFrame.from_dict(prepare_data_frame(realty_object.alltime_instant_income(), f"{realty_object.name}_instant_income"))
            monthly_income = pd.DataFrame.from_dict(prepare_data_frame(realty_object.alltime_cumulative_monthly_income(), f"{realty_object.name}_monthly_income"))

            instant_costs.plot(ax=axes[0], x="months_range", y=f"{realty_object.name}_instant_costs", kind="line", fontsize=20)
            axes[0].set_title('Instant Costs', fontsize=20)
            axes[0].set_xlabel('Months Range', fontsize=20)
            axes[0].set_ylabel('Costs', fontsize=20)

            monthly_costs.plot(ax=axes[1], x="months_range", y=f"{realty_object.name}_monthly_costs", kind="line", fontsize=20)
            axes[1].set_title('Monthly Costs', fontsize=20)
            axes[1].set_xlabel('Months Range', fontsize=20)
            axes[1].set_ylabel('Costs', fontsize=20)

            instant_income.plot(ax=axes[2], x="months_range", y=f"{realty_object.name}_instant_income", kind="line", fontsize=20)
            axes[2].set_title('Instant Income', fontsize=20)
            axes[2].set_xlabel('Months Range', fontsize=20)
            axes[2].set_ylabel('Income', fontsize=20)

            monthly_income.plot(ax=axes[3], x="months_range", y=f"{realty_object.name}_monthly_income", kind="line", fontsize=20)
            axes[3].set_title('Monthly Income', fontsize=20)
            axes[3].set_xlabel('Months Range', fontsize=20)
            axes[3].set_ylabel('Income', fontsize=20)

        plt.show()

        # Additional plot for cumulative result
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20, 10))
        for realty_object in self.realty_objects:
            cumulative_result = realty_object.alltime_instant_income() + realty_object.alltime_cumulative_monthly_income() + realty_object.alltime_instant_costs() - realty_object.alltime_cumulative_monthly_costs()
            cumulative_result_df = pd.DataFrame.from_dict(prepare_data_frame(cumulative_result, f"{realty_object.name}_cumulative_result"))
            cumulative_result_df.plot(ax=ax, x="months_range", y=f"{realty_object.name}_cumulative_result", kind="line", fontsize=20)

        ax.set_title('Cumulative Result', fontsize=20)
        ax.set_xlabel('Months Range', fontsize=20)
        ax.set_ylabel('Cumulative Result', fontsize=20)
        plt.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    appManager = ApplicationManager()
    sys.exit(app.exec())