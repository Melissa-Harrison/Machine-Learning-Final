# Machine-Learning-Final
A machine learning project focused on predicting the lifespan of goldfish.

For this project I found a dataset about goldfish from kaggle: https://www.kaggle.com/datasets/stealthtechnologies/predict-lifespan-of-a-comet-goldfish/data
The data includes factors including average length, weight, habitat, pH, color, gender, and life span. What I wanted to find, is that based on these factors is it possible to make a model to accurately predict the lifespan of a goldfish. This will require a regression model as the data for the lifespan is continuous. So that narrowed this down to what models I could use. 
For preprocessing, I made sure there were no duplicate entries, and to see what columns included null values, if any. There were only a few rows that had no gender, and since my feature selection excluded male fish, I dropped these rows. This helped my accuracy improve, but only slightly. I then used one hot encoding on the categorical variables of gender, habitat and colors of the fish. I also made a correlation matrix, and this showed that there was essentially no correlations between any of the factors (except for between male and female). 

Since the data was categorized by colors and also by habitats(pond,river, etc.), I initially started with Decision Tree regression. This model turned out to be extremely inaccurate and perform significantly worse than simple baseline accuracy, and doing more feature selection didn't improve the accuracy much.
Next, I tried to do linear regression. This did perform much better than the decision tree, but the accuracy of the model was about the same as just guessing each value was the median age of the data. 
Going back to decision trees, I made a model of a random forest. This was a significant improvement from just a decision tree alone, but suprisingly, it still performed worse than the linear regression model.
Overall, after looking at visualizations of the predicted vs actual values of my models, and the correlation matrix


Provide a report (in your repository as a README file) summarizing:
Problem definition and dataset description.
EDA findings.
Preprocessing steps.
For preprocessing, I made sure there were no duplicate entries, and to see what columns included null values, if any. There were only a few rows that had no gender, and since my feature selection excluded male fish, I dropped these rows. This helped my accuracy improve, but only slightly. Initially 
Modeling approach and results.
Reflections on challenges faced and lessons learned.
