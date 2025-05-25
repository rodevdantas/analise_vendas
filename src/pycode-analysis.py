import pandas as pd
import seaborn as sbn
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from scipy.stats import pearsonr
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import os

# %% Transferindo CSV pro explorador de variáveis
tb_clientes = pd.read_csv(os.path.join('..', 'data', 'tb_clientes.csv'))
tb_pedidos = pd.read_csv(os.path.join('..', 'data', 'tb_pedidos.csv'))
tb_produtos = pd.read_csv(os.path.join('..', 'data', 'tb_produtos.csv'))

# %% Conferindo 3 primeiras colunas de cada banco de dados
tb_clientes.head(3)
tb_produtos.head(3)
tb_pedidos.head(3)

# %% Criando um dataset único
dataset = tb_pedidos.merge(tb_clientes, on='cliente_id', how='left')
dataset= dataset.merge(tb_produtos, on='produto_id', how='left')

# %% Conversão das datas
dataset.info()
dataset['data_venda'] = pd.to_datetime(dataset["data_venda"])
dataset['data_entrega'] = pd.to_datetime(dataset["data_entrega"])

# %% Cálculo do lucro
dataset["Lucro"] = dataset['valor_vendas'] - dataset['desconto'] - dataset['custo_produto'] - dataset['custo_entrega']
print(dataset[['valor_vendas', 'desconto', 'custo_produto', 'custo_entrega', 'Lucro']].head().T)

# %% Criação de colunas temporais
dataset['ano'] = dataset['data_venda'].dt.year
dataset['mes'] = dataset['data_venda'].dt.month


# %% Agrupando vendas por ano e mês
dataset_agrupado_ano_mes = dataset.groupby(by=['ano', 'mes']).agg({'valor_vendas':"sum"}).reset_index()

# Gráfico de tendência de vendas por ano/mês
plt.figure(figsize=(14,8), dpi=600)
sbn.lineplot(data=dataset_agrupado_ano_mes, x='mes', y='valor_vendas', hue='ano', palette='viridis')
plt.xlabel("Mês", fontsize=14)
plt.ylabel("Total vendido", fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=16)
plt.title("Tendência Mensal de Vendas", fontsize=18)
plt.show()


# %% Correlação entre lucro e valor de vendas
correlation, p_value = pearsonr(dataset['valor_vendas'], dataset['Lucro'])
print(f"Correlação entre Lucro e Valor de Vendas: {correlation:.2f} (p-valor: {p_value:.4f})")

plt.figure(figsize=(14,8))
sbn.scatterplot(x=dataset['valor_vendas'], y=dataset['Lucro'])
plt.xlabel("Valor de Vendas", fontsize=14)
plt.ylabel("Lucro", fontsize=14)
plt.title("Correlação entre Lucro e Valor de Vendas", fontsize=18)
plt.show()


# %% Distruibuição de vendas por faixa de preço
faixa_preco = pd.cut(dataset['valor_vendas'], bins=[0, 100, 500, 1000, 5000, 10000], 
                      labels=['Até 100', '100-500', '500-1000', '1000-5000', 'Acima de 5000'])
dataset['faixa_preco'] = faixa_preco

vendas_faixa_preco = dataset.groupby('faixa_preco').agg({'valor_vendas':'sum'}).reset_index()

plt.figure(figsize=(14,8))
sbn.barplot(x='faixa_preco', y='valor_vendas', data=vendas_faixa_preco)
plt.xlabel("Faixa de Preço", fontsize=14)
plt.ylabel("Total Vendido", fontsize=14)
plt.title("Vendas por Faixa de Preço", fontsize=18)
plt.show()


# %% Modelo de previsão de vendas 
X = dataset_agrupado_ano_mes[['mes']]
y = dataset_agrupado_ano_mes['valor_vendas']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Regressão Linear
modelo = LinearRegression()
modelo.fit(X_train, y_train)

previsao_meses = pd.DataFrame({'mes': np.arange(1, 13)})
previsao_meses['previsao_vendas'] = modelo.predict(previsao_meses[['mes']])

plt.figure(figsize=(14,8))
sbn.lineplot(data=dataset_agrupado_ano_mes, x='mes', y='valor_vendas', hue='ano', palette='viridis')
sbn.lineplot(data=previsao_meses, x='mes', y='previsao_vendas', color="red", linestyle="dashed", label="Previsão")
plt.xlabel("Mês", fontsize=14)
plt.ylabel("Total Vendido", fontsize=14)
plt.legend()
plt.title("Previsão de Vendas para os Próximos Meses", fontsize=18)
plt.show()


# %% Clientes mais rentáveis

clientes_rentaveis = dataset.groupby(['cliente_id', 'nome']).agg({'valor_vendas': 'sum', 'Lucro': 'sum'}).reset_index()
clientes_rentaveis = clientes_rentaveis.sort_values(by='Lucro', ascending=False).head(10)

plt.figure(figsize=(14,8))
sbn.barplot(x=clientes_rentaveis['nome'], y=clientes_rentaveis['Lucro'], palette='viridis')
plt.xticks(rotation=45, ha="right")  
plt.xlabel("Cliente", fontsize=14)
plt.ylabel("Lucro Gerado", fontsize=14)
plt.title("Top 10 Clientes Mais Rentáveis", fontsize=18)
plt.show()


# %% Tempo médio de entrega // Impacto nas vendas
dataset["tempo_entrega"] = (dataset['data_entrega'] - dataset['data_venda']).dt.days

plt.figure(figsize=(14,8))
sbn.scatterplot(x=dataset['tempo_entrega'], y=dataset['Lucro'])
plt.xlabel("Dias para Entrega", fontsize=14)
plt.ylabel("Lucro", fontsize=14)
plt.title("Impacto do Tempo de Entrega no Lucro", fontsize=18)
plt.show()

# %% Vendas por dia da semana 
dias_ordenados = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

dataset['dia_semana'] = dataset['data_venda'].dt.day_name()

vendas_por_dia = dataset.groupby('dia_semana', as_index=False)['valor_vendas'].sum()
vendas_por_dia['dia_semana'] = pd.Categorical(vendas_por_dia['dia_semana'], categories=dias_ordenados, ordered=True)
vendas_por_dia = vendas_por_dia.sort_values('dia_semana')
vendas_por_dia['valor_vendas'] = vendas_por_dia['valor_vendas'].round(2)

plt.figure(figsize=(14, 6))
sbn.heatmap(vendas_por_dia.pivot_table(index='dia_semana', values='valor_vendas'),annot=True,cmap='coolwarm',fmt=".2f",linewidths=0.5,cbar_kws={'format': '%.0f'})
plt.title("Mapa de Calor - Vendas por Dia da Semana", fontsize=18)
plt.xlabel("Dia da Semana", fontsize=14)
plt.ylabel("")
plt.xticks(rotation=0)  
plt.show()



