import pandas as pd
data = pd.read_csv('./data_csv/강원특별자치도_일반음식점.csv',encoding = 'CP949',low_memory = False)
data_columns = list(data.columns)
print(data.info())
