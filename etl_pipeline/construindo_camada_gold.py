import duckdb

print("--- CONSTRUINDO A CAMADA GOLD (ESTRUTURANDO INSIGHTS) ---")

try:
    # 1. Conectar ao DuckDB
    con = duckdb.connect()
    
    # Como o ficheiro Parquet já está na pasta, o DuckDB consegue lê-lo diretamente via SQL!
    ficheiro_parquet = "violencia_mg_silver.parquet"
    
    # -------------------------------------------------------------------------
    # QUERY 1: O DESAFIO DA LEI MARIA DA PENHA (Descumprimento por Município)
    # -------------------------------------------------------------------------
    query_maria_da_penha = f"""
        SELECT 
            municipio_fato AS municipio,
            SUM(CAST(qtde_vitimas AS INTEGER)) AS total_descumprimentos
        FROM read_parquet('{ficheiro_parquet}')
        WHERE ano = 2023 
          AND natureza_delito = 'DESCUMPRIMENTO DE MEDIDA PROTETIVA DE URGENCIA'
        GROUP BY municipio_fato
        ORDER BY total_descumprimentos DESC
        LIMIT 10;
    """
    
    ranking_mp = con.execute(query_maria_da_penha).df()
    
    # -------------------------------------------------------------------------
    # QUERY 2: RANKING GERAL DE VIOLÊNCIA DOMÉSTICA POR CIDADE (TOP 10 - 2023)
    # -------------------------------------------------------------------------
    query_ranking_geral = f"""
        SELECT 
            municipio_fato AS municipio,
            rmbh AS regiao_metropolitana_bh,
            SUM(CAST(qtde_vitimas AS INTEGER)) AS total_geral_vitimas
        FROM read_parquet('{ficheiro_parquet}')
        WHERE ano = 2023
        GROUP BY municipio_fato, rmbh
        ORDER BY total_geral_vitimas DESC
        LIMIT 10;
    """
    
    ranking_geral = con.execute(query_ranking_geral).df()
    
    # -------------------------------------------------------------------------
    # EXIBIÇÃO DOS RESULTADOS NO TERMINAL
    # -------------------------------------------------------------------------
    print("\n🚨 TOP 10 CIDADES COM MAIS DESCUMPRIMENTOS DE MEDIDAS PROTETIVAS (2023):")
    print(ranking_mp.to_string(index=False))
    
    print("\n🏆 TOP 10 CIDADES COM MAIOR VOLUME GERAL DE VIOLÊNCIA DOMÉSTICA (2023):")
    print(ranking_geral.to_string(index=False))
    
    # Opcional: Salvar estes rankings para usar num dashboard ou relatório depois
    ranking_mp.to_csv("gold_ranking_maria_da_penha.csv", index=False)
    ranking_geral.to_csv("gold_ranking_geral_municipios.csv", index=False)
    print("\n💾 Tabelas da Camada Gold exportadas com sucesso em CSV para a pasta!")

except Exception as e:
    print(f"\n❌ Erro durante a análise analítica: {e}")