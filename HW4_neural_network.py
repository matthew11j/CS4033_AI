from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.model_selection import train_test_split

dataset = pd.read_excel("E:/tmp/HW3Data.xlsx")

x = dataset.drop('Class', axis=1)
y = dataset['Class']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30)

scaler = StandardScaler()

# Fit only to the training data
scaler.fit(x_train)

# Now apply the transformations to the data:
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier(hidden_layer_sizes=(2,))
mlp.fit(x_train,y_train)

predictions = mlp.predict(x_test)

from sklearn.metrics import classification_report,confusion_matrix
print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions))

# Display 70x70 2D grid
for x in range(71):
    for y in range(71):
        point = [[x,y]]
        output = mlp.predict(point)
        if output == 1:
            color = 'red'
        else:
            color = 'black'
        plt.plot(x,y,'o',color=color)
plt.show()

# Display the plot of the training data points
trained_classes = []
for val in y_train:
    trained_classes.append(val)

misclassified_cnt = 0
for index in range(len(x_train)):
    x_point = x_train[index][0]
    y_point = x_train[index][1]

    point = [[x_point,y_point]]
    predicted_class = mlp.predict(point)
    training_class = trained_classes[index]

    if predicted_class != training_class:
        symbol = 'x'
        color = 'gray'
        misclassified_cnt += 1
    else:
        symbol = 'o'
        if training_class == 1:
            color = 'red'
        elif training_class == 0:
            color = 'black'

    plt.plot(x_point, y_point, symbol, color=color)

print('Misclassified:', misclassified_cnt)
plt.show()