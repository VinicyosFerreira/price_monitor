from src.transform.main import Transform
import streamlit as st
from src.view.main import View
import subprocess as s
import sys
from pathlib import Path

def main() : 
     if(st.button("Iniciar coleta de dados")):

            # pegar caminhos relativo ao projeto
            root_path = Path(__file__).resolve().parent
            # pasta_projeto = "/home/vinicyos/python_projetos/monitoramento_preco/src/collect"
            current_path = root_path.joinpath("src", "collect")

            # deixar spinner rodando enquanto coleta
            try: 
                with st.spinner("Coletando dados..."):
                    # rodar o scrapy
                    result = s.run([sys.executable , "-m" , "scrapy" ,"crawl" , "MercadoLivre" ,"-o",  "../../data/products.jsonl"], 
                          cwd=str(current_path), capture_output=True, check=True, text=True)
                    
                    if result.returncode == 0 :
                        transform  = Transform()
                        transform.execute()
                    else : 
                        raise FileNotFoundError("Arquivo nao encontrado")
                    
            except FileNotFoundError as err:
                    st.error(f"Arquivo de coleta não foi encontrado {err}")
            except Exception as err:
                    st.error(f"Erro genérico {err}")

            # se tudo der certo
            else: 
                st.success("Dados coletados com sucesso")

            view = View()
            view.execute()
    
     else: 
        view = View()
        view.execute()

if __name__ == '__main__': 
    main()