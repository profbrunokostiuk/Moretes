from src.model.model import Model
import pickle


def main():

    print("Create Model")
    model = Model()

    print("Traning model")
    epocs = 100 #number of training epochs
    laerning_rate = 0.01 #learning rate
    regularization = 0.001 #regularization parameter
    
    model.make_model(epocs=epocs, learning_rate=laerning_rate, regularization=regularization)

    print("Saving model")
    file = open('./data/model', 'wb')
    pickle.dump(model,file)
    print("Model save")

   
if __name__=="__main__":
    main()