import datetime
import pandas as pd


class Person:

    """
    A class to represent a person for tracking health and fitness goals.

    Attributes
    ----------
    __name : str
        Private attribute to store the name of the person.
    __bdate : datetime.datetime
        Private attribute to store the birthdate of the person as a datetime object.
    __height : float
        Private attribute to store the height of the person in meters.
    __weight : float
        Private attribute to store the weight of the person in kilograms.
    __gender : str
        Private attribute to store the gender of the person.
    __purpose : str
        Private attribute to store the fitness purpose of the person.
    __frequency : int
        Private attribute to store the frequency of exercise sessions per week.

    Methods
    -------
    __init__(self, name, bdate, height, weight, gender, purpose, freq):
        Constructs all the necessary attributes for the person object.

    name(self):
        Gets the person's name.

    age(self):
        Calculates the person's age in years from their birthdate to the current date.

    height(self):
        Gets the person's height in meters.

    height(self, value):
        Sets the person's height in meters.

    weight(self):
        Gets the person's weight in kilograms.

    weight(self, value):
        Sets the person's weight in kilograms.

    gender(self):
        Gets the person's gender.

    purpose(self):
        Gets the person's fitness purpose.

    purpose(self, value):
        Sets the person's fitness purpose.

    frequency(self):
        Gets the frequency of the person's exercise sessions per week.

    frequency(self, value):
        Sets the frequency of the person's exercise sessions per week.
    """

    def __init__(self, name, bdate, height, weight, gender, purpose, freq):
        """
        Initializes the Person object with the provided name, birthdate, height,
        weight, gender, fitness purpose, and exercise frequency.

        Parameters
        ----------
        name : str
            The name of the person.
        bdate : str
            The birthdate of the person in 'YYYY-MM-DD' format.
        height : float
            The height of the person in meters.
        weight : float
            The weight of the person in kilograms.
        gender : str
            The gender of the person.
        purpose : str
            The fitness purpose of the person.
        freq : int
            The number of times the person exercises per week.
        """
        self.__name = name
        self.__bdate = datetime.datetime.strptime(bdate, '%Y-%m-%d')
        self.__height = height
        self.__weight = weight
        self.__gender = gender
        self.__purpose = purpose
        self.__frequency = freq

    @property
    def name(self):
        """
        Gets the private name of the person.

        Returns
        -------
        __name : str
            The name of the person.
        """
        return self.__name

    @property
    def age(self):
        """
        Calculates and returns the person's age in years.

        Returns
        -------
        age : int
            The age of the person in years.
        """
        return (datetime.datetime.now() - self.__bdate).total_seconds()//(365.25*24*60*60)

    @property
    def height(self):
        """
        Gets the private height of the person.

        Returns
        -------
        __height : float
            The height of the person in meters.
        """
        return self.__height

    @height.setter
    def height(self, value):
        """
        Sets the private height of the person.

        Parameters
        ----------
        value : float
            The new height of the person in meters.
        """
        self.__height = value

    @property
    def weight(self):
        """
        Gets the private weight of the person.

        Returns
        -------
        __weight : float
            The weight of the person in kilograms.
        """
        return self.__weight

    @weight.setter
    def weight(self, value):
        """
        Sets the private weight of the person.

        Parameters
        ----------
        value : float
            The new weight of the person in kilograms.
        """
        self.__weight = value

    @property
    def gender(self):
        """
        Gets the private gender of the person.

        Returns
        -------
        __gender : str
            The gender of the person.
        """
        return self.__gender

    @property
    def purpose(self):
        """
        Gets the private fitness purpose of the person.

        Returns
        -------
        __purpose : str
            The fitness purpose of the person.
        """
        return self.__purpose

    @purpose.setter
    def purpose(self, value):
        """
        Sets the private fitness purpose of the person.

        Parameters
        ----------
        value : str
            The new fitness purpose of the person.
        """
        self.__purpose = value

    @property
    def frequency(self):
        """
        Gets the private frequency of exercise sessions per week for the person.

        Returns
        -------
        __frequency : int
            The number of exercise sessions per week for the person.
        """
        return self.__frequency

    @frequency.setter
    def frequency(self, value):
        """
        Sets the private frequency of exercise sessions per week for the person.

        Parameters
        ----------
        value : int
            The new number of exercise sessions per week for the person.
        """
        self.__frequency = value
