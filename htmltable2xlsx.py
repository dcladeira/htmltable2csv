import streamlit as st
import pandas as pd

st.set_page_config(page_title='Tabela HTML para Excel')

st.header('Converte tabela HTML para arquivo Excel')
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
@st.cache_data
def importa_tabelas(url, decimal_chosen, thousands_chosen, header_chosen, skiprows_chosen):
    try:
        result = pd.read_html(url,
                            decimal=decimal_chosen,
                            thousands=thousands_chosen,
                            header=header_chosen,
                            skiprows=skiprows_chosen,
                            encoding='utf-8')
    except ValueError:
        st.write('Nenhuma tabela encontrada.')
    except:
        st.write('Não foi possível carregar a página.')
    else:
        return result

# IMPORTANT: Cache the conversion to prevent computation on every rerun
@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')
    #return df.to_csv()

# Aguarda inserção da url para executar a consulta
if url:
    df_list = importa_tabelas(url, decimal_chosen, thousands_chosen, header_chosen, skiprows_chosen)
    if df_list:
        st.write(f'Foram localizadas {len(df_list)} tabelas.')
        # Exibe select box para seleção, visualização e exportação das tabelas encontradas
        tabela_selecionada = st.selectbox('Selecione uma tabela para visualização e exportação:',
                                        ['Tabela %d' % i for i in range(len(df_list))])
        indice = int(tabela_selecionada.split(' ')[-1])
        st.table(df_list[indice])
        csv = convert_df(df_list[indice])

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=tabela_selecionada+'.csv',
            mime='text/csv',
        )
