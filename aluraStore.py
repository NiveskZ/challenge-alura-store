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

    print(f"Na {loja}, o(s) produto(s) mais vendido(s): {produtos_mais},com {qtd_mais} unidades vendidas. Já o(s) menos vendido(s): {produtos_menos}, com {qtd_menos} unidades.")


# %%
# Frete Médio por Loja

frete_medio = {}

for i, loja in enumerate(lojas,start=1):
    frete_medio[f'loja {i}'] = round(loja["Frete"].mean(),2)
pd.Series(frete_medio)
# %%
