from src.model.data import Bug, Test, Data
from alive_progress import alive_bar
import numpy as np
import math


from random import shuffle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class Model:
    def __init__(self):
        self.name = "Model"

        self.learning_rate = 0.0
        self.regularization = 0.0

        self.list_Bug = {}
        self.list_Test ={}

        self.interactions =[]
        self.precision = 0.0

        self.encode = SentenceTransformer('sentence-transformers/distiluse-base-multilingual-cased-v1')
        self.encode.max_seq_length = 512

        self.teams = []
        self.comps = []

    
    def load_data_from_file(self):
        self.list_Bug = Data.load_data_from_csv("./data/bugs.csv", Bug, self.encode)
        self.list_Test = Data.load_data_from_csv("./data/tests.csv", Test, self.encode)

        for bug in self.list_Bug.values():
            if bug.team not in self.teams:
                self.teams.append(bug.team)
            if bug.comp not in self.comps:
                self.comps.append(bug.comp)

        for test in self.list_Test.values():
            if test.team not in self.teams:
                self.teams.append(test.team)
            if test.comp not in self.comps:
                self.comps.append(test.comp)

        print(f"Bugs: {len(self.list_Bug)} Tests: {len(self.list_Test)}")

    
    def load_input(self, valid = False):
        data = Data.load_relations_from_csv("./data/relation.csv")
        if valid:
            return Data.split_data(data,[20,30,50],valid)
        else:
            return Data.split_data(data,[50,50])
    

    def info_colect(self, data):
        with alive_bar(len(data)) as bar:
            for link in data:
                bar()
                test = link["test_id"]
                bug = link["bug_id"]
                
                if test not in self.list_Bug[bug].tests_positive:
                    self.list_Bug[bug].tests_positive.append(test)
                if bug not in self.list_Test[test].bugs_positive:
                    self.list_Test[test].bugs_positive.append(bug)
                
                
        with alive_bar(len(self.list_Test)) as bar:
            for tes in self.list_Test.keys():
                bar()
                for b in self.list_Test[tes].bugs_positive:
                    for t2 in self.list_Bug[b].tests_positive:
                        if t2 not in self.list_Test[tes].tests_similar:
                            self.list_Test[tes].tests_similar.append(t2)
                            self.list_Test[tes].tests_similar_ocorrencias.append(1)
                        else:
                            self.list_Test[tes].tests_similar_ocorrencias[self.list_Test[tes].tests_similar.index(t2)] +=1
                

    def get_negatives(self, tam, bug):
        negatives = []
        list_aux = list(self.list_Test.values())
        shuffle(list_aux)
        for test in list_aux:
            if test.comp != bug.comp:
                if test.team != bug.team:
                    if test.id not in negatives:
                        negatives.append(test.id)
                    if len(negatives)>=tam:
                        return negatives
                    

    def sigmoid(self, x):
        return np.exp(-x) / (1.0 + np.exp(-x))
    
    def pre_train_model(self, data, n_negatives, epocs):
        print("Start Training")

        optimizer = self.learning_rate
        l2 = self.regularization

        test_list =[]
        bug_list = []
        for epc in range(epocs):
            print(f"Epoca:{epc+1}/{epocs}")
            with alive_bar(len(data)) as bar:
                for interation in data:
                    bar()
                    test = interation["test_id"]
                    bug  = interation["bug_id"]

                    if test not in test_list:
                        test_list.append(test)
                    if bug not in bug_list:
                        bug_list.append(bug)

                    bug_vec = np.array(self.list_Bug[bug].data)
                    test_vec = np.array(self.list_Test[test].data)

                    negatives = self.get_negatives(tam=n_negatives, bug = self.list_Bug[bug])
                    for neg in negatives:
                        neg_vec = np.array(self.list_Test[neg].data)

                        x_bt = np.inner(bug_vec, test_vec)
                        x_bn = np.inner(bug_vec, neg_vec)

                        x_btn = x_bt - x_bn
                        sigmoid = self.sigmoid(x_btn)

                        bug_grad = ((sigmoid * (test_vec - neg_vec)) + (l2 * bug_vec))
                        test_grad = ((sigmoid * (bug_vec)) + (l2 * test_vec))
                        neg_grad = ((sigmoid * (-bug_vec)) + (l2 * neg_vec))

                        next_bug_vec = bug_vec + optimizer*bug_grad
                        next_test_vec = test_vec + optimizer*test_grad
                        next_neg_vec = neg_vec + optimizer*neg_grad

                        self.list_Bug[bug].data = next_bug_vec.tolist()
                        self.list_Test[test].data = next_test_vec.tolist()
                        self.list_Test[neg].data = next_neg_vec.tolist()
        
        print(f"Tests used: {len(test_list)} of {len(self.list_Test)}")
        print(f"Bugs used: {len(bug_list)} of {len(self.list_Bug)}")
    
    
    def make_model(self, epocs, learning_rate=0.001, regularization=0.01): 
        self.learning_rate = learning_rate
        self.regularization = regularization

        print("load data...")    
        self.load_data_from_file()
        print("load inputs")
        data1, data2 = self.load_input()
        print("info colect")
        self.info_colect(data1+data2)
        print("Pré Training start")
        self.pre_train_model(data1+data2,10,epocs)
        
    def extract_interactions(self):
        with open("interactions.txt", "w") as file:
            for interact in self.interactions:
                file.write(f"{interact}\n")
    
    def get_rank_N_Tests(self, candidates,scores, num_elements):
        positives =[]
        for i in range(len(candidates[0])):
            positives.append([candidates[0][i],scores[0][i]])
        positives.sort(key = lambda x: x[1])

        negatives =[]
        for i in range(len(candidates[1])):
            negatives.append([candidates[1][i],scores[1][i]])
        negatives.sort(key = lambda x: x[1])

        noInteract = []
        for i in range(len(candidates[2])):
            noInteract.append([candidates[2][i],scores[2][i]])
        noInteract.sort(key = lambda x: x[1])

        retorno = positives[:num_elements[0]]+negatives[:num_elements[1]]+noInteract

        return retorno[:num_elements[0]+num_elements[1]+num_elements[2]]

    def score(self, bug_data, candidates):
        aux = []
        for i in candidates:
            aux.append(self.list_Test[i].data)

        aux = np.array(aux)
       
        pred = np.dot(bug_data, aux.T)
        
        return pred.flatten()
    
    def register_interactions(self, bugId, positives, negatives):
        self.interactions.append((bugId, positives, negatives))
        self.recommend_evaluation()

    def recommend_evaluation(self):
        total = 0
        negatives = 0
        positives = 0
        for interaction in self.interactions:
            posit = interaction[1]
            negat = interaction[2]
            positives+=len(posit)
            negatives+=len(negat)
            total+=len(posit)+len(negat)
        self.precision = positives/total

        
    
    def recommend(self, bug, num_elements):

        positivesLinked, negativesSameTC, noInteract = self.get_candidates(bug = bug)
        for n in negativesSameTC:
            if n in positivesLinked:
                negativesSameTC.remove(n)
        for no in noInteract:
            if no in positivesLinked or no in negativesSameTC:
                noInteract.remove(no)
        retorno = positivesLinked[:num_elements[0]]+negativesSameTC[:num_elements[1]]+noInteract[:]
        return retorno[:num_elements[0]+num_elements[1]+num_elements[2]]

       
    def SBertSimilarity(self, text):
        encode_text = self.encode.encode(text, convert_to_tensor=True).tolist()

        embeddings =  []
        for bug in self.list_Bug.values():
            embeddings.append(bug.embedding)
        cos_sin = cosine_similarity([encode_text],embeddings)
        if (max(cos_sin[0]) > 0.95):
            return np.argmax(cos_sin[0]), encode_text, max(cos_sin[0])
        elif (max(cos_sin[0]) > 0.50):
            return np.argmax(cos_sin[0]), encode_text, max(cos_sin[0])
        else:
            return -1, encode_text, max(cos_sin[0])
    
    def insert_Bug(self, encode_text, id, comp, team, key, opt, title):
        if opt > 0.50:
            #def __init__(self, id, key, team, comp, embedding):
            bug = Bug(id=key, title=title, team=team, comp=comp, embedding=encode_text)
            bug.data = self.list_Bug[id].data
            bug.tests_positive = self.list_Bug[id].tests_positive
            bug.tests_negative = self.list_Bug[id].tests_negative
            self.list_Bug[key] = bug
            
        else:
            bug = Bug(id=key, title=title, team=team, comp=comp, embedding=encode_text)

            list_bugs_emb = []
            for b in self.list_Bug.values():
                if comp == b.comp and team == b.team:
                    list_bugs_emb.append(b.data)

            if len(list_bugs_emb) == 0:
                for b in self.list_Bug.values():
                    if comp == b.comp:
                        list_bugs_emb.append(b.data)

            if len(list_bugs_emb) > 0:
                soma = []
                for i in range(len(list_bugs_emb[0])):
                    val = 0.0
                    for j in range(len(list_bugs_emb)):
                        val+=list_bugs_emb[j][i]
                    soma.append(val/len(list_bugs_emb))
                bug.data = soma 
            self.list_Bug[key] = bug



    def update_model(self, bug, positives, negatives):
        optimizer = self.learning_rate
        l2 = self.regularization
        for neg in negatives:
            if neg not in self.list_Bug[bug].tests_negative:
                self.list_Bug[bug].tests_negative.append(neg)


        for pos in positives:
            for pos1 in positives:
                if pos != pos1:
                    if pos1 not in self.list_Test[pos].tests_similar:
                        self.list_Test[pos].tests_similar.append(pos1)
                        self.list_Test[pos].tests_similar_ocorrencias.append(1)
                    else:
                        self.list_Test[pos].tests_similar_ocorrencias[self.list_Test[pos].tests_similar.index(pos1)] +=1

            if pos not in self.list_Bug[bug].tests_positive:
                    self.list_Bug[bug].tests_positive.append(pos)

                
            for neg in negatives:
                bug_vec = np.array(self.list_Bug[bug].data)
                test_vec = np.array(self.list_Test[pos].data)
                neg_vec = np.array(self.list_Test[neg].data)

                x_bt = np.inner(bug_vec, test_vec)
                x_bn = np.inner(bug_vec, neg_vec)

                x_btn = x_bt - x_bn
                sigmoid = self.sigmoid(x_btn)

                bug_grad = ((sigmoid * (test_vec - neg_vec)) + (l2 * bug_vec))
                test_grad = ((sigmoid * (bug_vec)) + (l2 * test_vec))
                neg_grad = ((sigmoid * (-bug_vec)) + (l2 * neg_vec))

                next_bug_vec = bug_vec + optimizer*bug_grad
                next_test_vec = test_vec + optimizer*test_grad
                next_neg_vec = neg_vec + optimizer*neg_grad

                self.list_Bug[bug].data = next_bug_vec.tolist()
                self.list_Test[pos].data = next_test_vec.tolist()
                self.list_Test[neg].data = next_neg_vec.tolist()
    
    def order_by_similarity_test_bug(self, listItens, focusItem):
        
        aux = [self.list_Test[i].data for i in listItens]

        cos_sin = cosine_similarity([focusItem.data],aux)

        indices = list(range(len(cos_sin[0])))
        indices.sort(key=lambda i: cos_sin[0][i], reverse=True) 

        new_listItens = [listItens[i] for i in indices]

        return new_listItens

    
    def get_candidates(self, bug):
        noInteract = []
        noInteractSameTC = []
        for tests in self.list_Test.values():
            if tests.id not in bug.tests_positive and tests.id not in bug.tests_negative:
                noInteract.append(tests.id)
                
                if tests.comp == bug.comp and tests.id not in noInteractSameTC:
                    noInteractSameTC.append(tests.id)
                    if tests.id in noInteract:
                        noInteract.remove(tests.id)
                
                if tests.team == bug.team and tests.id not in noInteractSameTC:
                    noInteractSameTC.append(tests.id)
                    if tests.id in noInteract:
                        noInteract.remove(tests.id)
    
        linked_tests =[]
        for tests in bug.tests_positive:
            for link in self.list_Test[tests].tests_similar:
                if link not in linked_tests and link not in bug.tests_positive and link not in bug.tests_negative:
                    linked_tests.append(link)
        for test in linked_tests:
            if tests in noInteract:
                noInteract.remove(test)
            if tests in noInteractSameTC:
                noInteractSameTC.remove(test)
        
        if (len(bug.tests_positive)>1):
            positives = self.order_by_similarity_test_bug(bug.tests_positive[:], bug)
        else:
            positives = bug.tests_positive[:]
        if (len(bug.tests_negative)>1):
            negatives = self.order_by_similarity_test_bug(bug.tests_negative[:], bug)
        else:
            negatives = bug.tests_negative[:]

        if (len(linked_tests)>1):
            linked_tests = self.order_by_similarity_test_bug(linked_tests, bug)
       
        if (len(noInteract)>1):
            noInteract = self.order_by_similarity_test_bug(noInteract, bug)

        if (len(noInteractSameTC)>1):
            noInteractSameTC  = self.order_by_similarity_test_bug(noInteractSameTC, bug)


        return positives + linked_tests, negatives[:2]+noInteractSameTC, noInteract


    
    def insert_new_bug(self, key, description, summary, teams, comp):
        encode_text = self.encode.encode(description, convert_to_tensor=True).tolist()
        bug = Bug(id=key, team=teams, title=summary, comp=comp, embedding=encode_text)
        self.list_Bug[key] = bug
        
    
    def insert_new_test(self, key, steps, summary, teams, comp):
        encode_text = self.encode.encode(steps, convert_to_tensor=True).tolist()
        test = Test(id=key, team=teams, title=summary, comp=comp, embedding=encode_text)
        self.list_Test[key] = test
        

    def update_bug_recomendation(self, bugKey, listTestes):
        try:
            testes = listTestes.replace("\n","").split(",")
            idB = self.get_id_bug_from_key(bugKey)
            for t in testes:
                id = self.get_id_test_from_key(t)
                if id >= 0 and id not in self.list_Bug[idB].tests_positive:
                    self.list_Bug[idB].tests_positive.append(id)
            return 1
        except:
            return -1


    def get_candidates_onelist(self, bug):
        testsId = [t.id for t in self.list_Test]
        return self.order_by_similarity_test_bug(testsId, bug)

    def get_candidates_onelist_no_positives(self, bug):
        testsId = [t.id for t in self.list_Test]
        for positive in bug.tests_positive:
            testsId.remove(positive)
        return self.order_by_similarity_test_bug(testsId, bug)

    def get_candidates_random(self, bug):
        testsId = [t.id for t in self.list_Test]
        shuffle(testsId)
        return testsId
    
    def get_candidates_TOPPOP(self, bug):
        testsId = [[],[]]
        for b in self.list_Bug:
            for t in b.tests_positive:
                if t not in testsId[0]:
                    testsId[0].append(t)
                    testsId[1].append([t,1])
                else:
                    testsId[1][testsId[0].index(t)][1]+=1
        listaOrdenada = sorted(testsId[1], key = lambda x: x[1], reverse=True)
        retorno = [x[0] for x in listaOrdenada]
        return retorno

    def validade_top_itens(self, listCandidates, idTest, topNumber):
        if idTest in listCandidates[:topNumber]:
            return True
        return False
    
    def ndcg(self, listCandidates, idTest, topNumber):
        if idTest in listCandidates[:topNumber]:
            pos = listCandidates.index(idTest)+1
            return 1/(math.log2(pos+1))
        return 0


    def test_module(self, dataInteractionTest, topNumber):
        correct = 0
        correctNP = 0
        correctM = 0
        correctTOP = 0
        correctRan = 0

        ndcg = 0
        ndcgNP = 0
        ndcgM = 0
        ndcgTOP = 0
        ndcgRan = 0

        with alive_bar(len(dataInteractionTest)) as bar:
            for interation in dataInteractionTest:
                bar()
                testId = interation["test_id"]
                bugId  = interation["bug_id"]

                candidates = self.get_candidates_onelist(self.list_Bug[bugId])
                candidatesNoPositive = self.get_candidates_onelist_no_positives(self.list_Bug[bugId])
                candidatesRandom = self.get_candidates_random(self.list_Bug[bugId])
                candidatesTOPPOP = self.get_candidates_TOPPOP(self.list_Bug[bugId])
                positivesLinked, negativesSameTC, noInteract = self.get_candidates(self.list_Bug[bugId])
                

                for n in negativesSameTC:
                    if n in positivesLinked:
                        negativesSameTC.remove(n)
                for no in noInteract:
                    if no in positivesLinked or no in negativesSameTC:
                        noInteract.remove(no)


                ndcg += self.ndcg(candidates, testId, topNumber)
                ndcgNP += self.ndcg(candidatesNoPositive, testId, topNumber)
                ndcgM += self.ndcg(positivesLinked+negativesSameTC+noInteract, testId, topNumber)
                ndcgTOP += self.ndcg(candidatesTOPPOP, testId, topNumber)
                ndcgRan += self.ndcg(candidatesRandom, testId, topNumber)

                if (self.validade_top_itens(candidates, testId, topNumber)):
                    correct+=1
                if (self.validade_top_itens(candidatesNoPositive, testId, topNumber)):
                    correctNP+=1
                
                if (self.validade_top_itens(positivesLinked+negativesSameTC+noInteract, testId, topNumber)):
                    correctM+=1

                if (self.validade_top_itens(candidatesTOPPOP, testId, topNumber)):
                    correctTOP+=1
                if (self.validade_top_itens(candidatesRandom, testId, topNumber)):
                    correctRan+=1
                
        
        return correct/len(dataInteractionTest), correctNP/len(dataInteractionTest), correctM/len(dataInteractionTest), correctTOP/len(dataInteractionTest), correctRan/len(dataInteractionTest), ndcg/len(dataInteractionTest), ndcgNP/len(dataInteractionTest), ndcgM/len(dataInteractionTest), ndcgTOP/len(dataInteractionTest), ndcgRan/len(dataInteractionTest)


    def split_cv_data(self, data, cv):
        dataCV = []
        cv_aux = 0
        tam = int(len(data)/cv)
        for i in range(cv):
            if i+1 == cv:
                dataCV.append(data[cv_aux:])
            else:
                dataCV.append(data[cv_aux:cv_aux+tam])
            cv_aux += tam
        return dataCV

    def assessment_model(self, epocs, cv): 
        
        listTest = [10,20,30,40,50]
        for topN in listTest:

            print("Load inputs")
            data = Data.load_input_from_csv("./data/Interacoes.csv")
            dataCV = self.split_cv_data(data, cv)

            results = []
            resultsNP = []
            resultsM = []
            resultsRand =[]
            resultsTOP =[]

            ndcgs =[]
            ndcgsNP =[]
            ndcgsM =[]
            ndcgsRand =[]
            ndcgsTOP =[]

            for i in range(cv):
                testData = dataCV[i]
                trainData = []
                for j in range(len(dataCV)):
                    if j != i:
                        for k in range(len(dataCV[j])):
                            trainData.append(dataCV[j][k])

                self.__init__()
                print(f"Cross Validation {i} \nLoad Data")    
                self.load_data_from_file()

                print("Info colect")
                self.info_colect(trainData)
                
                print("Pré Training start")
                self.pre_train_model(trainData,10,epocs)

                print("Testing Model")
                result, resultNP, resultM, resultTOP, resultRand, ndcg, ndcgNP, ndcgM, ndcgTOP, ndcgRand  = self.test_module(testData, topN)
                results.append(result)
                resultsNP.append(resultNP)
                resultsM.append(resultM)
                resultsRand.append(resultRand)
                resultsTOP.append(resultTOP)
                
                ndcgs.append(ndcg)
                ndcgsNP.append(ndcgNP)
                ndcgsM.append(ndcgM)
                ndcgsRand.append(ndcgRand)
                ndcgsTOP.append(ndcgTOP)

                print(f"Resultado parcial: {result}  NDCG: {ndcg}")
                print(f"Resultado parcial sem positivos: {resultNP}  NDCG: {ndcgNP}")
                print(f"Resultado parcial Model: {resultM}  NDCG: {ndcgM}")
                print(f"Resultado parcial Rand: {resultRand}  NDCG: {ndcgRand}")
                print(f"Resultado parcial TOPPOP: {resultTOP}  NDCG: {ndcgTOP}")


            mediaResults = sum(results)/len(results)
            mediaResultsNP = sum(resultsNP)/len(resultsNP)
            mediaResultsM = sum(resultsM)/len(resultsM)
            mediaResultsRand = sum(resultsRand)/len(resultsRand)
            mediaResultsTOP = sum(resultsTOP)/len(resultsTOP)

            mediaNDCGs = sum(ndcgs)/len(ndcgs)
            mediaNDCGsNP = sum(ndcgsNP)/len(ndcgsNP)
            mediaNDCGsM = sum(ndcgsM)/len(ndcgsM)
            mediaNDCGsRand = sum(ndcgsRand)/len(ndcgsRand)
            mediaNDCGsTOP = sum(ndcgsTOP)/len(ndcgsTOP)

            desvioResults = 0
            for re in results:
                desvioResults+= math.pow((re - mediaResults), 2)
            desvioResults = desvioResults/len(results)
            desvioResults = math.sqrt(desvioResults)

            desvioResultsNP = 0
            for re in resultsNP:
                desvioResultsNP+= math.pow((re - mediaResultsNP), 2)
            desvioResultsNP = desvioResultsNP/len(resultsNP)
            desvioResultsNP = math.sqrt(desvioResultsNP)

            desvioResultsM = 0
            for re in resultsM:
                desvioResultsM+= math.pow((re - mediaResultsM), 2)
            desvioResultsM = desvioResultsM/len(resultsM)
            desvioResultsM = math.sqrt(desvioResultsM)

            desvioResultsRand = 0
            for re in resultsRand:
                desvioResultsRand+= math.pow((re - mediaResultsRand), 2)
            desvioResultsRand = desvioResultsRand/len(resultsRand)
            desvioResultsRand = math.sqrt(desvioResultsRand)

            desvioResultsTOP = 0
            for re in resultsTOP:
                desvioResultsTOP+= math.pow((re - mediaResultsTOP), 2)
            desvioResultsTOP = desvioResultsTOP/len(resultsTOP)
            desvioResultsTOP = math.sqrt(desvioResultsTOP)

            desvioNDCGs = 0
            for re in ndcgs:
                desvioNDCGs+= math.pow((re - mediaNDCGs), 2)
            desvioNDCGs = desvioNDCGs/len(ndcgs)
            desvioNDCGs = math.sqrt(desvioNDCGs)

            desvioNDCGsNP = 0
            for re in ndcgsNP:
                desvioNDCGsNP+= math.pow((re - mediaNDCGsNP), 2)
            desvioNDCGsNP = desvioNDCGsNP/len(ndcgsNP)
            desvioNDCGsNP = math.sqrt(desvioNDCGsNP)

            desvioNDCGsM = 0
            for re in ndcgsM:
                desvioNDCGsM+= math.pow((re - mediaNDCGsM), 2)
            desvioNDCGsM = desvioNDCGsM/len(ndcgsM)
            desvioNDCGsM = math.sqrt(desvioNDCGsM)

            desvioNDCGsRand = 0
            for re in ndcgsRand:
                desvioNDCGsRand+= math.pow((re - mediaNDCGsRand), 2)
            desvioNDCGsRand = desvioNDCGsRand/len(ndcgsRand)
            desvioNDCGsRand = math.sqrt(desvioNDCGsRand)

            desvioNDCGsTOP = 0
            for re in ndcgsTOP:
                desvioNDCGsTOP+= math.pow((re - mediaNDCGsTOP), 2)
            desvioNDCGsTOP = desvioNDCGsTOP/len(ndcgsTOP)
            desvioNDCGsTOP = math.sqrt(desvioNDCGsTOP)



            print(f"Resultado base completa: {mediaResults} - desvio: {desvioResults}")
            print(f"Resultado base sem positivos completa: {mediaResultsNP} - desvio: {desvioResultsNP}")
            print(f"Resultado base sem Model: {mediaResultsM} - desvio: {desvioResultsM}")
            print(f"Resultado base Random: {mediaResultsRand} - desvio: {desvioResultsRand}")
            print(f"Resultado base TOPPOP: {mediaResultsTOP} - desvio: {desvioResultsTOP}")

            print(f"NDCG base completa: {mediaNDCGs} - desvio: {desvioNDCGs}")
            print(f"NDCG base sem positivos completa: {mediaNDCGsNP} - desvio: {desvioNDCGsNP}")
            print(f"NDCG base sem Model: {mediaNDCGsM} - desvio: {desvioNDCGsM}")
            print(f"NDCG base Random: {mediaNDCGsRand} - desvio: {desvioNDCGsRand}")
            print(f"NDCG base TOPPOP: {mediaNDCGsTOP} - desvio: {desvioNDCGsTOP}")

            file = open("C:\\Users\\Bruno\\Documents\\GitHub\\moretes\\results.txt",'a')
            file.write(f"Model: {self.name} - top{topN} - CS: {cv} - Epocs:{epocs}\n")

            file.write(f"Resultado base completa: {mediaResults} - desvio: {desvioResults}\n")
            file.write(f"Resultado base sem positivos completa: {mediaResultsNP} - desvio: {desvioResultsNP}\n")
            file.write(f"Resultado base com positivos Model: {mediaResultsM} - desvio: {desvioResultsM}\n")
            file.write(f"Resultado base com positivos Random: {mediaResultsRand} - desvio: {desvioResultsRand}\n")
            file.write(f"Resultado base com positivos TOPPOP: {mediaResultsTOP} - desvio: {desvioResultsTOP}\n")

            file.write(f"NDCG base completa: {mediaNDCGs} - desvio: {desvioNDCGs}\n")
            file.write(f"NDCG base sem positivos completa: {mediaNDCGsNP} - desvio: {desvioNDCGsNP}\n")
            file.write(f"NDCG base com positivos Model: {mediaNDCGsM} - desvio: {desvioNDCGsM}\n")
            file.write(f"NDCG base com positivos Random: {mediaNDCGsRand} - desvio: {desvioNDCGsRand}\n")
            file.write(f"NDCG base com positivos TOPPOP: {mediaNDCGsTOP} - desvio: {desvioNDCGsTOP}\n")

            file.write(f"Results of Folds base completa: {results}\n")
            file.write(f"Results of Folds base sem positivos completa: {resultsNP}\n")
            file.write(f"Results of Folds base com positivos Model: {resultsM}\n")
            file.write(f"Results of Folds base com Random: {resultsRand}\n")
            file.write(f"Results of Folds base com TOPPOP: {resultsTOP}\n")

            file.write(f"NDCG of Folds base completa: {ndcgs}\n")
            file.write(f"NDCG of Folds base sem positivos completa: {ndcgsNP}\n")
            file.write(f"NDCG of Folds base com positivos Model: {ndcgsM}\n")
            file.write(f"NDCG of Folds base com Random: {ndcgsRand}\n")
            file.write(f"NDCG of Folds base com TOPPOP: {ndcgsTOP}\n\n")
            file.close()