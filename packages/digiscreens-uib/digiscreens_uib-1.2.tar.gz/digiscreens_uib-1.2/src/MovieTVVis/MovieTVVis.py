import ast

import pandas as pd
import plotly.express as px

import src.MovieTVVis.helper as helper
from src.MovieTVVis.MTVFilter import MTVFilter


class MovieTVVis:

    def __init__(self):
        self.df_original = None
        self.df_processed = None
        self.id_column = None

    def import_csv(self, path: str, sep: str = ",", id_column: str = None):
        """
        Imports a csv file, stores this as a DataFrame, and creates a clean version of the same DataFrame for later use

        :param id_column: Column containing unique values for each observation
        :param path: Path to the csv file
        :param sep: Separator used in csv file
        """
        self.df_original = pd.read_csv(path, sep=sep,quotechar='"')
        if id_column is None:
            self.df_original['ID'] = range(1, len(self.df_original) + 1)
            self.id_column = 'ID'
        else:
            self.id_column = id_column

        list_columns = helper.get_list_column_names(self.df_original.select_dtypes("O"))
        converters = {column: self.safe_literal_eval for column in list_columns}

        self.df_processed = pd.read_csv(path, sep=sep, quotechar='"', converters=converters)
        if id_column is None:
            self.df_processed['ID'] = range(1, len(self.df_processed) + 1)
        else:
            self.id_column = id_column
        self.clean_data(list_columns)

    def safe_literal_eval(self, s):
        try:
            return ast.literal_eval(s)
        except (ValueError, SyntaxError):
            return s

    def get_processed_df(self):
        return self.df_processed

    def get_original_df(self):
        return self.df_original

    def clean_data(self, list_columns):
        """
        Takes the original DataFrame and transforms it into a long format such that it is easier to work with, as well
        as converting "string" columns only containing numeric values into a numeric column.
        """
        self.fix_numeric_columns(inplace=True)
        for col_name in list_columns:
            self.df_processed = self.df_processed.explode(col_name)

    def apply_filter(self, mtv_filter):
        """
        The method applies a MTVFilter to a copy of the processed DataFrame. It modifies a DataFrame based on specified
        criteria. It filters out rows based on an exclusion criteria, and retains rows based on an inclusion criteria.
        No modifications are done to the original DataFrame.

        :param mtv_filter: MTVFilter object with inclusions and/or exclusions
        :return: The filtered DataFrame
        """
        df_working_copy = self.df_processed.copy()

        for feature, values in mtv_filter.get_exclusions().items():
            df_working_copy = helper.filter_out(df_working_copy, feature, values)

        for feature, values in mtv_filter.get_inclusions().items():
            df_working_copy = helper.filter_in(df_working_copy, feature, values)
        return df_working_copy

    def heatmap(self, x, y, mtv_filter=MTVFilter(), relative_values="none", **kwargs):
        """
        Generates a heatmap visualising the relationship between x and y

        :param y: Variable to be visualised along the x-axis
        :param x: Variable to be visualised along the y-axis
        :param mtv_filter: MTVFilter object to be used for filtering values.
        :param relative_values: One of the values "x", "y", "all", or "none".
        This decides which axis is used for calculating percentages
        :param kwargs: Optional arguments to be passed to Plotly
        :return: A Plotly figure object.
        """
        df_filtered = self.apply_filter(mtv_filter=mtv_filter)
        df_filtered.drop_duplicates(
            subset=[self.id_column, y, x],
            keep="last",
            inplace=True
        )

        df_grouped = df_filtered.groupby([y, x]).count().reset_index()
        heatmap_data = df_grouped.pivot_table(index=y, columns=x, values=self.id_column)

        if relative_values == "x":
            heatmap_data = heatmap_data.apply(lambda z: z / z.sum(), axis=0)
        elif relative_values == "y":
            heatmap_data = heatmap_data.apply(lambda z: z / z.sum(), axis=1)
        elif relative_values == "all":
            heatmap_data = heatmap_data / heatmap_data.sum().sum()

        text_auto = {
            "x": ".0%",
            "y": ".0%",
            "all": ".0%",
            "none": True,

        }

        title = kwargs.pop("title", f"Number of screen content per {y} / {x}")
        template = kwargs.pop("template", "none")
        text_auto = kwargs.pop("text_auto", text_auto[relative_values])
        color_continuous_scale = kwargs.pop("color_continuous_scale", "Blues")

        fig = px.imshow(
            heatmap_data,
            template=template,
            text_auto=text_auto,
            color_continuous_scale=color_continuous_scale,
            title=title,
            **kwargs
        )

        fig.update_layout(
            coloraxis_showscale=False
        )

        return fig

    def pie(self, target, mtv_filter=MTVFilter(), relative_values=True, **kwargs):
        """
        Generates a pie plot visualising the distribution of the target variable

        :param target: The variable to be visualised
        :param mtv_filter: MTVFilter object to be used for filtering values.
        :param relative_values: True or False depending on whether values should be displayed as frequencies or relative
        frequencies
        :param kwargs: Optional arguments to be passed to Plotly
        :return: A Plotly figure object.
        """
        df = self.apply_filter(mtv_filter)
        df.drop_duplicates(
            subset=[self.id_column, target],
            keep="last",
            inplace=True
        )

        df_grouped = df.groupby([target])[target].count().reset_index(name="Count")

        template = kwargs.pop("template", "none")
        title = kwargs.pop("title", f"Distribution of screen content per {target}")

        fig = px.pie(
            data_frame=df_grouped,
            names=df_grouped[target],
            values=df_grouped["Count"],
            template=template,
            title=title,
            **kwargs
        )

        textinfo = [" + value", " + percent"]
        texttemplate = ["%{value}", "%{percent:.0%}"]

        fig.update_traces(
            textinfo="label" + textinfo[relative_values],
            textposition="outside",
            texttemplate="%{label} " + texttemplate[relative_values]
        )
        return fig

    def bar(self, target, mtv_filter=MTVFilter(), relative_values=True, **kwargs):
        """
        Generates a bar plot visualising the distribution of the target variable

        :param target: The variable to be visualised
        :param mtv_filter: MTVFilter object to be used for filtering values.
        :param relative_values: True or False depending on whether values should be displayed as frequencies or relative
        frequencies
        :param kwargs: Optional arguments to be passed to Plotly
        :return: A Plotly figure object.
        """
        df = self.apply_filter(mtv_filter)
        df.drop_duplicates(
            subset=[self.id_column, target],
            keep="last",
            inplace=True
        )

        df_grouped = df.groupby([target])[target].count().reset_index(name="Frequencies")
        df_grouped.sort_values(inplace=True, ascending=False, by="Frequencies")
        df_grouped["Relative frequencies"] = df_grouped["Frequencies"] / df_grouped["Frequencies"].sum()

        text_auto = kwargs.pop("text_auto", [True, ".0%"][relative_values])
        template = kwargs.pop("template", "none")
        title = kwargs.pop("title", f"Distribution of screen content per {target}")

        fig = px.bar(
            data_frame=df_grouped,
            x=target,
            y="Relative frequencies" if relative_values else "Frequencies",
            text_auto=text_auto,
            template=template,
            title=title,
            **kwargs
        )

        fig.update_traces(
            textposition="outside",
            cliponaxis=False
        )

        return fig

    def line(self, x, target, mtv_filter=MTVFilter(), relative_values=False, **kwargs):
        """
        Generates a line plot visualisation where x represents the x-axis, and target represents the different lines

        :param x: Variable to be used as the x-axis
        :param target: Variable to be used for individual lines
        :param mtv_filter: MTVFilter object to be used for filtering values.
        :param relative_values: True or False depending on whether values should be displayed as frequencies or relative
        frequencies
        :param kwargs: Optional arguments to be passed to Plotly
        :return: A Plotly figure object.
        """
        df = self.apply_filter(mtv_filter)
        df.drop_duplicates(
            subset=[self.id_column, x, target],
            keep="last",
            inplace=True
        )

        df_grouped = df.groupby([target, x])[target].count().reset_index(name="Frequencies")
        df_grouped.sort_values(inplace=True, ascending=False, by=x)
        df_grouped["Relative frequencies"] = df_grouped.groupby("Year")["Frequencies"].transform(lambda z: z / z.sum())

        template = kwargs.pop("template", "none")
        markers = kwargs.pop("markers", True)
        title = kwargs.pop("title", f"screen content per {x} for {target}")

        fig = px.line(
            df_grouped,
            x=x,
            y="Relative frequencies" if relative_values else "Frequencies",
            color=target,
            template=template,
            markers=markers,
            title=title,
            **kwargs
        )

        fig.update_yaxes(
            tickformat=".0%" if relative_values else None
        )
        return fig

    def scatter(self, x, y, mtv_filter=MTVFilter(), trendline=False, **kwargs):
        """
        Generates a scatter plot visualising the numerical variables x against y

        :param x: Name of the variable to be used as x-axis
        :param y: Name of the variable to be used as y-axis
        :param mtv_filter: MTVFilter obliject to be used for filtering values.
        :param trendline: True if the scatterplot should include an ordinary least squares trendline. False otherwise
        :param kwargs: Optional arguments to be passed to Plotly
        :return: A Plotly figure object
        """
        df = self.apply_filter(mtv_filter)
        df.drop_duplicates(
            subset=[self.id_column],
            keep="last",
            inplace=True
        )

        title = kwargs.pop("title", f"Relationship between {x} and {y}")
        trendline_variable = kwargs.pop("trendline", [None, "ols"][trendline])

        fig = px.scatter(
            df,
            x=x,
            y=y,
            trendline=trendline_variable,
            title=title,
            template="none",
            **kwargs
        )
        return fig

    def combine_features(self, feature_a, feature_b, new_feature_name):
        """
        Combine two feature columns into a new column.
        :param feature_a: Name of the first column to be combined
        :param feature_b: Name of the second column to be combined
        :param new_feature_name: Name of the new column name

        :return: A new DataFrame with the combined features if inplace = False, otherwise it changes the internal
        DataFrame and returns this.
        """
        df = self.df_processed.copy()
        df[new_feature_name] = df[feature_a]

        df_copied_rows = df[df[feature_b].notna()].copy()
        df_copied_rows[new_feature_name] = df_copied_rows[feature_b]
        df_copied_rows = df_copied_rows.drop(columns=[feature_b])

        df_combined = pd.concat([df, df_copied_rows], ignore_index=True)
        df_combined.drop_duplicates(inplace=True)
        df_combined.sort_values(by=self.id_column, inplace=True)
        self.df_processed = df_combined

        return df_combined

    def fill_nas(self, fill_with="", inplace=False):
        """
        Fills all NA values in all columns which are of type "object"
        :param fill_with: value to replace NA's
        :param inplace: True if the operation is to be executed on the internal DataFrame. False if a copy is created
        and returned
        :return: A DataFrame with NA's replaced. The DataFrame is the internal DataFrame if inplace = True, otherwise it
        returns a copy of the internal DataFrame
        """
        """

        :param fill_with: The value to fill NA's with
        :param inplace: True if the operation should be done on the internal object. 
        If False, a new DataFrame is returned.
        :return:
        """
        df = self.df_processed.copy()
        for feature in df.select_dtypes(include="O").columns:
            df[feature].fillna(fill_with, inplace=True)
        if inplace:
            self.df_processed = df
            return self.df_processed
        return df

    def fix_numeric_columns(self, inplace=False):
        """
        Finds the columns which should be numeric according to get_numeric_object_columns and transforms them to numeric.
        :param inplace: True if action should be done on the internal dataframe
        :return: None if inplace = True, converted dataframe if inplace= False
        """
        numeric_column_names = self.get_numeric_object_columns()
        return self.transform_columns_to_numeric(numeric_column_names, inplace=inplace)

    def get_numeric_object_columns(self):
        """
        Searches through the dataframe for columns which can be converted to numeric
        :return: list of column names which can be converted to numeric.
        """
        columns = self.df_processed.select_dtypes(include="object").columns
        return [column for column in columns if helper.column_is_numeric(self.convert_to_numeric(column))]

    def transform_columns_to_numeric(self, col_names, inplace):
        """
        Converts columns which can be converted to numeric, into numeric.
        :param col_names: Names of columns which should be converted
        :param inplace: True if action is taken on objects dataframe, False if a new dataframe should be returned
        :return: None if inplace = True, and a new dataframe if inplace = False
        """
        if inplace:
            self.df_processed[col_names] = self.df_processed[col_names].apply(lambda col: helper.to_numeric(col))
        else:
            df_copy = self.df_processed.copy()
            df_copy[col_names] = df_copy[col_names].apply(lambda col: helper.to_numeric(col))
            return df_copy

    def convert_to_numeric(self, column_name):
        """
        Replaces commas with periods and returns a column where the values have been converted to numeric.

        :param column_name: name of column to be converted
        :return: converted column
        """
        return pd.to_numeric(helper.to_numeric(self.df_processed[column_name]))

    def describe(self):
        """
        Prints a description of what columns and unique values are present in the DataFrame
        :return: None
        """
        columns = self.df_processed.columns.tolist()
        unique_values = [pd.unique(self.df_processed[column]).tolist() for column in columns]
        print("COLUMN NAMES AND UNIQUE VALUES\n")
        for column, values in zip(columns, unique_values):
            print(column)
            print(values)
            print()

    def print_unique_columns(self):
        """
        Prints a list of what columns are present in the DataFrame
        :return: None
        """
        print("COLUMNS PRESENT\n")
        for column in self.df_processed.columns:
            print(column)

    def print_unique_values(self, column_name):
        for value in pd.unique(self.df_processed[column_name]):
            print(value)
