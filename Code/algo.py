#%%
# coding: utf-8
import time
import os 
from operator import itemgetter
import yaml
import math 

DURATION = 24


starttime = time.time()

# %%
# TEST
def compute_nb_pods(nb_pods,ratio):
    nb = nb_pods*ratio
    return math.floor(nb)

def get_file_name(node_nb,pod_nb):
    if(node_nb == 1):
        new_file_name = "worker1_"+str(pod_nb)+".yaml"
    elif(node_nb == 2):
        new_file_name = "worker2_"+str(pod_nb)+".yaml"
    elif(node_nb == 3):
        new_file_name = "worker3_"+str(pod_nb)+".yaml"
    return new_file_name


def create_pod(origin_file,pod_nb,node_nb):
    file_name = get_file_name(node_nb,pod_nb)
    name = "pod"+str(pod_nb)
    os.system("cp "+origin_file+" "+file_name)
    with open(file_name, "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
        data['metadata']['name'] = name
        yamlfile.close()

    with open(file_name, 'w') as yamlfile:
        data1 = yaml.dump(data, yamlfile)
        yamlfile.close()
    os.system("sudo kubectl apply -f "+file_name)
    return file_name

def get_node_name_by_nb(node_nb):
    if (node_nb == 1):
        return "kind-worker"
    elif (node_nb == 1):
        return "kind-worker2"
    elif (node_nb == 3):
        return "kind-worker3"


def edit_node(node_nb,wi_pods_nb,wj_pods_nb,wi_pods_names,wj_pods_names):
    
    node_name = get_node_name_by_nb(node_nb)
    nb = wi_pods_nb[0]
    file_name = wi_pods_names[0]
    new_file_name = get_file_name(node_nb,nb)

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
    os.system("sudo kubectl delete pods pod"+str(nb))
    os.system("sudo kubectl apply -f "+new_file_name)

def compute_movement(old1,old2,old3,cur1,cur2,cur3):
    diff1 = int(old1 - cur1)
    diff2 = int(old2 - cur2)
    diff3 = int(old3 - cur3)
    # Calcul des déplacements de pods entres le node 1 et 2/3
    if ((diff1 == 0) or (diff1 < 0)) :
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
    if ((diff2 == 0) or (diff2 < 0)) :
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
    if ((diff3 == 0) or (diff3 < 0)) :
        w3_w1 = 0
        w3_w2= 0
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
    D = [w1_w2,w1_w3,w2_w3,w2_w1,w3_w1,w3_w2]
    return D

def move_pod(mv1,wi_pods_nb,wj_pods_nb,wi_pods_names,wj_pods_names,nb_node):
    if (mv1 != 0):
        for i in range(mv1):
            edit_node(nb_node,wi_pods_nb,wj_pods_nb,wi_pods_names,wj_pods_names)


# MAIN 

nb_pods = 10
L_ratio = [0.3,0.4,0.3, 0.4,0.3,0.3, 0.4,0.1,0.5]
w1_pods_nb = []
w1_pods_names = []
w2_pods_nb = []
w2_pods_names = []
w3_pods_nb = []
w3_pods_names = []
H = 3 #Nombres d'heures
init = 0
count_w1 = 0
count_w2 = 0
count_w3 = 0
for j in range(0,H):
    w1_nb = compute_nb_pods(nb_pods,L_ratio[j*H])
    w2_nb = compute_nb_pods(nb_pods,L_ratio[j*H + 1])
    w3_nb = compute_nb_pods(nb_pods,L_ratio[j*H + 2])
    if (init == 0):
        for a in range(1,int(w1_nb+1)):
            file = create_pod("worker1.yaml",a,1)
            count_w1 = count_w1 + 1
            w1_pods_nb.append(a)
            w1_pods_names.append(file)
        for b in range(1,int(w2_nb+1)):
            file = create_pod("worker2.yaml",b + count_w1,2)
            count_w2 = count_w2 + 1
            w2_pods_nb.append(b + count_w1)
            w2_pods_names.append(file)
        for c in range(1,int(w3_nb+1)):
            file = create_pod("worker3.yaml",c + count_w1 + count_w2,3)
            count_w3 = count_w3 + 1
            w3_pods_nb.append(c + count_w1 + count_w2)
            w3_pods_names.append(file)
        init = 1
        curr_w1 = count_w1
        curr_w2 = count_w2
        curr_w3 = count_w3
    else:
        D = compute_movement(curr_w1,curr_w2,curr_w3,w1_nb,w2_nb,w3_nb)
        move_pod(D[0],w1_pods_nb,w2_pods_nb,w1_pods_names,w2_pods_names,2)
        move_pod(D[1],w1_pods_nb,w3_pods_nb,w1_pods_names,w3_pods_names,3)
        move_pod(D[2],w2_pods_nb,w3_pods_nb,w2_pods_names,w3_pods_names,3)
        move_pod(D[3],w2_pods_nb,w1_pods_nb,w2_pods_names,w1_pods_names,1)
        move_pod(D[4],w3_pods_nb,w1_pods_nb,w3_pods_names,w1_pods_names,1)
        move_pod(D[5],w3_pods_nb,w2_pods_nb,w3_pods_names,w2_pods_names,2)
        curr_w1 = len(w1_pods_nb)
        curr_w2 = len(w2_pods_nb)
        curr_w3 = len(w3_pods_nb)

    print("Il y'a "+str(curr_w1)+" pods dans le worker 1")
    print("Il y'a "+str(curr_w2)+" pods dans le worker 2")
    print("Il y'a "+str(curr_w3)+" pods dans le worker 3")
    #time.sleep(5)



