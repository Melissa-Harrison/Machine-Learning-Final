# -*- coding: utf-8 -*-
"""Machine Learning Final - Goldfish Lifespan.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eDcmkv2cq5fv_xmdE0q8vVYEB1AGDZ08

**Predicting the lifespan of Comet Goldfish**

The age of a Comet goldfish is not directly influenced by their population. Instead, their lifespan is determined by various factors, including care, environment, and genetics.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

df = pd.read_csv('fish_data.csv')
df.head()

"""# EXPLORE AND CLEAN DATA"""

#Number of rows in the Dataset
df.shape[0]

#Check for duplicate rows
df.duplicated().sum()

#Check for Null values
print(df.isnull().sum())

null_gender_df = df[df['Gender'].isnull()]

# Print out the rows
null_gender_df.head()

#Drop rows with null gender
df = df.dropna()
print(df.isnull().sum())

"""# VISUALIZE THE DATASET"""

#Create a histogram to see life_span distribution
plt.figure(figsize=(8, 5))
sns.histplot(df['life_span'], bins=20, color='darkorange')
plt.xlabel('Lifespan in Years')
plt.ylabel('Frequency')
plt.title('Distribution of Lifespans')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

"""**NOTE: The gender column classifies False for Female and True for male.**"""

#Convert Gender column from true/fale to male/female
df["Gender"] = df["Gender"].map({True: "Male", False: "Female"})

#Male vs Female Distribution
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='Gender', color='darkorange')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.title('Male vs Female Distribution')
plt.show()

plt.figure(figsize=(8, 6))
sns.boxplot(x='Gender', y='life_span', data=df, palette='Set2')
plt.title('Lifespan Distribution by Gender')
plt.xlabel('Gender')
plt.ylabel('Lifespan')
plt.show()

#Color Distribution
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='color', order=df['color'].value_counts().index, palette="YlOrBr")
plt.xlabel('Color')
plt.ylabel('Count')
plt.title('Color Distribution')
plt.xticks(rotation=90)
plt.show

#Habitat Distribution
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='habitat', order=df['habitat'].value_counts().index, palette="YlOrBr")
plt.xlabel('Habitat')
plt.ylabel('Count')
plt.title('Habitat Distribution')
plt.xticks(rotation=90)
plt.show

"""# ENCODE DATA"""

# Encode categorical variables
df = pd.get_dummies(df, columns=['habitat', 'color', 'Gender'], drop_first=False)

df.head(2)

# Calculate the correlation matrix
corr_matrix = df.corr()

# Plot the heatmap
plt.figure(figsize=(15, 13))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Matrix')
plt.show()

#Feature select to only include female fish since the genders have high correlation.
df = df[df['Gender_Female'] == True]

#Drops the data down to 1007 rows of only female fish
df.shape[0]
df.head()

"""# **SPLIT DATA FOR TRAINING AND TESTING**"""

X = df.drop(columns=['life_span','id','Gender_Male'])
y = df['life_span']

X.head()

#Split data into 80/20 training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

baseline_pred = np.full(shape=y_test.shape, fill_value=y_train.mean())

# Evaluation Metrics for Baseline
baseline_mse = mean_squared_error(y_test, baseline_pred)
baseline_mae = mean_absolute_error(y_test, baseline_pred)
baseline_r2 = r2_score(y_test, baseline_pred)

# Print Baseline Metrics
print("Y_train Mean Lifespan",f"{y_train.mean():.2f}")
print(f"Baseline Mean Squared Error (MSE): {baseline_mse}")
print(f"Baseline Mean Absolute Error (MAE): {baseline_mae}")
print(f"Baseline R-squared (R²) Score: {baseline_r2}")

"""# **TRY DECISION TREE MODEL**"""

# Train Decision Tree Regressor
model = DecisionTreeRegressor(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the regression model with MAE MSE and r2
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Print the metrics
print(f'Mean Squared Error: {mse:.2f}')
print(f'Mean Absolute Error: {mae:.2f}')
print(f'R-squared: {r2:.2f}')

plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, color='darkorange')

plt.xlabel('Actual Lifespan (Years)')
plt.ylabel('Predicted Lifespan (Years)')
plt.title('Decision Tree - Actual vs. Predicted Lifespan')
plt.grid()
plt.show()

"""NOTE: This chart, if it was actually good at predicting the lifespan, should be showing a positive linear correlation. Instead it seems pretty random.

Also look at how much worse this performs than our baseline.

# **TRY LINEAR REGRESSION MODEL**
"""

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lin_model = LinearRegression()
lin_model.fit(X_train_scaled, y_train)

y_pred = lin_model.predict(X_test_scaled)

mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Print Evaluation Metrics
print(f"Mean Squared Error (MSE): {mse}")
print(f"Mean Absolute Error (MAE): {mae}")
print(f"R-squared (R²) Score: {r2}")

# Scatter Plot of Actual vs. Predicted Values
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, color='darkorange')

plt.xlabel('Actual Lifespan (Years)')
plt.ylabel('Predicted Lifespan (Years)')
plt.title('Linear Regression - Actual vs. Predicted Lifespan')
plt.grid()
plt.show()

"""NOTE: While the model does better than the decision tree, the R² score is still 0.017, and that is still horrible for a model. We can maybe see a little less scattering, but we should be seeing a much clearer trendline.

# **TRY RANDOM FOREST MODEL**
"""

from sklearn.ensemble import RandomForestRegressor

forest_model = RandomForestRegressor().fit(X_train, y_train)

y_pred = forest_model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"R-squared (R²) Score: {r2}")

plt.figure(figsize=(8,6))

sns.scatterplot(x=y_test, y=y_pred, color='darkorange', alpha=0.9, edgecolor='k', s=80)

#sns.regplot(x=y_test, y=y_pred)

plt.xlabel("Actual Values", fontsize=14)
plt.ylabel("Predicted Values", fontsize=14)
plt.title("Model Performance - Actual vs. Predicted Values", fontsize=16)
plt.grid()
plt.show()

"""NOTE: In this chart we can see the random forest has condensed the predicted value to a smaller range, around 10-19. And while the forest does perform much better than our decision tree, it is actually performing slightly worse than the linear regression model."""