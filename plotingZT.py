#setup:
import matplotlib.pyplot as plt
plt.rc('font', family='serif', size=20)
import csv
import math
def Import(file_pathname):
    data = []
    with open(file_pathname, 'r') as opened_File:
        CSV_File = csv.reader(opened_File)
        for row in CSV_File:
            #temporarily store the values in each row before adding it to the completed file
            store_row=[]
            # if there is stuff in the row
            if len(row) > 0:
                # if the first thing is a number with more than two digits so not 8
                if len(row[0]) > 1 and row[0].isdigit():
                    for value in row:
                        # if the value exists
                        if len(value) > 0:
                            store_row.append(float(value))
                    data.append(store_row)
    opened_File.close()
    return (file)

def Export(file_name, data):
    File = open(file_name, 'w')
    File.write("Temperature,Resistivity,Seebeck,Thermal Conductivity,zT,max Red efficiency,s,u,Red efficiency,Phi,efficiency,ZT")
    for datum in data:
        File.write("\n")
        for num in datum:
            File.write(str(num))
            File.write(",")
    File.close()
def optimizedU(data):
    Us = [.1, 4]
    while True:
        uMax = max(Us)
        uMin = min(Us)
        if uMax-Min < .000001:
            break
        test_U = []
        du = (uMax-uMin)/5
        for x in range(6):
            test_U.append(functions_efficiency_as_a_function_of_u(data, (uMin+x*du)))
        place = find_place(max(test_U), test_U)
        Us = []
        Us.append(uMin + du*place)
        test_U[place] = -100000
        Us.append(uMin + du*find_place(max(test_U), test_U))
    return (uMin)

def find_place(number, place): # find index (value, litslike)
    for thing in range(len(place)):
        #print (thing, place[thing])
        if place[thing] == number:
            return thing
    print ("Error in find_place")
def find_highest(place): #max()
    x = place[0]
    #print(place)
    for number in place:
        if number > x:
            x = number
    return (x)
def find_lowest(place): #min()
    x = place[0]
    for number in place:
        if number < x:
            x = number
    return (x)

def functions_zT(T,R,S,K):
    return ((T*(S**2)/(K*R))/10**7)
def functions_max_Red_eff(zT):
    return ((math.sqrt(1+zT)-1)/(math.sqrt(1+zT)+1))

def functions_efficiency_as_a_function_of_u(file, initial_u): # efficiency from u int(file , u_int):
    # predicts the efficiency of the total material form a given starting u.
    Us = [None for n in file]
    Us[0] = initial_u
    for datum in range(len(file)-1):
        Us[datum + 1] = (1/(((1/Us[datum])*math.sqrt(abs(1-2*Us[datum]*Us[datum]*(file[datum+1][1]*file[datum+1][3]+file[datum][1]*file[datum][3])*(10**-5)/2*(file[datum+1][0]-file[datum][0]))))-(file[datum+1][0]+file[datum][0])/2*(file[datum+1][2]-file[datum][2])*(10**-6)))
    NL = file[-1][2]*file[-1][0]/1000000+1/Us[-1]
    N1 = file[0][2]*file[0][0]/1000000+1/Us[0]
    (NL-N1)/NL
    return((NL-N1)/NL) #final - initial

    #return(eachZT)
#temperature(T) is in Kelvin
#R is in Ohm*Meters*10^-5
#S is in Volts/Kelvin*10^-6
#thermal conductivity(K) is in Watts/(Meter*Kelvin)*10^-1

def ploting_rangeL(to_plot):
    return (round(((min(to_plot)) - (.1 * (max(to_plot) - min(to_plot))))*100)/100)
def ploting_rangeH(to_plot):
    return (round(((max(to_plot)) + (.1 * (max(to_plot) - min(to_plot))))*100)/100)

def Device_Efficiency_versus_Relative_Current_Density(list_name):
    #why are there three listSeebeck? not two get rid of u_vs...
    #Relative_Current_Density aka U
    # not run
    U = []
    dev_eff = []
    x = 1
    u = .01
    while x > 0:
        x = (functions_efficiency_as_a_function_of_u(list_name, u))
        u += .01
        dev_eff.append(x)
        U.append(u)
    highest_dev_eff = max(dev_eff)
    hDF_U = find_place(highest_dev_eff,dev_eff)
    
    optimized_U = optimizedU(list_name)
    x = functions_efficiency_as_a_function_of_u(list_name, optimized_U)
    
  
    plt.plot(U, dev_eff,color="#065f00", linewidth=1.5)
    print ("optmissed u", optimized_U)
    print ("Highest device efficiency", x)
    plt.plot(hDF_U, highest_dev_eff, 'o', color="#821cff", linewidth=10,)
    plt.axis([((min(U)) - .01), ((max(U)) + .01), 0, ploting_rangeH(dev_eff)])
    plt.ylabel('Device Efficiency')
    plt.xlabel('Relative Current Density (u)')
    plt.show()

