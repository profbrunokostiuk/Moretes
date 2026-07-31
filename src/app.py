import pickle
from src.model.model import Model
from src.ui.window import Window


class App:
    def __init__(self):
        self.model: Model = self.load_model()
        

        self.ui = Window(self)
        self.ui.draw_frame(self.ui.screen.Main)

    def save_model(self, filename ='./data/model'):
        file = open(filename, 'wb')
        pickle.dump(self.model,file)
        file.close()
        

    def load_model(self):
        file = open('./data/model', 'rb')
        return pickle.load(file)
        

    def run(self):
        self.ui.mainloop()
