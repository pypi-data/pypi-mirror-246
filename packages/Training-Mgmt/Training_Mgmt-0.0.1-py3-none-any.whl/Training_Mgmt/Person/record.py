import datetime
import pandas as pd
import pygal
from IPython.display import display
from IPython.core.display import HTML


class Record(pd.DataFrame):
    """
    A class derived from pandas.DataFrame to manage and visualize nutrition records.

    Attributes
    ----------
    __record : pandas.DataFrame
        A private DataFrame to store the nutrition data.

    Methods
    -------
    add(date, protein, carbon, fat):
        Adds a new record to the DataFrame with the provided nutrition data.

    remove(date):
        Removes the record corresponding to the given date after user confirmation.

    modify(date, protein, carbon, fat):
        Modifies the nutrition data for the record corresponding to the given date after user confirmation.

    show(start_date, end_date, indicator):
        Displays a graphical representation of calorie or nutrition data between specified dates.
    """

    def __init__(self, nutrition):
        """
        Initializes the Record object as a DataFrame with the provided nutrition data.

        Parameters
        ----------
        nutrition : dict or DataFrame
            The initial nutrition data to populate the Record with.
        """
        super().__init__(nutrition)
        self.__record = nutrition

    def add(self, date, protein, carbon, fat):
        """
        Adds a new record with the provided nutrition data for the specified date.
        Calculates total calories and appends a new record if no entry exists for the date.

        Parameters
        ----------
        date : str
            The date for which to add the nutrition record.
        protein : float
            The amount of protein consumed, in grams.
        carbon : float
            The amount of carbohydrates consumed, in grams.
        fat : float
            The amount of fat consumed, in grams.

        Returns
        -------
        Record
            A new instance of Record with the updated data.
        """
        calorie = protein*4 + carbon*4 + fat*9
        new_record = pd.Series(
            {"Date": date, "Calorie": calorie, "Protein": protein, "Carbon": carbon, "Fat": fat})
        if self.__record[self.__record["Date"] == date].empty:
            new_data = self.__record.append(new_record, ignore_index=True)
        else:
            print("There has already been a record of the same date, please modify the record istead of adding a new one.")
            return Record(self.__record)
        return Record(new_data)

    def remove(self, date):
        """
        Removes the record corresponding to the given date after user confirmation.

        Parameters
        ----------
        date : str
            The date of the record to be removed.

        Returns
        -------
        Record
            A new instance of Record with the updated data.
        """
        record_to_remove = self.__record[self.__record["Date"] == date]
        if record_to_remove.empty:
            print("The record does NOT exist!")
            return Record(self.__record)
        else:
            print("Are you sure you want to delete the following record?\n",
                  record_to_remove)

        while True:
            check = input("""[1] for "YES"\n[2] for "NO and quit"\nChoice:""")
            if check == "1":
                break
            elif check == "2":
                return Record(self.__record)
            else:
                print("Invalid input, please re-enter.")
                continue

        new_data = self.__record[~(self.__record["Date"] == date)]
        return Record(new_data)

    def modify(self, date, protein, carbon, fat):
        """
        Modifies the nutrition data for the record corresponding to the given date.
        After user confirmation, updates the record with new nutrition values provided.

        Parameters
        ----------
        date : str
            The date of the record to modify.
        protein : float or str
            The new amount of protein, in grams or empty string to leave unchanged.
        carbon : float or str
            The new amount of carbohydrates, in grams or empty string to leave unchanged.
        fat : float or str
            The new amount of fat, in grams or empty string to leave unchanged.

        Returns
        -------
        Record
            A new instance of Record with the updated data.
        """
        row_to_modify = self.__record[self.__record["Date"] == date]
        if row_to_modify.empty:
            print("The record does NOT exist! Please check and try again!")
            return Record(self.__record)
        else:
            print("The record you are going to change:\n", row_to_modify)

        while True:
            check = input(
                "[1] for YES\n[2] for NO and return to the previous menu\nChoice:")
            if check == "1":
                break
            elif check == "2" or check == "q":
                return Record(self.__record)
            else:
                print("Invalid input, please re-enter.")
                continue

        if protein != '':
            self.__record.loc[row_to_modify.index[0], ("Protein",)] = protein
        if carbon != '':
            self.__record.loc[row_to_modify.index[0], ("Carbon",)] = carbon
        if fat != '':
            self.__record.loc[row_to_modify.index[0], ("Fat",)] = fat
        self.__record.loc[row_to_modify.index[0], ("Calorie",)] = self.__record.loc[row_to_modify.index[0], (
            "Protein",)]*4 + self.__record.loc[row_to_modify.index[0], ("Carbon",)]*4 + self.__record.loc[row_to_modify.index[0], ("Fat",)]*9
        new_data = self.__record
        return Record(new_data)

    def show(self, start_date, end_date, indicator=1):
        """
        Displays a graphical representation of calorie or nutrition data between specified dates.
        If indicator is 1, it shows calorie data. Otherwise, it shows a breakdown of nutrition data.

        Parameters
        ----------
        start_date : str
            The starting date for the range of records to display.
        end_date : str
            The ending date for the range of records to display.
        indicator : int, optional
            Indicator of which data to display: 1 for calories, other for nutrition breakdown.
        """
        condition = (self.__record["Date"] >= start_date) & (
            self.__record["Date"] <= end_date)
        row_to_display = self.__record[condition]
        if row_to_display.empty:
            return "There is NO record between the selected dates."

        # indicator == 1 means the user wants to display the record of Calories
        if indicator == 1:
            graph = pygal.Bar()
            graph.title = "Calorie Consumption Between {} and {}".format(
                start_date, end_date)
            graph.add("Calorie", row_to_display["Calorie"])
            graph.x_labels = row_to_display["Date"]

        # indicator != 1 means the user wants to display the record of other nutritions
        else:
            # pie chart will be used to display the nutritions of a single day
            if len(row_to_display) == 1:
                graph = pygal.Pie()
                graph.title = "Nutrition Consumption On {} (in g)".format(
                    row_to_display["Date"].values[0])
                graph.add("Protein", row_to_display["Protein"].values[0])
                graph.add("Carbon", row_to_display["Carbon"].values[0])
                graph.add("Fat", row_to_display["Fat"].values[0])

            # stackedline will be used to display the nutritions of multiple days
            else:
                graph = pygal.StackedLine(fill=True)
                graph.title = "Nutrition Consumption From {} to {} (in g)".format(
                    start_date, end_date)
                for each in row_to_display.keys()[2:]:
                    graph.add(each, row_to_display[each].to_list())
                graph.x_labels = row_to_display["Date"].to_list()

        # display the graph
        graph_svg = graph.render(is_unicode=True)
        display(HTML(graph_svg))
