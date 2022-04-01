import random
import math
from scipy.signal import savgol_filter

qos_constraint=400

class Site_info():
    def __init__(self,name,bandwidth):
        self.name=name
        self.bandwidth=bandwidth

class Client_info():
    def __init__(self,name):
        self.name=name

def create_Site(dir,Site_Count):
    with open(dir,'w')as f:
        Site=[]
        f.write("site_name,bandwidth\n")

        for i in range(Site_Count):
            line = ""
            line+="Site"
            line+=str(i)
            name="Site"+str(i)
            line+=","
            bandwidth=random.randint(100000,1000000)
            Site.append(Site_info(name,bandwidth))
            line+=str(bandwidth)
            line+="\n"
            f.write(line)
    return Site

def create_Client(Client_Count):
    Client=[]
    for i in range(Client_Count):
        name="Client"+str(i)
        Client.append(Client_info(name))
    return Client

def oneSiteQosCreate(Client_Count):
    lst=[]
    for i in range(Client_Count):
        tmp=random.randint(200,600)
        lst.append(tmp)
    for i in range(Client_Count):
        if lst[i]<qos_constraint:
            lst=[str(i) for i in lst]
            res=",".join(lst)
            return res
    return oneSiteQosCreate(Client_Count)

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


def create_demand(demand_path,time):
    with open(demand_path, 'w')as f:
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
                randDemand=random.randint(500,5000)
                lst.append(randDemand)
            lst_str=[str(i) for i in lst]
            full_str=",".join(lst_str)
            line+=full_str
            line+="\n"
            f.write(line)

def create_demand_different_by_day(demand_path,time):
    with open(demand_path, 'w')as f:
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
                day_time=t%288
                if day_time<12:#0-1
                    randDemand = random.randint(8000, 10000)
                elif day_time<24:#1-2
                    randDemand=random.randint(5000, 6000)
                elif day_time<36:#2-3
                    randDemand=random.randint(2000, 3000)
                elif day_time<48:#3-4
                    randDemand=random.randint(1000, 2000)
                elif day_time<60:#4-5
                    randDemand=random.randint(500, 1000)
                elif day_time<72:#5-6
                    randDemand=random.randint(1000, 2000)
                elif day_time<84:#6-7
                    randDemand=random.randint(2000, 3000)
                elif day_time<96:#7-8
                    randDemand=random.randint(3000, 4000)
                elif day_time<108:#8-9
                    randDemand=random.randint(3000, 5000)
                elif day_time<144:#9-12
                    randDemand=random.randint(3500, 6500)
                elif day_time<168:#12-14
                    randDemand=random.randint(5000, 8000)
                elif day_time<192:#14-16
                    randDemand=random.randint(4000, 6500)
                elif day_time<216:#16-18
                    randDemand=random.randint(5000, 7000)
                elif day_time<240:#18-20
                    randDemand=random.randint(6000, 8000)
                elif day_time<252:#20-21
                    randDemand=random.randint(6500, 8000)
                elif day_time<264:#21-22
                    randDemand=random.randint(7000, 9000)
                elif day_time<276:#22-23
                    randDemand=random.randint(8000, 10000)
                else:#23-24
                    randDemand=random.randint(8000, 10000)
                lst.append(randDemand)
            lst_str=[str(i) for i in lst]
            full_str=",".join(lst_str)
            line+=full_str
            line+="\n"
            f.write(line)

def create_demand_different_by_day_10(demand_path,time):
    with open(demand_path, 'w')as f:
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
                day_month=t//288
                day_month%=10
                if day_month<5:
                    base=day_month
                else:
                    base=10-day_month
                base=base*500
                day_time=t%288
                if day_time<12:#0-1
                    randDemand = random.randint(3000, base+5000)
                elif day_time<24:#1-2
                    randDemand=random.randint(2000, base+4000)
                elif day_time<36:#2-3
                    randDemand=random.randint(1000, base+4000)
                elif day_time<48:#3-4
                    randDemand=random.randint(750, base+1750)
                elif day_time<60:#4-5
                    randDemand=random.randint(100, base+1500)
                elif day_time<72:#5-6
                    randDemand=random.randint(750, base+1750)
                elif day_time<84:#6-7
                    randDemand=random.randint(1000, base+2500)
                elif day_time<96:#7-8
                    randDemand=random.randint(1500, base+2500)
                elif day_time<108:#8-9
                    randDemand=random.randint(1250, base+2500)
                elif day_time<144:#9-12
                    randDemand=random.randint(1500, base+3250)
                elif day_time<168:#12-14
                    randDemand=random.randint(2500, base+4000)
                elif day_time<192:#14-16
                    randDemand=random.randint(3000, base+3250)
                elif day_time<216:#16-18
                    randDemand=random.randint(3000, base+4000)
                elif day_time<240:#18-20
                    randDemand=random.randint(3000, base+4500)
                elif day_time<252:#20-21
                    randDemand=random.randint(3250, base+4500)
                elif day_time<264:#21-22
                    randDemand=random.randint(3500, base+4500)
                elif day_time<276:#22-23
                    randDemand=random.randint(3000, base+5000)
                else:#23-24
                    randDemand=random.randint(4000, 5000)
                lst.append(randDemand)
            lst_str=[str(i) for i in lst]
            full_str=",".join(lst_str)
            line+=full_str
            line+="\n"
            f.write(line)

