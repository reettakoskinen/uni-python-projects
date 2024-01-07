class Fraction:
    """
    This class represents one single fraction that consists of
    numerator and denominator.
    """

    def __init__(self, numerator, denominator):
        """
        Constructor. Checks that the numerator and denominator are of
        correct type and initializes them.

        :param numerator: int, fraction's numerator
        :param denominator: int, fraction's denominator
        """

        # check that both parameters are ints.
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise TypeError

        # Denominator can't be zero
        elif denominator == 0:
            raise ValueError

        self.__numerator = numerator
        self.__denominator = denominator

    def return_string(self):
        """
        :returns: str, a string-presentation of the fraction in the format
                       numerator/denominator.
        """

        if self.__numerator * self.__denominator < 0:
            sign = "-"

        else:
            sign = ""

        return f"{sign}{abs(self.__numerator)}/{abs(self.__denominator)}"

    def __str__(self):
        """
        Same as return string, but now you can use print function normally.

        :returns: str, a string-presentation of the fraction in the format
                       numerator/denominator.
        """
        if self.__numerator * self.__denominator < 0:
            sign = "-"

        else:
            sign = ""

        return f"{sign}{abs(self.__numerator)}/{abs(self.__denominator)}"

    def simplify(self):
        """
        Simplify the fraction to smallest possible numbers.
        """
        gcd = greatest_common_divisor(self.__numerator, self.__denominator)

        new_numerator = self.__numerator // gcd
        new_denominator = self.__denominator // gcd

        return Fraction(new_numerator, new_denominator)

    def complement(self):
        """
        Turn a fraction into its complement fraction.

        :return: instance of the class Fraction
        """
        numerator = self.__numerator * -1
        denominator = self.__denominator

        complement_fraction = Fraction(numerator, denominator)

        return complement_fraction

    def reciprocal(self):
        """
        Turn a fraction into its reciprocal fraction.

        :return: instance of the class Fraction
        """
        numerator = self.__denominator
        denominator = self.__numerator

        reciprocal_fraction = Fraction(numerator, denominator)

        return reciprocal_fraction

    def multiply(self, frac2):
        """
        Multiply a fraction with another fraction.

        :param frac2: instance of the class Fraction
        :return: new instance of the class Fraction
        """
        num1 = self.__numerator
        num2 = frac2.__numerator
        den1 = self.__denominator
        den2 = frac2.__denominator

        numerator = num1 * num2
        denominator = den1 * den2

        multiplied = Fraction(numerator, denominator)

        return multiplied

    def divide(self, frac2):
        """
        Divide a fraction with another fraction.

        :param frac2: instance of the class Fraction
        :return: new instance of the class Fraction
        """
        reciprocal = frac2.reciprocal()

        frac1 = Fraction(self.__numerator, self.__denominator)

        divide = frac1.multiply(reciprocal)

        return divide

    def sum(self, frac2):
        """
        Calculate the sum of two fractions.

        :param frac2: instance of the class Fraction
        :return: instance of the class Fraction, sum of two fractions
        """
        frac1 = Fraction(self.__numerator, self.__denominator)
        expand_frac1 = Fraction(frac2.__denominator, frac2.__denominator)  # Fix typo here
        expanded_frac1 = frac1.multiply(expand_frac1)
        expand_frac2 = Fraction(self.__denominator, self.__denominator)
        expanded_frac2 = frac2.multiply(expand_frac2)

        numerator = expanded_frac1.__numerator + expanded_frac2.__numerator
        denominator = expanded_frac2.__denominator

        sum_fraction = Fraction(numerator, denominator)

        return sum_fraction

    def deduct(self, frac2):
        """
        Deduct a fraction from another fraction.

        :param frac2: instance of the class Fraction
        :return: new instance of the class Fraction
        """
        frac1 = Fraction(self.__numerator, self.__denominator)

        expand_frac1 = Fraction(frac2.__denominator, frac2.__denominator)
        expand_frac1 = frac1.multiply(expand_frac1)
        expand_frac2 = Fraction(self.__denominator, self.__denominator)
        expand_frac2 = frac2.multiply(expand_frac2)

        numerator = expand_frac1.__numerator - expand_frac2.__numerator
        denominator = expand_frac2.__denominator

        deduct_fraction = Fraction(numerator, denominator)

        return deduct_fraction

    def into_float(self):
        """
        Turn a fraction into a decimal number for comparing them.

        :return: float, fraction as decimal
        """
        to_float = self.__numerator / self.__denominator

        return "{:.3f}".format(to_float)

    def __lt__(self, other):
        return self.into_float() < other.into_float()

    def __le__(self, other):
        return self.into_float() <= other.into_float()

    def __eq__(self, other):
        return self.into_float() == other.into_float()

    def __ne__(self, other):
        return self.into_float() != other.into_float()

    def __gt__(self, other):
        return self.into_float() > other.into_float()

    def __ge__(self, other):
        return self.into_float() >= other.into_float()


