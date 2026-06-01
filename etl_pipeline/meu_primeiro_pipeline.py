# ==========================================
# CONCEITO 1: EXTRAIR (Pegando os dados brutos)
# No mundo real, isso viria de uma API do governo
# ==========================================
dados_brutos_da_api = [
    {"id": 1, "data": "2026-05-10", "tipo_agressao": "física", "bairro_vitima": "Centro", "idade_vitima": "28"},
    {"id": 2, "data": "2026-05-11", "tipo_agressao": "psicológica", "bairro_vitima": "centro", "idade_vitima": "34"},
    {"id": 3, "data": "2026-05-12", "tipo_agressao": "FÍSICA", "bairro_vitima": "Zona Sul", "idade_vitima": "N/A"}, # Dado com erro (N/A)
]

print("--- FASE 1: Dados brutos extraídos com sucesso! ---")


# ==========================================
# CONCEITO 2: TRANSFORMAR (Limpando a bagunça)
# Engenheiros de dados corrigem erros de digitação e padronizam textos
# ==========================================
dados_limpos = []

for ocorrencia in dados_brutos_da_api:
    # 1. Padronizar o texto para letras maiúsculas (evita ter 'física', 'centro' e 'FÍSICA' separados)
    tipo_limpo = ocorrencia["tipo_agressao"].upper().strip()
    bairro_limpo = ocorrencia["bairro_vitima"].upper().strip()
    
    # 2. Tratar dados ausentes ou com erro (Idade)
    idade = ocorrencia["idade_vitima"]
    if idade == "N/A":
        idade_limpa = None # No Python, 'None' é o equivalente ao 'null' do JavaScript
    else:
        idade_limpa = int(idade) # Transforma o texto '28' em número 28
        
    # Criando o novo registro limpinho
    registro_transformado = {
        "id": ocorrencia["id"],
        "data_ocorrencia": ocorrencia["data"],
        "tipo_violencia": tipo_limpo,
        "bairro": bairro_limpo,
        "idade_vitima": idade_limpa
    }
    dados_limpos.append(registro_transformado)

print("\n--- FASE 2: Dados transformados e padronizados! ---")
print(dados_limpos)


# ==========================================
# CONCEITO 3: CARREGAR (Salvar para o analista ver)
# Vamos salvar isso em um arquivo final organizado
# ==========================================
import json

with open("dados_prontos_para_analise.json", "w", encoding="utf-8") as arquivo_final:
    json.dump(dados_limpos, arquivo_final, indent=4, ensure_ascii=False)

print("\n--- FASE 3: Dados carregados no arquivo final! Pipeline concluído. ---")