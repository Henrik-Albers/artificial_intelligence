# Imports
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Task 1
""" 
(a) Unsupervised Learning  : Because products bought together are a set of unlabeled data set where the  solving learning problem includes finding patterns and relationships between the objects.
(b) Reinforcement Learning : Because a chess computer needs to react with the player and take actions based on the previous outcome of the data set .
(c) Supervised Learning    : Because the spam recognition system  needs to classify the set of emails which is a set of labeled data.
(d) Supervised Learning    : Because the classification of applicants system  needs to classify the set of applicants as credit-worthy or unworthy which is a set of labeled data.
(e) Supervised Learning    : Because the Object recognition in computer vision needs to classify the set of objects based on their features .
(f) Reinforcement Learning : Because the Robot needs to be trained  and interact based on the obstacles and take actions to get to the end point.
(g) Unsupervised Learning  : Because the task involves involves clustering images with is a set of unlabeled data based on groups.
 """


# Task 2
seed = 42
# a)    Reading data 
data = pd.read_csv("./data/breast-cancer-wisconsin.data.txt", sep=",")
print(data.head())

# b)    Dropping missing or non numeric values
# No missing values in dataset
nan_rows = data.isna().any(axis=1)
print("Count of missing data: " + str(nan_rows.value_counts()))

# Identifying and removing non numeric data
print(data.info())
data = data.drop("bare_nuclei", axis=1)

# c)    Drop id column
data = data.drop("id", axis=1)

# d)    Create feature and label arrays
y = data["class"]
X = data.drop("class", axis=1)

# e)    Scaling feature matrix
sc = StandardScaler()
X = sc.fit_transform(X)

# f)    Transforming feature vector into bool
y = y.replace({2:False, 4:True})

# g)    Dividing data into train and test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=seed)


# Task 3
# a) Load the data in GD_Example.txt (it includes 500 pairs of data (xi,yi))
data = np.genfromtxt("./data/GD_Example.txt", delimiter=" ")
x = data[:, 0]  
y = data[:, 1]  

# b) Plot the data points
plt.scatter(x, y, label="Data Points")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()

# c) Implement the cost function

def cost_function(m, b, x, y):
    N = len(x)
    error = np.sum((y - (m * x + b))**2)
    return error * (1 / N)


# d) Using gradient descent algorithm with 500 iterations, find the best fitting line characterized by: 𝑚𝑥 + 𝑏. (determine m and b)

def gradient_descent(x, y, m, b, learning_rate, iterations):
    N = len(x)
    cost_history = []

    for _ in range(iterations):
        # Calculate the predicted values
        y_pred = m * x + b

        # Calculate the gradients
        dm = (1/N) * np.sum(-2 * x * (y - y_pred))
        db = (1/N) * np.sum(-2 * (y - y_pred))

        # Update parameters
        m -= dm * learning_rate
        b -= db * learning_rate

        # Calculate and store the cost
        cost = cost_function(m, b, x, y)
        cost_history.append(cost)

    return m, b, cost_history

# Initialize parameters and hyperparameters
initial_m = 0  # Initial guess for slope
initial_b = 0  # Initial guess for y-intercept
learning_rate = 0.01
iterations = 500

# Run gradient descent
m_final, b_final, cost_history = gradient_descent(x, y, initial_m, initial_b, learning_rate, iterations)

# e) Plot the final fitting line alongside with the scattered data points.

plt.scatter(x, y, label="Data Points")

# Plot the final fitting line
plt.plot(x, m_final * x + b_final, color='red', label="Fitted Line")

plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()

print("Final values: m =", m_final, "b =", b_final)
