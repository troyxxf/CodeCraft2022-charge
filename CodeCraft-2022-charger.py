import math

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
        Time_count=-1
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
            for client in range(Client_Count):
                lines=file_to_read.readline()
                lines=lines[:len(lines)-1]
                # lines[0]=lines.split(":<")

                if not lines:
                    #TODO：说明数据量与计费点*用户数不符合，需要报错
                    print("solution差数据")
                    break
                    pass

                p_tmp=lines.split(">,<")
                for i in range(len(p_tmp[0])):
                    if p_tmp[0][i] == ":":
                        name = p_tmp[0][:i]
                        p_tmp[0]=p_tmp[0][i+2:]
                        break
                #删除回车和<>等符号
                lastone=p_tmp[len(p_tmp)-1]
                if lastone[len(lastone)-2:]=="\n":
                    lastone=lastone[:len(lastone)-2]
                elif lastone[len(lastone)-1:]==">":
                    lastone=lastone[:len(lastone)-1]
                p_tmp[len(p_tmp)-1]=lastone
                given=0
                for i in p_tmp:
                    one_tmp=i.split(",")
                    for site_id in range(len(Site)):
                        if(Site[site_id].sitename==one_tmp[0]):#找节点的名字
                            if(Site[site_id].delayTime[client]>qos_constraint):
                                print(Client[client].name,"的qos未被满足，它发给了",Site[site_id])
                                exit()
                            Site[site_id].used[day]+=int(one_tmp[1])
                            given+=int(one_tmp[1])
                            if Site[site_id].used[day]>Site[site_id].bandwidth:
                                print(Site[site_id].sitename,"的负载超过了带宽")
                                print(Site[site_id].used)
                                print(Site[site_id].bandwidth)
                                exit()

            for cc in Client:
                if cc.name==name:
                    if given<cc.demand[day]:
                        print(cc.name,"的第",day,"个点没有满足需求")
                        print("分发了",given,"需求，需要",cc.demand[day])
                        exit()

def billing():
    sum=[]
    for i in range(len(Site)):
        charge_95=sorted(Site[i].used)
        point=math.ceil(len(charge_95)*0.95)-1
        sum.append(charge_95[point]*Site[i].price)
    return sum



if __name__ == '__main__':
    #读取输入文件
    demandFile = 'data/demand.csv'
    site_bandwidthFile = 'data/site_bandwidth.csv'
    solutionFile = 'solution.txt'
    qosFile='data/qos.csv'

    qos_constraint=400
    Client,Client_Count,Time_count=readDemand(demandFile)
    Site = readSite(site_bandwidthFile)
    readQos(qosFile)
    readSolution(solutionFile)
    price=billing()
    print(price)
    print(sum(price))






