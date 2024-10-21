import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o dataset
df = pd.read_csv('house02.csv')

# Título do dashboard
st.title('Dashboard de Aluguel de Casas no Brasil')

# Filtro para selecionar a cidade
cidade = st.selectbox('Selecione a cidade', df['city'].unique())

# Filtrar os dados pela cidade selecionada
df_filtered = df[df['city'] == cidade]

# Gráfico 1: Distribuição dos valores de aluguel na cidade selecionada
st.subheader(f'Distribuição de Valores de Aluguel em {cidade}')
fig, ax = plt.subplots()
sns.histplot(df_filtered['rent amount (R$)'], kde=True, ax=ax)
st.pyplot(fig)

# Gráfico 2: Relação entre área do imóvel e valor do aluguel
st.subheader(f'Relação entre Área e Valor do Aluguel em {cidade}')
fig, ax = plt.subplots()
sns.scatterplot(data=df_filtered, x='area', y='rent amount (R$)', hue='furniture', style='animal', ax=ax)
st.pyplot(fig)

# Gráfico 3: Comparação de imóveis mobiliados e não mobiliados
st.subheader('Comparação de Imóveis Mobiliados vs Não Mobiliados')
furnished_option = st.radio("Escolha o tipo de imóvel", ('furnished', 'not furnished'))
df_furnished = df[df['furniture'] == furnished_option]
fig, ax = plt.subplots()
sns.boxplot(data=df_furnished, x='city', y='rent amount (R$)', ax=ax)
st.pyplot(fig)

# Gráfico 4: Número de vagas de estacionamento em relação ao aluguel
st.subheader(f'Vagas de Estacionamento x Valor de Aluguel em {cidade}')
fig, ax = plt.subplots()
sns.boxplot(data=df_filtered, x='parking spaces', y='rent amount (R$)', ax=ax)
st.pyplot(fig)

# Conclusões
st.subheader("Conclusões")
st.write("""
Este dashboard permite uma análise dos preços de aluguel de imóveis em diferentes cidades do Brasil. Os gráficos mostram padrões interessantes como:
- A relação entre a área do imóvel e o valor do aluguel, indicando que imóveis maiores tendem a ter aluguéis mais caros.
- Diferenças de preço entre imóveis mobiliados e não mobiliados, dependendo da cidade.
- A distribuição de preços e a variação dependendo do número de vagas de estacionamento.
""")