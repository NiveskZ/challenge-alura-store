#%%
import pandas as pd

url = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_1.csv"
url2 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_2.csv"
url3 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_3.csv"
url4 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_4.csv"

loja1 = pd.read_csv(url)
loja2 = pd.read_csv(url2)
loja3 = pd.read_csv(url3)
loja4 = pd.read_csv(url4)

lojas = [loja1,loja2,loja3,loja4]
lojas_nomes = ['Loja 1', 'Loja 2', 'Loja 3', 'Loja 4']

loja1.head()
# %%
# Análise do faturamento
faturamentos = [loja['Preço'].sum() for loja in lojas]
for i,faturamento in enumerate(faturamentos,start=1):
    print(f"Faturamento total da loja {i}: R$ {faturamento:,.2f}")
# %%
# Vendas por categoria
venda_categoria = {}
for i, loja in enumerate(lojas,start=1):
    venda_categoria[f'loja{i}'] = loja.groupby("Categoria do Produto").size()
venda_categoria_df = pd.DataFrame(venda_categoria)
venda_categoria_df

# %%
# Média de Avaliação por loja
media_avaliacao = [loja['Avaliação da compra'].mean() for loja in lojas]
for i, media in enumerate(media_avaliacao,start=1):
    print(f"Média de avaliação da loja {i}: {media:.2f}")

# %%
# Produtos Mais e Menos Vendidos
mais_vendido = {}
menos_vendido = {}

for i, loja in enumerate(lojas,start=1):
    contagem = loja['Produto'].value_counts()
    
    max_vendas = contagem.iloc[0]
    min_vendas = contagem.iloc[-1]

    mais = contagem[contagem == max_vendas].index.to_list()
    menos = contagem[contagem == min_vendas].index.to_list()

    mais_vendido[f'loja {i}'] = mais, max_vendas
    menos_vendido[f'loja {i}'] = menos, min_vendas

for loja in mais_vendido:

    produtos_mais, qtd_mais = mais_vendido[loja]
    produtos_menos,qtd_menos = menos_vendido[loja]

    print(f"Na {loja}, o(s) produto(s) mais vendido(s): {produtos_mais},com {qtd_mais} unidades vendidas.\n Já o(s) menos vendido(s): {produtos_menos}, com {qtd_menos} unidades.\n")
#%%
# Receita dos produtos mais vendidos
for i,loja in enumerate(lojas):
    vendas = loja.groupby(['Produto'])['Preço'].sum()
    vendas = vendas.sort_values(ascending=False)
    for j in range(len(mais_vendido[f'loja {i+1}'][0])):
        produto = mais_vendido[f'loja {i+1}'][0][j]
        receita = vendas.loc[produto]
        print(f'receita loja {i+1} {produto}:R$ {receita}')
    
# %%
# Frete Médio por Loja

frete_medio = {}

for i, loja in enumerate(lojas,start=1):
    frete_medio[f'loja {i}'] = round(loja["Frete"].mean(),2)
pd.Series(frete_medio)
# %%
# Visualização através de gráficos
import matplotlib.pyplot as plt
# %%
# Gráfico de barras de faturamento por loja e frete médio por loja
df_frete_medio = pd.Series(frete_medio)
fretes = df_frete_medio.values.tolist()

fig, axs = plt.subplots(1,2,figsize=(15,5))
fig.subplots_adjust(hspace=0.5,wspace=0.3)
fig.suptitle('Gráficos de barra de Faturamento e Frete médio por loja')

axs[0].barh(lojas_nomes,faturamentos)
axs[0].set_title('Faturamento por loja')
axs[0].set_xlabel('Faturamento')
axs[0].ticklabel_format(style='plain',axis='x')
axs[0].tick_params('x',rotation=30)

axs[1].barh(lojas_nomes,fretes)
axs[1].set_title('Frete médio por loja')
axs[1].set_xlabel('Frete médio')

for ax in axs.flat:
    ax.invert_yaxis()
    ax.set_ylabel('Lojas')

plt.show()
# %%
# Gráfico de linhas para verificar tendência de venda por categoria em cada loja
categorias = venda_categoria_df.index.tolist()

fig, ax = plt.subplots(figsize=(10,6))
fig.suptitle('Unidades vendidas por categoria')

ax.plot(categorias,venda_categoria['loja1'],label='Loja 1')
ax.plot(categorias,venda_categoria['loja2'],label='Loja 2')
ax.plot(categorias,venda_categoria['loja3'],label='Loja 3')
ax.plot(categorias,venda_categoria['loja4'],label='Loja 4')

ax.legend()
ax.tick_params('x',rotation=50)
ax.set_xlabel('Categoria')
ax.set_ylabel('Unidades vendidas')

plt.show()
# %%
for loja in lojas:
    loja['Data da Compra'] = pd.to_datetime(loja['Data da Compra'],dayfirst=True)
# %%
soma_receita = []
for loja in lojas:
    soma_receita.append(loja.groupby(['Data da Compra'])['Preço'].sum())

# %%
fig, ax = plt.subplots(figsize=(10,6))

ax.set_title('Receita diária ao longo do tempo')

ax.scatter(soma_receita[0].index.tolist(),soma_receita[0].values.tolist(), label='Loja 1')
ax.scatter(soma_receita[1].index.tolist(),soma_receita[1].values.tolist(), label='Loja 2')
ax.scatter(soma_receita[2].index.tolist(),soma_receita[2].values.tolist(), label='Loja 3')
ax.scatter(soma_receita[3].index.tolist(),soma_receita[3].values.tolist(), label='Loja 4')

ax.set_xlabel('Data')
ax.set_ylabel('Receita')

ax.legend()
ax.grid()

# %%
fig, axs = plt.subplots(2,2,figsize=(10,6))
fig.subplots_adjust(hspace=0.6,wspace=0.3)
fig.suptitle('Distribuição da receita em número de dias')

axs[0,0].hist(soma_receita[0])
axs[0,0].set_title('Loja 1')

axs[0,1].hist(soma_receita[1])
axs[0,1].set_title('Loja 2')

axs[1,0].hist(soma_receita[2])
axs[1,0].set_title('Loja 3')

axs[1,1].hist(soma_receita[3])
axs[1,1].set_title('Loja 4')

for ax in axs.flat:
    ax.set_xlabel('Receita')
    ax.set_ylabel('Número de Dias')
    ax.tick_params('x',rotation=50)
    ax.grid()

xmax = 12000
ymax = 600
for ax in axs.ravel():
    ax.set_xlim(0,xmax)
    ax.set_ylim(0,ymax)
plt.show()
# %%
fig, axs = plt.subplots(2,2,figsize=(10,6))
fig.subplots_adjust(hspace=0.4,wspace=0.2)

imgs = []

imgs.append(axs[0, 0].hist2d(loja1['lon'], loja1['lat'], cmap='plasma')[3])
imgs.append(axs[0, 1].hist2d(loja2['lon'], loja2['lat'], cmap='plasma')[3])
imgs.append(axs[1, 0].hist2d(loja3['lon'], loja3['lat'], cmap='plasma')[3])
imgs.append(axs[1, 1].hist2d(loja4['lon'], loja4['lat'], cmap='plasma')[3])

for i, ax in enumerate(axs.flat):
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title(f'Loja {i+1}')
    ax.axis('equal')
    ax.grid()

cbar = fig.colorbar(imgs[0], ax=axs, orientation='vertical', shrink=0.8, label='Número de Vendas')
plt.show()
# %%
