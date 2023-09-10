# Imports
from datetime import datetime
import numpy as np
import os
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Task 1

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
print()

# Task 3
