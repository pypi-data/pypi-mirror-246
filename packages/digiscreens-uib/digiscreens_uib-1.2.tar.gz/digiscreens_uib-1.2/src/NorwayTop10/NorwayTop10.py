class NorwayTop10:
    def __init__(self):
        self.df = None

    def findTop10(self, dataframe, country, year, film=True, tv=True):
        """
        The function should find the most popular tv shows and films by giving 10 points to a film or TV if they are at the top of the top 10 list, and
        one point if they are tenth. Then we sum this together for the whole year for each movie and tv show. 
        This function takes in a dataframe from the netflix data, a country and year to sort the data on and a boolean value for film and tv.
        The boolean value for both film and tv is as standard set to true, meaning the top 10 list we create contains both films and tv shows.
        If we want to look at only films we set tv to False and if we only want tv we set film to false. If both are false we return an empty dictionary.
        The first part of the function checks given statements and make sures that the given input to the function is correct, and if the input in year or country
        is not correct it tries to correct it if possible. If the given country or year is not in the dataframe it raises a valueError.
        The next part of the function sorts on the given country and year and creates a copy of the dataframe to work on, to not change the given one.
        Then based on the boolean values for film and tv we sort the dataframe on movies or tv shows. 
        Next we apply a lambda function where we give 10 points to first place on the weekkly_rank and one point to last place.
        Then we groupby the show title and aggregate the points column we created in the last part by sum.
        Next we sort the values by points and get out the top 10 movies and tv shows for the given year and country.
        Lastly we convert the show_title and the points score to a dictionary displaying the shows in the top 10 and the points they got. 
        """
        if not film and not tv:
            return {}
        #Capitalize the first letter of country to extract country data from df
        country = country.capitalize()

        if not isinstance(year, str):
            year = str(year)

        if (country not in dataframe['country_name'].unique()):
            raise ValueError('Country not in the given dataset, check spelling.')

        if str(year) not in dataframe['week'].str.slice(0, 4).unique():
            raise ValueError('Year not in the dataset, check years included in the given dataset.')

        # Filter the dataframe based on the given country and year
        df_filtered = dataframe[
            (dataframe['country_name'] == country) & (dataframe['week'].str.startswith(str(year)))].copy()

        # Filter based on the category (Film or TV Shows)
        if film and not tv:
            df_filtered = df_filtered[df_filtered['category'] == 'Films']
        elif tv and not film:
            df_filtered = df_filtered[df_filtered['category'] != 'Films'] 

        # Assign points based on weekly rank
        df_filtered['points'] = df_filtered['weekly_rank'].apply(lambda x: 11 - x)

        # Group by show title and sum the points
        df_grouped = df_filtered.groupby('show_title').agg({'points': 'sum'}).reset_index()

        # Sort by points and get top 10
        top10_shows = df_grouped.sort_values(by='points', ascending=False).head(10)

        # Convert dataframe to dictionary
        result = top10_shows.set_index('show_title')['points'].to_dict()

        return result

    def cumulativeWeeksTop10(self, dataframe, country, year, film=True, tv=True):
        """
        The function should return the top 10 movies or tv shows that has been the most cumulative weeks in the top 10 on netflix in a given year.
        This function takes in a dataframe, a country and year to sort the data on and a boolean value for tv and film.
        The boolean value for both film and tv is as standard set to true, meaning the top 10 list we create contains both films and tv shows.
        If we want to look at only films we set tv to False and if we only want tv we set film to false. If both are false we return an empty dictionary.
        The first part of the function checks given statements and make sures that the given input to the function is correct, and if the input in year or country
        is not correct it tries to correct it if possible. If the given country or year is not in the dataframe it raises a valueError.
        The next part of the function sorts on the given country and year and creates a copy of the dataframe to work on, to not change the given one.
        Then based on the boolean values for film and tv we sort the dataframe on movies or tv shows. 
        Next we keep only the rows with the maximum value for cumulative weeks in top 10 and then filter the dataframe on these indexes.
        Then we sort the given dataframe based on weeks in top 10 and get the top 10 movies or tv shows and creates a dictionary with this information.
        """
        if not film and not tv:
            return {}
        # Capitalizes the first letter of country to extract country data from df
        country = country.capitalize()

        if not isinstance(year, str):
            year = str(year)

        if (country not in dataframe['country_name'].unique()):
            raise ValueError('Country not in the given dataset, check spelling.')
        if year not in dataframe['week'].str.slice(0, 4).unique():
            raise ValueError('Year not in the dataset, check years included in the given dataset.')

        # Filter the dataframe based on the given country and year
        df_filtered = dataframe[
            (dataframe['country_name'] == country) & (dataframe['week'].str.startswith(str(year)))].copy()

        # Filter based on the category (Film or TV Shows)
        if film and not tv:
            df_filtered = df_filtered[df_filtered['category'] == 'Films']
        elif tv and not film:
            df_filtered = df_filtered[df_filtered['category'] != 'Films'] 
        indexes = df_filtered.groupby('show_title')['cumulative_weeks_in_top_10'].idxmax()
        # Filter dataframe using the indices of max cumulative weeks in top 10
        df_max_cumulative = df_filtered.loc[indexes]
        top10shows = df_max_cumulative.sort_values(by='cumulative_weeks_in_top_10', ascending=False).head(10)
        result = top10shows.set_index('show_title')['cumulative_weeks_in_top_10'].to_dict()

        return result
