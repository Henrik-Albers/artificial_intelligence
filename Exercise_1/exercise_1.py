# Task 1
""" 
(a) Unsupervised Learning  : Because products bought toguether are a set of unlabled data set where the  solving learning problem includes finding patterns and relashionships between the objects.
(b) Reinforcement Learning : Because a chess computer needs to react with the player and take actions based on the previous outcome of the data set .
(c) Supervised Learning    : Because the spam recognition system  needs to classify the set of emails which is a set of labeled data.
(d) Supervised Learning    : Because the classification of applicants system  needs to classify the set of applicants as credit-worthy or unworthy which is a set of labeled data.
(e) Supervised Learning    : Because the Object recognition in computer vision needs to classify the set of objets based on their features .
(f) Reinforcement Learning : Because the Robot neds to be trained  and interact based on the obsticales and take actions to get to the end point.
(g) Unsupervised Learning  : Because the task involves invoves clustering images with is a set of unlabled data based on groups.
 """
# Task 2

# Task 3

import numpy as np

# a) Load the data in GD_Example.txt (it includes 500 pairs of data (xi,yi))
data = np.genfromtxt("GD_Example.txt", delimiter=",")
x = data[:, 0]  
y = data[:, 1]  

# b) Plot the data points
import matplotlib.pyplot as plt

plt.scatter(x, y, label="Data Points")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()

# c) Implement the cost function

def cost_function(m, b, x, y):
    N = len(x)
    error = np.sum((y - (m * x + b))**2)
    return error / (2 * N)


# d) Using gradient descent algorithm with 500 iterations, find the best fitting line characterized by: 𝑚𝑥 + 𝑏. (determine m and b)

def gradient_descent(x, y, m, b, learning_rate, iterations):
    N = len(x)
    cost_history = []

    for _ in range(iterations):
        # Calculate the predicted values
        y_pred = m * x + b

        # Calculate the gradients
        dm = (-1/N) * np.sum(x * (y - y_pred))
        db = (-1/N) * np.sum(y - y_pred)

        # Update parameters
        m -= learning_rate * dm
        b -= learning_rate * db

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
