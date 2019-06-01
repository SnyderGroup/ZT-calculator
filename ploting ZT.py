#setup:
import matplotlib.pyplot as plt
plt.rc('font', family='serif', size=20)
import csv
import math
def Import(file_name):
    file = []
    with open(file_name, 'r') as opended_File:
        File = csv.reader(opended_File)
        for row in File:
            #temperarlily store the values in eache row before adding it to the compleated file
            store_row=[]
            # if there is stuff in the row
            if len(row) > 0:
                # if the first thing is a number with more than two didgets so not 8
                if len(row[0]) > 1 and row[0].isdigit():
                    for value in row:
                        # if the value exiss
                        if len(value) > 0:
                            store_row.append(float(value))
                    file.append(store_row)
    opended_File.close()
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
def optomiseUfordefeff(data):
    Us = [.1, 4]
    while True:
        ux = find_highest(Us)
        um = find_lowest(Us)
        if abs(um-ux) < .000001:
            break
        test_U = []
        du = (ux-um)/5
        for x in range(6):
            test_U.append(functions_efficincy_as_a_function_of_u(data, (um+x*du)))
        place = find_place(find_highest(test_U), test_U)
        Us = []
        Us.append(um + du*place)
        test_U[place] = -100000
        Us.append(um + du*find_place(find_highest(test_U), test_U))
    return (um)

def find_place(number, place):
    for thing in range(len(place)):
        #print (thing, place[thing])
        if place[thing] == number:
            return thing
    print ("Error in find_place")
def find_highest(place):
    x = place[0]
    #print(place)
    for number in place:
        if number > x:
            x = number
    return (x)
def find_lowest(place):
    x = place[0]
    for number in place:
        if number < x:
            x = number
    return (x)

def functions_zT(T,R,S,K):
    return ((T*(S**2)/(K*R))/10**7)
def functions_max_Red_eff(zT):
    return ((math.sqrt(1+zT)-1)/(math.sqrt(1+zT)+1))

def functions_efficincy_as_a_function_of_u(file, initial_u):
    for datum in (file):
        if len(datum) < 8:
            datum.append(0)
    file[0][7] = (initial_u)
    for datum in range(len(file)-1):
        file[datum + 1][7] = (1/(((1/file[datum][7])*math.sqrt(abs(1-2*file[datum][7]*file[datum][7]*(file[datum+1][1]*file[datum+1][3]+file[datum][1]*file[datum][3])*(10**-5)/2*(file[datum+1][0]-file[datum][0]))))-(file[datum+1][0]+file[datum][0])/2*(file[datum+1][2]-file[datum][2])*(10**-6)))
    NL = file[-1][2]*file[-1][0]/1000000+1/file[-1][7]
    N1 = file[0][2]*file[0][0]/1000000+1/file[0][7]
    (NL-N1)/NL
    return((NL-N1)/NL)

    #return(eachZT)
#tempiture(T) is in Kelven
#R is in Ohm*Meters*10^-5
#S is in Volts/Kelven*10^-6
#thirmial conducttivity(K) is in Wats/Merer/Kelven*10^-1

def ploting_rangeL(to_plot):
    return (round(((find_lowest(to_plot)) - (.1 * (find_highest(to_plot) - find_lowest(to_plot))))*100)/100)
def ploting_rangeH(to_plot):
    return (round(((find_highest(to_plot)) + (.1 * (find_highest(to_plot) - find_lowest(to_plot))))*100)/100)

def Device_Efficiency_versus_Relative_Current_Density(list_name):
    #why are there three listSeebeck? not two get rid of u_vs...
    #Relative_Current_Density aka U
    U = []
    dev_eff = []
    x = 1
    u = .01
    while x > 0:
        x = (functions_efficincy_as_a_function_of_u(list_name, u))
        u += .01
        dev_eff.append(x)
        U.append(u)
    highest_dev_eff = find_highest(dev_eff)
    for position in range(len(dev_eff)):
        if dev_eff[position] == highest_dev_eff:
            hDF_U = U[position]
            break
    
    optimized_U = optomiseUfordefeff(list_name)
    x = functions_efficincy_as_a_function_of_u(list_name, optimized_U)
    
  
    plt.plot(U, dev_eff,color="#065f00", linewidth=1.5)
    print ("optimised u", optimized_U)
    print ("Highest device efficiancy", x)
    plt.plot(hDF_U, highest_dev_eff, 'o', color="#821cff", linewidth=10,)
    plt.axis([((find_lowest(U)) - .01), ((find_highest(U)) + .01), 0, ploting_rangeH(dev_eff)])
    plt.ylabel('Device Efficiency')
    plt.xlabel('Relative Current Density (u)')
    plt.show()