def create_demand_different_by_hand(demand_path,time):
    # lst_24=[6000,4000,2000,1000,500,1000,1500,2000,3000,3500,3800,4500,6000,7000,6000,5000,5500,6000,7000,7200,8000,8500,7600,7000]
    lst_24=[3000,2700,1500,1000,500,1000,1200,1500,1700,2000,2100,2300,2500,2700,3000,3200,3000,3400,3500,3600,3700,3800,3900,4000]
    lst_24_low=[1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000]
    with open(demand_path, 'w')as f:
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
            if t<time//6:
                for x in range(Client_Count):
                    day_month=t//288
                    day_month%=20
                    if day_month<10:
                        base=day_month
                    else:
                        base=20-day_month
                    base=base*1000
                    day_time=t%288
                    day_time=day_time//12
                    randDemand=math.ceil(lst_24[day_time]*math.sin(t/1000))+random.randint(0,lst_24_low[day_time])
                    lst.append(randDemand)
            elif t<time//3:
                for x in range(Client_Count):
                    day_month=t//288
                    day_month%=20
                    if day_month<10:
                        base=day_month
                    else:
                        base=20-day_month
                    base=base*1000
                    day_time=t%288
                    day_time=day_time//12
                    randDemand=lst_24[day_time]+random.randint(0,lst_24[day_time])
                    lst.append(randDemand)
            elif t<time//2:
                for x in range(Client_Count):
                    day_month=t//288
                    day_month%=20
                    if day_month<10:
                        base=day_month
                    else:
                        base=20-day_month
                    base=base*1000
                    day_time=t%288
                    day_time=day_time//12
                    randDemand=lst_24[day_time]+random.randint(0,lst_24_low[day_time])
                    lst.append(randDemand)
            elif t<time*2//3:
                for x in range(Client_Count):
                    day_month=t//288
                    day_month%=20
                    if day_month<10:
                        base=day_month
                    else:
                        base=20-day_month
                    base=base*1000
                    day_time=t%288
                    day_time=day_time//12
                    randDemand=lst_24_low[day_time]+random.randint(0,lst_24[day_time])
                    lst.append(randDemand)
            elif t<time*5//6:
                for x in range(Client_Count):
                    day_month=t//288
                    day_month%=20
                    if day_month<10:
                        base=day_month
                    else:
                        base=20-day_month
                    base=base*1000
                    day_time=t%288
                    day_time=day_time//12
                    randDemand=lst_24[day_time]+random.randint(0,base)
                    lst.append(randDemand)
            else:
                for x in range(Client_Count):
                    day_month=t//288
                    day_month%=20
                    if day_month<10:
                        base=day_month
                    else:
                        base=20-day_month
                    base=base*1000
                    day_time=t%288
                    day_time=day_time//12
                    randDemand=base+random.randint(0,lst_24_low[day_time])
                    lst.append(randDemand)
            lst_str=[str(i) for i in lst]
            full_str=",".join(lst_str)
            line+=full_str
            line+="\n"
            f.write(line)

def create_demand_different_by_sin(demand_path,time):
    # lst_24=[6000,4000,2000,1000,500,1000,1500,2000,3000,3500,3800,4500,6000,7000,6000,5000,5500,6000,7000,7200,8000,8500,7600,7000]
    lst_24=[3000,2700,1500,1000,500,1000,1200,1500,1700,2000,2100,2300,2500,2700,3000,3200,3000,3400,3500,3600,3700,3800,3900,4000]
    lst_24_low=[1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000]
    lst_24_high=[4000,4100,4200,4300,4400,4500,4600,4700,4800,5000,4800,4700,4600,4500,4400,4300,4200,4100,4000,3900,3800,3700,3800,3900]
    with open(demand_path, 'w')as f:
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
                day_month=t//288
                day_month%=20
                if day_month<10:
                    base=day_month
                else:
                    base=20-day_month
                base=base*1000
                day_time=t%288
                day_time=day_time//12
                randDemand=math.ceil(lst_24_high[day_time]*(math.sin(t/1000)+1))+random.randint(0,lst_24_low[day_time])
                lst.append(randDemand)

            lst_str=[str(i) for i in lst]
            full_str=",".join(lst_str)
            line+=full_str
            line+="\n"
            f.write(line)


if __name__ == '__main__':
    Client_Count=10
    Site_Count=25
    time=1500
    site_path='./test/site_bandwidth.csv'
    Qos_path='./test/qos.csv'
    demand_path='./test/demand.csv'


#Clean data
    file = open(site_path, 'w').close()
    file=open(Qos_path,'w').close()
    file=open(demand_path,'w').close()


    Site=create_Site(site_path,Site_Count)
    Client=create_Client(Client_Count)
    create_Qos(Qos_path)
    create_demand_different_by_sin(demand_path,time)
