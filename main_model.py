from src.model.model import Model
import pickle


def main():

    print("Create Model")
    model = Model()

    print("Traning model")
    epocs = 10
    model.make_model(epocs)

    print("Saving model")
    file = open('./data/model', 'wb')
    pickle.dump(model,file)
    print("Model save")

   
if __name__=="__main__":
    main()