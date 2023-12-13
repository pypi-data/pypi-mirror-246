import pandas as pd
import os

from Training_Mgmt.Person import Person

# exercise record class


class Record():

    """
    This class represents an exercise record for a person. It allows adding, removing, modifying,
    and displaying exercise data stored in a CSV file.

    Attributes:
        person (Person): The person associated with this exercise record.
        csv_file (str): The name of the CSV file used to store exercise data.
    """

    def __init__(self, person):
        """
        Initialize an Exercise Record object.

        Args:
            person (Person): The person associated with this exercise record.
        """
        self.person = person
        self.csv_file = person.name+"_exercise.csv"

    def add(self, list_of_dicts):
        """
        Add exercise data to the record.

        Args:
            list_of_dicts (list): A list of dictionaries containing exercise data.

        Notes:
            - Each dictionary should contain keys such as "date," "exercise_name," "exercise_set," and "exercise_rep."
        """

        if not list_of_dicts:
            return

        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(list_of_dicts)

        # Check if the file exists
        file_exists = os.path.isfile(self.csv_file)

        # If file exists, calculate the starting index as one plus the last index in the file
        if file_exists:
            existing_df = pd.read_csv(self.csv_file)
            if not existing_df.empty:
                # Start from the next index after the last one
                start_index = existing_df.index[-1] + 1
            else:
                start_index = 0
        else:
            start_index = 0

        # Add an index column starting from the calculated start_index
        df.index = range(start_index, start_index + len(df))

        # # Reset the index to make the index column part of the DataFrame
        # df.reset_index(inplace=True)

        # Write DataFrame to CSV, append if file exists, otherwise write new
        df.to_csv(self.csv_file, mode='a', index=True,
                  header=not file_exists, index_label='ID')

    def remove_by_index(self, index_to_remove):
        """
        Remove exercise data from the record by index.

        Args:
            index (int): The index of the exercise data to be removed (1-based index).

        Notes:
            - The index specifies the entry to be removed from the record.
        """
        # Check if the file exists
        if not os.path.isfile(self.csv_file):
            print("File does not exist.")
            return

        # Read CSV file with 'ID' as the index
        df = pd.read_csv(self.csv_file, index_col='ID')

        # Check if the index to remove is in the current index range
        if index_to_remove not in df.index:
            print(f"Index {index_to_remove} not found in the file.")
            return

        # Remove the row with the given index
        df = df.drop(index_to_remove)

        # Reset the index
        df.reset_index(drop=True, inplace=True)

        # Write the updated DataFrame back to the CSV, including the index
        df.to_csv(self.csv_file, index=True, index_label='ID')

    def modify(self, index, updates):
        """
        Modify exercise data in the record.

        Args:
            index (int): The index of the exercise data to be modified (1-based index).
            updates (dict): A dictionary containing the updated exercise data.

        Notes:
            - The index specifies the entry to be modified.
            - The updates dictionary should contain keys matching the exercise data columns to be updated.
        """

        # Check if the CSV file exists
        if not os.path.isfile(self.csv_file):
            print("CSV file does not exist.")
            return

        # Read the CSV file into a DataFrame using 'ID' as the index
        df = pd.read_csv(self.csv_file, index_col='ID')

        # Check if the id to modify exists in the DataFrame
        if index not in df.index:
            print(f"ID {index} not found in the CSV file.")
            return

        # Update the row with the specified ID
        for key, value in updates.items():
            if key in df.columns:
                df.at[index, key] = value
            else:
                print(f"Column {key} does not exist in the CSV file.")

        # Write the modified DataFrame back to the CSV file, maintaining the 'ID' column
        df.to_csv(self.csv_file, index=True, index_label='ID')

    def display(self):
        """
        Display the exercise data stored in the record.
        """
        df = pd.read_csv(self.csv_file)
        print(df.to_string(index=False))
