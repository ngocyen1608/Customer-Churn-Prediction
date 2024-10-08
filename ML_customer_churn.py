# -*- coding: utf-8 -*-
"""Nguyen_Ngoc_Yen_ML_Final_Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pU2Jbaeb9bfPazZ1rjlyo59tHD7IIGhM
"""

#Import libraries
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import datetime as dt
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

#Import data
from google.colab import files
uploaded = files.upload()
df = pd.read_excel('churn_prediction.xlsx')

df.head(3)

"""## **Overview the data:**"""

# Check info & missing values:
df.info()

#Remove unnecessary columns
##CustomerID is just a unique identifier to each user and has nothing to do with predicting if user churns or not.
df.drop(columns="CustomerID", inplace=True)

# Check imbalanced:
label_ratio = df['Churn'].value_counts(normalize=True)
label_ratio

"""The ration of label 1 on total is 16% &#8594; We can continue with the EDA and ML model"""

# Check duplicated values:
df.duplicated().unique()

# Check null values:
df.isnull().sum()

#Handle missing values
for col in df.columns:
    if df[col].isnull().sum() > 0:
        df[col].fillna(df[col].median(), inplace=True)
df.isnull().sum()

"""## **Define type of data**"""

df.dtypes.unique()

obj_cols = df.select_dtypes(include=['object'])
num_cols = df.select_dtypes(exclude=['object'])

num_cols.nunique()

""":As showing the unique values of each numeric columns, there's columns have low unique values (less than 10 values) &#8594; There's column has dtype = numeric but have category meaning."""

for col in num_cols:
    print(col, df[col].unique())

# convert num_cols to categories
df2 = df.copy()
for col in df2.columns:
    if df2[col].dtype == 'int':
        df2[col] = df2[col].astype(str)

df2.dtypes

for col in obj_cols:
    print(col, df[col].unique())

#In PreferredLoginDevice, Mobile Phone and Phone can be merged into one category
##In PreferredPaymentMode, Credit Card and CC can be merged into one category
###In PreferedOrderCat, Mobile Phone and Phone can be merged into one category
df['PreferredLoginDevice'] = df['PreferredLoginDevice'].replace('Phone', 'Mobile Phone')
df['PreferredPaymentMode'] = df['PreferredPaymentMode'].replace(['CC', 'COD'], ['Credit Card', 'Cash on Delivery'] )
df['PreferedOrderCat'] = df['PreferedOrderCat'].replace('Mobile', 'Mobile Phone')

cat_data = df2.select_dtypes(include=['object']).drop(columns=['Churn'])
num_data = df2.select_dtypes(exclude=['object'])

for col in cat_data:
    print(col, df2[col].unique())

"""## **Start Feature Engineering & EDA**

#### Check distribution (density) of some quantity features
"""

cols = ['Tenure','OrderCount']

plt.figure(figsize=(10, 6))

for i, col in enumerate(cols, 1):
    plt.subplot(len(cols), 1, i)
    sns.kdeplot(num_cols[col], shade=True)
    plt.title(f'Density Distribution of {col}')
    plt.xlabel('Value')
    plt.ylabel('Density')

plt.tight_layout()
plt.show()

"""#### Check correlation:"""

plt.figure(figsize=(15,8))
sns.heatmap(df.corr(numeric_only=True), annot=True)
plt.title("Correlation Matrix for the Customer Dataset")
plt.show()

"""Based on correlation heatmap, we see the Complain has
high correlation with Churn
"""

sns.boxplot(data=df, x='Churn',y='Complain')

"""### Category Features:"""

df_c = df2[df2['Churn']=='1'].copy()
df_nc = df2[df2['Churn']=='0'].copy()

fig, ax = plt.subplots(4,3,figsize=(20, 18))
fig.suptitle('Density of Numeric Features by Churn', fontsize=20)
ax = ax.flatten()

for col, subplot in zip(cat_data, ax.flatten()):
    sns.countplot(x=df[col], hue=df.Churn, ax=subplot)

plt.show()