def CalculateData(data):
    for datum in data:
        zT = functions_zT(datum[0], datum[1], datum[2], datum[3])
        datum.append(zT)
    for datum in data:
        Red_eff = functions_max_Red_eff(datum[4])
        datum.append(Red_eff)
    for datum in data:
        S = (math.sqrt(1+datum[4])-1)/(datum[2]*datum[0]/1000000)
        datum.append(S)
    for datum in data:
        if len(datum) < 8:
            datum.append(.123)

    optimized_U = optimizedU(data)
    #(functions_efficiency_as_a_function_of_u(data, optimized_U))

    data[0][7] = optimized_U
    for datum in range(len(data)-1):
        data[datum + 1][7] = (1/(((1/data[datum][7])*math.sqrt(abs(1-2*data[datum][7]*data[datum][7]*(data[datum+1][1]*data[datum+1][3]+data[datum][1]*data[datum][3])*(10**-5)/2*(data[datum+1][0]-data[datum][0]))))-(data[datum+1][0]+data[datum][0])/2*(data[datum+1][2]-data[datum][2])*(10**-6)))

    for datum in data:
        redefficiency = ((datum[7]*(datum[2]-datum[7]*datum[1]*datum[3]*10)/10**6)/(datum[7]*datum[2]/10**6+1/datum[0]))
        datum.append(redefficiency)
    for datum in data:
        Phi = (datum[2]*datum[0]/1000000+1/datum[7])
        datum.append(Phi)
    for datum in range(len(data)-1):
        efficiency = ((data[datum+1][9]-data[0][9])/data[datum+1][9])
        data[datum+1].append(efficiency)
    for datum in range(len(data)-1):
        ZT = (((data[datum+1][0]-data[0][0]*(1-data[datum+1][10]))/(data[datum+1][0]*(1-data[datum+1][10])-data[0][0]))**2-1)
        data[datum+1].append(ZT)
        
