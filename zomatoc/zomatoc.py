import requests
import ast
import csv

base_url = "https://developers.zomato.com/api/v2.1/"


def initialize_app(config):
    return Zomato(config)


class Zomato:
    def __init__(self, config):
        self.user_key = config["user_key"]


    def get_city_ID(self, city_name):
        """
        Takes City Name as input.
        Returns the ID for the city given as input.
        """
        if city_name.isalpha() == False:
            #raise ValueError('InvalidCityName')
            return 0
        city_name = city_name.split(' ')
        city_name = '%20'.join(city_name)
        headers = {'Accept': 'application/json', 'user-key': self.user_key}
        r = (requests.get(base_url + "locations?query=" + city_name, headers=headers).content).decode("utf-8")
        a = ast.literal_eval(r)

        self.is_key_invalid(a)
        self.is_rate_exceeded(a)

        if len(a['location_suggestions']) == 0:
            #raise Exception('invalid_city_name')
            return 0
        elif 'city_name' in a['location_suggestions'][0]:
            city_name = city_name.replace('%20', ' ')
            if str(a['location_suggestions'][0]['city_name']).lower() == str(city_name).lower():
                return a['location_suggestions'][0]['city_id']
            else:
                #raise ValueError('InvalidCityId')
                return 0


    def get_city_name(self, city_ID):
        """
        Takes City ID as input.
        Returns the name of the city ID given as input.
        """
        self.is_valid_city_id(city_ID)

        headers = {'Accept': 'application/json', 'user-key': self.user_key}
        r = (requests.get(base_url + "cities?city_ids=" + str(city_ID), headers=headers).content).decode("utf-8")
        a = ast.literal_eval(r)

        self.is_key_invalid(a)
        self.is_rate_exceeded(a)

        if a['location_suggestions'][0]['country_name'] == "":
            raise ValueError('InvalidCityId')
        else:
            temp_city_ID = a['location_suggestions'][0]['id']
            if temp_city_ID == str(city_ID):
                return a['location_suggestions'][0]['name']


    def restaurant_search(self, cityid="", start="", count="20"):
        """
        Takes cityid,start and count(default 20) as input.
        Returns a list of 'count' numbers of (MAX 20) Restaurant's Details starting from 'start'.
        """
        
        headers = {'Accept': 'application/json', 'user-key': self.user_key}
        r = (requests.get(base_url + "search?entity_id=" + str(cityid) + "&entity_type=city&start=" + str(start) + "&count=" + str(count), headers=headers).content).decode("utf-8")
        a = ast.literal_eval(r)

        restaurants = []
        restaurant_details = []
        
        if a['results_found'] == 0:
            return []
        else:
            for restaurant in a['restaurants']:
                restaurants.append(restaurant['restaurant']['id'])
                restaurant_details.append({"average_cost_for_two" : restaurant['restaurant']['average_cost_for_two'],"name" : restaurant['restaurant']['name']})
                 

        return restaurant_details

    def get_avg_cost(self,citylist):
        """
        Takes a list of city names as input and creates a csv file with the cityname and list
        of 100 resturants with average_Cost_for_two
        """
        for ci in citylist:
            cid=self.get_city_ID(ci);
            if(cid==0):
                print("\nCity not Found")
            else:
                st=0

                filename=ci+".csv"

                with open(filename, 'w', newline='') as csvfile:
                        fieldnames = ['name', 'average_cost_for_two']
                        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
                        writer.writeheader()
                        while(st<=81):
                                restaurant_list = self.restaurant_search(cityid=cid,start=st)
                                print(type(restaurant_list))
                                print(restaurant_list)
                                writer.writerows(restaurant_list)
                                #print("Done")
                                st=st+20
                print("\nFile Created")




    def is_valid_restaurant_id(self, restaurant_ID):
        """
        Checks if the Restaurant ID is valid or invalid.
        If invalid, throws a InvalidRestaurantId Exception.
        """
        restaurant_ID = str(restaurant_ID)
        if restaurant_ID.isnumeric() == False:
            raise ValueError('InvalidRestaurantId')



    def is_valid_city_id(self, city_ID):
        """
        Checks if the City ID is valid or invalid.
        If invalid, throws a InvalidCityId Exception.
        """
        city_ID = str(city_ID)
        if city_ID.isnumeric() == False:
            raise ValueError('InvalidCityId')



    def is_key_invalid(self, a):
        """
        Checks if the API key provided is valid or invalid.
        If invalid, throws a InvalidKey Exception.
        """
        if 'code' in a:
            if a['code'] == 403:
                raise ValueError('InvalidKey')



    def is_rate_exceeded(self, a):
        """
        Checks if the request limit for the API key is exceeded or not.
        If exceeded, throws a ApiLimitExceeded Exception.
        """
        if 'code' in a:
            if a['code'] == 440:
                raise Exception('ApiLimitExceeded')



class DotDict(dict):
    """
    Dot notation access to dictionary attributes
    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
