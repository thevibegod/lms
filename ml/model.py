import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from termcolor import colored as cl

df = pd.read_csv('shuffled_dataset.csv')
X = df.iloc[:, :-1].values
y = df['Next Mode']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3, random_state = 3)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
pd.DataFrame(y_test).to_csv("file2.csv")
print(y_pred)
print(y_test)
print(cl('R-Squared :', attrs=['bold']), model.score(X_test,y_test))