def PlotData(data):
    # I wonder if this is faster then doing it the fancy way.
    All_tempatures = []
    All_R = []
    All_Seebeck = []
    All_K = []
    All_zT = []
    All_max_Red_eff = []
    All_S = []
    All_u = []
    All_reduced_efficiency = []
    All_Phi = []
    All_efficiency = []
    All_ZT = []
    for datum in data:
        All_tempatures.append(datum[0])
        All_R.append(datum[1])
        All_Seebeck.append(datum[2])
        All_K.append(datum[3])
        All_zT.append(datum[4])
        All_max_Red_eff.append(datum[5])
        All_S.append(datum[6])
        All_u.append(datum[7])
        All_reduced_efficiency.append(datum[8])
        All_Phi.append(datum[9])
    for datum in range(len(data)-1):
        All_efficiency.append(data[datum+1][10])
        All_ZT.append(data[datum+1][11])

    temp_incroment = All_tempatures[2]-All_tempatures[1]
    maxy = max(All_tempatures) + temp_incroment
    miny = min(All_tempatures) - temp_incroment
        
    plt.plot(All_tempatures, All_R)
    plt.axis([miny, maxy, ploting_rangeL(All_R), ploting_rangeH(All_R)])
    plt.ylabel('Resistance')
    plt.xlabel('Temperature (K)')
    plt.show()
    #1
    plt.plot(All_tempatures, All_Seebeck)
    plt.axis([miny, maxy, ploting_rangeL(All_Seebeck), ploting_rangeH(All_Seebeck)])
    plt.ylabel('Seebeck')
    plt.xlabel('Temperature (K)')
    plt.show()
    #2
    plt.plot(All_tempatures, All_K)
    plt.axis([miny, maxy, ploting_rangeL(All_K), ploting_rangeH(All_K)])
    plt.ylabel('Thermal conductivity')
    plt.xlabel('Temperature (K)')
    plt.show()
    #3
    plt.plot(All_tempatures, All_zT)
    plt.axis([miny, maxy, ploting_rangeL(All_zT), ploting_rangeH(All_zT)])
    plt.ylabel('zT')
    plt.xlabel('Temperature (K)')
    plt.show()
    #4
    plt.plot(All_tempatures, All_max_Red_eff)
    plt.axis([miny, maxy, ploting_rangeL(All_max_Red_eff), ploting_rangeH(All_max_Red_eff)])
    plt.ylabel('Maximum Reduced efficiency')
    plt.xlabel('Temperature (K)')
    plt.show()
    #5
    plt.plot(All_tempatures, All_S)
    plt.axis([miny, maxy, ploting_rangeL(All_S), ploting_rangeH(All_S)])
    plt.ylabel('s (1/V)')
    plt.xlabel('Temperature (K)')
    plt.show()
    #6
    plt.plot(All_tempatures, All_u)
    plt.axis([miny, maxy, ploting_rangeL(All_u), ploting_rangeH(All_u)])
    plt.ylabel('u (1/V)')
    plt.xlabel('Temperature (K)')
    plt.show()
    #7
    plt.plot(All_tempatures, All_reduced_efficiency)
    plt.axis([miny, maxy, ploting_rangeL(All_reduced_efficiency), ploting_rangeH(All_reduced_efficiency)])
    plt.ylabel('Reduced efficiency')
    plt.xlabel('Temperature (K)')
    plt.show()
    #8
    plt.plot(All_tempatures, All_Phi)
    plt.axis([miny, maxy, ploting_rangeL(All_Phi), ploting_rangeH(All_Phi)])
    plt.ylabel('(|) Phi')
    plt.xlabel('Temperature (K)')
    plt.show()
    #9
    del All_tempatures[0]
    plt.plot(All_tempatures, All_efficiency)
    plt.axis([miny, maxy, ploting_rangeL(All_efficiency), ploting_rangeH(All_efficiency)])
    plt.ylabel('efficiency')
    plt.xlabel('Temperature (K)')
    plt.show()
    #10
    plt.plot(All_tempatures, All_ZT)
    plt.axis([miny, maxy, ploting_rangeL(All_ZT), ploting_rangeH(All_ZT)])
    plt.ylabel('ZT')
    plt.xlabel('Temperature (K)')
    plt.show()
    #11
    
    U = []
    dev_eff = []
    x = 1
    u = .01
    while x > 0:
        x = functions_efficiency_as_a_function_of_u(data, u)
        u += .01
        dev_eff.append(x)
        U.append(u)

    optimized_U = data[0][7]# look for optimized_U in CalculateData
    x = functions_efficiency_as_a_function_of_u(data, optimized_U)
    U_incroment = U[2]-U[1]# always .01?
    plt.plot(U, dev_eff,color="#065f00", linewidth=1.5)
    print ("optmissed u", optimized_U)
    print ("Highest device efficiency", x)
    plt.plot(optimized_U, x, 'o', color="#821cff", linewidth=10,)
    plt.axis([((min(U)) - U_incroment), ((max(U)) + U_incroment), 0, ploting_rangeH(dev_eff)])
    plt.ylabel('Device Efficiency')
    plt.xlabel('Relative Current Density (u)')
    plt.show()

print ("Units:")
print ("your units should be miliOhm centimeters, micro volts per kelvin and watts per meter kelvin")
print ("the first column should have temperature the second Resistance the third Sebec and the last Conductivity")

while True:
    print("These are the instructions. Enter:")
    print("A) to create a new CSV file with calculated ZT and other values")
    print("B) to graph data")
    print("C) to do both")
    print("Q) to end the program.")
    mode = input("What do you want to do?(A, B, C)\n")
    if mode.upper() == 'A':
        fileName = input("What is the name and path of the file?\n")
        #Import
        CSV = Import(fileName)
        #Extend list
        CalculateData(CSV)
        #export
        destination = input("When this file is exported what do you want to save it as?\n")
        Export(destination, CSV)
    elif mode.upper() == 'B':
        fileName = input("What is the name of the file?\n")
        #Import
        CSV = Import(fileName)
        #Extend list
        CalculateData(CSV)
        #Print graphs do not change csv file
        PlotData(CSV)
    elif mode.upper() == 'C':
        fileName = input("What is the name of the file?\n")
        #Import
        CSV = Import(fileName)
        #Extend list
        CalculateData(CSV)
        #do A and B
        PlotData(CSV)
        destination = input("When this file is exported what do you want to save it as?\n")
        Export(destination, CSV)
    elif mode.upper() == 'Q':
        break
    else:
        print("That made no sense.")