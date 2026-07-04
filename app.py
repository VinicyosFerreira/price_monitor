from pathlib import Path
import streamlit as st
from src.extract.main import Extractor
from src.transform.main import Transform
from src.view.main import View

PRODUCTS_CSV = Path(__file__).resolve().parent / "data" / "products.csv"

def prepare_initial_data():
    """Executa o ETL automaticamente somente quando o CSV ainda não existe."""
    if not PRODUCTS_CSV.exists():
        try:
            with st.spinner("Preparando os dados iniciais..."):
                products_path = Extractor().execute()
                Transform(source_path=products_path).execute()
        except FileNotFoundError as error:
            st.error(f"Arquivo de produtos não foi encontrado: {error}")
        except Exception as error:
            st.error(f"Erro ao processar os dados: {error}")
        else:
            st.success("Dados iniciais preparados com sucesso")

def main():
    prepare_initial_data()
    View().execute()

if __name__ == "__main__":
    main()
