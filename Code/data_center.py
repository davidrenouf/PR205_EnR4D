# coding: utf-8
import requests
import time
import os 

starttime = time.time()

class DataCenter :
    "Definition d'un data center"

    def __init__(self,ensoleillement,rendement,temperature,kWc):
        "Initialisation"
        self.ensoleillement = ensoleillement
        self.rendement = rendement
        self.temperature = temperature
        self.kWc = kWc
    
    def calcul_production(self,t):
        "Production sur t secondes"
        production = self.ensoleillement * self.kWc * self.rendement
        productionf = production*(1 - abs(25-self.temperature)*0.004)
        productiont = (productionf * t) / 31536000
        
        return round(productiont * 1000)  #1000 nb de panneau

    def calcul_consommation(sel,t,coeff):
        "Consommation sur t secondes"
        consommation = (5.15*10**6*1 * t) / 31536000 * coeff #MkWh/m²/an*t * m² / t_total

        return round(consommation)

    def maj_ensoleillement(self,ensoleillement):
        self.ensoleillement = ensoleillement

    def maj_rendement(self,rendement):
        self.rendement = rendement

    def maj_temperature(self,temperature):
        self.tempretaure = temperature
    
    def maj_kWc(self,kWc):
        self.kWc = kWc
     

def appel_api(dc_city):
    #API call

    """ params = {
    'access_key': '5e3640eadf328a6a816431fe5502cb3f',
    'query': dc_city
    }

    api_result = requests.get('http://api.weatherstack.com/current', params) """
    
    api_result = requests.get('http://localhost:8080/scenario1/' + str(nb))

    api_response = api_result.json()
    
    return api_response[dc_city]


def main():
    
    cities_list = ['Rouen', 'Bordeaux', 'Nice']

    #Normandie 1
    #Normandie 2
    #Chartres
    
    # Création des DataCenters avec les paramètres:
    # ensoleillement / rendement / temperature / kWc
    Rouen = DataCenter(1000,1,25,3)
    Bordeaux = DataCenter(1200,1,25,3)
    Nice = DataCenter(1500,1,25,3)
    
    energy_available = [500, 500, 500] 

    while True: # 30 seconds loop
        
        temperature = []
        meteo_code = []
        uv_index = []       #API data
        cloud_cover = []
        humidity = []

        prod = []       #production/consommation/ratio
        conso = []
        ratio = []

        #for i in range(len(cities_list)):
                #appel API wiremock temperature
                #appel API wiremock meteo code
                #appel API wiremock uv index
                #appel API wiremock cloud cover
                #appel API wiremock humidity
                

        prod.append(Rouen.calcul_production(3600))
        prod.append(Bordeaux.calcul_production(3600))
        prod.append(Nice.calcul_production(3600))

        conso.append(Rouen.calcul_consommation(3600,1))
        conso.append(Bordeaux.calcul_consommation(3600,0.9))
        conso.append(Nice.calcul_consommation(3600,0.8))

        for i in range(len(cities_list)):
            energy_available[i] += prod[i]
            energy_available[i] -= conso[i]
            if energy_available[i] < 0:
                energy_available[i] = 0


        #Rouen.maj_temperature(temperature[0])
        #Bordeaux.maj_temperature(temperature[1])
        #Nice.maj_temperature(temperature[2])
        
        somme = sum(energy_available)
        for i in range(3):
            if (energy_available[i]/somme <0):
                ratio.append(0)
            else:
                ratio.append(round(energy_available[i]/somme,2))

        print("Production = ", prod)
        print("Consommation = ",conso)
        print("Energy = ", energy_available)
        print("Ratio = ",ratio)

        time.sleep(30.0 - ((time.time() - starttime) % 30.0))

main()