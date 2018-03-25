# Zomatopy
A Python wrapper for the Zomato API v2.1

This is a fork of original Zomatopy wrapper. This takes input the city_names and creates a city_name.csv file with list of 100 restaurants with their name and the average_cost_for_two.



## Getting Started
### Python Version
This wrapper was written for Python 3 and might not work well with Python 2.

### Adding Zomatoc to your application
Keep the zomatoc folder in the same solder as your mail program. Use/modify the code from mail.py as needed.

```python
import zomatoc

config={
  "user_key":"ZOMATO_API_KEY"
}
    
zomato = zomatopy.initialize_app(config)
```
## Methods
### Common

#### Getting ID for a particular city
- Takes City Name as input.
- Returns the City ID of the city.
- Can raise ```InvalidCityName``` exception.

```python
# city_name must be a string without numbers or special characters.

city_ID = zomatoc.get_city_ID(city_name)
```

#### Getting Name for a particular City ID
- Takes City ID as input.
- Returns name of the city with that ID.
- Can raise ```InvalidCityId``` exception.

```python
# city_ID must be an integer.

city_name = zomatoc.get_city_name(city_ID)
```

#### Searching restaurants based on query, latitude/longitude and/or cuisine IDs
- Takes cityid,start and count(default 20) as input.
- Returns a list of 'count' numbers of (MAX 20) Restaurant's Details starting from 'start'.

```python
# latitude and longitude must be float or string representation of a float.
# multiple cuisine IDs can be specified by separating with commas. Must be a string.

restaurant_details = restaurant_search(cityid=cid,start=st)
```
- The details can be appended by adding attribute and values in restaurant_details : ```python
restaurant_details.append({"average_cost_for_two" : restaurant['restaurant']['average_cost_for_two'],"name" : restaurant['restaurant']['name'],"currency" : restaurant['restaurant']['currency']})
```
## Exceptions

#### InvalidKey
- If the key is not a valid Zomato API Key.

```
ValueError: InvalidKey
```
#### InvalidCityId
- If the City ID contains an alphabet or special characters.
- If the City ID is not present in the Zomato database.

```
ValueError: InvalidCityId
```
#### InvalidCityName
- If the City Name consists of numbers or special characters.
- If the City Name is not present in the Zomato database.

```
ValueError: InvalidCityName
```
#### InvalidRestaurantId
- If the Restaurant ID consists of alphabets or special characters.
- If the Restaurant ID is not present in the Zomato database.

```
ValueError: InvalidRestaurantId
```
#### InvalidLatitudeOrLongitude
- If the latitude or longitude value provided in not a number or string representation of a number.

```
ValueError: InvalidLatitudeOrLongitude
```
#### LimitNotInteger
- If the limit parameter provided for the ```get_collections()``` or ```restaurant_search()``` methods is not an integer.

```
ValueError: LimitNotInteger
```
#### ApiLimitExceeded
- If the daily call limit of the API Key is exceeded.

```
Exception: ApiLimitExceeded
```
