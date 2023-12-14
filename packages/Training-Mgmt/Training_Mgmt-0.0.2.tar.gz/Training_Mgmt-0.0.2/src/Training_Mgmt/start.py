from Training_Mgmt.Person import Person, calculate, record
from Training_Mgmt.Exercise import Record as Exercise_Record
from Training_Mgmt.Exercise import Exercise as Exercise
import os
import sys
import pandas as pd
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def start():

    try:
        name = input("Please enter the user name:")
        basic_info = pd.read_csv(name+"_person.csv")
        person = Person.Person(basic_info["Name"][0], basic_info["Birthdate"][0], basic_info['Height'][0],
                               basic_info['Weight'][0], basic_info['Gender'][0], basic_info['Purpose'][0], basic_info['Frequency'][0])
        nutrition_data = pd.read_csv(name+"_nutrition.csv")
        record_nutrition = record.Record(nutrition_data)
        exercise_record = Exercise_Record.Record(person)
        record_exercise = pd.read_csv(name+"_exercise.csv")
    except FileNotFoundError:
        print('The user does NOT exist')
        check = input(
            "Do you want to create the user?\n[1]: YES\n[q] to quit\n[any] for NO:\nChoice:")
        if check == '1':
            print('Please create your user.')
            # create the user record file
            basic_info = create()
            basic_info.to_csv(basic_info['Name'][0]+"_person.csv", index=False)
            # create the nutrition record file
            df_nutrition = pd.DataFrame(
                {'Date': [], 'Calorie': [], 'Protein': [], 'Carbon': [], 'Fat': []})
            df_nutrition.to_csv(
                basic_info['Name'][0]+"_nutrition.csv", index=False)
            # create the exercise record file
            df_exercise = pd.DataFrame({'ID': [], 'date': [], 'exercise_name': [
            ], 'exercise_set': [], 'exercise_rep': []})
            df_exercise.to_csv(basic_info['Name']
                               [0]+"_exercise.csv", index=False)
            start()
            return None
        elif check == 'q':
            print('Thank you for using, see you!')
            return None
        else:
            print("Please try another user name.")
            start()
            return None

    while True:
        # main menu: choice_1
        choice_1 = input(
            'What do you want to do:\n[1]: Calculate Nutrition\n[2]: Manipulate the Nutrition Record\n[3]: Exercise Suggestion\n[4]: Manipulate Exercise Record\n[5]: Change Person information\n[6]: Exit\nChoice:')
        if choice_1 not in ['1', '2', '3', '4', '5', '6']:
            print("Invalid choice, please try again.")
            continue

        # function 6: save the file and exit the software
        elif choice_1 == '6':
            basic_info.to_csv(str(person.name)+"_person.csv", index=False)
            record_nutrition.to_csv(
                str(person.name)+"_nutrition.csv", index=False)
            print("Thank you for using, see you!")
            break

        # function 1: calculate the target nutrition
        elif choice_1 == '1':
            bmr = calculate.bmr(person)
            tdee = calculate.tdee(person)
            calorie = calculate.calorie(person)
            protein, carbon, fat = calculate.nutrition(person)
            print("The nutrition indicators based on your personal information are:\nBMR (Basal Metabolic Rate):{} kcal/day\nTDEE (Total Daily Energy Expenditure): {}kcal/day\nCalorie: {}cal\nProtein: {}g\nCarbon: {}g\nFat: {}g".format(bmr, tdee, calorie, protein, carbon, fat))
            continue

        # function 2: manipulate the nutrition record
        elif choice_1 == '2':
            while True:
                choice_2 = input(
                    "What do you want to with your nutrition record:\n[1]: Add new record\n[2]: Delete existed record\n[3]: Modify the existed record\n[4]: Display the record\n[5]: Return to the previous menu\nChoice:")
                if choice_2 not in ['1', '2', '3', '4', '5']:
                    print("Invalid choice, please try again.")
                    continue
                elif choice_2 == '5':
                    break
                elif choice_2 == '1':
                    # input the date, protein, carbon and fat of the newly added record
                    new_date = get_date(
                        "Please enter the date of the newly added record: ")
                    protein = get_float_input(
                        "Please enter the protein (in g): ")
                    carbon = get_float_input(
                        "Please enter the carbon (in g): ")
                    fat = get_float_input("Please enter the fat (in g): ")
                    record_nutrition = record_nutrition.add(
                        new_date, protein, carbon, fat)
                    continue
                elif choice_2 == '2':
                    new_date = get_date(
                        "Please enter the date of the record to delete: ")
                    record_nutrition = record_nutrition.remove(new_date)
                    continue
                elif choice_2 == '3':
                    new_date = get_date(
                        "Please enter the date of the record to modify: ")
                    change = input(
                        "Which indicators do you want to change?(Calories will be calculated automatically)\n[1]: Protein\n[2]: Carbon\n[3]: Fat\nFor more than one indicators, seperate the number with ','\nChoice:")
                    valid_formats = [r"\d+,\d+,\d+", r"\d+,\d+", r"^\d+"]
                    valid = False
                    for each in valid_formats:
                        if re.match(each, change):
                            valid = True
                            break
                    if not valid:
                        print("Invalid format, please check and try again!")
                        continue
                    change = change.split(',')
                    protein, carbon, fat = '', '', ''
                    for each in change:
                        if each == '1':
                            protein = get_float_input(
                                "Please enter the protein (in g): ")
                        elif each == '2':
                            carbon = get_float_input(
                                "Please enter the carbon (in g): ")
                        elif each == '3':
                            fat = get_float_input(
                                "Please enter the fat (in g): ")
                        else:
                            valid = False
                            print("Invalid choice, please check and try again!")
                    if valid:
                        record_nutrition = record_nutrition.modify(
                            new_date, protein, carbon, fat)
                    continue
                elif choice_2 == '4':
                    start_date = get_date("Please enter the start date: ")
                    end_date = get_date("Please enter the end date: ")
                    indicator = input(
                        "What indicators do you want to display:\n[1] Calories\n[2] Protein, Carbon and Fat\nChoice:")
                    if indicator not in ["1", '2']:
                        print('Invalid Input, please check and try again!')
                        continue
                    record_nutrition.show(start_date, end_date, int(indicator))
                    continue
            continue

        # function 3: exercise suggestion
        elif choice_1 == '3':
            intensity_level_choice = input(
                "Please choose the intensity level:\n[1]: easy\n[2]: medium\n[3]: hard\nChoice: ")
            if intensity_level_choice not in ['1', '2', '3']:
                print("Invalid choice, please try again.")
                continue
            else:
                intensity_dict = {'1': 'easy', '2': 'medium',
                                  '3': 'hard'}
                intensity_level_choice = intensity_dict[intensity_level_choice]
            type_of_exericise_choice = input(
                "What kind of sports suggestion do you want to ask:\n[1]: Strength\n[2]: Cardio\n[3]: Hybrid\nChoice: ")
            if type_of_exericise_choice not in ['1', '2', '3']:
                print("Invalid choice, please try again.")
                continue

            # strength suggestion
            elif type_of_exericise_choice == '1':
                strength_helper(intensity_level_choice, 1)
            # cardio suggestion
            elif type_of_exericise_choice == '2':
                exercise = Exercise.Exercise(intensity_level_choice)
                cardio_exercise, cardio_min = exercise.cardio_suggestion()
                print()
                print(
                    f'Based on your intensity level of {intensity_level_choice}:')
                print(
                    f'The suggested cardio today is {cardio_exercise} for {str(cardio_min)} minutes')
                print()
            # hybrid suggestion
            elif type_of_exericise_choice == '3':

                strength_helper(intensity_level_choice, 2)

        # function 4: manipulate exercise record
        elif choice_1 == '4':
            while True:
                choice_2 = input(
                    "What do you want to do with your exercise record:\n[1]: Add new record\n[2]: Delete existed record\n[3]: Modify the existed record\n[4]: Display the record\n[5]: Return to the previous menu\nChoice:")
                if choice_2 not in ['1', '2', '3', '4', '5']:
                    print("Invalid choice, please try again.")
                    continue
                # return to the previous menu
                elif choice_2 == '5':
                    break
                # add exercise record
                elif choice_2 == '1':
                    add_lst = []
                    new_date = get_date(
                        "Please enter the date of the exercise: ")
                    exercise_name = input(
                        "Please enter the name of the exercise: ")
                    exercise_set = get_int_input(
                        "Please enter the number of the sets: ")
                    exercise_rep = get_int_input(
                        "Please enter the number of the reps: ")
                    add_lst.append({"date": new_date, "exercise_name": exercise_name,
                                    "exercise_set": exercise_set, "exercise_rep": exercise_rep})
                    exercise_record.add(add_lst)
                    continue
                # delete an exercise record
                elif choice_2 == '2':
                    index = get_int_input(
                        "Please enter the index of entry you want to remove: ")
                    exercise_record.remove_by_index(index)
                    continue
                # modify an exercise record
                elif choice_2 == '3':
                    modify_index = get_int_input(
                        "Please enter the index you want to modify: ")
                    new_date = get_date("Please enter the new date: ")
                    new_exercise_name = input(
                        "Please enter the new exercise name: ")
                    new_exercise_sets = get_int_input(
                        "Please enter the new exercise sets: ")
                    new_exercise_reps = get_int_input(
                        "Please enter the new exercise reps: ")

                    exercise_record.modify(modify_index, {"date": new_date,
                                           "exercise_name": new_exercise_name, "exercise_set": new_exercise_sets, "exercise_rep": new_exercise_reps})
                    continue
                # display
                elif choice_2 == '4':
                    exercise_record.display()
                    continue
            continue

        elif choice_1 == '5':
            while True:
                choice_2 = input(
                    "Which person information do you want to change?\n[1]: Height\n[2]: Weight\n[3]: Purpose\n[4]: Frequency\n[5]: Return to the previous menu.\nChoice:")
                if choice_2 not in ['1', '2', '3', '4', '5']:
                    print("Invalid choice, please check and choose again")
                    continue
                elif choice_2 == '1':
                    basic_info["Height"][0] = get_int_input(
                        "Please enter your new height (cm):")
                elif choice_2 == '2':
                    basic_info["Weight"][0] = get_int_input(
                        "Please enter your new weight (kg):")
                elif choice_2 == '3':
                    while True:
                        purpose = input(
                            "Please enter the purpose [1] for bulking\n[2] for cutting]:")
                        if purpose not in ['1', '2']:
                            print(
                                "The purpose is NOT correct, please check and try again.")
                            continue
                        elif purpose == '1':
                            purpose = 'Bulking'
                            break
                        else:
                            purpose = 'Cutting'
                            break
                    basic_info["Purpose"][0] = purpose
                elif choice_2 == '4':
                    while True:
                        freq = input(
                            "Please choose the frequecy of exercise.\n[1]: No exercise\n[2]: 1-2 times per week\n[3]: 3-4 times per week\n[4]: 5-6 times per week\n[5]: more than 6 times per week\nPlease choose:")
                        if freq not in ['1', '2', '3', '4', '5']:
                            print(
                                'The frequency is NOT correct, please check and try again.')
                            continue
                        else:
                            freq_dict = {'1': 'No exercise', '2': 'Lightly exercise',
                                         '3': 'Moderately active', '4': 'Very active', '5': 'Super active'}
                            freq = freq_dict[freq]
                            break
                    basic_info["Frequency"][0] = freq
                elif choice_2 == '5':
                    person.height = basic_info["Height"][0]
                    person.weight = basic_info["Weight"][0]
                    person.purpose = basic_info["Purpose"][0]
                    person.frequency = basic_info["Frequency"][0]
                    break

    return None


