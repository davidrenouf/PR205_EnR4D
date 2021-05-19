# %%
# coding: utf-8
import time
import os
from operator import itemgetter
import yaml
import numpy as np
import requests
import math


def compute_nb_pods(nb_pods, ratio):
    nb = nb_pods*ratio
    return math.floor(nb)


def get_file_name(node_nb, pod_nb):
    if(node_nb == 1):
        new_file_name = "worker1_"+str(pod_nb)+".yaml"
    elif(node_nb == 2):
        new_file_name = "worker2_"+str(pod_nb)+".yaml"
    elif(node_nb == 3):
        new_file_name = "worker3_"+str(pod_nb)+".yaml"
    return new_file_name


def create_pod(origin_file, pod_nb, node_nb):
    file_name = get_file_name(node_nb, pod_nb)
    name = "pod"+str(pod_nb)
    os.system("cp "+origin_file+" "+file_name)
    with open(file_name, "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
        data['metadata']['name'] = name
        yamlfile.close()

    with open(file_name, 'w') as yamlfile:
        data1 = yaml.dump(data, yamlfile)
        yamlfile.close()
    os.system("kubectl apply -f "+file_name)
    return file_name


def get_node_name_by_nb(node_nb):
    if (node_nb == 1):
        return "kind-worker"
    elif (node_nb == 1):
        return "kind-worker2"
    elif (node_nb == 3):
        return "kind-worker3"


def edit_node(node_nb, wi_pods_nb, wj_pods_nb, wi_pods_names, wj_pods_names):

    node_name = get_node_name_by_nb(node_nb)
    nb = wi_pods_nb[0]
    file_name = wi_pods_names[0]
    new_file_name = get_file_name(node_nb, nb)

    wj_pods_names.append(new_file_name)
    wj_pods_nb.append(nb)
    wi_pods_names.pop(0)
    wi_pods_nb.pop(0)

    os.system("cp "+file_name+" "+new_file_name)
    os.system("rm "+file_name)

    with open(new_file_name, "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
        data['spec']['nodeName'] = node_name
        yamlfile.close()

    with open(new_file_name, 'w') as yamlfile:
        data1 = yaml.dump(data, yamlfile)
        yamlfile.close()
    os.system("kubectl delete pod pod"+str(nb))
    os.system("kubectl apply -f "+new_file_name)


def compute_movement(old1, old2, old3, cur1, cur2, cur3):
    diff1 = int(old1 - cur1)
    diff2 = int(old2 - cur2)
    diff3 = int(old3 - cur3)
    # Calcul des déplacements de pods entres le node 1 et 2/3
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

    # Calcul des déplacements de pods entres le node 2 et 3/1
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

    # Calcul des déplacements de pods entres le node 3 et 1/2
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
    D = [w1_w2, w1_w3, w2_w3, w2_w1, w3_w1, w3_w2]
    return D


def move_pod(mv1, wi_pods_nb, wj_pods_nb, wi_pods_names, wj_pods_names, nb_node):
    if (mv1 != 0):
        for i in range(mv1):
            edit_node(nb_node, wi_pods_nb, wj_pods_nb,
                      wi_pods_names, wj_pods_names)


def predict_conso(nb_pod1, nb_pod2, nb_pod3):
    return [nb_pod1*10, nb_pod2*10, nb_pod3*10]


def predict_prod():
    return [10, 20, 50]


def appel_api(dc_city, nb):
    # API call

    api_result = requests.get('http://localhost:8080/scenario1/' + str(nb))

    api_response = api_result.json()

    return api_response[dc_city][0]


class DataCenter:
    "Definition d'un data center"

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

    def calcul_redement(self):
        rendement = 1

        # Weather code 113 = sunny

        if (self.weather_code != 113):
            rendement *= 0.7

        if (self.uv >= 3):
            rendement *= 1.2

        if (self.humidity >= 50):
            rendement *= 0.9

        if (self.cloud_cover >= 50):
            rendement *= 0.5

        if (rendement > 1):
            rendement = 1

        self.rendement = rendement

    def calcul_production(self, t):
        "Production sur t secondes"
        production = self.ensoleillement * self.kWc * self.rendement
        productionf = production*(1 - abs(25-self.temperature)*0.004)
        productiont = (productionf * t) / 31536000

        return round(productiont * 1000)  # 1000 nb de panneau

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
nb_pods = 10
L_ratio = [0.2, 0.5, 0.3, 0.3, 0.6, 0.1, 0.3, 0.5, 0.2]
w1_pods_nb = []
w1_pods_names = []
w2_pods_nb = []
w2_pods_names = []
w3_pods_nb = []
w3_pods_names = []
H = 12  # Nombres d'heures
init = 0
count_w1 = 0
count_w2 = 0
count_w3 = 0

# Datacenters
cities_name = ['Rouen', 'Bordeaux', 'Nice']

Rouen = DataCenter(1000, 1, 25, 3, 20, 3, 113, 10)
Bordeaux = DataCenter(1200, 1, 25, 3, 20, 3, 113, 10)
Nice = DataCenter(1500, 1, 25, 3, 20, 3, 113, 10)

cities_list = []

cities_list.append(Rouen)
cities_list.append(Bordeaux)
cities_list.append(Nice)

# Metrics
energy = np.zeros([H+1, 3])
pod_number = np.zeros([H, 3])
energy_available = [1550, 1200, 850]

for i in range(0, 3):
    energy[0][i] = energy_available[i]

for j in range(0, H):

    ## Metrics initialisation : consumption / production / ratio (scoring system)
    conso = []
    prod = []
    ratio = get_ratio(energy_available)
    print('Ratio de David :',ratio)
    
    ## Get prod and conso
    for i in range(3):
        data = appel_api(cities_name[i], j+1)

        cities_list[i].maj_temperature(data['Temperature'])
        cities_list[i].maj_uv(data['UV index'])
        cities_list[i].maj_weather_code(data['Weather Code'])
        cities_list[i].maj_cloud_cover(data['Cloud Cover'])
        cities_list[i].maj_humidity(data['Humidity'])

        cities_list[i].calcul_redement()

        prod.append(cities_list[i].calcul_production(1800))

        conso.append(cities_list[i].calcul_consommation(
            1800, 1))  # ajuster dans le code final

    ## Pod distribution according to ratio
    w1_nb = compute_nb_pods(nb_pods, ratio[0])
    w2_nb = compute_nb_pods(nb_pods, ratio[1])
    w3_nb = compute_nb_pods(nb_pods, ratio[2])

    ##------------------------------ j = 0 ------------------------------##
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

        ## Get green energy available
        #conso = predict_conso(curr_w1, curr_w2, curr_w3)

        for i in range(0, 3):
            energy_available[i] = energy_available[i] + prod[i] - conso[i]
            energy[j+1][i] = energy_available[i]

        print('Consommation : ', conso)
        print('Production : ', prod)
        print('Energie disponible : ', energy_available)

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

        # Update energy metrics

        for i in range(0, 3):
            energy_available[i] = energy_available[i] + prod[i] - conso[i]
            energy[j+1][i] = energy_available[i]

        print('Consommation : ', conso)
        print('Production : ', prod)
        print('Energie disponible : ', energy_available)


        pod_number[j][0] = curr_w1
        pod_number[j][1] = curr_w2
        pod_number[j][2] = curr_w3

    print("Il y'a "+str(curr_w1)+" pods dans le worker 1")
    print("Il y'a "+str(curr_w2)+" pods dans le worker 2")
    print("Il y'a "+str(curr_w3)+" pods dans le worker 3")

print('Energie disponible : ', energy)
print('Nombre de pods : ', pod_number)

# time.sleep(5)
# %%
