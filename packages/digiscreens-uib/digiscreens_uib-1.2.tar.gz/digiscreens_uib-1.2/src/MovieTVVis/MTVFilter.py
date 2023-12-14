import pandas as pd


class MTVFilter:

    def __init__(self) -> None:
        self.exclusions = {}
        self.inclusions = {}

    def __add_to_filter(self, exclusion: bool, column_name: str, values: list) -> None:
        if exclusion:
            self.exclusions[column_name] = values
        else:
            self.inclusions[column_name] = values

    def add_exclusion(self, column_name: str, values: list) -> None:
        """
        Adds an exclusions to the filter

        :param column_name: Name of the column with values to be excluded
        :param values: to be excluded
        :return: None
        """
        self.__add_to_filter(exclusion=True, column_name=column_name, values=values)

    def add_inclusion(self, column_name: str, values: list) -> None:
        """
        Adds an inclusion to the filter

        :param column_name: Name of the column with values to be included
        :param values: to be included
        :return: None
        """
        self.__add_to_filter(exclusion=False, column_name=column_name, values=values)

    def add_exclusions(self, filter_dict: dict) -> None:
        """
        Adds multiple exclusions to the filter in a single operation
        :param filter_dict: Dictionary containing column names as keys and list of values as values
        :return: None
        """
        for column, values in filter_dict.items():
            self.add_exclusion(column, values)

    def add_inclusions(self, filter_dict: dict) -> None:
        """
        Adds multiple inclusions to the filter in a single operation
        :param filter_dict: Dictionary containing column names as keys and list of values as values
        :return: None
        """
        for column, values in filter_dict.items():
            self.add_inclusion(column, values)

    def remove_exclusion(self, column_name: str) -> None:
        """
        Removes the exclusion of a single column from the filter. All values from the column are removed from the filter.
        :param column_name: to be removed from the filter
        :return: None
        """
        del self.exclusions[column_name]

    def remove_inclusion(self, column_name: str) -> None:
        """
        Removes the inclusion of a single column from the filter. All values from the column are removed from the filter.
        :param column_name: to be removed from the filter
        :return: None
        """
        del self.inclusions[column_name]

    def remove_exclusions(self, column_names: list) -> None:
        """
        Removes the exclusion of multiple columns from the filter. All values from the columns are removed from the filter
        :param column_names: to be removed from the filter
        :return: None
        """
        for column_name in column_names:
            self.remove_exclusion(column_name)

    def remove_inclusions(self, column_names: list) -> None:
        """
        Removes the inclusions of multiple columns from the filter. All values from the columns are removed from the filter
        :param column_names: to be removed from the filter
        :return: None
        """
        for column_name in column_names:
            self.remove_inclusion(column_name)

    def get_exclusions(self) -> dict:
        return self.exclusions

    def get_inclusions(self) -> dict:
        return self.inclusions

    def get_filter(self) -> (dict, dict):
        return self.get_exclusions(), self.get_inclusions()

    def reset(self) -> None:
        """
        Resets the entire filter to its default state
        :return: None
        """
        self.reset_exclusions()
        self.reset_inclusions()

    def reset_exclusions(self) -> None:
        """
        Resets the exclusion filter to its default state
        :return: None
        """
        self.exclusions.clear()

    def reset_inclusions(self) -> None:
        """
        Resets the inclusion filter to its default state
        :return: None
        """
        self.inclusions.clear()

    def describe(self) -> None:
        """
        Prints out a description of which columns and belonging values are to be excluded, and likewise for inclusions
        :return: None
        """
        df_exclusions = pd.DataFrame(data={
            "Columns": list(self.exclusions.keys()),
            "Values": list(self.exclusions.values())
        })

        df_inclusions = pd.DataFrame(data={
            "Columns": list(self.inclusions.keys()),
            "Values": list(self.inclusions.values())
        })

        print("EXCLUSIONS")
        if len(self.exclusions) == 0:
            print("None set")
        else:
            print(df_exclusions.set_index("Columns"))
        print("\nINCLUSIONS")
        if len(self.inclusions) == 0:
            print("None set")
        else:
            print(df_inclusions.set_index("Columns"))
