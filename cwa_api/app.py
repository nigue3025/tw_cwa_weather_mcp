from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)

def get_api_key(filename='GOV_api_key.txt'):
    with open(filename, 'r') as file:
        api_key = file.read().strip()
    return api_key

def load_alias_county_name(filename='aliased.txt'):
    alias_county_name = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            key, value = line.strip().split(',')
            alias_county_name[key] = value
    return alias_county_name

def load_counties(filename='counties.txt'):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

alias_county_name = load_alias_county_name()
counties = load_counties()

BASE_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"  # Updated base URL
API_KEY = get_api_key()  # Retrieve API key from file

def normalize_weather_data(raw_data: dict) -> dict:
    """將氣象局爛格式轉成結構化良好的 JSON"""
    result = {}

    # 資料集描述
    dataset_desc = raw_data.get("records", {}).get("datasetDescription", "")
    result["datasetDescription"] = dataset_desc
    result["locations"] = []

    for loc in raw_data.get("records", {}).get("location", []):
        location_name = loc.get("locationName")
        elements = loc.get("weatherElement", [])

        # 先整理各 elementName 對應時間資料
        timeline_map = {}
        for elem in elements:
            elem_name = elem["elementName"]
            for t in elem["time"]:
                start = t["startTime"]
                end = t["endTime"]
                param = t["parameter"]

                key = (start, end)
                if key not in timeline_map:
                    timeline_map[key] = {
                        "startTime": start,
                        "endTime": end
                    }

                # 動態建立 element 內容，只加有值的欄位
                entry = {}
                name = param.get("parameterName")
                value = param.get("parameterValue")
                unit = param.get("parameterUnit")

                if name is not None:
                    entry["value"] = name
                #if value is not None:
                #    entry["index"] = value
                if unit is not None:
                    entry["unit"] = unit

                # 只有當 entry 有內容才加入
                if entry:
                    timeline_map[key][elem_name] = entry

        # 轉成 list 並依時間排序
        timeline = sorted(timeline_map.values(), key=lambda x: x["startTime"])

        result["locations"].append({
            "locationName": location_name,
            "timeline": timeline
        })

    return result
@app.route('/get_weather', methods=['GET'])
def get_weather():
    selected_county = request.args.get('selected_county')
    global alias_county_name
    if selected_county in alias_county_name:
        selected_county = alias_county_name[selected_county]

    if not selected_county:
        return Response(json.dumps({"error": "selected_county parameter is required"}, ensure_ascii=False), status=400, mimetype='application/json')

    # Construct the URL
    url = f"{BASE_URL}?Authorization={API_KEY}&format=JSON&locationName={selected_county}"  # Use API key dynamically

    try:
        # Fetch data from the API
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        data=normalize_weather_data(data)
        # Return the response with ensure_ascii=False to keep non-ASCII characters
        return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')
    except requests.exceptions.RequestException as e:
        return Response(json.dumps({"error": str(e)}, ensure_ascii=False), status=500, mimetype='application/json')

@app.route('/list_available_locations', methods=['GET'])
def list_available_locations():
    # Return the list of available locations
    global counties
    return Response(json.dumps({"available_locations": counties,"alias_counties": alias_county_name}, ensure_ascii=False), mimetype='application/json')

    #exists = location in counties or location in alias_county_name
  
    #return Response(json.dumps({"location": location, "exists": exists}, ensure_ascii=False), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)