#coding=utf-8
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
        self.T_Load=[]#[T][name,size]
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
        if lines=="[config]\n":
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
            site.used=[0 for i in range(Time_Count)]
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
        lines = file_to_read.readline()
        for i in range(len(lines)):
            if lines[i] == "\n":
                lines = lines[:i]
                break
        special_site_name=lines.split(",")
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
                                    exit()
                                Site[site_id].used[day]+=tmp_used

                                ##for T_Load picture
                                for element in Site[site_id].T_Load[day]:
                                    if element[0]==Client[find_index].name:
                                        element[1]+=tmp_used
                                        break

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
    return special_site_name

def billing_90():
    result=[]
    for i in range(len(Site)):
        if Site[i].sitename in special_site_name:
            charge_90=sorted(Site[i].used)
            point = math.ceil(len(charge_90) * 0.9) - 1
            if sum(charge_90)==0:
                sum_real=0
            else:
                if charge_90[point]*Site[i].price<=base_count:
                    sum_real=base_count
                else:
                    sum_real = (charge_90[point] * Site[i].price - base_count) * (
                                charge_90[point] * Site[i].price - base_count) / Site[i].bandwidth + charge_90[point] * \
                               Site[i].price
        else:
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
                    # if sum_real >= (sum_real // 1 + 0.5):
                    #     sum_real = math.ceil(sum_real)
                    # else:
                    #     sum_real = math.floor(sum_real)
        result.append(sum_real)
    return result

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
                # if sum_real >= (sum_real // 1 + 0.5):
                #     sum_real = math.ceil(sum_real)
                # else:
                #     sum_real = math.floor(sum_real)
        result.append(sum_real)
    return result

def delete_picture(dir):
    shutil.rmtree(dir)
    os.mkdir(dir)

def picture_T_Load(site):
    if site.sitename not in special_site_name:
        return
    plt.cla()
    color = ["#fc0303", "#a14545", "#e09292", "#a37979", "#ffb303", "#a68946", "#dbc797", "#f8fc00",
             "#9c9e37", "#66ff00", "#5a9134", "#264f0a", "#05f79a", "#26996d", "#00ffdd",
             "#2b9e8f", "#0b5e53", "#05c7f2", "#3e9bb0", "#06677d", "#0565f5", "#2b5aa1",
             "#7092c4", "#380ef0", "#5441ab", "#8c80c2", "#7b00ff", "#803ec7", "#a583c9",
             "#8400b8", "#6d3185", "#ff00e6", "#a8209b", "#d979cf", "#ff0088", "#a8487c", "#632c3b",
             "#653b6b", "#3b6b69", "#1c4023"]
    x=range(len(site.used))
    bottom_d=[0 for i in range(len(x))]
    for client in range(len(Client)):
        y_tmp=[]
        for t in range(len(Time)):
            y_tmp.append(site.T_Load[t][client][1])
        if sum(y_tmp)==0:
            continue
        plt.bar(x,y_tmp,bottom=bottom_d,label=Client[client].name,color=color[client])
        for bd in range(len(bottom_d)):
            bottom_d[bd]+=y_tmp[bd]
    y=site.used
    # plt.plot(y)
    paixu = site.used
    charge_95 = sorted(paixu)
    # point=math.ceil(len(charge_95) * 0.9) - 1
    point = math.ceil(len(charge_95) * 0.95) - 1
    if sum(charge_95) == 0:
        sum_real = 0
    else:
        if charge_95[point] * site.price <= base_count:
            sum_real = base_count
        else:
            sum_real = (charge_95[point] * site.price - base_count) * (charge_95[point] * site.price - base_count) / site.bandwidth + charge_95[point] * site.price

    link = 0
    for j in site.delayTime:
        if j < qos_constraint:
            link += 1
    # plt.rcParams["figure.figsize"] = (24.0, 12.0)
    # plt.rcParams["savefig.dpi"] = 150
    # plt.bar(x,y)

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

    # plt.text(x[0], y[0], y[0], ha='center', va='bottom', fontsize=12)
    # plt.text(x[point], y[point], y[point], ha='center', va='bottom', fontsize=12)
    # plt.text(x[len(x) - 1], y[len(x) - 1], y[len(x) - 1], ha='center', va='bottom', fontsize=12)
    plt.axhline(y=charge_95[point], ls=":", c="red", label="95_point")  # 添加水平直线
    plt.axhline(y=base_count, ls=":", c="green", label="V")  # 添加水平直线
    plt.xlabel('Time')
    plt.ylabel('Load')
    plt.title("Name:" + site.sitename + "  link:" + str(link) + "\nCap:" + str(
        site.bandwidth) + " Cost:" + str(math.ceil(sum_real)) + "  95:" + str(math.ceil(charge_95[point])))

    # plt.axhline(y=site.bandwidth, ls=":", c="green")  # 添加水平直线
    plt.legend()
    plt.savefig("./site_load_pic/"+site.sitename)

