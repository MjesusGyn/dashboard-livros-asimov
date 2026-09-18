import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')

# 1. Carregar dados limpando espaços invisíveis
@st.cache_data
def carregar_dados():
    df_rev = pd.read_csv("datasets/customer reviews.csv")
    df_books = pd.read_csv("datasets/Top-100 Trending Books.csv")
    
    df_books["book title"] = df_books["book title"].astype(str).str.strip()
    df_rev["book name"] = df_rev["book name"].astype(str).str.strip()
    return df_rev, df_books

df_reviews, df_top_100_books = carregar_dados()

# 2. Criar a lista de livros para a Sidebar
books = sorted(df_top_100_books["book title"].unique())
book = st.sidebar.selectbox("Escolha um Livro", books)

# 3. Filtrar os DataFrames
df_book = df_top_100_books[df_top_100_books["book title"] == book]
df_reviews_f = df_reviews[df_reviews["book name"] == book]

# 4. Renderizar dados do livro (Apenas se encontrar)
if not df_book.empty:
    book_title = df_book["book title"].values[0]
    book_genre = df_book["genre"].values[0]
    
    try:
        book_price = float(df_book['book price'].values[0])
    except:
        book_price = 0.0
        
    book_rating = df_book["rating"].values[0]
    book_year = df_book["year of publication"].values[0]

    # Exibição dos dados do livro
    st.title(book_title)
    st.write(f"**Gênero:** {book_genre}")
    st.write(f"**Preço:** ${book_price:.2f}")
    st.write(f"**Avaliação:** {book_rating}/5")
    st.write(f"**Ano de Publicação:** {book_year}")

    # Exibição das métricas em colunas
    col1, col2, col3 = st.columns(3)
    col1.metric("Preço", f"${book_price:.2f}")
    col2.metric("Avaliação", f"{book_rating}/5")
    col3.metric("Ano de Publicação", str(book_year))

    st.divider()

# 5. Seção de Avaliações Agrupadas em HTML (Livre de bugs do React)
st.subheader("Avaliações dos Leitores")

if not df_reviews_f.empty:
    html_reviews = ""
    for row in df_reviews_f.values:
        # row[2] para o título/autor e row[5] para a mensagem
        html_reviews += f"""
        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #ff4b4b;">
            <p style="margin: 0; color: #31333F; font-size: 16px;"><b>{row[2]}</b></p>
            <p style="margin: 5px 0 0 0; color: #555555; font-size: 14px;">{row[5]}</p>
        </div>
        """
    st.markdown(html_reviews, unsafe_allow_html=True)
else:
    st.info("Nenhuma avaliação encontrada para este livro.")

    # ... (código anterior mantido idêntico)

    # 1. Calcular a média geral de todos os 100 livros do catálogo
    media_geral_catalogo = df_top_100_books["rating"].mean()

    # 2. Calcular a diferença (delta) entre o livro atual e a média geral
    # O valor float garante que o cálculo funcione perfeitamente
    diferenca_media = float(book_rating) - media_geral_catalogo

    # Exibição das métricas em colunas (Agora com 4 colunas)
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Preço", f"${book_price:.2f}")
    
    # Coluna de Avaliação com o comparativo (Delta)
    col2.metric(
        label="Avaliação", 
        value=f"{book_rating}/5",
        delta=f"{diferenca_media:+.2f} vs média"
    )
    
    # Nova coluna mostrando a média fixa do catálogo
    col3.metric("Média do Catálogo", f"{media_geral_catalogo:.2f}/5")
    
    col4.metric("Ano de Publicação", str(book_year))

    st.divider()
    
    # ... (resto do código de avaliações)
