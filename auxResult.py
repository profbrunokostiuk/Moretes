file = open("results.txt",'r')
lines = file.readlines()
file.close()

print(len(lines))

file = open("results_data.csv",'w')

lin = 0
while lin < len(lines):
    #print(lines[lin][:5])
    if lines[lin][:5] == "Model":
        file.write(lines[lin].replace("\n",""))
        #print(lines[lin])
        for i in range(1,11):
            aux = lines[lin+i].split(":")
            res = aux[1].split('-')[0].strip()
            des = aux[2].strip()
            file.write(";"+res.replace(".",",")+";"+des.replace(".",","))
            # print(res)
            # print(des)
        lin+=11
        file.write("\n")
    lin+=1
    
