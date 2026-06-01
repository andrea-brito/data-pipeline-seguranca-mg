import pandas as pd
import json

# 1. Vamos ler o arquivo JSON limpo que você gerou no passo anterior
with open("dados_prontos_para_analise.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

# 2. A mágica do Pandas: Transforma o JSON em um "DataFrame" (que é o nome técnico para Tabela)
tabela = pd.DataFrame(dados)

# 3. Vamos exibir a tabela na tela
print("--- SUA PRIMEIRA TABELA EM PYTHON ---")
print(tabela)

# 4. Quer ver outra mágica? O Pandas te dá estatísticas automáticas dos dados
print("\n--- ANÁLISE EXPRESSA DOS DADOS ---")
print(f"Idade média das vítimas: {tabela['idade_vitima'].mean()} anos")

# 5. Salvando a tabela no formato padrão dos Engenheiros de Dados (Parquet)
tabela.to_parquet("dados_finais.parquet", index=False)

print("\n--- FASE 4: Arquivo Parquet gerado com sucesso! ---")