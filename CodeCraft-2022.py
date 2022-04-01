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
        lines = file_to_read.readline()  # ���ж�ȡ����
        for i in range(len(Site)):
            lines = file_to_read.readline()  # ���ж�ȡ����
            if not lines:
                break
            lines=lines[:len(lines)-1]
            p_tmp=lines.split(",")
            p_tmp=p_tmp[1:]
            Site[i].delayTime=[int(j) for j in p_tmp]

def readConfig(dir):
    with open(dir, 'r') as file_to_read:
        lines = file_to_read.readline()  # ���ж�ȡ����
        if lines=="[config]":
            print("��ȡ�����ļ�")
        lines = file_to_read.readline()  # ���ж�ȡ����
        for i in range(len(lines)):
            if lines[i]=="=":
                right=lines[i+1:len(lines)]
                break
        for i in range(len(right)):
            if(right[i]=="\n"):
                qos=int(right[:i])
                break
        lines = file_to_read.readline()  # ���ж�ȡ����
        for i in range(len(lines)):
            if lines[i]=="=":
                base_count=int(lines[i+1:len(lines)])
    return qos,base_count

def readDemand(dir):
    with open(dir, 'r') as file_to_read:
        lines = file_to_read.readline()  # ���ж�ȡ����
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
            lines = file_to_read.readline()  # ���ж�ȡ����
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
            flag=0#�����ʱ���Ƿ�ͳ�ƹ�
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
        lines = file_to_read.readline()  # ���ж�ȡ����
        lines = lines[:len(lines) - 1]
        p_tmp = lines.split(",")
        Site=[]
        while True:
            lines = file_to_read.readline()  # ���ж�ȡ����
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
                    print("solution������")
                    break
                    pass
                given = 0
                p_tmp = lines.split(">,<")
                for i in range(len(p_tmp[0])):
                    if p_tmp[0][i] == ":":
                        name = p_tmp[0][:i]
                        p_tmp[0] = p_tmp[0][i + 2:]
                        break
                ##��client������
                find_flag = 0
                find_index=client
                for find_index_tmp in range(len(Client)):
                    if Client[find_index_tmp].name == name:
                        find_flag = 1
                        if is_Done[find_index_tmp] == 1:
                            print(day, "ʱ���", name, "�Ѿ����ֹ���")
                            exit()
                        else:
                            is_Done[find_index_tmp] = 1
                        find_index=find_index_tmp
                        break
                if find_flag == 0:
                    print(day, "ʱ���", name, "����Client��������")
                    exit()

                # A: �յ����
                if (len(lines) == len(name) + 1):
                    if Client[find_index].demand!=0:
                        print(Client[find_index].name,"��",day,"ʱ��û�з������󣬵�����������",sum(Client[find_index].demand[day]))
                    continue

                #ɾ���س���<>�ȷ���
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
                        if(Site[site_id].sitename==one_tmp[0]):#�ҽڵ������
                            flag=1
                            if(Site[site_id].delayTime[find_index]>=qos_constraint):#find_index�ǽڵ��id
                                print(Client[find_index].name,"��qosδ�����㣬��������",Site[site_id].sitename)
                                # exit()
                            for use_id in range(1,len(one_tmp)):
                                stream_flag=0
                                for stream in Time[day].stream:
                                    if stream.name==one_tmp[use_id]:
                                        stream_flag=1
                                        tmp_used=stream.lst[find_index]
                                        break
                                if stream_flag==0:
                                    print("ʱ��",day,"��",Client[find_index].name,"û��",one_tmp[use_id],"�����")
                                Site[site_id].used[day]+=tmp_used
                                given+=tmp_used
                            if Site[site_id].used[day]>Site[site_id].bandwidth:
                                print(Site[site_id].sitename,"�ĸ��س����˴���")
                                print(Site[site_id].used)
                                print(Site[site_id].bandwidth)
                                exit()
                            break
                    if(flag==0):
                        print("��ʱ��",day,"û������ڵ�",one_tmp[0])
                if given!=sum(Client[find_index].demand[day]):
                    print(Client[find_index].name, "�ĵ�", day, "����¼��û����������")
                    print("�ַ���", given, "������Ҫ", sum(Client[find_index].demand[day]))
                    # exit()
            for i in range(len(is_Done)):
                if is_Done[i]==0:
                    print(Client[i].name,"û�г���")

        lines = file_to_read.readline()
        if not lines:
            print("solution�պö���")
        else:
            print("��ô������һ����")
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
    plt.axhline(y=charge_95[point], ls=":", c="red")  # ���ˮƽֱ��
    # plt.axhline(y=site.bandwidth, ls=":", c="green")  # ���ˮƽֱ��
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
        # print(Site[i].sitename,"in ��ͼ",y)
        # plt.plot(y)
        y.sort()
        # print(Site[i].sitename, "in ��ͼ", y)
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

        plt.axhline(y=charge_95[point], ls=":", c="red")  # ���ˮƽֱ��
        # plt.axhline(y=site.bandwidth, ls=":", c="green")  # ���ˮƽֱ��
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
    #��ȡ�����ļ�
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
    #
    # delete_picture("site_load_pic")
    #
    #
    # # picture(Site[0])
    # site_waste_sort=sort_waste_rate(Site)
    # # print(site_waste_sort)
    # picture_according_load(site_waste_sort,Site)
    #
    #     # print("picture ",site_waste_sort[i][0])



