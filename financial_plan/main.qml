import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 800
    height: 600

    ScrollView {
        width: parent.width
        height: parent.height

        Column {
            spacing: 10
            padding: 10

            Label { text: "RealtyObject Name" }
            TextField {
                id: nameInput
                placeholderText: "Enter RealtyObject name"
                text: "Reality object"
            }


            Label { text: "RealtyObject Value" }
            TextField {
                id: valueInput
                placeholderText: "Enter RealtyObject value"
                text: "12500000"
            }

            Label { text: "Instant Price (RUR)" }
            TextField {
                id: instantPriceInput
                placeholderText: "Enter instant price"
                text: "2000000"
            }

            Label { text: "Instant Price Renovation (RUR)" }
            TextField {
                id: instantPriceRenovationInput
                placeholderText: "Enter instant_price_renovation_rur"
                text: "2500000"
            }

            Label { text: "Renovation Principal and Interest (RUR)" }
            TextField {
                id: renovationPrincipalInput
                placeholderText: "Enter renovation_principal_and_interest_rur"
                text: "0"
            }

            Label { text: "Renovation Payments (Months)" }
            TextField {
                id: renovationPaymentsInput
                placeholderText: "Enter renovation_principal_and_interest_payments_months"
                text: "0"
            }

            Label { text: "Mortgage Principal and Interest (RUR)" }
            TextField {
                id: mortgagePrincipalInput
                placeholderText: "Enter realty_mortgage_principal_and_interest_rur"
                text: "62952"
            }

            Label { text: "Mortgage Payments (Months)" }
            TextField {
                id: mortgagePaymentsInput
                placeholderText: "Enter realty_mortgage_principal_and_interest_payments_months"
                text: "360"
            }

            Label { text: "CapEx (RUR)" }
            TextField {
                id: capExInput
                placeholderText: "Enter cap_ex_rur"
                text: "5000"
            }

            Label { text: "Income Tax Percentage" }
            TextField {
                id: incomeTaxInput
                placeholderText: "Enter income_tax_percentage"
                text: "0.07"
            }

            Label { text: "Property Management (RUR)" }
            TextField {
                id: propertyManagementInput
                placeholderText: "Enter property_management_rur"
                text: "20000"
            }

            Label { text: "Insurance (RUR)" }
            TextField {
                id: insuranceInput
                placeholderText: "Enter insurance_rur"
                text: "0"
            }

            Label { text: "Additional Monthly Expenses (RUR)" }
            TextField {
                id: additionalExpensesInput
                placeholderText: "Enter additional_monthly_expenses_rur"
                text: "0"
            }

            Label { text: "Utilities (RUR)" }
            TextField {
                id: utilitiesInput
                placeholderText: "Enter utilities_rur"
                text: "0"
            }

            Label { text: "Date of Getting Keys" }
            TextField {
                id: dateOfGettingKeysInput
                placeholderText: "Enter date_of_getting_keys"
                text: "2027-06-01"
            }

            Label { text: "Renovation Time (Months)" }
            TextField {
                id: renovationTimeInput
                placeholderText: "Enter renovation_time_months"
                text: "3"
            }

            Label { text: "Realty Object Price (RUB)" }
            TextField {
                id: realtyObjectPriceInput
                placeholderText: "Enter realty_object_price_rub"
                text: "22000000"
            }

            Label { text: "Expected Monthly Rent (RUR)" }
            TextField {
                id: expectedRentInput
                placeholderText: "Enter expected_monthly_rent_rur"
                text: "120000"
            }

            Label { text: "Additional Income (RUR)" }
            TextField {
                id: additionalIncomeInput
                placeholderText: "Enter additional_income_rur"
                text: "0"
            }

            Label { text: "Vacancy Percentage" }
            TextField {
                id: vacancyPercentageInput
                placeholderText: "Enter vacancy_percentage"
                text: "0.9"
            }

            Label { text: "Cumulative Realty Price Change Monthly Rate" }
            TextField {
                id: cumulativePriceChangeInput
                placeholderText: "Enter cumulative_realty_price_change_monthly_rate"
                text: "0.01"
            }

            Label { text: "Cumulative Realty Rent Change Monthly Rate" }
            TextField {
                id: cumulativeRentChangeInput
                placeholderText: "Enter cumulative_realty_rent_change_monthly_rate"
                text: "0.01"
            }

            Label { text: "Cumulative Inflation Rate" }
            TextField {
                id: cumulativeInflationInput
                placeholderText: "Enter cumulative_inflation_rate"
                text: "0.02"
            }

            Button {
                text: "Add RealtyObject"
                onClicked: {
                    mainWin.add_realty_object(
                        nameInput.text, parseFloat(instantPriceInput.text), parseFloat(valueInput.text), parseFloat(instantPriceRenovationInput.text),
                        parseFloat(renovationPrincipalInput.text), parseInt(renovationPaymentsInput.text),
                        parseFloat(mortgagePrincipalInput.text), parseInt(mortgagePaymentsInput.text),
                        parseFloat(capExInput.text), parseFloat(incomeTaxInput.text), parseFloat(propertyManagementInput.text),
                        parseFloat(insuranceInput.text), parseFloat(additionalExpensesInput.text), parseFloat(utilitiesInput.text),
                        dateOfGettingKeysInput.text, parseInt(renovationTimeInput.text), parseFloat(realtyObjectPriceInput.text),
                        parseFloat(expectedRentInput.text), parseFloat(additionalIncomeInput.text), parseFloat(vacancyPercentageInput.text)
                    )
                }
            }

            // Bond Parameters
            Label { text: "Bond Parameters" }
            Label { text: "Bond Name" }
            TextField {
                id: bondNameInput
                placeholderText: "Enter Bond name"
                text: "GovBond1"
            }

            Label { text: "Face Value (RUR)" }
            TextField {
                id: bondFaceValueInput
                placeholderText: "Enter face value"
                text: "1000"
            }

            Label { text: "Purchase Price (RUR)" }
            TextField {
                id: bondPurchasePriceInput
                placeholderText: "Enter purchase price"
                text: "980"
            }

            Label { text: "Annual Coupon Rate" }
            TextField {
                id: bondCouponRateInput
                placeholderText: "Enter coupon rate (e.g., 0.07 for 7%)"
                text: "0.18"
            }

            Label { text: "Coupon Frequency (Months)" }
            TextField {
                id: bondCouponFrequencyInput
                placeholderText: "Enter coupon frequency in months"
                text: "6"
            }

            Label { text: "Time to Maturity (Months)" }
            TextField {
                id: bondMaturityInput
                placeholderText: "Enter time to maturity in months"
                text: "260"
            }

            Label { text: "Purchase Date" }
            TextField {
                id: bondPurchaseDateInput
                placeholderText: "Enter purchase date (YYYY-MM-DD)"
                text: "2025-04-01"
            }

            Label { text: "Number of Bonds" }
            TextField {
                id: bondNumberInput
                placeholderText: "Enter number of bonds"
                text: "10"
            }

            Label { text: "Monthly Investment (RUR)" }
            TextField {
                id: bondMonthlyInvestmentInput
                placeholderText: "Enter monthly investment amount"
                text: "62952"
            }

            Button {
                text: "Add Bond"
                onClicked: {
                    mainWin.add_bond(
                        bondNameInput.text,
                        parseInt(bondFaceValueInput.text),
                        parseInt(bondPurchasePriceInput.text),
                        parseFloat(bondCouponRateInput.text),
                        parseInt(bondCouponFrequencyInput.text),
                        parseInt(bondMaturityInput.text),
                        bondPurchaseDateInput.text,
                        parseInt(bondNumberInput.text),
                        parseInt(bondMonthlyInvestmentInput.text)
                    )
                }
            }

            Button {
                text: "Plot charts"
                onClicked: mainWin.plot_realty_objects()
            }
        }
    }
}
