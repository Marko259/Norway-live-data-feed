from time import sleep

import requests, json

def main():
    while True:
        try:
            request = requests.get('https://data.vatsim.net/v3/vatsim-data.json', headers={'Accept': 'application/json'})
            if request.status_code == requests.codes.ok:
                feedback = request.json()
                get_dep_arr_data(feedback)
                get_controller_data(feedback)
            get_metar_data()
            sleep(20)
        except Exception as e:
            print(e)

def get_dep_arr_data(feedback):
    data = open('airports.json')
    airports = json.load(data)
    for airport in airports:
        for type in airports[airport]:
            i = 0
            for pilot in feedback['pilots']:
                if pilot['flight_plan'] is None or pilot['flight_plan']['arrival'] is None or pilot['flight_plan']['departure'] is None:
                    continue
                if pilot['flight_plan'][type].upper() == airport.upper():
                    i += 1
            with open(f'data/airports/{airport}_{type}.txt', 'w') as f:
                f.write(f'{type.capitalize()}s: {str(i)}')

def get_controller_data(feedback):
    data = open('controllers.json')
    controllers = json.load(data)

    for position in controllers['positions']:
        name = 'N/A'
        for controller in feedback['controllers']:
            if controller['callsign'].upper() == position.upper():
                name = controller['name'].title()
        with open(f'data/controllers/{position.upper()}_controller.txt', 'w') as f:
            f.write(f'{name}')

def get_metar_data():
    data = open('metar.json')
    metars = json.load(data)
    for airport in metars["airports"]:
        request = requests.get(f'https://metar.vatsim.net/metar.php?id={airport}', headers={'Accept': 'application/json'})
        if request.status_code == requests.codes.ok:
            feedback = str(request.content)
            metar = feedback.replace("'", "")
            metar = metar.replace('b', '')
            with open(f'data/metars/{airport.upper()}_metar.txt', 'w') as f:
                f.write(f'{metar}')



main()
