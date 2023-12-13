import pandas as pd


def column_is_numeric(column: pd.DataFrame):
    """
    Calculates the percentage of non-NA values in a column which are numeric, and returns True if this value is 100%

    :param column: Pandas column
    :return: True if all values are numeric, not counting nan values. False otherwise.
    """
    converted_proportion = column.notna().mean()
    return converted_proportion == 1


def to_numeric(column: pd.DataFrame):
    """
    Replaces commas with periods, and converts the given column to numeric

    :param column: To be converted to numeric values
    :return: converted column with numeric values
    """
    return pd.to_numeric(column.str.replace(",", "."), errors="coerce")


def filter_in(df: pd.DataFrame, variable: str, values: list):
    """
    Filter a DataFrame to include only specified values in a particular column.

    :param df: The input DataFrame to be filtered
    :param variable: Name of column in df which is to be filtered
    :param values: List of values which should be retained in the DataFrame.
    :return: The filtered DataFrame containing only rows with values in filter_values for the column filter_variable
    """
    if values is not None:
        return df[df[variable].isin(values)]
    return df


def filter_out(df, variable, values):
    """
    Filter a DataFrame to exclude all values specified in a particular column.

    :param df: The input DataFrame to be filtered
    :param variable: Name of column in df which is to be filtered
    :param values: List of values which should be excluded in the DataFrame.
    :return: The filtered DataFrame containing only rows with values not in filter_values for the column filter_variable
    """
    if values is not None:
        return df[~df[variable].isin(values)]
    return df


def column_values_are_lists(df, column_name):
    """
    Checks if all non-Na values in a DataFrame column are enclosed with square brackets and returns True if this is
    the case

    :param df: Dataframe with column to be checked
    :param column_name: Name of column in Dataframe
    :return: True if all values in the specified column are "list-like"
    """
    df_column = df[column_name]
    return df_column.apply(lambda x: x.startswith("[") and x.endswith("]") if pd.notna(x) else True).all()


def get_list_column_names(df):
    """
    Returns a list of the names of columns in a DataFrame which are "list-like"

    :param df: DataFrame to be checked
    :return: list of column names which are "list-like"
    """
    column_names = []
    for col_name in df.columns:
        if column_values_are_lists(df, col_name):
            column_names.append(col_name)

    return column_names
