import streamlit as st
import pandas as pd
import os
import plotly.express as px
from pathlib import Path

class View: 

    def __init__(self):
        self.__target_path = str(Path(__file__).resolve().parent.parent.parent.joinpath("data", "products.csv"))

    def execute(self):
        
        st.title("Monitoramento de preço de notebooks")

        if(not os.path.exists(self.__target_path)):
            st.write("Clique no botão para iniciar a coleta de dados")
            st.stop()

        df = pd.read_csv(self.__target_path)

        st.subheader("KPIs")

        # aumentar a largura das colunas
        col1, col2, col3 = st.columns(3, gap="large")
        st.set_page_config(layout="wide")

        total_itens = df.shape[0]
        col1.metric(label="Total de itens", value=total_itens)

        unique_stores = df['store'].nunique()
        col2.metric(label="Total de lojas", value=unique_stores)

        average_price = df['currentPrice'].mean()
        col3.metric(label="Preço médio", value=f"R${average_price:.2f}")

        # Quais sao as lojas mais encontradas
        st.subheader("Lojas mais encontradas no sistema até a página 10")
        col1, col2 = st.columns([4 , 2])
        store_count = df['store'].value_counts().sort_values(ascending=False).head(15).reset_index()
        fig = px.bar(store_count, x="store", y="count", labels={"store": "Loja" , "count": "Quantidade"}, 
                     color_discrete_sequence=px.colors.qualitative.Plotly)
        col1.plotly_chart(fig)
        col2.dataframe(
            store_count,
            hide_index=True,
            column_config = {
                "store": "Loja/Marca",
                "count": "Quantidade"
            }
        )

        # Preço médio por loja
        st.subheader("Preço médio por loja")
        col1, col2 = st.columns([4, 2])
        average_price_by_store = df.groupby('store')['currentPrice'].mean().sort_values(ascending=False).head(15).reset_index()
        fig2 = px.histogram(average_price_by_store, x="store", y="currentPrice", color_discrete_sequence=px.colors.qualitative.Bold, 
                      labels={"store": "Loja", "currentPrice": "Preço médio"})
        fig2.update_layout(
            yaxis_tickprefix = 'R$ ',
            yaxis_tickformat = ',.2f',
            separators=",.",
        )
        col1.plotly_chart(fig2)
        col2.dataframe(
            average_price_by_store,
            hide_index=True,
            column_config = {
                "store": "Loja/Marca",
                "currentPrice": st.column_config.NumberColumn("Preço médio", format="R$ %.2f")
            }
        )
        

        st.subheader("Lojas com melhores taxas de desconto")
        col1, col2 = st.columns([4, 2])
        df['discout_rate'] = (1 - (df['currentPrice'] / df['oldPrice'])) * 100
        rating_discount = df.groupby('store')['discout_rate'].mean().sort_values(ascending=False).head(15).reset_index()
        fig3 = px.line(rating_discount, x="store", y="discout_rate", color_discrete_sequence=px.colors.qualitative.Vivid, 
                      labels={"store": "Loja", "discout_rate": "Taxa de desconto"})
        fig3.update_layout(
            yaxis_tickformat = ',.2f',
            yaxis_ticksuffix = ' %',
        )
        col1.plotly_chart(fig3)
        col2.dataframe(
            rating_discount,
            hide_index=True,
            column_config = {
                "store": "Loja/Marca",
                "discout_rate": st.column_config.NumberColumn("Taxa de desconto", format="%.2f %%")
            }
        )

            
