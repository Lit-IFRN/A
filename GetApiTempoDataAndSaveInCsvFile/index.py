import requests
import pandas as pd
import json

# Faz a requisição e pega os valores em json
response = requests.get('https://apitempo.inmet.gov.br/estacao/diaria/2007-01-07/2020-09-30/A304')
data = response.text
jsonData = json.loads(data)


for i in range(0, len(jsonData)):
    if jsonData[i]['CHUVA'] == None:
        year = int(jsonData[i]['DT_MEDICAO'][0:4])
        isLeap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        if(isLeap):
            isFirstYear = i < 366
            lastYearInDays = 366
        else:
            isFirstYear = i < 365
            lastYearInDays = 365

        if(isFirstYear):
            jsonData[i]['CHUVA'] = '0'
        else:
            jsonData[i]['CHUVA'] = jsonData[i-lastYearInDays]['CHUVA']
        


# Salva o resultado da requisição pra o arquivo data.json
with open('data.json', 'w') as outfile:
    json.dump(jsonData, outfile, ensure_ascii=False)

# Lê os dados do arquivo data.json
df = pd.read_json('data.json', encoding="latin")

# Converte para csv
df.to_csv('data.csv')
