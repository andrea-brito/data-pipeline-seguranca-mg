import pandas as pd
import duckdb

print("--- CONSTRUINDO A CAMADA SILVER (MÉTODO ULTRA ROBUSTO) ---")

try:
    # 1. Lendo os arquivos
    df_2018 = pd.read_csv('minas_gerais_2018.csv', sep=None, engine='python', encoding='latin-1', on_bad_lines='skip')
    df_2023 = pd.read_csv('minas_gerais_2023.csv', sep=None, engine='python', encoding='utf-8', on_bad_lines='skip')
    
    # 2. Forçando a limpeza dos espaços em branco de todas as colunas
    df_2018.columns = df_2018.columns.str.strip()
    df_2023.columns = df_2023.columns.str.strip()
    
    # 3. O PULO DO GATO: Não importa o nome da 1ª coluna, nós rebatizamos para 'municipio_cod'
    df_2018.rename(columns={df_2018.columns[0]: 'municipio_cod'}, inplace=True)
    df_2023.rename(columns={df_2023.columns[0]: 'municipio_cod'}, inplace=True)
    
    # 4. Tratando a coluna de crime que falta em 2018
    if 'natureza_delito' not in df_2018.columns:
        df_2018['natureza_delito'] = 'FEMINICÍDIO'
        
    # 5. Selecionando exatamente as colunas necessárias para o projeto
    colunas_projeto = [
        'municipio_cod', 'municipio_fato', 'data_fato', 
        'mes', 'ano', 'risp', 'rmbh', 'natureza_delito', 
        'tentado_consumado', 'qtde_vitimas'
    ]
    
    # Filtra e padroniza
    df_2018_estruturado = df_2018[colunas_projeto].copy()
    df_2023_estruturado = df_2023[colunas_projeto].copy()
    
    # 6. Junta tudo na memória
    df_silver_pandas = pd.concat([df_2018_estruturado, df_2023_estruturado], ignore_index=True)
    
    # Altera o nome final da coluna ID para a camada Silver
    df_silver_pandas = df_silver_pandas.rename(columns={'municipio_cod': 'municipio_id'})
    
    print(f"⚡ Sucesso! Pandas unificou {len(df_silver_pandas)} linhas.")
    
    # 7. Conecta ao DuckDB para salvar o arquivo Parquet final
    con = duckdb.connect()
    con.execute("CREATE OR REPLACE TABLE violencia_mg_silver AS SELECT * FROM df_silver_pandas")
    con.execute("COPY violencia_mg_silver TO 'violencia_mg_silver.parquet' (FORMAT PARQUET)")
    print("💾 Camada Silver salva com sucesso em 'violencia_mg_silver.parquet'!")
    
    # 8. Exibe a análise agregada na tela
    print("\n--- 📊 ANÁLISE REAL DE VÍTIMAS EM MINAS GERAIS (2018 vs 2023) ---")
    resultado = con.execute("""
        SELECT 
            ano, 
            natureza_delito, 
            SUM(CAST(qtde_vitimas AS INTEGER)) as total_vitimas
        FROM violencia_mg_silver
        GROUP BY ano, natureza_delito
        ORDER BY ano ASC, total_vitimas DESC
    """).df()
    
    print(resultado)

except Exception as e:
    print(f"\n❌ Erro durante a execução: {e}")