def create():
    while True:
        name = input("Please enter the user name:")
        if name.isdigit():
            print(
                "The user name cannot be only numbers, please choose another another name!")
        elif name+"_person.csv" in os.listdir():
            print("The user has already existed, please choose another name.")
        elif name == '':
            print("The user name cannot be empty.")
        else:
            break

    bdate = get_date(
        "Please enter the birthdate of the newly added user (YYYY-MM-DD):")

    while True:
        height = input("Please enter the height (cm):")
        try:
            height = int(height)
            break
        except ValueError:
            print("The height should be numeric, please enter again.")

    while True:
        weight = input("Please enter the weight (kg):")
        try:
            weight = int(weight)
            break
        except ValueError:
            print("The weight should be numeric, please enter again.")

    while True:
        class InvalidChoiceError(Exception):
            pass
        gender = input("Please enter the gender['F'/'M']:")

        try:
            if gender == "F":
                gender = "Female"
                break
            elif gender == 'M':
                gender = "Male"
                break
            elif gender not in ["F", "M"]:
                raise InvalidChoiceError(
                    "The gender is NOT correct, please check and try again.")
        except InvalidChoiceError as err:
            print(err)

    while True:
        purpose = input(
            "Please enter the purpose for training\n[1] for bulking\n[2] for cutting\nChoice:")
        if purpose not in ['1', '2']:
            print("The purpose is NOT correct, please check and try again.")
            continue
        elif purpose == '1':
            purpose = 'Bulking'
            break
        else:
            purpose = 'Cutting'
            break

    while True:
        freq = input(
            "Please choose the frequecy of exercise.\n[1]: No exercise\n[2]: 1-2 times per week\n[3]: 3-4 times per week\n[4]: 5-6 times per week\n[5]: more than 6 times per week\nPlease choose:")
        if freq not in ['1', '2', '3', '4', '5']:
            print('The frequency is NOT correct, please check and try again.')
            continue
        else:
            freq_dict = {'1': 'No exercise', '2': 'Lightly exercise',
                         '3': 'Moderately active', '4': 'Very active', '5': 'Super active'}
            freq = freq_dict[freq]
            break

    person_data = pd.DataFrame({'Name': [name], 'Birthdate': [bdate], 'Height': [height], 'Weight': [
                               weight], 'Gender': [gender], 'Purpose': [purpose], 'Frequency': [freq]})
    return person_data


