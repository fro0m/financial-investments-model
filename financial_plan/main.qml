import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 800
    height: 600

    Item {
        width: parent.width
        height: parent.height

        Column {
            spacing: 10
            padding: 10

            TextField {
                id: nameInput
                placeholderText: "Enter RealtyObject name"
                text: "Avant"
            }

            TextField {
                id: valueInput
                placeholderText: "Enter RealtyObject value"
                text: "6000000"
            }

            TextField {
                id: instantPriceRenovationInput
                placeholderText: "Enter instant_price_renovation_rur"
                text: "2500000"
            }

            TextField {
                id: renovationPrincipalInput
                placeholderText: "Enter renovation_principal_and_interest_rur"
                text: "0"
            }

            TextField {
                id: renovationPaymentsInput
                placeholderText: "Enter renovation_principal_and_interest_payments_months"
                text: "0"
            }

            TextField {
                id: mortgagePrincipalInput
                placeholderText: "Enter realty_mortgage_principal_and_interest_rur"
                text: "254222"
            }

            TextField {
                id: mortgagePaymentsInput
                placeholderText: "Enter realty_mortgage_principal_and_interest_payments_months"
                text: "360"
            }

            TextField {
                id: capExInput
                placeholderText: "Enter cap_ex_rur"
                text: "5000"
            }

            TextField {
                id: incomeTaxInput
                placeholderText: "Enter income_tax_percentage"
                text: "0.07"
            }

            TextField {
                id: propertyManagementInput
                placeholderText: "Enter property_management_rur"
                text: "20000"
            }

            TextField {
                id: insuranceInput
                placeholderText: "Enter insurance_rur"
                text: "0"
            }

            TextField {
                id: additionalExpensesInput
                placeholderText: "Enter additional_monthly_expenses_rur"
                text: "0"
            }

            TextField {
                id: utilitiesInput
                placeholderText: "Enter utilities_rur"
                text: "0"
            }

            TextField {
                id: dateOfGettingKeysInput
                placeholderText: "Enter date_of_getting_keys"
                text: "2027-06-01"
            }

            TextField {
                id: renovationTimeInput
                placeholderText: "Enter renovation_time_months"
                text: "3"
            }

            TextField {
                id: realtyObjectPriceInput
                placeholderText: "Enter realty_object_price_rub"
                text: "22000000"
            }

            TextField {
                id: expectedRentInput
                placeholderText: "Enter expected_monthly_rent_rur"
                text: "120000"
            }

            TextField {
                id: additionalIncomeInput
                placeholderText: "Enter additional_income_rur"
                text: "0"
            }

            TextField {
                id: vacancyPercentageInput
                placeholderText: "Enter vacancy_percentage"
                text: "0.9"
            }

            TextField {
                id: cumulativePriceChangeInput
                placeholderText: "Enter cumulative_realty_price_change_monthly_rate"
                text: "0.01"
            }

            TextField {
                id: cumulativeRentChangeInput
                placeholderText: "Enter cumulative_realty_rent_change_monthly_rate"
                text: "0.01"
            }

            TextField {
                id: cumulativeInflationInput
                placeholderText: "Enter cumulative_inflation_rate"
                text: "0.02"
            }

            Button {
                text: "Add RealtyObject"
                onClicked: {
                    mainWin.add_realty_object(
                        nameInput.text, parseFloat(valueInput.text), parseFloat(instantPriceRenovationInput.text),
                        parseFloat(renovationPrincipalInput.text), parseInt(renovationPaymentsInput.text),
                        parseFloat(mortgagePrincipalInput.text), parseInt(mortgagePaymentsInput.text),
                        parseFloat(capExInput.text), parseFloat(incomeTaxInput.text), parseFloat(propertyManagementInput.text),
                        parseFloat(insuranceInput.text), parseFloat(additionalExpensesInput.text), parseFloat(utilitiesInput.text),
                        dateOfGettingKeysInput.text, parseInt(renovationTimeInput.text), parseFloat(realtyObjectPriceInput.text),
                        parseFloat(expectedRentInput.text), parseFloat(additionalIncomeInput.text), parseFloat(vacancyPercentageInput.text)
                    )
                }
            }

            Button {
                text: "Plot RealtyObjects"
                onClicked: mainWin.plot_realty_objects()
            }
        }
    }
}
