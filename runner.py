import sys
from streamlit.web import cli as stcli


sys.argv ["streamlit", "run", "app.py"]
sys.exit(stcli.main())
@st.cache_data
def carregar_dados():
    # Links ajustados para ler os arquivos diretamente da raiz do seu repositório GitHub
    url_reviews = "https://githubusercontent.com"
    url_books = "https://githubusercontent.com"
    
    df_rev = pd.read_csv(url_reviews)
    df_books = pd.read_csv(url_books)
    
    df_books["book title"] = df_books["book title"].astype(str).str.strip()
    df_rev["book name"] = df_rev["book name"].astype(str).str.strip()
    return df_rev, df_books

df_reviews, df_top_100_books = carregar_dados()
