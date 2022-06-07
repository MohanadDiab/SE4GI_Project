import pickle
import time

import pandas as pd
from sql import connect_sql

list_0 = [5, '0_Apartment', '0_Semi-Detached', '0_Single storey', '0_Town House', '1_1', '1_2', '1_3', '1_4', '1_5',
          '1_5+', '2_100 metres or less', '2_200 m', '2_300 m', '2_400 m', '2_400 m +', '3_45', '3_46', '3_47', '3_48',
          '3_49', '3_50', '3_51', '3_52', '3_53', '3_54', '3_55', '3_56', '3_57', '3_58', '3_60', '3_61', '3_62',
          '3_63', '3_64', '3_65', '3_77', '4_1900s Below', '4_1910s (Old style)', '4_1920s', '4_1930s', '4_1940-1960s',
          '4_1970s', '4_1980s', '4_1990s', '4_2000s', '4_2010 + Modern']
_dict = {}

(conn, c) = connect_sql()


def runML(_temp):
    uuid = _temp[0]
    df = pd.DataFrame([list(_temp)])
    dummies = pd.get_dummies(df, columns=df.columns[1:])
    list_1 = dummies.columns.values.tolist()
    print(dummies)
    for i in list_0:
        if i in list_1:
            _dict[i] = [1]
        else:
            _dict[i] = [0]
    result = pd.DataFrame(_dict)
    loaded_model = pickle.load(open("rf.dat", "rb"))
    y_pred = loaded_model.predict(result)
    sql = 'update "Housing Data" set "9_Quality_of_housing" = \'{}\' where ec5_uuid=\'{}\''.format(int(y_pred[0]), uuid)
    c.execute(sql)
    conn.commit()
    print('successfully predicted the quality of this house, which is {}'.format(y_pred[0]))


if __name__ == '__main__':
    while True:
        c.execute(
            'select ec5_uuid,"3_Dwelling_type","4_Number_of_trees","5_Distance_to_major_","6_Decibel_reading","8_Age_of_Property" from "Housing Data" where "9_Quality_of_housing" = \'-1\'')
        _temp = c.fetchone()
        if _temp is not None:
            print('Detected newly inserted row, start to run the algorithm.')
            runML(_temp)
        else:
            time.sleep(5)
