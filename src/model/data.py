import csv

class Bug:
    def __init__(self, id, title, team, comp, embedding):
        self.id = id
        self.title = title
        self.team = team
        self.comp = comp
        self.embedding = embedding 
       
        self.data = embedding 
        self.tests_positive = [] 
        self.tests_negative =[] 


class Test:
    def __init__(self, id, title, team, comp, embedding):
        self.id = id
        self.title = title
        self.team = team
        self.comp = comp
        self.embedding = embedding

        self.data = embedding
        self.tests_similar = []
        self.tests_similar_ocorrencias = []
        self.bugs_positive =[]
        

class Data:
    def load_data_from_csv(filepath, type, encode):
        data = {}
        with open(filepath, newline="",encoding='utf-8-sig') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=";")
            next(spamreader, None)
            for row in spamreader:
                data[row[0]]=(type(id=row[0], team=row[1], comp=row[2], title=row[3], embedding=encode.encode(row[4])))
        return data.copy()


    def load_relations_from_csv(filepath):
        data = []
        with open(filepath, newline="",encoding='utf-8-sig') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=";")
            next(spamreader, None)
            for row in spamreader:
                data.append({"test_id": row[0], "bug_id": row[1]})
        return data
    
    def split_data(data, tam_split, validation = False):
        if validation:
            tam_train = (tam_split[0]*len(data))//100
            tam_test  = (tam_split[1]*len(data))//100

            #tam_valid = tam_split[2]
            return data[:tam_train], data[tam_train:tam_test], data[tam_test:]
        else:
            tam_train = (tam_split[0]*len(data))//100
            return data[:tam_train], data[tam_train:]
        
