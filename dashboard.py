import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o dataset
df = pd.read_csv('house02.csv')

# Mapeamento das opções de 'furnished' para português
furniture_map = {
    'furnished': 'mobiliado',
    'not furnished': 'não mobiliado'
}

# Mapeamento das opções de 'accept' para português
# accept_map = {'accept': 'aceita', 'not accept': 'não aceita'}


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
ax.set_xlabel('Valor do Aluguel (R$)')
ax.set_ylabel('Frequência')
st.pyplot(fig)

# # Gráfico 2: Relação entre área do imóvel e valor do aluguel
# st.subheader(f'Relação entre Área e Valor do Aluguel em {cidade}')
# # Mapeamento dos valores da coluna 'furniture' para português no dataframe filtrado
# df_filtered['furniture_pt'] = df_filtered['furniture'].map(furniture_map)
# # Mapeamento dos valores da coluna 'accept' para português no dataframe filtrado
# df_filtered['accept_pt'] = df_filtered['animal'].map(accept_map)
# fig, ax = plt.subplots()
# # sns.scatterplot(data=df_filtered, x='area', y='rent amount (R$)', hue='furniture', style='animal', ax=ax)
# sns.scatterplot(data=df_filtered, x='area', y='rent amount (R$)', hue='furniture_pt', style='animal', ax=ax)
# ax.set_xlabel('Área (m²)')
# ax.set_ylabel('Valor do Aluguel (R$)')
# st.pyplot(fig)
# Gráfico 2: Relação entre área do imóvel e valor do aluguel
st.subheader(f'Relação entre Área e Valor do Aluguel em {cidade}')

# Mapeamento dos valores da coluna 'furniture' para português no dataframe filtrado
df_filtered.loc[:,'furniture_pt'] = df_filtered['furniture'].map(furniture_map)

# Mapeamento dos valores da coluna 'animal' (accept) para português no dataframe filtrado
accept_map = {'acept': 'aceita', 'not acept': 'não aceita'}
df_filtered.loc[:,'accept_pt'] = df_filtered['animal'].map(accept_map)

fig, ax = plt.subplots()

# Criar o scatterplot com a legenda traduzida
scatter = sns.scatterplot(data=df_filtered, x='area', y='rent amount (R$)', hue='furniture_pt', style='accept_pt', ax=ax)

# Ajustar o título da legenda para "Tipo de Mobiliário"
handles, labels = ax.get_legend_handles_labels()

# Atualizar os rótulos da legenda
new_labels = [label.replace('furniture_pt', 'Tipo de Mobiliário').replace('animal', 'Aceitação de Animais') for label in labels]
ax.legend(handles, new_labels, title='Legenda')

# Definir rótulos dos eixos
ax.set_xlabel('Área (m²)')
ax.set_ylabel('Valor do Aluguel (R$)')

# Exibir o gráfico
st.pyplot(fig)


# Gráfico 3: Comparação de imóveis mobiliados e não mobiliados
st.subheader('Comparação de Imóveis Mobiliados vs Não Mobiliados')
# furnished_option = st.radio("Escolha o tipo de imóvel", ('furnished', 'not furnished'))
furnished_option_pt = st.radio("Escolha o tipo de imóvel", ('mobiliado', 'não mobiliado'))

# Traduzir de volta para o valor original do dataframe
furnished_option = [k for k, v in furniture_map.items() if v == furnished_option_pt][0]
df_furnished = df[df['furniture'] == furnished_option]
fig, ax = plt.subplots()
sns.boxplot(data=df_furnished, x='city', y='rent amount (R$)', ax=ax)
ax.set_xlabel('Cidade')
ax.set_ylabel('Valor do Aluguel (R$)')
st.pyplot(fig)

# Gráfico 4: Número de vagas de estacionamento em relação ao aluguel
st.subheader(f'Vagas de Estacionamento x Valor de Aluguel em {cidade}')
fig, ax = plt.subplots()
sns.boxplot(data=df_filtered, x='parking spaces', y='rent amount (R$)', ax=ax)
ax.set_xlabel('Número de Vagas de Estacionamento')
ax.set_ylabel('Valor do Aluguel (R$)')
st.pyplot(fig)

# Conclusões
st.subheader("Conclusões")
st.write("""
Este dashboard permite uma análise dos preços de aluguel de imóveis em diferentes cidades do Brasil. Os gráficos mostram padrões interessantes como:
- A relação entre a área do imóvel e o valor do aluguel, indicando que imóveis maiores tendem a ter aluguéis mais caros.
- Diferenças de preço entre imóveis mobiliados e não mobiliados, dependendo da cidade.
- A distribuição de preços e a variação dependendo do número de vagas de estacionamento.
""")