def greatest_common_divisor(a, b):
    """
    Euclidean algorithm. Returns the greatest common
    divisor.  When both the numerator
    and the denominator are divided by their greatest common divisor,
    the result will be the most reduced version of the fraction in question.
    """

    while b != 0:
        a, b = b, a % b

    return a


def main():
    do_loop = True

    dict_of_fractions = {}

    while do_loop:
        command = input("> ")

        if command == "add":
            fraction = input("Enter a fraction in the form integer/integer: ")
            name = input("Enter a name: ")
            numerator, denominator = fraction.split("/")
            dict_of_fractions[name] = Fraction(int(numerator), int(denominator))

        elif command == "print":
            name = input("Enter a name: ")
            if name in dict_of_fractions:
                print(f"{name} = {dict_of_fractions[name]}")
            else:
                print(f"Name {name} was not found")

        elif command == "simplify":
            name = input("Enter a name: ")
            if name in dict_of_fractions:
                simplified = dict_of_fractions[name].simplify()
                print(f"Simplified {name} = {simplified}")
            else:
                print(f"Name {name} was not found")

        elif command == "complement":
            name = input("Enter a name: ")
            if name in dict_of_fractions:
                complemented = dict_of_fractions[name].complement()
                print(f"Complement of {name} = {complemented}")
            else:
                print(f"Name {name} was not found")

        elif command == "divide":
            frac1_name = input("Enter the name of the first fraction: ")
            frac2_name = input("Enter the name of the second fraction: ")

            if frac1_name in dict_of_fractions and frac2_name in dict_of_fractions:
                frac1 = dict_of_fractions[frac1_name]
                frac2 = dict_of_fractions[frac2_name]

                divided = frac1.divide(frac2)
                print(f"{frac1_name} / {frac2_name} = {divided}")
                simplified = divided.simplify()
                print(f"Simplified {simplified}")
            else:
                print("One or more names were not found")

        elif command == "sum":
            frac1_name = input("Enter the name of the first fraction: ")
            frac2_name = input("Enter the name of the second fraction: ")

            if frac1_name in dict_of_fractions and frac2_name in dict_of_fractions:
                frac1 = dict_of_fractions[frac1_name]
                frac2 = dict_of_fractions[frac2_name]

                summed = frac1.sum(frac2)
                print(f"{frac1_name} + {frac2_name} = {summed}")
                simplified = summed.simplify()
                print(f"Simplified {simplified}")
            else:
                print("One or more names were not found")

        elif command == "deduct":
            frac1_name = input("Enter the name of the first fraction: ")
            frac2_name = input("Enter the name of the second fraction: ")

            if frac1_name in dict_of_fractions and frac2_name in dict_of_fractions:
                frac1 = dict_of_fractions[frac1_name]
                frac2 = dict_of_fractions[frac2_name]

                deducted = frac1.deduct(frac2)
                print(f"{frac1_name} - {frac2_name} = {deducted}")
                simplified = deducted.simplify()
                print(f"Simplified {simplified}")
            else:
                print("One or more names were not found")

        elif command == "file":
            try:
                file_name = input("Enter the name of the file: ")
                with open(file_name, mode="r") as file:  # Use 'with' to ensure the file is properly closed
                    for line in file:
                        line = line.strip()
                        name, fraction = line.split("=")  # Fix here
                        numerator, denominator = fraction.split("/")
                        new_fraction = Fraction(int(numerator), int(denominator))
                        dict_of_fractions[name] = new_fraction

            except OSError:
                print("Error: the file cannot be read.")
                continue

            except ValueError:
                print("Error: the file cannot be read.")
                continue

        elif command == "list":
            for fraction in sorted(dict_of_fractions):
                print(f"{fraction} = {dict_of_fractions[fraction]}")

        elif command == "quit":
            print("Bye bye!")
            do_loop = False

        else:
            print("Unknown command!")


if __name__ == '__main__':
    main()