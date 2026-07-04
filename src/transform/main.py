# %%
import pandas as pd
import datetime as dt 
import os
from pathlib import Path

class Transform: 
     # read data json file
    def __init__(self, source_path=None):
        self.__target_path = str(Path(__file__).resolve().parent.parent.parent.joinpath("data", "products.csv"))
        self.__source_path = source_path or Path(__file__).resolve().parents[2].joinpath("data", "products.jsonl")
        self.__df = pd.read_json(self.__source_path, lines=True)
    
    def execute(self):
        Path(self.__target_path).parent.mkdir(parents=True, exist_ok=True)
        # transformations here, astype to convert data types
        self.__df['currentPrice'] = self.__df['currentPrice'].astype(float)
        self.__df['oldPrice'] = self.__df['oldPrice'].astype(float)

        # rating with null change by default value "Nao informado"
        self.__df['rating'] = self.__df['rating'].fillna('Não informado')

        # Store with null change by default value "Loja não informada"
        self.__df['store'] = self.__df['store'].fillna('Loja não informada')

        # oldPrice with null change by default currentPrice value
        self.__df['oldPrice'] = self.__df['oldPrice'].fillna(self.__df['currentPrice'])
                    
        # removing point price
        self.__df['currentPrice'] = self.__df['currentPrice'].astype(str).str.replace('.' , '')
        self.__df['oldPrice'] = self.__df['oldPrice'].astype(str).str.replace('.' , '')
        # cast to float
        self.__df['currentPrice'] = pd.to_numeric(self.__df['currentPrice'], errors='coerce')
        self.__df['oldPrice'] = pd.to_numeric(self.__df['oldPrice'], errors='coerce')

        # create colum date with analysis 
        self.__df['date'] = dt.datetime.now().strftime('%d/%m/%Y')

        if(os.path.isfile(self.__target_path)): 
            print("Arquivo existente")
            self.__df.to_csv(self.__target_path, index=False, mode='a', header=False)
        else: 
            print("Arquivo nao existente")
            self.__df.to_csv(self.__target_path, index=False)







