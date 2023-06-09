# -*- coding: utf-8 -*-
"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans.

Example:
    $ python app.py
"""
import sys
import fire
import questionary
import csv
from pathlib import Path

from qualifier.utils.fileio import load_csv#, save_csv

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value


def load_bank_data():
    """Ask for the file path to the latest banking data and load the CSV file.

    Returns:
        The bank data from the data rate sheet CSV file.
    """

    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)
    if not csvpath.exists():
        sys.exit(f"Oops! Can't find this path:{csvpath}")

    return load_csv(csvpath)

# def save_qualifying_loan():
#     """Asks the user where they would like to save their Qualifying Loans

#      Returns:
#         A Path to the CSV file they wish to save their data in
#     """
    
#     csvpath = questionary.text("Where would you like to save your Qualifying Loan Data? (.csv):").ask()
#     csvpath = Path(csvpath)

#     return csvpath


def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
        Returns the applicant's financial information.
    """

    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask() # does not allow 0 value. add code to force > 0 results or have zero value act as "no house"

    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value


def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio 
    # 20230327 currently throws err when home value = 0
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)   # does not account for a zero value
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")    # make option to pass no home value (0)

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered


def save_qualifying_loans(a):
    """Saves the qualifying loans to a CSV file.

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
    """
    # @TODO: Complete the usability dialog for savings the CSV Files.
    # YOUR CODE HERE!
    if len(a) != 0: # checks if list of qualifying loans isn't 0
        # asks user if they want to save
        save_option = questionary.select("Would you like to save the results to a .csv?", choices=["y","n"],).ask()
        # checks user input
        if save_option != "n":
            # if yes, requests where they would like to create the .csv and save the info
            csvpath = questionary.text("Where would you like to save your Qualifying Loan Data? (.csv):").ask()
            csvpath = Path(csvpath)
            # creates .csv file using user input stored in csvpath
            with open(csvpath, "w", newline='') as f: 
                csvwriter = csv.writer(f)
                csvwriter.writerows(a)
        # notifies the user that output won't be saved. 
        else: print("Qualifying Loans not saved.")
    else:
        sys.exit("No Qualifying Loans Exist. GET YOUR GAME UP!") # exits out of the program if 0 qualifying loans


def run():
    """The main function for running the script."""

    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    # Save qualifying loans
    save_qualifying_loans(qualifying_loans)


if __name__ == "__main__":
    fire.Fire(run)