#To make the inferences more insightful we can find out the per cent churn contributed by each category for each variable.
fig, ax = plt.subplots(2, 3, figsize=(30, 20))
plt.rcParams['font.size'] = '16'
for col,subplot in zip(cat_data, ax.flatten()):
    #calculate percent churn
    temp = df.groupby(by=df[col]).Churn.sum()
    total = df.value_counts(col).sort_index()
    res1 = temp/total*100
    #visualising the result
    subplot.pie(labels = res1.index, x = res1.values, autopct='%.0f%%',textprops={'fontsize': 16})

"""## **Feature Transforming**

###Encoding
"""

# check before encoding that my catogries for my columns are limited
for i in df.columns:
    if df[i].dtype == 'object':
        print(df[i].value_counts())
        print('*' * 40)

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

# Encode for obj_cols
for i in df.columns:
  if df[i].dtype == 'object':
    df[i] = le.fit_transform(df[i])

df.head(3)

"""###Handling Imbalanced Data"""

X = df.drop('Churn' , axis = 1)
Y = df['Churn']

from imblearn.combine import SMOTETomek

smt = SMOTETomek(random_state=42)
x_over , y_over = smt.fit_resample(X , Y)

x_over.shape, y_over.shape

"""###Normalization"""

from sklearn.model_selection import train_test_split

# divided into train and test data
x_train , x_test , y_train , y_test = train_test_split(x_over , y_over , test_size = 0.30 , random_state = 42)

# Now we  will make normalization for all data to make them in commom range
from sklearn.preprocessing import MinMaxScaler , StandardScaler , RobustScaler

MN = MinMaxScaler()
# SC = StandardScaler()
# Rb = RobustScaler()
x_train_scaled = MN.fit_transform(x_train)
x_test_scaled = MN.fit_transform(x_test)

"""## **Model**"""

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import AdaBoostClassifier
import warnings
from sklearn.metrics import accuracy_score
warnings.filterwarnings("ignore")

logisreg_clf = LogisticRegression()
svm_clf = SVC()
dt_clf = DecisionTreeClassifier()
rf_clf = RandomForestClassifier()
XGB_clf = XGBClassifier()
ada_clf = AdaBoostClassifier()

clf_list = [logisreg_clf, svm_clf, dt_clf, rf_clf, XGB_clf, ada_clf]
clf_name_list = ['Logistic Regression', 'Support Vector Machine', 'Decision Tree', 'Random Forest', 'XGBClassifier' , 'AdaBoostClassifier']

for clf in clf_list:
    clf.fit(x_train_scaled,y_train)

train_acc_list = []
test_acc_list = []

for clf,name in zip(clf_list,clf_name_list):
    y_pred_train = clf.predict(x_train_scaled)
    y_pred_test = clf.predict(x_test_scaled)
    print(f'Using model: {name}')
    print(f'Trainning Score: {clf.score(x_train_scaled, y_train)}')
    print(f'Test Score: {clf.score(x_test_scaled, y_test)}')
    print(f'Acc Train: {accuracy_score(y_train, y_pred_train)}')
    print(f'Acc Test: {accuracy_score(y_test, y_pred_test)}')
    train_acc_list.append(accuracy_score(y_train, y_pred_train))
    test_acc_list.append(accuracy_score(y_test, y_pred_test))
    print(' ' * 60)
    print('*' * 60)
    print(' ' * 60)

# graph to determine best 2 models

all_models = pd.DataFrame({'Train_Accuarcy': train_acc_list , 'Test_Accuarcy' : test_acc_list}  , index = clf_name_list)
all_models

!pip install mlxtend

"""## **Evaluation**"""

from mlxtend.plotting import plot_confusion_matrix
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report, RocCurveDisplay, confusion_matrix

