import pandas as pd

print("--- INVESTIGANDO OS ARQUIVOS REAIS DE MINAS GERAIS ---")

# Investigando o primeiro arquivo (2018)
try:
    # Ajustado para ignorar linhas problemáticas se houver e ler enconding comum do governo
    df1 = pd.read_csv("minas_gerais_2018.csv", sep=None, engine='python', encoding='latin-1', on_bad_lines='skip')
    print(f"\n📊 ARQUIVO 1 (`minas_gerais_2018.csv`):")
    print(f"   Total de linhas: {len(df1)}")
    print("   Colunas encontradas:")
    for col in df1.columns:
        print(f"     - {col}")
except FileNotFoundError:
    print("\n❌ Erro: O arquivo 'minas_gerais_2018.csv' não foi encontrado na pasta.")
except Exception as e:
    print(f"\n❌ Erro ao ler o arquivo 1: {e}")

# Investigando o segundo arquivo (2022)
try:
    df2 = pd.read_csv("minas_gerais_2023.csv", sep=None, engine='python', encoding='latin-1', on_bad_lines='skip')
    print(f"\n📊 ARQUIVO 2 (`minas_gerais_2023.csv`):")
    print(f"   Total de linhas: {len(df2)}")
    print("   Colunas encontradas:")
    for col in df2.columns:
        print(f"     - {col}")
except FileNotFoundError:
    print("\n❌ Erro: O arquivo 'minas_gerais_2023.csv' não foi encontrado na pasta.")
except Exception as e:
    print(f"\n❌ Erro ao ler o arquivo 2: {e}")