def picture(site):
    plt.cla()
    x=range(len(site.used))
    y=site.used
    # plt.plot(y)
    paixu = site.used
    charge_95 = sorted(paixu)
    point = math.ceil(len(charge_95) * 0.95) - 1
    if sum(charge_95) == 0:
        sum_real = 0
    else:
        if charge_95[point] * site.price <= base_count:
            sum_real = base_count
        else:
            sum_real = (charge_95[point] * site.price - base_count) * (charge_95[point] * site.price - base_count) / site.bandwidth + charge_95[point] * site.price

    link = 0
    for j in site.delayTime:
        if j < qos_constraint:
            link += 1
    # plt.rcParams["figure.figsize"] = (24.0, 12.0)
    # plt.rcParams["savefig.dpi"] = 150
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

    # plt.text(x[0], y[0], y[0], ha='center', va='bottom', fontsize=12)
    # plt.text(x[point], y[point], y[point], ha='center', va='bottom', fontsize=12)
    # plt.text(x[len(x) - 1], y[len(x) - 1], y[len(x) - 1], ha='center', va='bottom', fontsize=12)
    plt.axhline(y=charge_95[point], ls=":", c="red", label="95_point")  # 添加水平直线
    plt.axhline(y=base_count, ls=":", c="yellow", label="V")  # 添加水平直线
    plt.xlabel('Time')
    plt.ylabel('Load')
    plt.title("Name:" + site.sitename + "  link:" + str(link) + "\nCap:" + str(
        site.bandwidth) + " Cost:" + str(math.ceil(sum_real)) + "  95:" + str(math.ceil(charge_95[point])))

    # plt.axhline(y=site.bandwidth, ls=":", c="green")  # 添加水平直线
    plt.legend()
    plt.savefig("./site_load_pic/"+site.sitename)

def picture_according_load(site_waste_sort,Site):
    # print(site_waste_sort)
    for i in range(len(site_waste_sort)):
        # print("picture ",site_waste_sort[i][0])
        # print(Site[i].sitename,Site[i].used)
        # plt.clf()
        x=range(len(Site[site_waste_sort[i][0]].used))
        y=Site[site_waste_sort[i][0]].used
        # print(Site[i].sitename,"in 画图",y)
        # plt.plot(y)
        y.sort()
        # print(Site[i].sitename, "in 画图", y)
        # plt.text(20, 1000, str(y))
        plt.plot(x,y,label="Load_descending")

        # plt.bar(x,y)
        link=0
        for j in Site[site_waste_sort[i][0]].delayTime:
            if j<qos_constraint:
                link+=1
        paixu=Site[site_waste_sort[i][0]].used
        charge_95 = sorted(paixu)
        point = math.ceil(len(charge_95) * 0.95)-1
        if sum(charge_95)==0:
            sum_real=0
        else:
            if charge_95[point]*Site[i].price<=base_count:
                sum_real=base_count
            else:
                sum_real=(charge_95[point]*Site[i].price-base_count)*(charge_95[point]*Site[i].price-base_count)/Site[i].bandwidth+charge_95[point]*Site[i].price


        sense_use=0
        for j in range(len(paixu)):
            if paixu[j]<charge_95[point]:
                sense_use+=paixu[j]
            else:
                sense_use+=charge_95[point]

        plt.text(x[0],y[0],y[0],ha='center', va='bottom', fontsize=12)
        plt.text(x[point], y[point], y[point], ha='center', va='bottom', fontsize=12)
        plt.text(x[len(x)-1], y[len(x)-1], y[len(x)-1], ha='center', va='bottom', fontsize=12)

        # fflag = 0
        # for a, b in zip(x[-(len(x) - point):], y[-(len(y) - point):]):
        #     if fflag == 0:
        #         plt.text(a + 30, b, b, ha='center', va='bottom', fontsize=8)
        #         fflag += 1
        #     else:
        #         plt.text(a - 30, b, b, ha='center', va='bottom', fontsize=8)
        #         fflag -= 1

        plt.xlabel('Time')
        plt.ylabel('Load')
        plt.title("Name:"+Site[site_waste_sort[i][0]].sitename+ "  link:" + str(link) + "\nCap:" + str(Site[i].bandwidth)+" Cost:"+str(math.ceil(sum_real))+"  95:"+str(math.ceil(charge_95[point])))
        demand_downsort=charge_95[:]
        demand_downsort.reverse()
        # plt.text(1,2,demand_downsort)
        # if charge_95[point]==0:
        #     plt.title(Site[site_waste_sort[i][0]].sitename+"  0 use"+str(Site[i].used.reversed()))
        # else:
        #     waste_rate=(charge_95[point]*len(Site[site_waste_sort[i][0]].used)-sense_use)/(charge_95[point]*len(Site[site_waste_sort[i][0]].used))
        #     plt.title(Site[site_waste_sort[i][0]].sitename+"  waste_rate:"+str(waste_rate)+"\n link_count:"+str(link)+"\nbandwidth:"+str(Site[i].bandwidth))

        plt.axhline(y=charge_95[point], ls=":", c="red",label="95_point")  # 添加水平直线
        plt.axhline(y=base_count, ls=":", c="yellow",label="V")  # 添加水平直线
        # plt.axhline(y=site.bandwidth, ls=":", c="green")  # 添加水平直线
        plt.legend()



        plt.savefig("./site_load_pic/"+Site[site_waste_sort[i][0]].sitename)

        plt.close()


def T_Load_init(Site):
    for site in Site:
        T_Load=[]
        for t in range(len(Time)):
            Loat_tmp=[]
            for client in Client:
                tmp=[]
                tmp.append(client.name)
                tmp.append(0)
                Loat_tmp.append(tmp)
            T_Load.append(Loat_tmp)
        site.T_Load=T_Load




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
    T_Load_init(Site)

    special_site_name=readSolution(solutionFile)
    #
    price=billing_90()
    print(price)
    ans=sum(price)
    if ans >= (ans // 1 + 0.5):
        ans = math.ceil(ans)
    else:
        ans = math.floor(ans)
    print("90价格",ans)

    price=billing()
    ans = sum(price)
    if ans >= (ans // 1 + 0.5):
        ans = math.ceil(ans)
    else:
        ans = math.floor(ans)
    print("95价格",ans)

    delete_picture("site_load_pic")

    for site in Site:
        picture_T_Load(site)


    #
    # site_waste_sort=sort_waste_rate(Site)
    # picture_according_load(site_waste_sort,Site)
    # #
    #     # print("picture ",site_waste_sort[i][0])



