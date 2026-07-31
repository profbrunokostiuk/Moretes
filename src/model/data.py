import csv

class Bug:
    def __init__(self, id, key, status, team, comp, embedding):
        self.key = key
        self.id = id
        self.team = team
        self.comp = comp
        self.embedding = embedding #512
        self.summary = ""
        self.status = status

        self.data = embedding #vetor pesos
        self.tests_positive = [] 
        self.tests_negative =[] 


class Test:
    def __init__(self, id, key, status, team, comp, embedding):
        self.key = key
        self.id = id
        self.team = team
        self.comp = comp
        self.embedding = embedding
        self.summary = ""
        self.status = status

        self.data = embedding
        self.tests_similar = []
        self.tests_similar_ocorrencias = []
        self.bugs_positive =[]
        

class Teams_Comps:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return self.name


class Data:
    def load_data_from_csv(filepath, type):
        data = []
        with open(filepath, newline="") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",")
            for row in spamreader:
                data.append(type(id=int(float(row[0])), key=row[1], status=row[2], team=row[3].split("#"), comp=row[4].split("#"),embedding=[float(i) for i in row[5:]]))
        return data

    def load_input_from_csv(filepath):
        data = []
        with open(filepath, newline="") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",")
            for row in spamreader:
                data.append({"test_id": int(float(row[0])), "bug_id": int(float(row[1])), "rating":int(float(row[2])), "time_stamp":int(float(row[3]))})
        return sorted(data, key=lambda d: d['time_stamp'])
    
    def split_data(data, tam_split, validation = False):
        if validation:
            tam_train = (tam_split[0]*len(data))//100
            tam_test  = (tam_split[1]*len(data))//100

            #tam_valid = tam_split[2]
            return data[:tam_train], data[tam_train:tam_test], data[tam_test:]
        else:
            tam_train = (tam_split[0]*len(data))//100
            return data[:tam_train], data[tam_train:]
        
    def get_item_by_id(id, data):
        for item in range(len(data)):
            if data[item].id == id:
                return item
        return None
    
    def load_comps_teams(filepath):
        data = []
        with open(filepath, newline="") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",")
            for row in spamreader:
                data.append(Teams_Comps(id=int(float(row[0])), name= row[1]))
        return sorted(data, key=lambda d: d.name)
    
    def load_summary_file(filepath):
        data = {}
        with open(filepath, newline="\n", encoding="utf-8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",")
            for row in spamreader:
                data[row[0]] = row[1]
        return data