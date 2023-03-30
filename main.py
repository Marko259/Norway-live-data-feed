from time import sleep

import requests, json

def main():
    while True:
        try:
            data = open('airport.json')
            airports = json.load(data)
            request = requests.get('https://data.vatsim.net/v3/vatsim-data.json', headers={'Accept': 'application/json'})
            if request.status_code == requests.codes.ok:
                feedback = request.json()['pilots']
                for airport in airports:
                    for type in airports[airport]:
                        i = 0
                        for pilot in feedback:
                            if pilot['flight_plan'] is None or pilot['flight_plan']['arrival'] is None or pilot['flight_plan']['departure'] is None:
                                continue
                            if pilot['flight_plan'][type] == airport:
                                i += 1
                        with open(f'data/{airport}_{type}.txt', 'w') as f:
                            f.write(f'{type.capitalize()}: {str(i)}')
            
            sleep(20)
        except Exception as e:
            print(e)

main()
