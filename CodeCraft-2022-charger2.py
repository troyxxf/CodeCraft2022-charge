#coding=gbk
import math
import os
import shutil
import matplotlib.pyplot as plt

class stream_info():
    def __init__(self,name,lst):
        self.name=name
        self.lst=lst

class time_info():
    def __init__(self,name):
        self.name=name
        self.stream=[]

class site_info():
    def __init__(self,name,bandwidth):
        self.sitename=name
        self.bandwidth=bandwidth
        self.used=[]
        self.delayTime=[]
        self.price=1

class client_info():
    def __init__(self,name,demand):
        self.name=name
        self.demand=[]

def readQos(dir):
    with open(dir, 'r') as file_to_read:
        lines = file_to_read.readline()  # 整行读取数据
        for i in range(len(Site)):
            lines = file_to_read.readline()  # 整行读取数据
            if not lines:
                break
            lines=lines[:len(lines)-1]
            p_tmp=lines.split(",")
            p_tmp=p_tmp[1:]
            Site[i].delayTime=[int(j) for j in p_tmp]

def readConfig(dir):
    with open(dir, 'r') as file_to_read:
        lines = file_to_read.readline()  # 整行读取数据
        if lines=="[config]":
            print("读取配置文件")
        lines = file_to_read.readline()  # 整行读取数据
        for i in range(len(lines)):
            if lines[i]=="=":
                right=lines[i+1:len(lines)]
                break
        for i in range(len(right)):
            if(right[i]=="\n"):
                qos=int(right[:i])
                break
        lines = file_to_read.readline()  # 整行读取数据
        for i in range(len(lines)):
            if lines[i]=="=":
                base_count=int(lines[i+1:len(lines)])
    return qos,base_count

def readDemand(dir):
    with open(dir, 'r') as file_to_read:
        lines = file_to_read.readline()  # 整行读取数据
        for i in range(len(lines)):
            if lines[i] == "\n":
                lines = lines[:i]
                break
        p_tmp = lines.split(",")
        Client_Count=len(p_tmp)-2
        Client=[client_info for i in range(Client_Count)]
        for i in range(2,len(p_tmp)):
            Client[i-2]=client_info(p_tmp[i],[])
        Time_count=0
        Time=[]

        while True:
            lines = file_to_read.readline()  # 整行读取数据
            if not lines:
                break
                pass

            # lines=lines[:len(lines)-1]
            for i in range(len(lines)):
                if lines[i]=="\n":
                    lines=lines[:i]
                    break
            p_tmp=lines.split(",")
            t_name =p_tmp[0]
            stream_name=p_tmp[1]
            stream_tmp=[int(p_tmp[i]) for i in range(2,len(p_tmp))]
            new_stream=stream_info(stream_name,stream_tmp)
            # print(stream_tmp)
            # for i in range(2,len(p_tmp)):
            #     Client[i-2].demand.append(int(p_tmp[i]))
            flag=0#找这个时间是否统计过
            for tt in Time:
                if tt.name==t_name:
                    flag=1
                    tt.stream.append(new_stream)
                    break
            if flag==0:
                new_t=time_info(t_name)
                new_t.stream.append(new_stream)
                Time.append(new_t)

    return Time,Client

def readSite(dir):
    with open(dir, 'r') as file_to_read:
        lines = file_to_read.readline()  # 整行读取数据
        lines = lines[:len(lines) - 1]
        p_tmp = lines.split(",")
        Site=[]
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            if not lines:
                break
            lines=lines[:len(lines)-1]
            p_tmp = lines.split(",")
            site=site_info(p_tmp[0],int(p_tmp[1]))
            site.used=[0 for i in range(Time_Count+1)]
            Site.append(site)
    return Site

def addStreamDemandToClient(Client,Time):
    for client_index in range(len(Client)):
        for t in Time:
            demand_one_t = []
            for stream_one in t.stream:
                # print(stream_one.lst)
                demand_one_t.append(stream_one.lst[client_index])
            Client[client_index].demand.append(demand_one_t)