def CalculateData(data):
    for thing in data:
        zT = functions_zT(thing[0], thing[1], thing[2], thing[3])
        thing.append(zT)
    for datum in data:
        Red_eff = functions_max_Red_eff(datum[4])
        datum.append(Red_eff)
    for datum in data:
        S = (math.sqrt(1+datum[4])-1)/(datum[2]*datum[0]/1000000)
        datum.append(S)
    for datum in (data):
        if len(datum) < 8:
            datum.append(.123)

    optimized_U = optomiseUfordefeff(data)
    (functions_efficincy_as_a_function_of_u(data, optimized_U))

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
    maxy = (find_highest(All_tempatures)) + temp_incroment
    miny = (find_lowest(All_tempatures)) - temp_incroment
        
    plt.plot(All_tempatures, All_R)
    plt.axis([miny, maxy, ploting_rangeL(All_R), ploting_rangeH(All_R)])
    plt.ylabel('Ristance')
    plt.xlabel('Tempiture (K)')
    plt.show()
    #1
    plt.plot(All_tempatures, All_Seebeck)
    plt.axis([miny, maxy, ploting_rangeL(All_Seebeck), ploting_rangeH(All_Seebeck)])
    plt.ylabel('Maxemun Redused effecentcy')
    plt.xlabel('Tempiture (K)')
    plt.show()
    #2
    plt.plot(All_tempatures, All_K)
    plt.axis([miny, maxy, ploting_rangeL(All_K), ploting_rangeH(All_K)])
    plt.ylabel('Maxemun Redused effecentcy')
    plt.xlabel('Tempiture (K)')
    plt.show()
    #3
    plt.plot(All_tempatures, All_zT)
    plt.axis([miny, maxy, ploting_rangeL(All_zT), ploting_rangeH(All_zT)])
    plt.ylabel('Maxemun Redused effecentcy')
    plt.xlabel('Tempiture (K)')
    plt.show()
    #4
    plt.plot(All_tempatures, All_max_Red_eff)
    plt.axis([miny, maxy, ploting_rangeL(All_max_Red_eff), ploting_rangeH(All_max_Red_eff)])
    plt.ylabel('S (1/V)')
    plt.xlabel('Tempiture (K)')
    plt.show()
    #5
    plt.plot(All_tempatures, All_S)
    plt.axis([miny, maxy, ploting_rangeL(All_S), ploting_rangeH(All_S)])
    plt.ylabel('Maxemun Redused effecentcy')
    plt.xlabel('Tempiture (K)')
    plt.show()
    #6
    plt.plot(All_tempatures, All_u)
    plt.axis([miny, maxy, ploting_rangeL(All_u), ploting_rangeH(All_u)])
    plt.ylabel('Maxemun Redused effecentcy')
    plt.xlabel('Tempiture (K)')
    plt.show()
    #7
    plt.plot(All_tempatures, All_reduced_efficiency)
    plt.axis([miny, maxy, ploting_rangeL(All_reduced_efficiency), ploting_rangeH(All_reduced_efficiency)])
    plt.ylabel('Maxemun Redused effecentcy')
    plt.xlabel('Tempiture (K)')
    plt.show()
    #8
    plt.plot(All_tempatures, All_Phi)
    plt.axis([miny, maxy, ploting_rangeL(All_Phi), ploting_rangeH(All_Phi)])
    plt.ylabel('Maxemun Redused effecentcy')
    plt.xlabel('Tempiture (K)')
    plt.show()
    del All_tempatures[0]
    plt.plot(All_tempatures, All_efficiency)
    plt.axis([miny, maxy, ploting_rangeL(All_reduced_efficiency), ploting_rangeH(All_efficiency)])
    plt.ylabel('Maxemun Redused effecentcy')
    plt.xlabel('Tempiture (K)')
    plt.show()
    #10
    plt.plot(All_tempatures, All_ZT)
    plt.axis([miny, maxy, ploting_rangeL(All_ZT), ploting_rangeH(All_ZT)])
    plt.ylabel('Maxemun Redused effecentcy')
    plt.xlabel('Tempiture (K)')
    plt.show()
    #11
    
    u_vs_dev_eff = []
    U = []
    dev_eff = []
    x = 1
    u = .01
    while x > 0:
        x = (functions_efficincy_as_a_function_of_u(data, u))
        u_vs_dev_eff.append([u, x])
        u += .01
        dev_eff.append(x)
        U.append(u)
    highest_dev_eff = find_highest(dev_eff)
    for thing in u_vs_dev_eff:
        if thing[1] == highest_dev_eff:
            hDF_U = thing[0]
            break
    optimized_U = optomiseUfordefeff(data)
    x = (functions_efficincy_as_a_function_of_u(data, optimized_U))
    U_incroment = U[2]-U[1]
    plt.plot(U, dev_eff,color="#065f00", linewidth=1.5)
    print ("optimised u", optimized_U)
    print ("Highest device efficiancy", x)
    plt.plot(hDF_U, highest_dev_eff, 'o', color="#821cff", linewidth=10,)
    plt.axis([((find_lowest(U)) - U_incroment), ((find_highest(U)) + U_incroment), 0, ploting_rangeH(dev_eff)])
    plt.ylabel('Device Efficiency')
    plt.xlabel('Relative Current Density (u)')
    plt.show()

    #Export("MLM_export.csv", CSV)
while True:
    print("These are the instructions.")
    print("A) creat a CSV file with calculated stuff")
    print("B) print some graphs")
    print("C) do both")
    print("type 'Q' to end the program.")
    mode = input("What do you want to do?(A, B, C)   ")
    if mode.upper() == 'A':
        fileName = "csv three.CSV"#input("What is the name of the file?   ")
        #Import
        CSV = Import(fileName)
        #Extend list
        CalculateData(CSV)
        #export
        destination = input("When this file is exported what do you want to save it as?   ")
        Export(destination, CSV)
        #Extend existing csv file
        ...
    elif mode.upper() == 'B':
        fileName = "csv three.CSV"#input("What is the name of the file?   ")
        #Import
        CSV = Import(fileName)
        #Extend list
        CalculateData(CSV)
        #Print graphs do not change csv file
        PlotData(CSV)
    elif mode.upper() == 'C':
        fileName = input("What is the name of the file?   ")
        #Import
        CSV = Import(fileName)
        #Extend list
        CalculateData(CSV)
        #do A and B
        ...
    elif mode.upper() == 'Q':
        break
    else:
        print("That made no sence")

"""print ("instructions:")
print ("your units should be miliOhme centimerters, micro volts per kelven and, wats per meter kelven")
print ("the first colem should have tempeture the second Ristance the third Sebec and the last Conductivity")
test("MLM.csv")"""
