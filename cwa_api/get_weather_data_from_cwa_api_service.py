import requests
import csv
import pandas as pd
import inspect

reverse_function_mapping={}
def convert_dct_to_dct_lst(dct,value_name='value',key_name='date_time'):
    """
    Convert a dictionary to a list of dictionaries with 'key' and 'value' keys.
    """
    return [{key_name: key, value_name: value} for key, value in dct.items()]

def parse_temperature(temperatures):
    data={}
    if len(temperatures) > 0:
        for temp in temperatures['Time']:             
            data[temp['DataTime']] = temp['ElementValue'][0]["Temperature"]
    
    data=convert_dct_to_dct_lst(data, value_name=reverse_function_mapping[inspect.stack()[0].function])
    return data

def parse_humidity(humidities):
    data={}
    if len(humidities) > 0:
        for humidity in humidities['Time']:
            data[humidity['DataTime']] = humidity['ElementValue'][0]["RelativeHumidity"]
    data=convert_dct_to_dct_lst(data, value_name=reverse_function_mapping[inspect.stack()[0].function])
    return data

def parse_comfort(comforts):
    data={}
    if len(comforts) > 0:
        for comfort in comforts['Time']:
            data[comfort['DataTime']] = comfort['ElementValue'][0]["ComfortIndexDescription"]
    data=convert_dct_to_dct_lst(data, value_name=reverse_function_mapping[inspect.stack()[0].function])
    return data

def parse_body_temperature(body_temperatures):
    data={}
    if len(body_temperatures) > 0:
        for body_temp in body_temperatures['Time']:
            data[body_temp['DataTime']] = body_temp['ElementValue'][0]["ApparentTemperature"]
    data=convert_dct_to_dct_lst(data, value_name=reverse_function_mapping[inspect.stack()[0].function])
    return data
def parse_beaufort_wind(beaufort_winds):
    data={}
    if len(beaufort_winds) > 0:
        for beaufort_wind in beaufort_winds['Time']:
            data[beaufort_wind['DataTime']] = beaufort_wind['ElementValue'][0]["BeaufortScale"]
    data=convert_dct_to_dct_lst(data, value_name=reverse_function_mapping[inspect.stack()[0].function])
    return data


def parse_wind_direction(wind_directions):
    data={}
    if len(wind_directions) > 0:
        for wind_direction in wind_directions['Time']:
            data[wind_direction['DataTime']] = wind_direction['ElementValue'][0]["WindDirection"]
    data=convert_dct_to_dct_lst(data, value_name=reverse_function_mapping[inspect.stack()[0].function])
    return data

def parse_rainfall(rainfalls):
    data={}
    if len(rainfalls) > 0:
        for rainfall in rainfalls['Time']:
            data[rainfall['StartTime']] = rainfall['ElementValue'][0]["ProbabilityOfPrecipitation"]
    data=convert_dct_to_dct_lst(data, value_name=reverse_function_mapping[inspect.stack()[0].function])
    return data
def parse_status(statuses):
    data={}
    if len(statuses) > 0:
        for status in statuses['Time']:
            data[status['StartTime']] = status['ElementValue'][0]["Weather"]

    data=convert_dct_to_dct_lst(data, value_name=reverse_function_mapping[inspect.stack()[0].function])
    return data


#key_mapping = {'相對濕度':'humidity','舒適度指數':'Comfort','溫度':'Temperature','體感溫度':'BodyTemperature','風速':'Beaufort_Wind','風向':'Wind_dir','降雨量':'Rainfall','天氣現象':'status'}
key_mapping = {'相對濕度':'humidity','溫度':'Temperature','舒適度指數':'Comfort','體感溫度':'body_temp','風速':'Beaufort_Wind','風向':'Wind_dir', '3小時降雨機率':'Rainfall','天氣現象':'status'}


function_mapping ={'Temperature': parse_temperature,
                   'humidity': parse_humidity,
                   'Comfort': parse_comfort,
                   'body_temp': parse_body_temperature,
                   'Beaufort_Wind': parse_beaufort_wind,
                   'Wind_dir': parse_wind_direction,
                   'Rainfall': parse_rainfall,
                   'status': parse_status}


reverse_function_mapping = {v.__name__: k for k,v in function_mapping.items()}


def get_county_data(filename='全臺縣市鄉鎮對照表_20250610.csv'):
    county_data={}
    with open(filename) as csvfile:
    
        reader = csv.DictReader(csvfile)
        header=reader.fieldnames  # Get the header of the CSV file
        for row in reader:
            
            county_data[row[header[0]]] = {'code': row[header[1]], 'town': row[header[2]].split(' ')} #取得縣市代碼以及所屬鄉鎮名稱
            
    counties=list(county_data.keys())  # 縣市名稱
    return counties, county_data


def get_api_key(filename='GOV_api_key.txt'):
    with open(filename, 'r') as file:
        api_key = file.read().strip()
    return api_key



def convert_town_name_to_url_part(town_name):
    # Convert the town name to a URL-friendly format
    return "LocationName="+ ",".join(town_name)  # Join with a comma for the API format


def get_distCode(a_Locations):
    LocationName = a_Locations["LocationName"]
    Distcode = a_Locations["Geocode"]


api_key=get_api_key()
counties, county_data = get_county_data()

source_url="https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization="+api_key+"&format=JSON&"





selected_county = counties[0]  # Select the first county for demonstration
#selected_county="高雄市"

#url=source_url+"locationId="+county_data[selected_county]['code']+"&"+convert_town_name_to_url_part(county_data[selected_county]['town'])  # Example for the first county and its first town
url=source_url+"&locationName="+selected_county+"&sort=time"

df = pd.DataFrame()
total_rslts=[]
try:
    response = requests.get(url)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

    data = response.json()
    print(data)
    #locations=data['records']['Locations'][0]["Location"]#[0]  # Extract the 'records' key from the JSON response
    #Locations_Name = data['records']['Locations'][0]["LocationsName"]

   
    #print(df[50:100])
    #print(len(df))

except requests.exceptions.RequestException as e:
    print(f"Error during request: {e}")
except ValueError as e:
    print(f"Error parsing JSON: {e}")