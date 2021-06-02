# %%
# coding: utf-8
import time
import os
from operator import itemgetter
import yaml
import numpy as np
import requests
import math

# Give the pod number depending on the ratio
def compute_nb_pods(nb_pods, ratio):
    nb = nb_pods*ratio
    return math.floor(nb)

# Create the new file name, depending on the pod number
def get_file_name(node_nb, pod_nb):
    if(node_nb == 1):
        new_file_name = "worker1_"+str(pod_nb)+".yaml"
    elif(node_nb == 2):
        new_file_name = "worker2_"+str(pod_nb)+".yaml"
    elif(node_nb == 3):
        new_file_name = "worker3_"+str(pod_nb)+".yaml"
    return new_file_name

# Initialisation and creation of a pod 
def create_pod(origin_file, pod_nb, node_nb):
    # Get the file name and pod name
    file_name = get_file_name(node_nb, pod_nb)
    name = "pod"+str(pod_nb)

    # Create the new file
    os.system("cp "+origin_file+" "+file_name)

    # Modify the pod name in the yaml file
    with open(file_name, "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
        data['metadata']['name'] = name
        yamlfile.close()
    with open(file_name, 'w') as yamlfile:
        data1 = yaml.dump(data, yamlfile)
        yamlfile.close()
    
    # Apply the yaml file
    os.system("kubectl apply -f "+file_name)
    return file_name

def get_node_name_by_nb(node_nb):
    if (node_nb == 1):
        return "kind-worker"
    elif (node_nb == 1):
        return "kind-worker2"
    elif (node_nb == 3):
        return "kind-worker3"

# Edit the yaml file of a pod, for a reschudling
def edit_node(node_nb, wi_pods_nb, wj_pods_nb, wi_pods_names, wj_pods_names):
    # Get node name, pod number, file name and new file name
    node_name = get_node_name_by_nb(node_nb)
    nb = wi_pods_nb[0]
    file_name = wi_pods_names[0]
    new_file_name = get_file_name(node_nb, nb)

    # Modify list of pods names and list of pods number to be up to date
    wj_pods_names.append(new_file_name)
    wj_pods_nb.append(nb)
    wi_pods_names.pop(0)
    wi_pods_nb.pop(0)

    # Modify the yaml name
    os.system("cp "+file_name+" "+new_file_name)
    os.system("rm "+file_name)

    # Modify the node selected
    with open(new_file_name, "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
        data['spec']['nodeName'] = node_name
        yamlfile.close()

    with open(new_file_name, 'w') as yamlfile:
        data1 = yaml.dump(data, yamlfile)
        yamlfile.close()

    # Delete the pod and apply the new yaml file
    os.system("kubectl delete pod pod"+str(nb))
    os.system("kubectl apply -f "+new_file_name)

# Function wich computes the pods movement
def compute_movement(old1, old2, old3, cur1, cur2, cur3):
    # Number of pods wich will be added or removed on each pods 
    diff1 = int(old1 - cur1)
    diff2 = int(old2 - cur2)
    diff3 = int(old3 - cur3)

    # Pods movement from node 1 to 2 or/and 3 
    if ((diff1 == 0) or (diff1 < 0)):
        w1_w2 = 0
        w1_w3 = 0
    elif (diff1 > 0):
        if (diff2 < 0):
            if (abs(diff1) <= abs(diff2)):
                w1_w2 = int(abs(diff1))
                w1_w3 = 0
            elif (abs(diff1) > abs(diff2)):
                w1_w2 = int(abs(diff2))
                w1_w3 = int(abs(abs(diff2) - abs(diff1)))
        else:
            w1_w2 = 0
            w1_w3 = int(abs(diff1))

    # Pods movement from node 2 to 3 or/and 1
    if ((diff2 == 0) or (diff2 < 0)):
        w2_w3 = 0
        w2_w1 = 0
    elif (diff2 > 0):
        if (diff3 < 0):
            if (abs(diff2) <= abs(diff3)):
                w2_w3 = int(abs(diff2))
                w2_w1 = 0
            elif (abs(diff2) > abs(diff3)):
                w2_w3 = int(abs(diff3))
                w2_w1 = int(abs(abs(diff3) - abs(diff2)))
        else:
            w2_w3 = 0
            w2_w1 = int(abs(diff2))

    # Pods movement from node 3 to 1 or/and 2
    if ((diff3 == 0) or (diff3 < 0)):
        w3_w1 = 0
        w3_w2 = 0
    elif (diff3 > 0):
        if (diff1 < 0):
            if (abs(diff3) <= abs(diff1)):
                w3_w1 = int(abs(diff3))
                w3_w2 = 0
            elif (abs(diff3) > abs(diff1)):
                w3_w1 = int(abs(diff1))
                w3_w2 = int(abs(abs(diff1) - abs(diff3)))
        else:
            w3_w1 = 0
            w3_w2 = int(abs(diff3))
    
    # List of every pods movement
    # wi_wj : pods movement from node i to node j
    D = [w1_w2, w1_w3, w2_w3, w2_w1, w3_w1, w3_w2]
    return D

# Function wich moves pods
def move_pod(mv1, wi_pods_nb, wj_pods_nb, wi_pods_names, wj_pods_names, nb_node):
    if (mv1 != 0): # test if there are pods to move
        for i in range(mv1):
            edit_node(nb_node, wi_pods_nb, wj_pods_nb,
                      wi_pods_names, wj_pods_names)

# Prediction of the comsumption on each nodes
def predict_conso(nb_pod1, nb_pod2, nb_pod3):
    return [nb_pod1*10, nb_pod2*10, nb_pod3*10]


def predict_prod():
    return [10, 20, 50]

# Call to the Api
def appel_api(dc_city, nb):
    # API call

    api_result = requests.get('http://localhost:8080/scenario1/' + str(nb))

    api_response = api_result.json()

    return api_response[dc_city]


class DataCenter:
    "Definition of data center"

    def __init__(self, ensoleillement, rendement, temperature, kWc, humidity, uv, weather_code, cloud_cover):
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

    def calcul_production(self, t):
        "Production sur t secondes"
        production = self.ensoleillement * self.kWc * self.rendement
        productionf = production*(1 - abs(25-self.temperature)*0.004)
        productiont = (productionf * t) / 31536000

        return round(productiont * 1000 * 6)  # 1000 nb de panneau

    def calcul_consommation(sel, t, nb_pod):
        "Consommation sur t secondes"
        consommation = (5.15*10**6*1 * t) / 31536000 * \
            nb_pod  # MkWh/m²/an*t * m² / t_total

        return round(consommation/4)

    def maj_ensoleillement(self, ensoleillement):
        self.ensoleillement = ensoleillement

    def maj_rendement(self, rendement):
        self.rendement = rendement

    def maj_temperature(self, temperature):
        self.temperature = temperature

    def maj_kWc(self, kWc):
        self.kWc = kWc

    def maj_humidity(self, humidity):
        self.humidity = humidity

    def maj_uv(self, uv):
        self.uv = uv

    def maj_weather_code(self, weather_code):
        self.weather_code = weather_code

    def maj_cloud_cover(self, cloud_cover):
        self.cloud_cover = cloud_cover

def get_ratio(energy_available):
    ratio = []

    somme = sum(energy_available)
    for i in range(3):
        if (energy_available[i]/somme < 0):
            ratio.append(0)
        else:
            ratio.append(round(energy_available[i]/somme, 2))
    return ratio

# MAIN
# Init
nb_pods = 20 # Number of pods, in range 1:110
L_ratio = [0.2, 0.5, 0.3, 0.3, 0.6, 0.1, 0.3, 0.5, 0.2] # Initial ratio
w1_pods_nb = []
w1_pods_names = []
w2_pods_nb = []
w2_pods_names = []
w3_pods_nb = []
w3_pods_names = []
H = 24  # Hours number
init = 0
count_w1 = 0
count_w2 = 0
count_w3 = 0

# Datacenters
cities_name = ['Paris', 'Rouen', 'Nice']

Paris = DataCenter(1000, 1, 25, 3, 20, 3, 113, 10)
Rouen = DataCenter(1200, 1, 25, 3, 20, 3, 113, 10)
Nice = DataCenter(1500, 1, 25, 3, 20, 3, 113, 10)

cities_list = []

cities_list.append(Paris)
cities_list.append(Rouen)
cities_list.append(Nice)

# Metrics
energy = np.zeros([H+1, 3])
pod_number = np.zeros([H, 3])
production = np.zeros([H+1, 3])
consommation = np.zeros([H+1, 3])
energy_available = [1000, 2500, 1500]

for i in range(0, 3):
    energy[0][i] = energy_available[i]

for j in range(0, H):

    ## Metrics initialisation : consumption / production / ratio (scoring system)
    conso = []
    prod = []
    ratio = get_ratio(energy_available)

    print()
    print()
    print('--------------------------------  ',j, 'h' + '  --------------------------------')
    print('Liste des ratios : ',ratio)

    ## Pod distribution according to ratio
    w1_nb = compute_nb_pods(nb_pods, ratio[0])
    w2_nb = compute_nb_pods(nb_pods, ratio[1])
    w3_nb = compute_nb_pods(nb_pods, ratio[2])

    ##------------------------------ j = 0 ------------------------------##
    # First pods creations
    if (init == 0):
        for a in range(1, int(w1_nb+1)):
            file = create_pod("worker1.yaml", a, 1)
            count_w1 = count_w1 + 1
            w1_pods_nb.append(a)
            w1_pods_names.append(file)
        for b in range(1, int(w2_nb+1)):
            file = create_pod("worker2.yaml", b + count_w1, 2)
            count_w2 = count_w2 + 1
            w2_pods_nb.append(b + count_w1)
            w2_pods_names.append(file)
        for c in range(1, int(w3_nb+1)):
            file = create_pod("worker3.yaml", c + count_w1 + count_w2, 3)
            count_w3 = count_w3 + 1
            w3_pods_nb.append(c + count_w1 + count_w2)
            w3_pods_names.append(file)

        init = 1

        ## Pod current number on each node
        curr_w1 = count_w1
        curr_w2 = count_w2
        curr_w3 = count_w3

        curr_nb_pods = [curr_w1, curr_w2, curr_w3]

        ## Get prod and conso
        for i in range(3):
            data = appel_api(cities_name[i], j+1)

            cities_list[i].maj_temperature(data['Temperature'])
            cities_list[i].maj_uv(data['UV index'])
            cities_list[i].maj_weather_code(data['Weather Code'])
            cities_list[i].maj_cloud_cover(data['Cloud Cover'])
            cities_list[i].maj_humidity(data['Humidity'])

            cities_list[i].calcul_redement(j)

            prod.append(cities_list[i].calcul_production(3600))

            conso.append(cities_list[i].calcul_consommation(
                3600, curr_nb_pods[i]))  # ajuster dans le code final


        ## Get green energy available
        #conso = predict_conso(curr_w1, curr_w2, curr_w3)

        for i in range(0, 3):
            energy_available[i] = energy_available[i] + prod[i] - conso[i]

            if energy_available[i] < 0:
                energy_available[i] = 0

            energy[j+1][i] = energy_available[i]
            consommation[j+1][i] = conso[i]
            production[j+1][i] = prod[i]




        print('Liste des consommations : ', conso)
        print('Liste des productions : ', prod)
        print('Liste des energies disponible : ', energy_available)

        pod_number[j][0] = curr_w1
        pod_number[j][1] = curr_w2
        pod_number[j][2] = curr_w3

    ##------------------------------ j != 0 ------------------------------##
    else:
        # Pod distribution
        D = compute_movement(curr_w1, curr_w2, curr_w3, w1_nb, w2_nb, w3_nb)
        move_pod(D[0], w1_pods_nb, w2_pods_nb, w1_pods_names, w2_pods_names, 2)
        move_pod(D[1], w1_pods_nb, w3_pods_nb, w1_pods_names, w3_pods_names, 3)
        move_pod(D[2], w2_pods_nb, w3_pods_nb, w2_pods_names, w3_pods_names, 3)
        move_pod(D[3], w2_pods_nb, w1_pods_nb, w2_pods_names, w1_pods_names, 1)
        move_pod(D[4], w3_pods_nb, w1_pods_nb, w3_pods_names, w1_pods_names, 1)
        move_pod(D[5], w3_pods_nb, w2_pods_nb, w3_pods_names, w2_pods_names, 2)
        curr_w1 = len(w1_pods_nb)
        curr_w2 = len(w2_pods_nb)
        curr_w3 = len(w3_pods_nb)

        curr_nb_pods = [curr_w1, curr_w2, curr_w3]

            ## Get prod and conso
        for i in range(3):
            data = appel_api(cities_name[i], j+1)

            cities_list[i].maj_temperature(data['Temperature'])
            cities_list[i].maj_uv(data['UV index'])
            cities_list[i].maj_weather_code(data['Weather Code'])
            cities_list[i].maj_cloud_cover(data['Cloud Cover'])
            cities_list[i].maj_humidity(data['Humidity'])

            cities_list[i].calcul_redement(j)

            prod.append(cities_list[i].calcul_production(3600))

            conso.append(cities_list[i].calcul_consommation(
                3600, curr_nb_pods[i]))  # ajuster dans le code final

        # Update energy metrics

        for i in range(0, 3):
            energy_available[i] = energy_available[i] + prod[i] - conso[i]

            if energy_available[i] < 0:
                energy_available[i] = 0

            energy[j+1][i] = energy_available[i]
            consommation[j+1][i] = conso[i]
            production[j+1][i] = prod[i]

        print('Liste des consommations : ', conso)
        print('Liste des productions : ', prod)
        print('Liste des energies disponible : ', energy_available)


        pod_number[j][0] = curr_w1
        pod_number[j][1] = curr_w2
        pod_number[j][2] = curr_w3

    print("Nombre de workload sur le Datacenter Paris : "+str(curr_w1))
    print("Nombre de workload sur le Datacenter Rouen : "+str(curr_w2))
    print("Nombre de workload sur le Datacenter Nice : "+str(curr_w3))

print('Energie disponible : ', energy)
print('Nombre de pods : ', pod_number)
print('Production : ', production)
print('Consommation : ', consommation)


# time.sleep(5)
# %%
# import matplotlib.pyplot as plt

## DISPLAY SECTION ##

# ## Display the green energy evolution

# plt.figure(1)
# plt.figure(figsize=(14, 10))    

# ax = plt.subplot(111)    
# ax.spines["top"].set_visible(False)    
# ax.spines["bottom"].set_visible(False)    
# ax.spines["right"].set_visible(False)    
# ax.spines["left"].set_visible(False)       
# ax.get_xaxis().tick_bottom()    
# ax.get_yaxis().tick_left() 
# ax.set_axisbelow(True)
# plt.grid(True, color="#93a1a1", alpha=0.3)
# plt.plot(energy, ":o")
# plt.title('Green energy evolution by time')
# plt.xlabel('Time [h]')
# plt.ylabel('Green energy available [kWh]')


# plt.legend(['Datacenter Paris', 'Datacenter Rouen', 'Datacenter Nice'])
# plt.show()
# plt.savefig("green_energy.png")

# ## Display the evolution of pod numbers on each node

# plt.figure(2)
# plt.figure(figsize=(10, 10))    

# ax = plt.subplot(111)    
# ax.spines["top"].set_visible(False)    
# ax.spines["bottom"].set_visible(False)    
# ax.spines["right"].set_visible(False)    
# ax.spines["left"].set_visible(False)       
# ax.get_xaxis().tick_bottom()    
# ax.get_yaxis().tick_left() 
# ax.set_axisbelow(True)
# plt.grid(True, color="#93a1a1", alpha=0.3)
# plt.plot(pod_number, ":o", label={'DC Nice', 'DC Rouen', 'DC Paris'})
# #plt.hist(pod_number[:,0], bins=24, alpha=0.5)
# #plt.hist(pod_number[:,1], bins=24, alpha=0.5)
# #plt.hist(pod_number[:,2], bins=24, alpha=0.5)
# plt.title('Workload number evolution by time')
# plt.xlabel('Time [h]')
# plt.ylabel('Workload number')

# plt.legend(['Datacenter Paris', 'Datacenter Rouen', 'Datacenter Nice'])
# plt.show()
# plt.savefig("pod_number.png")

# ## Display the evolution of node production

# plt.figure(3)
# plt.figure(figsize=(14, 10))    

# ax = plt.subplot(111)    
# ax.spines["top"].set_visible(False)    
# ax.spines["bottom"].set_visible(False)    
# ax.spines["right"].set_visible(False)    
# ax.spines["left"].set_visible(False)       
# ax.get_xaxis().tick_bottom()    
# ax.get_yaxis().tick_left() 
# ax.set_axisbelow(True)
# plt.grid(True, color="#93a1a1", alpha=0.3)
# plt.plot(production, ":o", label={'DC Paris', 'DC Rouen', 'DC Nice'})
# plt.title('Datacenter production evolution by time')
# plt.xlabel('Time [h]')
# plt.ylabel('Production [kWh]')

# plt.legend(['Datacenter Paris', 'Datacenter Rouen', 'Datacenter Nice'])
# plt.show()
# plt.savefig("production.png")

# ## Display the evolution of node production

# plt.figure(4)
# plt.figure(figsize=(10, 10))    

# ax = plt.subplot(111)    
# ax.spines["top"].set_visible(False)    
# ax.spines["bottom"].set_visible(False)    
# ax.spines["right"].set_visible(False)    
# ax.spines["left"].set_visible(False)       
# ax.get_xaxis().tick_bottom()    
# ax.get_yaxis().tick_left() 
# ax.set_axisbelow(True)
# plt.grid(True, color="#93a1a1", alpha=0.3)
# plt.plot(consommation, ":o", label={'DC Nice', 'DC Rouen', 'DC Paris'})
# plt.title('Node consumption evolution by time')
# plt.xlabel('Time [h]')
# plt.ylabel('Consumption [kWh]')

# plt.legend(['Datacenter Paris', 'Datacenter Rouen', 'Datacenter Nice'])
# plt.show()
# plt.savefig("consumption.png")


# %%
