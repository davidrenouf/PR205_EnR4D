# coding: utf-8
import requests
import time
import os 
from kubernetes import client, config



starttime = time.time()

def k8s_test():
    config.load_kube_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


def appel_api(dc_city):
    #API call

    params = {
    'access_key': '5e3640eadf328a6a816431fe5502cb3f',
    'query': dc_city
    }

    api_result = requests.get('http://api.weatherstack.com/current', params)

    api_response = api_result.json()
    temperature = api_response['current']['temperature']

    print(u'Current temperature in %s is %d ℃' % (api_response['location']['name'], api_response['current']['temperature']))

    return temperature



def add_green_label(dc_name):
    #Adding a green label to a Kubernetes Node

    os.system("kubectl label nodes %s green=yes --overwrite=true"%(dc_name))
    #os.system("kubectl taint nodes %s green=true:PreferNoSchedule --overwrite=true"%(dc_name))
    print("Node %s labelled green=yes"%(dc_name))

def remove_green_label(dc_name):
    #Removing a green label to a Kubernetes Node

    os.system("kubectl label nodes %s green=no --overwrite=true"%(dc_name))
    #os.system("kubectl taint nodes %s green=true:PreferNoSchedule-"%(dc_name))
    print("Node %s no more green" % (dc_name))

def predict_production(temperature):
    #A basic function which predicts the datacenter production according to the temperature

    production = (temperature + 10)
    return production

def predict_conso():
    conso = []
    PROMETHEUS = 'http://localhost:9090'
    CONSO_MOY = 10


    response = requests.get(PROMETHEUS + '/api/v1/query',
    params={
        'query': 'kubelet_running_pods',
        })
    results = response.json()

    for i in range(0,3):
        
        print('Node : ', results["data"]["result"][i]["metric"]["node"], ' with ', results["data"]["result"][i]["value"][1], 'Pods running on it')
        conso.append(int(results["data"]["result"][i]["value"][1])*CONSO_MOY)

    return(conso)
    


def main():
    #Main function : Each 60 seconds, check meteorological datas for each datacenters -> predict production 
    #Check pod CPU usage
    #green=yes <=> production - pod usage > treshlod
    #If the production verify a condition, the datacenter is labelled "green"

    energy_available = [550, 600, 650]

    while True: # 30 seconds loop
        
        print()
        print("Production d'énergie renouvelable disponible : ", energy_available)

        dc_list = ["kind-worker", "kind-worker2", "kind-worker3"]
        cities_list = ["Bordeaux", "Rouen", "Nice"]
        temperature = []
        production = []
        conso = []

        for i in range(len(cities_list)):
            temperature.append(appel_api(cities_list[i]))
            production.append(predict_production(temperature[i]))

        conso = predict_conso()

        print('Liste des températures :', temperature)
        print('Liste des productions :', production)
        print('Liste des consommations :', conso)


        for i in range(len(production)):
            energy_available[i] = energy_available[i] + production[i] - conso[i]
            if energy_available[i] > 500:
                add_green_label(dc_list[i])
            else:
                remove_green_label(dc_list[i])
                
        
        time.sleep(30.0 - ((time.time() - starttime) % 30.0))
    

k8s_test()
main()