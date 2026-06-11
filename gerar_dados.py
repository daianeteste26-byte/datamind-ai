import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuração
np.random.seed(42)
random.seed(42)
num_registros = 1000

# Listas de dados fictícios
produtos = [
    "Notebook Dell", "Mouse Logitech", "Teclado Mecânico", "Monitor LG 24",
    "Headset HyperX", "Webcam Logitech", "SSD Kingston 480GB", "Cadeira Gamer",
    "Mousepad RGB", "Hub USB", "Carregador USB-C", "Cabo HDMI"
]

categorias_map = {
    "Notebook Dell": "Informática", "Mouse Logitech": "Periféricos",
    "Teclado Mecânico": "Periféricos", "Monitor LG 24": "Informática",
    "Headset HyperX": "Áudio", "Webcam Logitech": "Periféricos",
    "SSD Kingston 480GB": "Armazenamento", "Cadeira Gamer": "Móveis",
    "Mousepad RGB": "Acessórios", "Hub USB": "Acessórios",
    "Carregador USB-C": "Acessórios", "Cabo HDMI": "Acessórios"
}

lojas = ["Loja Centro", "Loja Shopping", "Loja Online", "Loja Norte", "Loja Sul"]
vendedores = ["Ana Silva", "Carlos Souza", "Mariana Costa", "João Pereira", "Beatriz Lima"]
formas_pagamento = ["Cartão de Crédito", "PIX", "Boleto", "Dinheiro", "Cartão de Débito"]
regioes = ["Sudeste", "Sul", "Nordeste", "Norte", "Centro-Oeste"]

# Gerar dados
dados = []
data_inicial = datetime(2024, 1, 1)
data_final = datetime(2026, 6, 10)

for i in range(1, num_registros + 1):
    produto = random.choice(produtos)
    categoria = categorias_map[produto]
    quantidade = random.randint(1, 10)
    preco_unitario = round(random.uniform(50, 3500), 2)
    valor_total = round(quantidade * preco_unitario, 2)
    dias_aleatorios = random.randint(0, (data_final - data_inicial).days)
    data_venda = data_inicial + timedelta(days=dias_aleatorios)
    
    dados.append({
        "ID_Venda": f"V{i:05d}",
        "SKU": f"SKU-{random.randint(1000, 9999)}",
        "Data": data_venda,
        "Produto": produto,
        "Categoria": categoria,
        "Quantidade": quantidade,
        "Preco_Unitario": preco_unitario,
        "Valor_Total": valor_total,
        "Loja": random.choice(lojas),
        "Vendedor": random.choice(vendedores),
        "Forma_Pagamento": random.choice(formas_pagamento),
        "Regiao": random.choice(regioes)
    })

# Criar DataFrame e salvar
df = pd.DataFrame(dados)
df.to_excel("vendas.xlsx", index=False)

print(f"✅ Arquivo 'vendas.xlsx' criado com {len(df)} registros!")
print(f"📊 Colunas: {list(df.columns)}")
print(df.head())
