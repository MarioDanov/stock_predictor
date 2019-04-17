# Importing all necessary libraries for the program
import pandas as pd
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima_model import ARIMA
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
from tkinter import filedialog
# Definition for the file dialog 
def fileDialog():
# filename - variable which value is the location of the .csv file. It is defined as global because it was used in the internal function(ArimaModel()).
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File")
    Label(root,text = filename).pack(side = TOP)
# Definition for the internal function ArimaModel(), which takes care for the data input into algorithms that calculate the predictions.
# entry_1 is variable which takes the input values of the number of days file dialog. The .get() method was used to take the input value which is out of the function definition.
# 70% of the data provided by the .csv file is used for the training session.    
# 30% of the data provided by the .csv file is used for the testing session.    
    def ArimaModel(self):
        entry_1 = int(root.entry_1.get()) 
        data_set = pd.read_csv(filename) 
        data_set1 = data_set[['date', 'close']]
        data_set1['Date'] = pd.to_datetime(data_set1["date"], format = "%d/%m/%Y")
        train = data_set1[int(len(data_set1) * 0): int(len(data_set1) * 0.7)]['close'].values 
        test = data_set1[int(len(data_set1) * 0.7): int(len(data_set1) * 1)]['close'].values 
# Definition of the list "predictions" which is going to be filled with prediction values predictied by the ARIMA model using the past values from the training session.
        predictions = list()
        actual = [x for x in train]
# actual was reshaped into an array because ARIMA needs one dimentional array to output 2 dim arrays
# Loop in which ARIMA method is used to make prediction for every value in the training session 
        for t in range(len(test)):
            model = ARIMA(actual, order=(5, 1, 0))
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            prediction = output[0]
            predictions.append(prediction)
            observations = test[t]
            actual.append(observations)
            print('Predicted values=%f, Expected=%f' % (prediction, observations))
# Model fitting for the new days stated by the interface
        output_new = model_fit.forecast(entry_1)
        predictionnew = output_new[0]
# list consisting of the data predictions for the days stated by the user

        for n in range(0, entry_1):
            print('Future prediction=%f ' % (predictionnew[n]))
# calculate error in predictions
        error = mean_squared_error(test, predictions)
        print('Mean_squared_error: %.3f' % error)
# Creating type object Figure() from matplotlib.figure
        graph = Figure()
# Ploting the graphs for testing, testing predictions and the future predictions
        subplot = graph.add_subplot(111)
        subplot.plot(predictions, color='red')
        subplot.plot(test, color='black')
        subplot.plot(range(len(predictions), len(predictionnew) + len(predictions)), predictionnew, color='orange')
        subplot.set_xlim(0, (len(predictions) + entry_1))
        canvas_1 = FigureCanvasTkAgg(graph, root)
        canvas_1._tkcanvas.pack()
        Label(root, text=('Mean squared error: %.3f' % error)).pack(side = RIGHT)

    Label(root, text='Number of days:', fg='black').pack(side = LEFT)
    root.entry_1 = Entry(root, textvariable = StringVar())
    root.entry_1.pack(side = LEFT)
    root.entry_1.insert(0, "0")
    Button(root, text = 'RUN', command = ArimaModel).pack(side = LEFT)
    root.bind('<Return>', ArimaModel)
# Main loop for the program
root = Tk()

Title = root.title("Stock Market Predictions")

root.minsize(width=850, height=500)

label_1 = Label(root, text = 'Insert the number of days you want the prediction for and press Run', fg='black').pack(side=TOP)
label_open = Label(root, text = "Choose a File:").pack(side = TOP)
browse_button = Button(root,text = "File Browser...", command = fileDialog).pack(side = TOP)

root.mainloop()