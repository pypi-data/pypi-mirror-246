# Training Management Software [![Build Status](https://app.travis-ci.com/willgeminix/Training_Mgmt.svg?token=buDhdVZJqj5j61LpuHjh&branch=main)](https://app.travis-ci.com/willgeminix/Training_Mgmt)


## Overview
This software is designed to help users track and manage their health and fitness goals. It consists of several Python modules that work together to provide insights into exercise routines, dietary habits, and overall wellness.

## Main Function
### `start.py`
This module acts as the entry point for the application. It imports necessary modules and initiates the user interface for interaction.

## Subpackage 1 - Person
### `Person.py`
Defines the `Person` class, which encapsulates personal data like name, birthdate, height, weight, gender, purpose, and exercise frequency. This class is central to the application, as it holds user-specific data.

### Module 1: `calculate.py`

This module consists of functions designed to calculate various health and fitness metrics for a given person. These calculations include the Basal Metabolic Rate (BMR), Total Daily Energy Expenditure (TDEE), daily calorie needs, and macronutrient distribution. 

#### Functions:
- `bmr(person)`: Calculates the Basal Metabolic Rate based on the person's gender, weight, height, and age. The function returns the BMR as a float rounded to 2 decimal places.
- `tdee(person)`: Determines the Total Daily Energy Expenditure, which factors in the person's level of physical activity along with the BMR. The result is returned as a float rounded to 2 decimal places.
- `calorie(person)`: Estimates the daily calorie intake needed for the person based on their TDEE and fitness goal (bulking or cutting). This function incorporates a random element to simulate the variability in daily calorie needs.
- `nutrition(person)`: Provides a breakdown of the macronutrient distribution (protein, carbohydrates, and fat) based on the person's daily calorie needs. The macronutrients are calculated in grams and rounded to 2 decimal places.

#### Usage:
These functions are intended to be used in conjunction with the `Person` class from the `Training_Mgmt` module. A valid `Person` instance is required to perform the calculations, as it provides necessary personal data like age, weight, height, fitness goals, and activity level. The module is particularly useful for individuals seeking to tailor their diet and exercise plans according to specific health and fitness objectives.

### Module 2: `Record.py`

This module introduces the `Record` class, extending pandas.DataFrame (inherit from pandas.DataFrame), to manage and visualize nutrition records. It allows for tracking and analyzing dietary intake over time through various functionalities.

#### Attributes:
- `__record` (pandas.DataFrame): A private DataFrame holding the nutrition data, including dates, calorie intake, and macronutrient breakdown.

#### Methods:
- `__init__(self, nutrition)`: Initializes the Record object with a given set of nutrition data.
- `add(self, date, protein, carbon, fat)`: Adds a new nutrition record to the DataFrame. It computes total calories based on the given macronutrient values and appends the record if the date does not already exist.
- `remove(self, date)`: Removes a record corresponding to a specified date after user confirmation. The method prompts the user for confirmation before deletion.
- `modify(self, date, protein, carbon, fat)`: Modifies the nutrition data for a record on a given date. It allows updating protein, carbohydrate, and fat values and recalculates total calories.
- `show(self, start_date, end_date, indicator)`: Displays a graphical representation of nutritional data over a specified date range. The method offers an option to show either calorie data or a detailed breakdown of macronutrients.

#### Usage:
The `Record` class is designed for individuals who want to keep a detailed log of their dietary intake. It offers functionalities to add, remove, and modify records, as well as to visualize the data for easy interpretation. The class can be particularly useful for dietitians, fitness enthusiasts, or anyone interested in tracking their nutritional habits.

## Subpackage 2 - Exercise
### Module 1: `Exercise.py`

This module defines the `Exercise` class, which provides exercise recommendations based on the intensity level and targeted body parts. It is designed to offer a personalized workout plan that includes a variety of strength and cardio exercises.

#### Attributes:
- `__intensity_level` (str): Represents the exercise intensity level which can be "easy", "medium", or "hard".
- `__body_part` (list): A list of body parts that the user intends to target in their strength training sessions.
- `chest_exercises` (dict): A collection of chest-targeted exercises with corresponding video demonstrations.
- `shoulder_exercises` (dict): A collection of shoulder-targeted exercises with corresponding video demonstrations.
- `back_exercises` (dict): A collection of back-targeted exercises with corresponding video demonstrations.
- `legs_exercises` (dict): A collection of leg-targeted exercises with corresponding video demonstrations.
- `biceps_exercises` (dict): A collection of bicep-targeted exercises with corresponding video demonstrations.
- `triceps_exercises` (dict): A collection of tricep-targeted exercises with corresponding video demonstrations.
- `cardio_list` (list): A list of various cardio exercises.

#### Functions:
- `intensity_level(self)`: Property to get or set the exercise intensity level.
- `body_part(self)`: Property to get or set the targeted body parts for strength training.
- `strength_suggestion(self)`: Generates strength exercise recommendations based on the set intensity level and targeted body parts.
- `cardio_suggestion(self)`: Recommends a cardio exercise and duration based on the set intensity level.
- `hybrid_suggestion(self)`: Combines strength and cardio exercise recommendations for a holistic workout plan based on the set intensity level.
- `strength_choices_helper(self, exercise_num)`: A helper function that selects a random set of strength exercises based on the number of exercises needed and the targeted body parts.

This class allows users to create a customized exercise plan that aligns with their fitness goals, whether they are looking to bulk up, slim down, or simply maintain a healthy lifestyle.

### Module 2: `Record.py`

This module provides the `Record` class, which is designed to handle the exercise records for individuals. It facilitates the management of exercise data by allowing operations such as adding, removing, and modifying records, as well as displaying the stored data.

#### Attributes:
- `person` (Person): An instance of the `Person` class representing the individual associated with the exercise record.
- `csv_file` (str): The path to the CSV file where exercise records are stored. It is named after the person's name with "_exercise.csv" as the suffix.

#### Methods:
- `__init__(self, person)`: Constructor that initializes the `Record` object with the associated person.
- `add(self, list_of_dicts)`: Adds new entries to the exercise record. Each entry is a dictionary representing exercise data for a specific date.
- `remove_by_index(self, index_to_remove)`: Removes an entry from the exercise record based on its index within the CSV file.
- `modify(self, index, updates)`: Modifies an existing entry in the exercise record at the specified index with the provided updates.
- `display(self)`: Displays the entire exercise record in a tabular format.

#### Usage:
The `Record` class is used in conjunction with the `Person` class from the `Training_Mgmt` module. It requires a valid `Person` instance upon initialization and interacts with a CSV file to persist exercise data. This class is particularly useful for tracking workouts and progress over time.

## Usage
To use this application, run the `start.py` script. The user will be prompted to enter their personal details and health goals, which will then be used by the application to provide customized health and fitness recommendations.

## Dependencies
- Python 3
- Pandas: For data manipulation and analysis.
- Pygal (in `record.py`): For generating graphical representations of data.
- IPython (in `record.py` and `Record.py`): For displaying outputs within Jupyter Notebooks.

## Note
Please ensure that all dependencies are installed before running the application.

## Credit to
Xing (Will) Xu

Bingshen (Gevin) Yang
