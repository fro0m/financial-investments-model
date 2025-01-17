from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLineEdit, QLabel, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from cash_flow_calc import RealtyObject, prepare_data_frame, cumulative_inflation_rate, cumulative_realty_price_change_monthly_rate, cumulative_realty_rent_change_monthly_rate  # Import the RealtyObject class and prepare_data_frame function
import pandas as pd
import sys
import numpy as np
from datetime import datetime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Realty Objects Manager")
        self.setGeometry(100, 100, 800, 600)

        self.realty_objects = []

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter RealtyObject name")
        self.name_input.setText("Avant")
        layout.addWidget(self.name_input)

        self.value_input = QLineEdit(self)
        self.value_input.setPlaceholderText("Enter RealtyObject value")
        self.value_input.setText("6000000")
        layout.addWidget(self.value_input)

        self.instant_price_renovation_rur_input = QLineEdit(self)
        self.instant_price_renovation_rur_input.setPlaceholderText("Enter instant_price_renovation_rur")
        self.instant_price_renovation_rur_input.setText("2500000")
        layout.addWidget(self.instant_price_renovation_rur_input)

        self.renovation_principal_and_interest_rur_input = QLineEdit(self)
        self.renovation_principal_and_interest_rur_input.setPlaceholderText("Enter renovation_principal_and_interest_rur")
        self.renovation_principal_and_interest_rur_input.setText("0")
        layout.addWidget(self.renovation_principal_and_interest_rur_input)

        self.renovation_principal_and_interest_payments_months_input = QLineEdit(self)
        self.renovation_principal_and_interest_payments_months_input.setPlaceholderText("Enter renovation_principal_and_interest_payments_months")
        self.renovation_principal_and_interest_payments_months_input.setText("0")
        layout.addWidget(self.renovation_principal_and_interest_payments_months_input)

        self.realty_mortgage_principal_and_interest_rur_input = QLineEdit(self)
        self.realty_mortgage_principal_and_interest_rur_input.setPlaceholderText("Enter realty_mortgage_principal_and_interest_rur")
        self.realty_mortgage_principal_and_interest_rur_input.setText("254222")
        layout.addWidget(self.realty_mortgage_principal_and_interest_rur_input)

        self.realty_mortgage_principal_and_interest_payments_months_input = QLineEdit(self)
        self.realty_mortgage_principal_and_interest_payments_months_input.setPlaceholderText("Enter realty_mortgage_principal_and_interest_payments_months")
        self.realty_mortgage_principal_and_interest_payments_months_input.setText("360")
        layout.addWidget(self.realty_mortgage_principal_and_interest_payments_months_input)

        self.cap_ex_rur_input = QLineEdit(self)
        self.cap_ex_rur_input.setPlaceholderText("Enter cap_ex_rur")
        self.cap_ex_rur_input.setText("5000")
        layout.addWidget(self.cap_ex_rur_input)

        self.income_tax_percentage_input = QLineEdit(self)
        self.income_tax_percentage_input.setPlaceholderText("Enter income_tax_percentage")
        self.income_tax_percentage_input.setText("0.07")
        layout.addWidget(self.income_tax_percentage_input)

        self.property_management_rur_input = QLineEdit(self)
        self.property_management_rur_input.setPlaceholderText("Enter property_management_rur")
        self.property_management_rur_input.setText("20000")
        layout.addWidget(self.property_management_rur_input)

        self.insurance_rur_input = QLineEdit(self)
        self.insurance_rur_input.setPlaceholderText("Enter insurance_rur")
        self.insurance_rur_input.setText("0")
        layout.addWidget(self.insurance_rur_input)

        self.additional_monthly_expenses_rur_input = QLineEdit(self)
        self.additional_monthly_expenses_rur_input.setPlaceholderText("Enter additional_monthly_expenses_rur")
        self.additional_monthly_expenses_rur_input.setText("0")
        layout.addWidget(self.additional_monthly_expenses_rur_input)

        self.utilities_rur_input = QLineEdit(self)
        self.utilities_rur_input.setPlaceholderText("Enter utilities_rur")
        self.utilities_rur_input.setText("0")
        layout.addWidget(self.utilities_rur_input)

        self.date_of_getting_keys_input = QLineEdit(self)
        self.date_of_getting_keys_input.setPlaceholderText("Enter date_of_getting_keys")
        self.date_of_getting_keys_input.setText("2027-06-01")
        layout.addWidget(self.date_of_getting_keys_input)

        self.renovation_time_months_input = QLineEdit(self)
        self.renovation_time_months_input.setPlaceholderText("Enter renovation_time_months")
        self.renovation_time_months_input.setText("3")
        layout.addWidget(self.renovation_time_months_input)

        self.realty_object_price_rub_input = QLineEdit(self)
        self.realty_object_price_rub_input.setPlaceholderText("Enter realty_object_price_rub")
        self.realty_object_price_rub_input.setText("22000000")
        layout.addWidget(self.realty_object_price_rub_input)

        self.expected_monthly_rent_rur_input = QLineEdit(self)
        self.expected_monthly_rent_rur_input.setPlaceholderText("Enter expected_monthly_rent_rur")
        self.expected_monthly_rent_rur_input.setText("120000")
        layout.addWidget(self.expected_monthly_rent_rur_input)

        self.additional_income_rur_input = QLineEdit(self)
        self.additional_income_rur_input.setPlaceholderText("Enter additional_income_rur")
        self.additional_income_rur_input.setText("0")
        layout.addWidget(self.additional_income_rur_input)

        self.vacancy_percentage_input = QLineEdit(self)
        self.vacancy_percentage_input.setPlaceholderText("Enter vacancy_percentage")
        self.vacancy_percentage_input.setText("0.9")
        layout.addWidget(self.vacancy_percentage_input)

        self.cumulative_realty_price_change_monthly_rate_input = QLineEdit(self)
        self.cumulative_realty_price_change_monthly_rate_input.setPlaceholderText("Enter cumulative_realty_price_change_monthly_rate")
        self.cumulative_realty_price_change_monthly_rate_input.setText("0.01")  # Set a valid default value
        layout.addWidget(self.cumulative_realty_price_change_monthly_rate_input)

        self.cumulative_realty_rent_change_monthly_rate_input = QLineEdit(self)
        self.cumulative_realty_rent_change_monthly_rate_input.setPlaceholderText("Enter cumulative_realty_rent_change_monthly_rate")
        self.cumulative_realty_rent_change_monthly_rate_input.setText("0.01")  # Set a valid default value
        layout.addWidget(self.cumulative_realty_rent_change_monthly_rate_input)

        self.cumulative_inflation_rate_input = QLineEdit(self)
        self.cumulative_inflation_rate_input.setPlaceholderText("Enter cumulative_inflation_rate")
        self.cumulative_inflation_rate_input.setText("0.02")  # Set a valid default value
        layout.addWidget(self.cumulative_inflation_rate_input)

        add_button = QPushButton("Add RealtyObject", self)
        add_button.clicked.connect(self.add_realty_object)
        layout.addWidget(add_button)

        self.plot_button = QPushButton("Plot RealtyObjects", self)
        self.plot_button.clicked.connect(self.plot_realty_objects)
        layout.addWidget(self.plot_button)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_realty_object(self):
        name = self.name_input.text()
        value = float(self.value_input.text())
        instant_price_renovation_rur = float(self.instant_price_renovation_rur_input.text())
        renovation_principal_and_interest_rur = float(self.renovation_principal_and_interest_rur_input.text())
        renovation_principal_and_interest_payments_months = int(self.renovation_principal_and_interest_payments_months_input.text())
        realty_mortgage_principal_and_interest_rur = float(self.realty_mortgage_principal_and_interest_rur_input.text())
        realty_mortgage_principal_and_interest_payments_months = int(self.realty_mortgage_principal_and_interest_payments_months_input.text())
        cap_ex_rur = float(self.cap_ex_rur_input.text())
        income_tax_percentage = float(self.income_tax_percentage_input.text())
        property_management_rur = float(self.property_management_rur_input.text())
        insurance_rur = float(self.insurance_rur_input.text())
        additional_monthly_expenses_rur = float(self.additional_monthly_expenses_rur_input.text())
        utilities_rur = float(self.utilities_rur_input.text())
        date_of_getting_keys = datetime.strptime(self.date_of_getting_keys_input.text(), "%Y-%m-%d").date()
        renovation_time_months = int(self.renovation_time_months_input.text())
        realty_object_price_rub = float(self.realty_object_price_rub_input.text())
        expected_monthly_rent_rur = float(self.expected_monthly_rent_rur_input.text())
        additional_income_rur = float(self.additional_income_rur_input.text())
        vacancy_percentage = float(self.vacancy_percentage_input.text())


        self.realty_objects.append(RealtyObject(
            name, value, instant_price_renovation_rur, renovation_principal_and_interest_rur,
            renovation_principal_and_interest_payments_months, realty_mortgage_principal_and_interest_rur,
            realty_mortgage_principal_and_interest_payments_months, cap_ex_rur, income_tax_percentage,
            property_management_rur, insurance_rur, additional_monthly_expenses_rur, utilities_rur,
            date_of_getting_keys, renovation_time_months, realty_object_price_rub, expected_monthly_rent_rur,
            additional_income_rur, vacancy_percentage, cumulative_inflation_rate,
            cumulative_realty_price_change_monthly_rate, cumulative_realty_rent_change_monthly_rate
        ))

        self.name_input.clear()
        self.value_input.clear()
        self.instant_price_renovation_rur_input.clear()
        self.renovation_principal_and_interest_rur_input.clear()
        self.renovation_principal_and_interest_payments_months_input.clear()
        self.realty_mortgage_principal_and_interest_rur_input.clear()
        self.realty_mortgage_principal_and_interest_payments_months_input.clear()
        self.cap_ex_rur_input.clear()
        self.income_tax_percentage_input.clear()
        self.property_management_rur_input.clear()
        self.insurance_rur_input.clear()
        self.additional_monthly_expenses_rur_input.clear()
        self.utilities_rur_input.clear()
        self.date_of_getting_keys_input.clear()
        self.renovation_time_months_input.clear()
        self.realty_object_price_rub_input.clear()
        self.expected_monthly_rent_rur_input.clear()
        self.additional_income_rur_input.clear()
        self.vacancy_percentage_input.clear()
        self.cumulative_inflation_rate_input.clear()
        self.cumulative_realty_price_change_monthly_rate_input.clear()
        self.cumulative_realty_rent_change_monthly_rate_input.clear()

    def plot_realty_objects(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        for obj in self.realty_objects:
            profitability = obj.alltime_instant_income() + obj.alltime_cumulative_monthly_income() - obj.alltime_instant_costs() - obj.alltime_cumulative_monthly_costs()
            df_profitability = pd.DataFrame.from_dict(prepare_data_frame(profitability, f"{obj.name}_profitability"))
            df_profitability.plot(ax=ax, x="months_range", y=f"{obj.name}_profitability", kind="line", label=obj.name)
        ax.set_title('Profitability Over Time')
        ax.set_xlabel('Months')
        ax.set_ylabel('Profitability')
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())