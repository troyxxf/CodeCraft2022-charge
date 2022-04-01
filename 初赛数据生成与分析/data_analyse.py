#coding=utf-8

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

def drawLink(All_Site):
    with open("data_analysis/link.txt",'w')as f:
        name_lst = []
        for client in Client:
            name_lst.append(client.name)
        name_string = ",".join(name_lst)
        name_string+="\n"
        f.write(name_string)
        delay=[]
        for site in All_Site:
            line=site.sitename
            delay_lst=[]
            for link_judge in site.delayTime:
                if link_judge<=qos_constraint:
                    delay_lst.append(1)
                else:
                    delay_lst.append(0)
            delay.append(delay_lst)
            delay_str=[str(i) for i in delay_lst]
            line_delay=",".join(delay_str)
            line+=line_delay
            line+="\n"
            f.write(line)
    plt.cla()
    link_count_lst=[0 for i in range(Client_Count+1)]
    for i in range(len(All_Site)):

        link_count_lst[sum(delay[i])]+=1
    x=[i for i in range(Client_Count+1)]
    plt.bar(x,link_count_lst)
    plt.title("Link_")
    plt.savefig("data_analysis/link")


def drawBandwidth(All_Site):
    plt.cla()
    x=[]
    y=[]
    link=[]
    for site in All_Site:
        x.append(site.sitename)
        y.append(site.bandwidth)
        delay_lst = []
        for link_judge in site.delayTime:
            if link_judge <= qos_constraint:
                delay_lst.append(1)
            else:
                delay_lst.append(0)
        link.append(sum(delay_lst))
    link=[i*10000 for i in link]
    plt.title("bandwidth")
    plt.plot(x,y,label="bandwidth",color="green")
    plt.plot(x, link,label='link_count', color="blue")
    plt.savefig("data_analysis/bandwidth")

def drawSortBandwidth(All_Site):
    plt.cla()
    ans=[]
    for site in All_Site:
        tmp=[]
        tmp.append(site.sitename)
        tmp.append(site.bandwidth)
        ans.append(tmp)
    plt.title("sorted_bandwidth")
    x=[s[0] for s in ans]
    y=[s[0] for s in ans]
    plt.plot(x, y, label="bandwidth", color="green")
    plt.savefig("data_analysis/sort_bandwidth")

def delete_picture(dir):
    shutil.rmtree(dir)
    os.mkdir(dir)

def draw_demand(client):
    plt.cla()
    x=range(len(client.demand))
    y=client.demand
    plt.plot(y)
    plt.savefig("data_analysis/"+client.name)

def draw_all_demand(Client):
    plt.cla()
    demand_all=[]
    x=[i for i in range(len(Client[0].demand))]
    print(x)
    for demand_index in range(len(Client[0].demand)):
        demand_tmp=0
        for client_index in range(len(Client)):
            demand_tmp+=Client[client_index].demand[demand_index]
        demand_all.append(demand_tmp)
    print(demand_all)
    plt.title("demand_all")
    plt.plot(x,demand_all)
    plt.savefig("data_analysis/demand_all")

def draw_all_sort_demand(Client):
    plt.cla()
    demand_all=[]
    x=[i for i in range(len(Client[0].demand))]
    print(x)
    for demand_index in range(len(Client[0].demand)):
        demand_tmp=0
        for client_index in range(len(Client)):
            demand_tmp+=Client[client_index].demand[demand_index]
        demand_all.append(demand_tmp)
    print(demand_all)
    demand_all.sort()
    plt.title("demand_all")
    plt.plot(x,demand_all)
    plt.savefig("data_analysis/demand_sort_all")

def draw_3D():
    import math

    from pyecharts import options as opts
    from pyecharts.charts import Line3D
    from pyecharts.faker import Faker

    data = []
    for i in range(len(Client[0].demand)):
        x=i
        for j in range(Client_Count):
            y=Client[j].name
            z=Client[j].demand[i]
            data.append([x,y,z])
    # for t in range(0, 25000):
    #     _t = t / 1000
    #     x = (1 + 0.25 * math.cos(75 * _t)) * math.cos(_t)
    #     y = (1 + 0.25 * math.cos(75 * _t)) * math.sin(_t)
    #     z = _t + 2.0 * math.sin(75 * _t)
    #     data.append([x, y, z])
    c = (
        Line3D()
            .add(
            "",
            data,
        )
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(
                max_=30, min_=0, range_color=Faker.visual_color
            ),
            title_opts=opts.TitleOpts(title="Line3D"),
        )
            .render("line3d_autorotate.html")
    )


if __name__ == '__main__':
    #读取输入文件
    # demandFile = 'data/demand.csv'
    # site_bandwidthFile = 'data/site_bandwidth.csv'
    # solutionFile = 'output/solution.txt'
    # qosFile='data/qos.csv'

    demandFile='test/demand.csv'
    site_bandwidthFile = 'test/site_bandwidth.csv'
    qosFile='test/qos.csv'


    qos_constraint=400
    Client,Client_Count,Time_count=readDemand(demandFile)
    Site = readSite(site_bandwidthFile)
    readQos(qosFile)

    delete_picture("data_analysis")

#画3D图
    draw_3D()

    ##连通性 矩阵
    drawLink(Site)
    ##带宽图+连通性
    ##排序后带宽图
    # drawSortBandwidth(Site)

    ##每个客户的请求 x_时间
    for client in Client:
        draw_demand(client)
    #总的客户请求——x时间
    draw_all_demand(Client)
    draw_all_sort_demand(Client)