# Logistic regression
model= LogisticRegression()
model.fit(x_train_scaled,y_train)
y_pred = model.predict(x_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
roc_auc1 = roc_auc_score(y_test, y_pred)
print("Accuracy = {}".format(accuracy))
print("ROC Area under Curve = {}".format(roc_auc1))
print(classification_report(y_test,y_pred,digits=5))
plot_confusion_matrix(confusion_matrix(y_test , y_pred))
print('*' * 70)
RocCurveDisplay.from_estimator(model , x_test_scaled , y_test)

# Decision Tree
model=DecisionTreeClassifier()
model.fit(x_train_scaled,y_train)
y_pred = model.predict(x_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
roc_auc3 = roc_auc_score(y_test, y_pred)
print("Accuracy = {}".format(accuracy))
print("ROC Area under Curve = {}".format(roc_auc3))
print(classification_report(y_test,y_pred,digits=5))
plot_confusion_matrix(confusion_matrix(y_test , y_pred))
RocCurveDisplay.from_estimator(model , x_test_scaled , y_test)

# random forest
import time
start=time.time()

model=RandomForestClassifier()
model.fit(x_train_scaled,y_train)

end=time.time()
training_time=end-start
print(f'Training time: {training_time:.3f} seconds')

pred_start=time.time()
y_pred = model.predict(x_test_scaled)
pred_end = time.time()
pred_time = (pred_end-pred_start)/len(x_test_scaled)
print(f'Average prediction time per customer: {pred_time:.6f} seconds')

accuracy = accuracy_score(y_test, y_pred)
roc_auc4 = roc_auc_score(y_test, y_pred)
print("Accuracy = {}".format(accuracy))
print("ROC Area under Curve = {}".format(roc_auc4))
print(classification_report(y_test,y_pred,digits=5))
plot_confusion_matrix(confusion_matrix(y_test , y_pred))
RocCurveDisplay.from_estimator(model , x_test_scaled , y_test)

"""## **Hyperparameter Tuning**"""

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

#  RandomForestClassifier
rf_classifier = RandomForestClassifier()

#create hyperparameter
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4] }

# Use the best cv score and the best parameters
grid_search = GridSearchCV(estimator=rf_classifier, param_grid=param_grid, cv=3)
grid_search.fit(x_train_scaled, y_train)

# print the best parameters
best_params = grid_search.best_params_
print("Best Hyperparameters:", best_params)

#fit the object to the data
grid_search.fit(X_train, y_train)

#feature importance
feature_importance=pd.DataFrame(grid_search.best_estimator_[2].feature_importances_, columns=['importance'])
feature_importance['features'] = x_train.columns

plt.figure(figsize=(10,8))
sns.barplot(x='importance', y='features', data=feature_importance.sort_values(by='importance', ascending=False))
plt.title('Feature importances')
plt.show()

"""## **Conclusion**

What are the patterns/behavior of churned users?
1. The biggest particular influences for eliminating customer e-commerce services are “Complain”, “MaterialStatus”, “SatisfactionScore”, “PreferedOrderCat”, “DaySinceLastOrder”, “CashbackAmount” and “Tenure”.
2. Customers who stay with the service tend to have a longer tenure, while those who leave (churn) typically do so after a shorter duration.
3. Customers who prefer using a computer for login have a slightly higher churn rate compared to those who prefer mobile phones.
4. Male customers have a slightly higher churn rate compared to female customers
5. Single customers have a significantly higher churn rate compared to married  and divorced customers.
6. Surprisingly, the average satisfaction score is higher for customers who churned compared to those who didn’t. This might suggest that factors other than satisfaction scores are influencing the decision to churn, or that the satisfaction scores may not fully capture the customer’s experience or likelihood to remain with the service.

What are your suggestions to the
company to reduce churned users.

1. Should consider that the higher percentage are males increasing the products that grap the males interest and so on
2. May be the comapny should consider taking care of the products that suits the single and the married customers as the single are more likly to churn
3. The company should think of another technique other than satisfaction score or complaining may be a hot line to recive the complains to get fast results or provied regular phone calls to recive feedback from the customers
4. The company should check the mobile version of the store to see if there is any problem with the ui/ux
5. Once the customer has reached 12%-15% orderamount the company should consider focusing more on grap their attention with the products they like
6. For customers who have just bought electronic goods, cross-selling can be done by offering electronic accessories, such as keyboards, mice, etc.
"""