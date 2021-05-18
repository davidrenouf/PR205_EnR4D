#%%
# coding: utf-8
import requests
import time
import os 
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
from matplotlib.lines import Line2D

DURATION = 24


starttime = time.time()

def predict_conso():
    conso = [0,0,0]
    PROMETHEUS = 'http://localhost:9090'
    CONSO_MOY = 10


    response = requests.get(PROMETHEUS + '/api/v1/query',
    params={
        'query': 'kubelet_running_pods',
        })
    results = response.json()


    for i in range(0,4):
        dc_name = results["data"]["result"][i]["metric"]["node"]
        dc_conso = int(results["data"]["result"][i]["value"][1])*CONSO_MOY
        if (dc_name == 'kind-worker'):
            conso[0] = dc_conso
        elif (dc_name == 'kind-worker2'):
            conso[1] = dc_conso
        elif (dc_name == 'kind-worker3'):
            conso[2] = dc_conso
        print('Node : ', results["data"]["result"][i]["metric"]["node"], ' with ', results["data"]["result"][i]["value"][1], 'Pods running on it')
    print(conso)

    return conso

def get_weather_data(dc_city):
    #API call

    params = {
    'access_key': 'ee3b900900726eccd97cb1ac36288c59',
    'query': dc_city
    }

    api_result = requests.get('http://api.weatherstack.com/current', params)

    api_response = api_result.json()
    temperature = api_response['current']['temperature']

    print(u'Current temperature in %s is %d ℃' % (api_response['location']['name'], api_response['current']['temperature']))

    return temperature

def init_green_labels(dc_list):
    #Adding a green label to a Kubernetes Node

    for k in range(len(dc_list)):
        for i in range(0,4):
            os.system("kubectl label nodes %s green=%s --overwrite=true"%(dc_list[k], i))



def add_green_label(dc_name, priority):
    #Adding a green label to a Kubernetes Node

    os.system("kubectl label nodes %s green=%s --overwrite=true"%(dc_name, priority))
    #os.system("kubectl taint nodes %s green=true:PreferNoSchedule --overwrite=true"%(dc_name))
    print("Node %s labelled green=%s"%(dc_name, priority))



def addScoringLabels(dc_list, energy):
    
    # Remove old labels
    init_green_labels(dc_list)

    L = enumerate(energy)
    energy_sorted = sorted(L, key=itemgetter(1))
    indexes = [e[0] for e in energy_sorted]
    elements = [e[1] for e in energy_sorted]

    print(indexes)

    # Add scoring label according to the green energy availabled
    for i in range(0,3):
        rank = indexes[i]
        add_green_label(dc_list[rank], i+1)


def predict_production(temperature):
    #A basic function which predicts the datacenter production according to the temperature

    production = (temperature + 10)
    return production
    
energy = np.zeros([DURATION,3])
pod_number = np.zeros([DURATION,3])

if __name__ == "__main__":

    dc_list = ["kind-worker", "kind-worker2", "kind-worker3"]
    cities_list = ["Bordeaux", "Rouen", "Nice"]

    ## Initialize each node with 3 level of green labels
    init_green_labels(dc_list)

    ## Green energy available on each node
    energy_available = [1550, 1200, 850]
    cpt = 0

    while cpt<DURATION: # 30 seconds loop
        
        print()
        print("Production d'énergie renouvelable disponible : ", energy_available)

        temperature = []
        production = []
        consommation = []

        ## Get production
        for i in range(len(cities_list)):
            temperature.append(get_weather_data(cities_list[i]))
            production.append(predict_production(temperature[i]))

        ## Get consommation
        consommation = predict_conso()

        for i in range(len(consommation)):
            pod_number[cpt][i] = consommation[i]/10

        ## Display the datas
        print('Liste des températures :', temperature)
        print('Liste des productions :', production)
        print('Liste des consommations :', consommation)

        ## Green energy available on each node
        for i in range(len(production)):
            energy_available[i] = energy_available[i] + production[i] - consommation[i]
            energy[cpt][i] = energy_available[i]

        ## Scoring with labelling
        addScoringLabels(dc_list, energy_available)
        

        ## Re start all the pods     
        os.system("kubectl rollout restart deployment/nginx-dep")

        print(energy)
        print(pod_number)
        
        cpt += 1

        time.sleep(40.0 - ((time.time() - starttime) % 40.0))

# %%
## Display the green energy evolution
zero = np.zeros(DURATION)
print(zero)

plt.plot(energy, ":o", label={'DC Bordeaux', 'DC Rouen', 'DC Nice'})
plt.plot(zero, 'r--')
plt.title('Green energy evolution by time')
plt.xlabel('Time [h]')
plt.ylabel('Green energy availabled')

plt.legend()
plt.show()

## Display the evolution of pod numbers on each node


plt.plot(pod_number, ":o", label={'DC Bordeaux', 'DC Rouen', 'DC Nice'})
plt.title('pod number evolution by time')
plt.xlabel('Time [h]')
plt.ylabel('Pod numbers')

plt.legend()
plt.show()

# %%
