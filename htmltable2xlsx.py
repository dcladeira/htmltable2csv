import streamlit as st
import pandas as pd
import os
import html5lib
import lxlm

st.set_page_config(page_title='Tabela HTML para Excel')

st.header('Converte tabela HTML para arquivo Excel')
st.write('Os arquivos serão salvos na pasta:')
st.write(os.getcwd())
st.divider()

# Obtem os parâmetros da função pd.read_html()
column_1, column_2, column_3, column_4 = st.columns(4)

with column_1:
    decimal_chosen = st.selectbox('Separador decimal: ', [',', '.'])
with column_2:
    if decimal_chosen == '.':
        thousands_chosen = ','
    else:
        thousands_chosen = '.'
    st.write('Separador milhar:')
    st.write(thousands_chosen)
with column_3:
    skiprows_chosen = st.slider('Linhas descartadas', 0, 10)
with column_4:
    header_chosen = st.toggle('Linha de cabeçalho')
    if header_chosen == True:
        header_chosen = 0
    else:
        header_chosen = None
st.divider()

url = st.text_input('Insira o endereço da página e pressione ENTER: ')

# Função para consultar e armazenar resultado em cache.
# Atualiza a consulta toda vez que houver alteração nos widgets.


# Aguarda inserção de url para executar a consulta
if url:
    #df_list = importa_tabelas(url, decimal_chosen, thousands_chosen, header_chosen, skiprows_chosen)
    #df_list = pd.read_html(url, flavor='html5lib')
    df_list = pd.read_html(url)
    if df_list:
        st.write(f'Foram localizadas {len(df_list)} tabelas.')
        # Exibe select box para seleção, visualização e exportação das tabelas encontradas
        tabela_selecionada = st.selectbox('Selecione uma tabela para visualização e exportação:',
                                        ['Tabela %d' % i for i in range(len(df_list))])
        indice = int(tabela_selecionada.split(' ')[-1])
        st.table(df_list[indice])
        # Exporta tabela se o botão for pressionado
        if st.button('Exporta arquivo Excel'):
            df_list[indice].to_excel(tabela_selecionada+'.xlsx')