def readSolution(dir):
    with open(solutionFile,'r')as file_to_read:
        for day in range(len(Time)):
            is_Done = [0 for i in range(len(Client))]
            for client in range(len(Client)):
                lines = file_to_read.readline()
                for i in range(len(lines)):
                    if lines[i] == "\n":
                        lines = lines[:i]
                        break
                # lines[0]=lines.split(":<")

                if not lines:
                    print("solution差数据")
                    break
                    pass
                given = 0
                p_tmp = lines.split(">,<")
                for i in range(len(p_tmp[0])):
                    if p_tmp[0][i] == ":":
                        name = p_tmp[0][:i]
                        p_tmp[0] = p_tmp[0][i + 2:]
                        break
                ##找client的名字
                find_flag = 0
                find_index=client
                for find_index_tmp in range(len(Client)):
                    if Client[find_index_tmp].name == name:
                        find_flag = 1
                        if is_Done[find_index_tmp] == 1:
                            print(day, "时间点", name, "已经出现过了")
                            exit()
                        else:
                            is_Done[find_index_tmp] = 1
                        find_index=find_index_tmp
                        break
                if find_flag == 0:
                    print(day, "时间点", name, "不在Client的名字中")
                    exit()

                # A: 空的情况
                if (len(lines) == len(name) + 1):
                    if Client[find_index].demand!=0:
                        print(Client[find_index].name,"在",day,"时刻没有分配需求，但是其需求是",sum(Client[find_index].demand[day]))
                    continue

                #删除回车和<>等符号
                lastone=p_tmp[len(p_tmp)-1]
                if lastone[len(lastone)-2:]=="\n":
                    lastone=lastone[:len(lastone)-2]
                elif lastone[len(lastone)-1:]==">":
                    lastone=lastone[:len(lastone)-1]
                p_tmp[len(p_tmp)-1]=lastone

                for i in p_tmp:
                    one_tmp=i.split(",")
                    flag=0
                    for site_id in range(len(Site)):
                        if(Site[site_id].sitename==one_tmp[0]):#找节点的名字
                            flag=1
                            if(Site[site_id].delayTime[find_index]>=qos_constraint):#find_index是节点的id
                                print(Client[find_index].name,"的qos未被满足，它发给了",Site[site_id].sitename)
                                # exit()
                            for use_id in range(1,len(one_tmp)):
                                stream_flag=0
                                for stream in Time[day].stream:
                                    if stream.name==one_tmp[use_id]:
                                        stream_flag=1
                                        tmp_used=stream.lst[find_index]
                                        break
                                if stream_flag==0:
                                    print("时刻",day,"中",Client[find_index].name,"没有",one_tmp[use_id],"这个流")
                                Site[site_id].used[day]+=tmp_used
                                given+=tmp_used
                            if Site[site_id].used[day]>Site[site_id].bandwidth:
                                print(Site[site_id].sitename,"的负载超过了带宽")
                                print(Site[site_id].used)
                                print(Site[site_id].bandwidth)
                                exit()
                            break
                    if(flag==0):
                        print("在时刻",day,"没有这个节点",one_tmp[0])
                if given!=sum(Client[find_index].demand[day]):
                    print(Client[find_index].name, "的第", day, "个记录点没有满足需求")
                    print("分发了", given, "需求，需要", sum(Client[find_index].demand[day]))
                    # exit()
            for i in range(len(is_Done)):
                if is_Done[i]==0:
                    print(Client[i].name,"没有出现")

        lines = file_to_read.readline()
        if not lines:
            print("solution刚好读完")
        else:
            print("怎么读出多一行了")
            print(lines)

def billing():
    result=[]
    for i in range(len(Site)):
        charge_95=sorted(Site[i].used)
        # print(charge_95)
        point=math.ceil(len(charge_95)*0.95)-1
        if sum(charge_95)==0:
            sum_real=0
        else:
            if charge_95[point]*Site[i].price<=base_count:
                sum_real=base_count
            else:
                sum_real=(charge_95[point]*Site[i].price-base_count)*(charge_95[point]*Site[i].price-base_count)/Site[i].bandwidth+charge_95[point]*Site[i].price
                if sum_real>=(sum_real//1+0.5):
                    sum_real=math.ceil(sum_real)
                else:
                    sum_real=math.floor(sum_real)
        result.append(sum_real)
    return result


if __name__ == '__main__':
    #读取输入文件
    configFile='data/config.ini'
    demandFile = 'data/demand.csv'
    site_bandwidthFile = 'data/site_bandwidth.csv'
    solutionFile = 'output/solution.txt'
    qosFile='data/qos.csv'

    qos_constraint,base_count=readConfig(configFile)
    Time,Client=readDemand(demandFile)
    Time_Count = len(Time)
    Site = readSite(site_bandwidthFile)
    addStreamDemandToClient(Client,Time)
    readQos(qosFile)

    readSolution(solutionFile)

    price=billing()
    print(price)
    print(sum(price))




