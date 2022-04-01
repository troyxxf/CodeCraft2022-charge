#coding:UTF-8

import random
import math
from scipy.signal import savgol_filter

qos_constraint=400

class Site_info():
    def __init__(self,name,bandwidth,qos):
        self.name=name
        self.bandwidth=bandwidth
        self.qos=qos

class Client_info():
    def __init__(self,name):
        self.name=name
        self.demand=[]

def create_Site(Site_Count):
    Site=[]
    for i in range(Site_Count):
        name="Site"+str(i)
        bandwidth=0
        qos=oneSiteQosCreate(Client_Count)
        Site.append(Site_info(name,bandwidth,qos))
    return Site

def set_bandwidth(site):
    bandwidth_t = []
    for t in range(time):
        cur_bandwidth = 0
        for can_com in range(len(site.qos)):
            if site.qos[can_com] < qos_constraint:
                con_count=0
                for s in range(Site_Count):
                    if Site[s].qos[can_com]<qos_constraint:
                        con_count+=1
                cur_bandwidth+=Client[can_com].demand[t]//con_count+1
                # cur_bandwidth += Client[can_com].demand[t]
        bandwidth_t.append(cur_bandwidth)
    # print(bandwidth_t)
    site.bandwidth=math.ceil(max(bandwidth_t)*hard)


def create_Client(Client_Count):
    Client=[]
    for i in range(Client_Count):
        name="Client"+str(i)
        client=Client_info(name)
        demand=[]
        for i in range(time):
            touzi=random.randint(0,8)
            if touzi<5:
                demand_tmp=demand_all[i]//Client_Count*2+random.randint(0,10000)
            else:
                demand_tmp=demand_all[i]//Client_Count+random.randint(0,50000)

            demand_tmp = demand_all[i] // Client_Count + random.randint(0, 50000)
            # demand_tmp=random.randint(400000,500000)
            demand.append(demand_tmp)
        client.demand=demand
        Client.append(client)
    return Client

def oneSiteQosCreate(Client_Count):
    lst=[]
    for i in range(Client_Count):
        tmp=random.randint(350,850)
        # tmp=random.randint(350,800)
        lst.append(tmp)
    for i in range(Client_Count):
        if lst[i]<qos_constraint:
            return lst
    return oneSiteQosCreate(Client_Count)

def write_demand(dir):
    with open(dir, 'w')as f:
        line = "mtime,"
        client_names = []
        for client_index in range(Client_Count):
            client_names.append(Client[client_index].name)
        nameString = ",".join(client_names)
        line += nameString
        line += "\n"
        f.write(line)
        for t in range(time):
            line="2021-11-01T00:00"
            line+=","
            lst=[]
            for x in range(Client_Count):
                lst.append(Client[x].demand[t])

            lst_str=[str(i) for i in lst]
            full_str=",".join(lst_str)
            line+=full_str
            line+="\n"
            f.write(line)

def write_qos(dir):
    with open(dir,'w')as f:
        line="site_name,"
        client_names=[]
        for client_index in range(Client_Count):
            client_names.append(Client[client_index].name)
        nameString=",".join(client_names)
        line+=nameString
        line+="\n"
        f.write(line)
        for site_index in range(Site_Count):
            line=Site[site_index].name
            line+=","
            qos_line=Site[site_index].qos
            qos_line=[str(i) for i in qos_line]
            qoo=",".join(qos_line)
            line+=qoo
            line+="\n"
            f.write(line)

def write_bandwidth(dir):
    with open(dir, 'w')as f:
        f.write("site_name,bandwidth\n")

        for i in range(Site_Count):
            line = ""
            line += Site[i].name
            line += ","
            line += str(Site[i].bandwidth)
            line += "\n"
            f.write(line)


def create_Qos(Qos_path):
    with open(Qos_path,'w')as f:
        line="site_name,"
        client_names=[]
        for client_index in range(Client_Count):
            client_names.append(Client[client_index].name)
        nameString=",".join(client_names)
        line+=nameString
        line+="\n"
        f.write(line)
        for site_index in range(Site_Count):
            line=Site[site_index].name
            line+=","
            qoe_line=oneSiteQosCreate(Client_Count)
            line+=qoe_line
            line+="\n"
            f.write(line)


if __name__ == '__main__':
    Client_Count=35
    Site_Count=135
    time=8928
    hard=3#1最难，2减半

    site_path='./test/site_bandwidth.csv'
    Qos_path='./test/qos.csv'
    demand_path='./test/demand.csv'


#Clean data
    file = open(site_path, 'w').close()
    file=open(Qos_path,'w').close()
    file=open(demand_path,'w').close()

    Site_Bandwidth_init=[0 for i in range(Site_Count)]
    demand_all=[]
    for t in range(time):
        # demand_all.append(math.ceil(550000*(math.sin(t/1000)+1)))
        demand_all.append(math.ceil(2100000+500000*random.random()))
    # print(demand_all)
    Client=create_Client(Client_Count)
    Site=create_Site(Site_Count)
    for i in range(Site_Count):
        set_bandwidth(Site[i])

    write_demand(demand_path)
    write_qos(Qos_path)
    write_bandwidth(site_path)

    # for s in range(Site_Count):
    #     print(Site[s].bandwidth)


    #

    # create_Qos(Qos_path)
    # create_demand_different_by_sin(demand_path,time)
