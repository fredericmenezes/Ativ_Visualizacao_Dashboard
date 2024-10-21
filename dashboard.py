import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações de estilo do Seaborn
sns.set(style="whitegrid")

# Carregar o dataset
df = pd.read_csv('house02.csv')

# Mapeamento das opções de 'furnished' para português
furniture_map = {
    'furnished': 'mobiliado',
    'not furnished': 'não mobiliado'
}

# Mapeamento das opções de 'accept' para português
accept_map = {
    'acept': 'aceita',
    'not acept': 'não aceita'
}

# Título do dashboard
st.title('Dashboard de Aluguel de Casas no Brasil')

# Adicionando uma barra lateral para filtro da cidade
st.sidebar.header('Filtros')
cidade = st.sidebar.selectbox('Selecione a cidade', df['city'].unique())

# Filtrar os dados pela cidade selecionada
dados = df[df['city'] == cidade]

# Remover outliers baseados na área
q = dados["area"].quantile(0.99)
df_filtered = dados[dados["area"] < q]

# Colunas para espalhar os gráficos
col1, col2 = st.columns(2)

# Gráfico 1: Distribuição dos valores de aluguel na cidade selecionada
with col1:
    st.subheader(f'Distribuição de Valores de Aluguel em {cidade}')
    if not df_filtered.empty:
        fig, ax = plt.subplots()
        sns.histplot(df_filtered['rent amount (R$)'], kde=True, ax=ax)
        ax.set_xlabel('Valor do Aluguel (R$)')
        ax.set_ylabel('Frequência')
        st.pyplot(fig)
    else:
        st.warning('Não há dados disponíveis para esta cidade.')

# Gráfico 2: Relação entre área do imóvel e valor do aluguel
with col2:
    st.subheader(f'Relação entre Área e Valor do Aluguel em {cidade}')
    if not df_filtered.empty:
        df_filtered['Mobilia:'] = df_filtered['furniture'].map(furniture_map)
        df_filtered['Animais:'] = df_filtered['animal'].map(accept_map)
        fig, ax = plt.subplots()
        sns.scatterplot(data=df_filtered, x='area', y='rent amount (R$)', hue='Mobilia:', style='Animais:', ax=ax)
        ax.set_xlabel('Área (m²)')
        ax.set_ylabel('Valor do Aluguel (R$)')
        st.pyplot(fig)
    else:
        st.warning('Não há dados disponíveis para esta cidade.')

# Colunas para os próximos gráficos
col3, col4 = st.columns(2)

# Gráfico 3: Comparação de imóveis mobiliados e não mobiliados
with col3:
    st.subheader('Comparação de Imóveis Mobiliados vs Não Mobiliados')
    furnished_option_pt = st.radio("Escolha o tipo de imóvel", ('mobiliado', 'não mobiliado'))

    # Traduzir de volta para o valor original do dataframe
    furnished_option = [k for k, v in furniture_map.items() if v == furnished_option_pt][0]
    df_furnished = df[df['furniture'] == furnished_option]
    
    if not df_furnished.empty:
        fig, ax = plt.subplots()
        sns.boxplot(data=df_furnished, x='city', y='rent amount (R$)', ax=ax)
        ax.set_xlabel('Cidade')
        ax.set_ylabel('Valor do Aluguel (R$)')
        st.pyplot(fig)
    else:
        st.warning('Não há dados disponíveis para este tipo de imóvel.')

# Gráfico 4: Número de vagas de estacionamento em relação ao aluguel
with col4:
    st.subheader(f'Vagas de Estacionamento x Valor de Aluguel em {cidade}')
    if not df_filtered.empty:
        fig, ax = plt.subplots()
        sns.boxplot(data=df_filtered, x='parking spaces', y='rent amount (R$)', ax=ax)
        ax.set_xlabel('Número de Vagas de Estacionamento')
        ax.set_ylabel('Valor do Aluguel (R$)')
        st.pyplot(fig)
    else:
        st.warning('Não há dados disponíveis para esta cidade.')

# Conclusões
st.subheader("Conclusões")
st.write("""
Este dashboard permite uma análise dos preços de aluguel de imóveis em diferentes cidades do Brasil. 
Os gráficos mostram padrões interessantes como:
- A relação entre a área do imóvel e o valor do aluguel, indicando que imóveis maiores tendem a ter aluguéis mais caros.
- Diferenças de preço entre imóveis mobiliados e não mobiliados, dependendo da cidade.
- A distribuição de preços e a variação dependendo do número de vagas de estacionamento.
""")
