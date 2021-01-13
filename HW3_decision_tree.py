import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text

dataset = pd.read_excel("E:/tmp/HW3Data.xlsx")

x = dataset.drop('Class', axis=1)
y = dataset['Class']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30)

classifier = DecisionTreeClassifier(min_impurity_split=0.10)
classifier.fit(x_train, y_train)

# Generate a decision tree in dot file format that can be viewed with graphviz
tree.export_graphviz(classifier, out_file = 'decision_tree.dot')
# r = export_text(classifier)
# print(r)

# Confustion matrix/metrics
from sklearn.metrics import classification_report, confusion_matrix
y_prediction = classifier.predict(x_test)

print(confusion_matrix(y_test, y_prediction))
print(classification_report(y_test, y_prediction))

# Display the plot of the given dataset
x_data = dataset['X'].tolist()
y_data = dataset['Y'].tolist()
classes = dataset['Class'].tolist()
colors = []
for data_class in classes:
    if data_class == 1:
        color = 'red'
    else:
        color = 'black'
    colors.append(color)

for index in range(85):
    plt.plot(x_data[index],y_data[index],'o',color=colors[index])

plt.show()

# Display 70x70 2D grid
for x in range(71):
    for y in range(71):
        point = [[x,y]]
        output = classifier.predict(point)
        if output == 1:
            color = 'red'
        else:
            color = 'black'
        plt.plot(x,y,'o',color=color)

plt.show()