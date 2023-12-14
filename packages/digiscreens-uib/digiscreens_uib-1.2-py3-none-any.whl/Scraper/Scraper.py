import requests
from bs4 import BeautifulSoup


def get_most_popular_title_urls(url: str) -> list:
    """
    Takes in a JustWatch search page and returns a list of urls to the titles on the page

    :param url: URL to a JustWatch search page
    :return: A list of urls to the titles on the page
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        a_tags = soup.find_all("a", class_="title-list-grid__item--link")
        hrefs = ["https://www.justwatch.com" + a_tag.get("href") for a_tag in a_tags]
        return hrefs


def get_popularity_list_urls(providers: list, years: list) -> dict:
    """
    Creates a list of urls using the provided parameters for the JustWatch popularity website

    :param providers: List of providers to include in the url
    :param years: List of years to include in the url
    :return: List of urls
    """
    popularity_list_urls = {}
    for provider in providers:
        for year in years:
            url = F"https://www.justwatch.com/no/provider/{provider}/tv-series?exclude_genres=doc&exclude_genres=fml&exclude_genres=rly&release_year_from={year}&release_year_until={year}"
            popularity_list_urls[(provider, year)] = url
    return popularity_list_urls


def get_title(object_url: str) -> str | None:
    """
    Retrieves the title of a title on JustWatch

    :param object_url: url of a title on JustWatch
    :return: The title for the given url
    """
    response = requests.get(object_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        tags = soup.find_all("h1")
        name = tags[0].text.strip()
        return name
    else:
        return None


def get_detail_infos(object_url: str, heading_of_interest: str) -> list:
    response = requests.get(object_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        names = soup.find_all("h3", class_="detail-infos__subheading")
        tags = soup.find_all("div", class_="detail-infos__value")
        headings = [x.text.strip() for x in names]

        if heading_of_interest in headings:
            index = headings.index(heading_of_interest)
            values = tags[index].text.strip().split(", ")
            return [value.strip() for value in values]

    return []


def get_prod_country(object_url: str) -> list:
    """
    Retrieves the production country / countries of a title on JustWatch
    :param object_url: url of a title on JustWatch
    :return: a list of production countries for the given url
    """
    return get_detail_infos(object_url, "Production country")


def get_genre(object_url: str) -> list:
    """
    Retrieves the genre / genres of a title on JustWatch
    :param object_url: url of a title on JustWatch
    :return: a list of genres for the given url
    """
    return get_detail_infos(object_url, "Genres")


def get_director(object_url: str) -> list:
    return get_detail_infos(object_url, "Director")


def get_synopsis(object_url: str) -> str | None:
    """
    Retrieves the synopsis of a title on JustWatch

    :param object_url: url of a title on JustWatch
    :return: The synopsis for the given url
    """
    response = requests.get(object_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        synopsis = soup.find_all("p", class_="text-wrap-pre-line mt-0")
        if len(synopsis) > 0:
            return synopsis[0].text.strip()
    else:
        return None


def get_cast(object_url):
    """
    Retrieves the cast of a title on JustWatch

    :param object_url: url of a title on JustWatch
    :return: The cast for the given url
    """
    response = requests.get(object_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        cast = soup.find_all("span", class_="title-credit-name")
        cast = [c.text.strip() for c in cast]
        return cast
    else:
        return None


def get_languages(tmdb_details):
    """
    Finds the different languages of a movie or tv show, using the details from a search to TMDB's api.
    """
    languages = tmdb_details.get("languages", [])
    return languages


def get_original_language(tmdb_details):
    """
    Finds the original language of a movie or tv show, using the details from a search to TMDB's api.
    """
    original_language = tmdb_details.get("original_language", "")
    return original_language


def get_production_companies(tmdb_details):
    """
    Finds the production companies involved in creating the tv show or movie, using the details from a search to TMDB's api.
    """
    production_companies = tmdb_details.get("production_companies", [])
    return [company["name"] for company in production_companies]


def get_tmdb_details(title, api_key, is_movie=False):
    """
    Searches TMDB's api for the given movie title and gets important information about the movie or tv show.
    To get this function to work you need to request TMDB for your own api key, and then input this key as a string to this function.
    """
    base_url = "https://api.themoviedb.org/3"
    search_url = f"{base_url}/search/movie" if is_movie else f"{base_url}/search/tv"
    params = {
        "api_key": api_key,
        "query": title
    }
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            # Assuming the first result is the most relevant
            id = results[0]["id"]
            details_url = f"{base_url}/movie/{id}" if is_movie else f"{base_url}/tv/{id}"
            details_response = requests.get(details_url, params={"api_key": api_key})
            if details_response.status_code == 200:
                return details_response.json()
    return {"original_language": [],
            "languages": [],
            "production_companies": []}


class Scraper:
    def __init__(self):
        self.metadata = {
            "Rank": [],
            "Title": [],
            "ProductionCountry": [],
            "Genre": [],
            "Cast": [],
            "Synopsis": [],
            "Original language": [],
            "Languages": [],
            "Production Companies": [],
            "Director": []
        }

    def get_jw_metadata(self, object_url, api_key):
        """
        Retrieves the metadata for a title on JustWatch and adds it to the Scraper object
        :param api_key:
        :param object_url:
        :return:
        """
        self.metadata["Rank"].append(len(self.metadata["Rank"]) + 1)
        self.metadata["Title"].append(get_title(object_url))
        self.metadata["ProductionCountry"].append(get_prod_country(object_url))
        self.metadata["Genre"].append(get_genre(object_url))
        self.metadata["Cast"].append(get_cast(object_url))
        self.metadata["Synopsis"].append(get_synopsis(object_url))
        self.metadata["Director"].append(get_director(object_url))

        tmdb_details = get_tmdb_details(get_title(object_url), api_key)
        self.metadata["Original language"].append(get_original_language(tmdb_details))
        self.metadata["Languages"].append(get_languages(tmdb_details))
        self.metadata["Production Companies"].append(get_production_companies(tmdb_details))

    def get_metadata(self):
        return self.metadata
