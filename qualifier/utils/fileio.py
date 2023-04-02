# -*- coding: utf-8 -*-
"""Helper functions to load and save CSV data.

This contains a helper function for loading and saving CSV files.

"""
import csv


def load_csv(csvpath):
    """Reads the CSV file from path provided.

    Args:
        csvpath (Path): The csv file path.

    Returns:
        A list of lists that contains the rows of data from the CSV file.

    """
    with open(csvpath, "r") as csvfile:
        data = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # Skip the CSV Header
        next(csvreader)

        # Read the CSV data
        for row in csvreader:
            data.append(row)
    return data

# def save_csv(csvpath):
#     with open(csvpath, "w", newline='') as f:
#         csvwriter = csv.writer(f)
#         csvwriter.writerows(qualifying_loans)

# def save_qualifying_loans(qualifying_loans):
#     """Saves the qualifying loans to a CSV file.

#     Args:
#         qualifying_loans (list of lists): The qualifying bank loans.
#     """
#     # @TODO: Complete the usability dialog for savings the CSV Files.
#     # YOUR CODE HERE!
#    with open({save_loans_filepath}, mode='w') as csv_file: