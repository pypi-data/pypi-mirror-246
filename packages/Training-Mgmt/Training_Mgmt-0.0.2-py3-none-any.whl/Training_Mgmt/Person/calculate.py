import random


def bmr(person):
    """
    Calculate the Basal Metabolic Rate (BMR) for a given person.

    Parameters
    ----------
    person : Person object
        The person object for whom the BMR is to be calculated. The object must have 
        'gender', 'weight', 'height', and 'age' attributes.

    Returns
    -------
    float
        The calculated BMR rounded to 2 decimal places.
    """
    if person.gender == "Male":
        bmr = 88.362 + (13.397*person.weight) + \
            (4.799*person.height) - (5.677*person.age)
    else:
        bmr = 447.593 + (9.247*person.weight) + \
            (3.098*person.height) - (4.330*person.age)

    return round(bmr, 2)


def tdee(person):
    """
    Calculate the Total Daily Energy Expenditure (TDEE) for a given person.

    Parameters
    ----------
    person : Person object
        The person object for whom the TDEE is to be calculated. The object must have
        'frequency' attribute along with those required for BMR calculation.

    Returns
    -------
    float
        The calculated TDEE rounded to 2 decimal places.
    """
    p_bmr = bmr(person)

    active_factor = {"No exercise": 1.2, "Lightly exercise": 1.375,
                     "Moderately active": 1.55, "Very active": 1.725, "Super active": 1.9}
    tdee = p_bmr * active_factor[person.frequency]

    return round(tdee, 2)


def calorie(person):
    """
    Calculate the daily calorie needs for a given person based on their TDEE and fitness goal.

    Parameters
    ----------
    person : Person object
        The person object for whom the daily calorie needs are to be calculated. The object must have
        'purpose' attribute along with those required for TDEE calculation.

    Returns
    -------
    float
        The calculated daily calorie intake rounded to 2 decimal places.
    """
    p_tdee = tdee(person)

    if person.purpose == "Bulking":
        calorie = p_tdee + round(random.uniform(250, 500))
    else:
        calorie = p_tdee + round(random.uniform(-1000, -500))

    return round(calorie, 2)


def nutrition(person):
    """
    Calculate the macronutrient distribution for a given person based on their daily calorie needs.

    Parameters
    ----------
    person : Person object
        The person object for whom the macronutrient distribution is to be calculated. The object must have
        'purpose' attribute along with those required for calorie calculation.

    Returns
    -------
    tuple
        A tuple containing the calculated protein, carbohydrates, and fat intake in grams, each rounded to 2 decimal places.
    """
    p_calorie = calorie(person)

    if person.purpose == "Bulking":
        protein = p_calorie * 0.4
        carbon = p_calorie * random.uniform(0.3, 0.4)
        fat = p_calorie - protein - carbon

    else:
        protein = p_calorie * 0.65
        carbon = p_calorie * random.uniform(0.15, 0.2)
        fat = p_calorie - protein - carbon

    # change the unit of each nutrition to gram
    protein = protein / 4
    carbon = carbon / 4
    fat = fat / 9

    return round(protein, 2), round(carbon, 2), round(fat, 2)