def get_int_input(prompt):
    class InvalidInputError(Exception):
        pass

    while True:
        value = input(prompt)
        try:
            if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
                return int(value)
            else:
                raise InvalidInputError(
                    "The input should be a valid integer. Please check and try again.")
        except InvalidInputError as err:
            print(err)


def get_float_input(prompt):
    class InvalidInputError(Exception):
        pass
    while True:
        value = input(prompt)
        try:
            if value.replace(".", "", 1).isdigit():
                return float(value)
            else:
                raise InvalidInputError(
                    "The input should be a valid number. Please check and try again.")
        except InvalidInputError as err:
            print(err)


def get_date(prompt):
    while True:
        new_date = input(prompt)
        re_bdate = r'\d{4}-\d{2}-\d{2}'
        if not re.match(re_bdate, new_date):
            print(
                "The date does not follow the required format, please check and try again.")
            continue
        elif new_date[5:7] not in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
            print(
                "The MONTH does NOT align with the format, please check and enter again.")
            continue
        elif (not new_date[8:].isnumeric()) or (int(new_date[8:]) <= 0) or (int(new_date[8:]) > 31):
            print("The DAY does NOT align with the format, please check and enter again.")
            continue
        else:
            return new_date


def strength_helper(intensity_level_choice, mode):
    bool_flag = True
    body_part_lst_instance = []
    body_part_dic = {"1": "chest", "2": "shoulder",
                     "3": "back", "4": "leg", "5": "tricep", "6": "bicep"}
    while bool_flag:
        body_parts = input(
            "Please choose the body part(s):\n[1]: Chest\n[2]: Shoulder\n[3]: Back\n[4]: Legs\n[5]: Triceps\n[6]: Biceps\nIf you want to train multiple body parts, use ',' to separate, e.g. 1,2,3\nHowever, note that you can't choose more than 3 parts at once, it would be an inappropriate training way\nChoice: ")
        valid_formats = [r"\d+,\d+,\d+", r"\d+,\d+", r"^\d+"]
        valid = False
        for each in valid_formats:
            if re.match(each, body_parts):
                valid = True
                break
        if not valid:
            print("Invalid format, please check and try again!")
            continue
        body_part_lst = body_parts.split(',')
        if len(body_part_lst) > 3:
            print(
                "You can't choose more than 3 body parts! Please try again.")
            continue
        for element in body_part_lst:
            # verify if input is number
            if element.strip().isdigit():
                num = int(element.strip())
                if num < 1 or num > 6 or not (element in body_part_dic):
                    print(
                        f"Invalid entry: {element}. Please enter a number between 1 and 6. Please try again")
                    continue
                else:   # all correct
                    body_part_lst_instance.append(
                        body_part_dic[element])
                    exercise = Exercise.Exercise(
                        intensity_level_choice, body_part_lst_instance)
                    if mode == 1:
                        exercise_result = exercise.strength_suggestion()
                        print(
                            "Here are the strength exercises recommended for you Today!!! Enjoy your workout!")
                        exercise_index = 1
                        for key, value in exercise_result.items():
                            print(
                                f'Exercise {exercise_index}: {key}, Youtube Tutorial Link: {value}')
                            exercise_index += 1
                        bool_flag = False
                        break
                    elif mode == 2:
                        exercise_result = exercise.hybrid_suggestion()
                        strength = exercise_result[0]
                        (cardio_exercise,
                         cardio_min), = exercise_result[1].items()
                        exercise_index = 1
                        for key, value in strength.items():
                            print(
                                f'Exercise {exercise_index}: {key}, Youtube Tutorial Link: {value}')
                            exercise_index += 1
                        cardio_exercise, cardio_min = exercise.cardio_suggestion()
                        print()
                        print(
                            f'Based on your intensity level of {intensity_level_choice}:')
                        print(
                            f'The suggested cardio today is {cardio_exercise} for {str(cardio_min)} minutes')
                        print()
                        bool_flag = False
                        break

            else:
                print(
                    f"Invalid entry: {element}. Please enter the number")
                break


if __name__ == '__main__':
    start()
