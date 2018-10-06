import pandas as pd 
import re
from geotext import GeoText

def main():
    try:
        data = pd.read_csv("abcnews-date-text.csv") 
    except Exception as e:
        print("Error in reading the file")
        exit(0)

    try:
        # First word of the headline is capitalized
        data = data.headline_text.str.capitalize()

        def capitalize_countries_cites(row):
            """
            capitalize countries and cities
            """
            _title = row.title()
            geo_obj = GeoText(_title)
            _countries = geo_obj.countries
            _cities = geo_obj.cities

            tmp_row = row
            if _countries:
                for country in _countries:
                    insensitive_country = re.compile(re.escape(country), 
                                                        re.IGNORECASE)
                    tmp_row = insensitive_country.sub(country, tmp_row)
            if _cities:
                for city in _cities:
                    insensitive_city = re.compile(re.escape(city), 
                                                    re.IGNORECASE)
                    tmp_row = insensitive_city.sub(city, tmp_row)
            return tmp_row

        data = data.apply(capitalize_countries_cites)
        data.to_csv('result.csv')

    except Exception as e:
        print(e)
        exit(0)

if __name__ == '__main__':
    main()
