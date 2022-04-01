import math
import matplotlib.pyplot as plt
import shutil
import os
class site_info():
    def __init__(self,name,bandwidth):
        self.sitename=name
        self.bandwidth=bandwidth
        self.used=[]

        self.delayTime=[]
        self.price=1

class client_info():
    def __init__(self,name):
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

def readDemand(dir):
    with open(dir, 'r') as file_to_read:
        lines = file_to_read.readline()  # 整行读取数据
        lines = lines[:len(lines) - 1]
        p_tmp = lines.split(",")
        Client_Count=len(p_tmp)-1
        Client=[client_info for i in range(Client_Count)]
        for i in range(1,len(p_tmp)):
            Client[i-1]=client_info(p_tmp[i])
        Time_count=0
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            if not lines:
                break
                pass
            Time_count += 1
            lines=lines[:len(lines)-1]
            p_tmp=lines.split(",")
            for i in range(1,len(p_tmp)):
                Client[i-1].demand.append(int(p_tmp[i]))
    return Client,Client_Count,Time_count

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
            site.used=[0 for i in range(Time_count)]
            Site.append(site)
    return Site

def readSolution(dir):
    with open(solutionFile,'r')as file_to_read:
        for day in range(Time_count):
            is_Done = [0 for i in range(Client_Count)]
            for client in range(Client_Count):
                lines = file_to_read.readline()
                lines = lines[:len(lines) - 1]
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
                for find_index_tmp in range(Client_Count):
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
                        print(Client[find_index].name,"在",day,"时刻没有分配需求，但是其需求是",Client[find_index].demand[day])
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
                            if(Site[site_id].delayTime[find_index]>=qos_constraint):
                                print(Client[find_index].name,"的qos未被满足，它发给了",Site[site_id].sitename)
                                # exit()
                            Site[site_id].used[day]+=int(one_tmp[1])
                            given+=int(one_tmp[1])
                            if Site[site_id].used[day]>Site[site_id].bandwidth:
                                print(Site[site_id].sitename,"的负载超过了带宽")
                                print(Site[site_id].used)
                                print(Site[site_id].bandwidth)
                                exit()
                            break
                    if(flag==0):
                        print("在时刻",day,"没有这个节点",one_tmp[0])
                if given!=Client[find_index].demand[day]:
                    print(Client[find_index].name, "的第", day, "个记录点没有满足需求")
                    print("分发了", given, "需求，需要", Client[find_index].demand[day])
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
    sum=[]
    for i in range(len(Site)):
        charge_95=sorted(Site[i].used)
        point=math.ceil(len(charge_95)*0.95)-1
        sum.append(charge_95[point]*Site[i].price)
    return sum

def delete_picture(dir):
    shutil.rmtree(dir)
    os.mkdir(dir)

def picture(site):
    plt.cla()
    x=range(len(site.used))
    y=site.used
    # plt.plot(y)
    plt.bar(x,y)
    charge_95 = sorted(site.used)
    point = math.ceil(len(charge_95) * 0.95)-1
    sense_use=0
    for i in range(len(site.used)):
        if site.used[i]<charge_95[point]:
            sense_use+=site.used[i]
        else:
            sense_use+=charge_95[point]
    if charge_95[point]==0:
        plt.title(site.sitename+"  0 use")
    else:
        waste_rate=(charge_95[point]*len(site.used)-sense_use)/(charge_95[point]*len(site.used))
        plt.title(site.sitename+"  waste_rate:"+str(waste_rate))
    plt.axhline(y=charge_95[point], ls=":", c="red")  # 添加水平直线
    # plt.axhline(y=site.bandwidth, ls=":", c="green")  # 添加水平直线
    plt.savefig("./site_load_pic/"+site.sitename)


def picture_according_load(site_waste_sort,Site):
    print(site_waste_sort)
    for i in range(len(site_waste_sort)):
        if Site[site_waste_sort[i][0]].sitename=="Dn":
            print("-------------------------------------------------")
        print("picture ",site_waste_sort[i][0])
        # print(Site[i].sitename,Site[i].used)
        # plt.clf()
        x=range(len(Site[site_waste_sort[i][0]].used))
        y=Site[site_waste_sort[i][0]].used
        # print(Site[i].sitename,"in 画图",y)
        # plt.plot(y)
        y.sort()
        # print(Site[i].sitename, "in 画图", y)
        # plt.text(20, 1000, str(y))
        plt.plot(x,y)
        # plt.bar(x,y)
        link=0
        for j in Site[site_waste_sort[i][0]].delayTime:
            if j<qos_constraint:
                link+=1
        paixu=Site[site_waste_sort[i][0]].used
        charge_95 = sorted(paixu)
        point = math.ceil(len(charge_95) * 0.95)-1
        sense_use=0
        for j in range(len(paixu)):
            if paixu[j]<charge_95[point]:
                sense_use+=paixu[j]
            else:
                sense_use+=charge_95[point]
        if charge_95[point]==0:
            plt.title(Site[site_waste_sort[i][0]].sitename+"  0 use"+str(Site[i].used))
        else:
            waste_rate=(charge_95[point]*len(Site[site_waste_sort[i][0]].used)-sense_use)/(charge_95[point]*len(Site[site_waste_sort[i][0]].used))
            plt.title(Site[site_waste_sort[i][0]].sitename+"  waste_rate:"+str(waste_rate)+"\n link_count:"+str(link)+"\nbandwidth:"+str(Site[i].bandwidth))

        plt.axhline(y=charge_95[point], ls=":", c="red")  # 添加水平直线
        # plt.axhline(y=site.bandwidth, ls=":", c="green")  # 添加水平直线
        plt.savefig("./site_load_pic/"+Site[site_waste_sort[i][0]].sitename)

        plt.close()


def sort_waste_rate(Site):
    site_waste_sort = []
    for i in range(len(Site)):
        tmp = []
        tmp.append(i)
        charge_95 = sorted(Site[i].used)
        point = math.ceil(len(charge_95) * 0.95) - 1
        sense_use = 0
        for j in range(len(Site[i].used)):
            if Site[i].used[j] < charge_95[point]:
                sense_use += Site[i].used[j]
            else:
                sense_use += charge_95[point]
        if charge_95[point] == 0:
            waste_rate = 0
        else:
            waste_rate = (charge_95[point] * len(Site[i].used) - sense_use) / (charge_95[point] * len(Site[i].used))
        tmp.append(waste_rate)
        # print(tmp)
        site_waste_sort.append(tmp)
    # print(site_waste_sort)
    site_waste_sort.sort(key=lambda x: x[1], reverse=1)
    return site_waste_sort


if __name__ == '__main__':
    #读取输入文件
    demandFile = 'data/demand.csv'
    site_bandwidthFile = 'data/site_bandwidth.csv'
    solutionFile = 'output/solution.txt'
    qosFile='data/qos.csv'

    qos_constraint=400
    Client,Client_Count,Time_count=readDemand(demandFile)
    Site = readSite(site_bandwidthFile)
    readQos(qosFile)
    readSolution(solutionFile)
    price=billing()
    print(price)
    print(sum(price))

    delete_picture("site_load_pic")


    # picture(Site[0])
    site_waste_sort=sort_waste_rate(Site)
    # print(site_waste_sort)
    picture_according_load(site_waste_sort,Site)

        # print("picture ",site_waste_sort[i][0])








