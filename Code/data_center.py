# coding: utf-8
import requests
import time
import os 

nb_hour = 24

starttime = time.time()

def appel_api(dc_city,nb):
    #API call
    
    api_result = requests.get('http://localhost:8080/scenario1/' + str(nb))

    api_response = api_result.json()
    
    return api_response[dc_city]

class DataCenter :
    "Definition d'un data center"

    def __init__(self,ensoleillement,rendement,temperature,kWc,humidity,uv,weather_code,cloud_cover):
        "Initialisation"
        self.ensoleillement = ensoleillement
        self.rendement = rendement
        self.temperature = temperature
        self.kWc = kWc
        self.humidity = humidity
        self.uv = uv
        self.weather_code = weather_code
        self.cloud_cover = cloud_cover

    def calcul_redement(self,hour):
        rendement = 1

        tab_rendement = [0.2, 0.2, 0.2, 0, 0, 0, 0.2, 0.2, 0.2, 0.6, 0.6, 0.6, 0.8, 0.8, 0.8, 1, 1, 1, 0.6, 0.6, 0.6, 0.4, 0.4, 0.4]

        #Weather code 113 = sunny 
        #Weather code 119 = cloudy
        #Weather code 302 = rainy

        if (self.weather_code == 113):
            
            rendement *= (1-self.cloud_cover/100)
            
            if (self.uv >= 5):
                rendement *= 1.2

        if (self.weather_code == 119):

            rendement *= (1-self.cloud_cover/100)

            if (70 > self.humidity > 50):
                rendement *= 0.9
            elif (self.humidity >= 70):
                rendement *= 0.8

        if (self.weather_code == 302):

            rendement *= (1-self.cloud_cover/100)
            
            rendement *= 0.7
        
        if (rendement > 1 ):
            rendement = 1

        self.rendement = rendement*tab_rendement[hour-1]

    def calcul_production(self,t):
        "Production sur t secondes"
        production = self.ensoleillement * self.kWc * self.rendement
        productionf = production*(1 - abs(25-self.temperature)*0.004)
        productiont = (productionf * t) / 31536000
        
        return round(productiont * 1000)  #1000 nb de panneau

    def calcul_consommation(sel,t,nb_pod):
        "Consommation sur t secondes"
        consommation = (5.15*10**6*1 * t) / 31536000 * nb_pod #MkWh/m²/an*t * m² / t_total

        return round(consommation/4)



    def maj_ensoleillement(self,ensoleillement):
        self.ensoleillement = ensoleillement

    def maj_rendement(self,rendement):
        self.rendement = rendement

    def maj_temperature(self,temperature):
        self.temperature = temperature
    
    def maj_kWc(self,kWc):
        self.kWc = kWc

    def maj_humidity(self,humidity):
        self.humidity = humidity

    def maj_uv(self,uv):
        self.uv = uv

    def maj_weather_code(self,weather_code):
        self.weather_code = weather_code

    def maj_cloud_cover(self,cloud_cover):
        self.cloud_cover = cloud_cover
     



def main():
    
    cities_name = ['Rouen', 'Bordeaux', 'Nice']

    #Normandie 1
    #Normandie 2
    #Chartres
    
    # Création des DataCenters avec les paramètres:
    # ensoleillement / rendement / temperature / kWc / humidity / uv / weather_code / cloud_cover
    
    Rouen = DataCenter(1000,1,25,3,20,3,113,10)
    Bordeaux = DataCenter(1200,1,25,3,20,3,113,10)
    Nice = DataCenter(1500,1,25,3,20,3,113,10)
 
    cities_list = []

    cities_list.append(Rouen)
    cities_list.append(Bordeaux)
    cities_list.append(Nice)
    
    energy_available = [500, 500, 500] 

    compteur = 1

    while compteur <= nb_hour: # 2 seconds loop

        prod = []       #production/consommation/ratio
        conso = []
        ratio = []

        for i in range(3):
            data = appel_api(cities_name[i],compteur)

            cities_list[i].maj_temperature(data['Temperature'])
            cities_list[i].maj_uv(data['UV index'])
            cities_list[i].maj_weather_code(data['Weather Code'])
            cities_list[i].maj_cloud_cover(data['Cloud Cover'])
            cities_list[i].maj_humidity(data['Humidity'])

            cities_list[i].calcul_redement(compteur)
            
            prod.append(cities_list[i].calcul_production(3600))
        
            conso.append(cities_list[i].calcul_consommation(3600,1))  #ajuster dans le code final

            energy_available[i] += prod[i]
            energy_available[i] -= conso[i]

            if energy_available[i] < 0:
                energy_available[i] = 0


        """ for i in range(len(cities_list)):
            energy_available[i] += prod[i]
            energy_available[i] -= conso[i]
            if energy_available[i] < 0:
                energy_available[i] = 0 """


        somme = sum(energy_available)
        for i in range(3):
            if somme == 0:
                ratio.append(0.33)
            elif (energy_available[i]/somme <0):
                ratio.append(0)
            else:
                ratio.append(round(energy_available[i]/somme,1))

        #print("Production = ", prod)
        #print("Consommation = ",conso)
        print("Energy = ", energy_available)
        print("Ratio = ",ratio)
        print("\n")

        compteur += 1

        time.sleep(0.1 - ((time.time() - starttime) % 0.1))

main()