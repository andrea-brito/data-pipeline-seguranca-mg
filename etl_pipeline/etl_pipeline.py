"""
etl_pipeline.py
---------------
Demonstração dos três estágios de um pipeline ETL (Extract, Transform, Load)
aplicado a dados de ocorrências de violência doméstica.

Estágios:
    1. Extract  — simula a ingestão de dados brutos de uma API governamental.
    2. Transform — padroniza textos, trata valores ausentes e renomeia campos.
    3. Load      — persiste os dados limpos em um arquivo JSON estruturado.

Uso:
    python etl_pipeline.py
"""

import json
import logging
from typing import Optional

# ---------------------------------------------------------------------------
# Configuração de logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Tipos
# ---------------------------------------------------------------------------
RawRecord = dict[str, str | int]
CleanRecord = dict[str, str | int | None]


# ---------------------------------------------------------------------------
# 1. EXTRACT
# ---------------------------------------------------------------------------
def extract() -> list[RawRecord]:
    """
    Simula a extração de dados brutos de uma API governamental.

    Em produção, esta função faria uma requisição HTTP ao endpoint da SEJUSP-MG
    e retornaria os registros desserializados.

    Returns:
        Lista de dicionários com os dados brutos, sem nenhum tratamento.
    """
    raw_data: list[RawRecord] = [
        {
            "id": 1,
            "data": "2026-05-10",
            "tipo_agressao": "física",
            "bairro_vitima": "Centro",
            "idade_vitima": "28",
        },
        {
            "id": 2,
            "data": "2026-05-11",
            "tipo_agressao": "psicológica",
            "bairro_vitima": "centro",
            "idade_vitima": "34",
        },
        {
            "id": 3,
            "data": "2026-05-12",
            "tipo_agressao": "FÍSICA",
            "bairro_vitima": "Zona Sul",
            "idade_vitima": "N/A",  # valor ausente intencional para demonstração
        },
    ]

    logger.info("Extract concluído — %d registros brutos carregados.", len(raw_data))
    return raw_data


# ---------------------------------------------------------------------------
# 2. TRANSFORM
# ---------------------------------------------------------------------------
def _parse_age(value: str) -> Optional[int]:
    """
    Converte uma string de idade para inteiro, retornando None para valores inválidos.

    Args:
        value: String representando a idade (ex.: "28", "N/A").

    Returns:
        Inteiro com a idade ou None se o valor não for conversível.
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def transform(raw_records: list[RawRecord]) -> list[CleanRecord]:
    """
    Aplica as regras de limpeza e padronização sobre os registros brutos.

    Regras aplicadas:
        - Campos de texto são normalizados para maiúsculas sem espaços extras.
        - Idades inválidas (ex.: "N/A") são convertidas para None.
        - Os campos são renomeados para o esquema canônico do projeto.

    Args:
        raw_records: Lista de registros brutos retornados por extract().

    Returns:
        Lista de registros limpos e padronizados.
    """
    clean_records: list[CleanRecord] = []

    for record in raw_records:
        clean_record: CleanRecord = {
            "id": record["id"],
            "data_ocorrencia": record["data"],
            "tipo_violencia": str(record["tipo_agressao"]).upper().strip(),
            "bairro": str(record["bairro_vitima"]).upper().strip(),
            "idade_vitima": _parse_age(str(record["idade_vitima"])),
        }
        clean_records.append(clean_record)

    nulls = sum(1 for r in clean_records if r["idade_vitima"] is None)
    logger.info(
        "Transform concluído — %d registros processados, %d com idade ausente.",
        len(clean_records),
        nulls,
    )
    return clean_records


# ---------------------------------------------------------------------------
# 3. LOAD
# ---------------------------------------------------------------------------
def load(records: list[CleanRecord], output_path: str = "dados_prontos_para_analise.json") -> None:
    """
    Persiste os registros transformados em um arquivo JSON.

    Em produção, esta etapa poderia gravar em um banco de dados,
    um data lake (S3/ADLS) ou diretamente em um arquivo Parquet.

    Args:
        records:     Lista de registros limpos a serem gravados.
        output_path: Caminho do arquivo de saída (padrão: dados_prontos_para_analise.json).
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4, ensure_ascii=False)

    logger.info("Load concluído — dados gravados em '%s'.", output_path)


# ---------------------------------------------------------------------------
# Orquestrador
# ---------------------------------------------------------------------------
def run_pipeline() -> None:
    """Executa o pipeline ETL completo: Extract → Transform → Load."""
    logger.info("Iniciando pipeline ETL.")
    raw = extract()
    clean = transform(raw)
    load(clean)
    logger.info("Pipeline ETL finalizado com sucesso.")


if __name__ == "__main__":
    run_pipeline()
