import duckdb

# 1. Criamos uma conexão com o DuckDB (ele roda na memória do PC, super leve)
con = duckdb.connect()

print("--- EXECUTANDO CONSULTA SQL NO ARQUIVO PARQUET ---")

# 2. A mágica: No SQL, em vez de passar o nome de uma tabela de banco,
# nós passamos o caminho do arquivo Parquet diretamente!
query_sql = """
    SELECT 
        tipo_violencia,
        COUNT(*) as total_casos,
        AVG(idade_vitima) as idade_media
    FROM 'dados_finais.parquet'
    GROUP BY tipo_violencia
"""

# 3. Executa a query e transforma o resultado de volta em algo fácil de ler
resultado = con.execute(query_sql).df()

print(resultado)