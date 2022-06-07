import pickle

import pandas as pd

(conn,c) = connect_sql()
c.execute('select "3_Dwelling_type","4_Number_of_trees","5_Distance_to_major_","6_Decibel_reading","8_Age_of_Property","9_Quality_of_housing" from "Housing Data" where "9_Quality_of_housing" != \'-1\'')
df = pd.DataFrame(list(c.fetchall()))
dummies = pd.get_dummies(df, columns = df.columns[:-1])
print(dummies.columns.values.tolist())
X_train, y_train=(dummies,df[5])
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators=200, random_state=0)
regressor.fit(X_train, y_train)
pickle.dump(regressor, open("../rf.dat", "wb"))