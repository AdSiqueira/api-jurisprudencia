from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List
from google.cloud import bigquery

app = FastAPI(title="API de Pesquisa de Decisões do STF")

# Configurações do BigQuery – substitua pelos seus dados
PROJECT_ID = "seu-projeto-gcp"
DATASET_ID = "seu_dataset"       # Ex: "basedosdados"
TABLE_ID = "sua_tabela"          # Ex: "cf7572de-c961-4c53-9b3a-4ef4eb05084c"

client = bigquery.Client(project=PROJECT_ID)

# Modelo de dados para a resposta (ajuste os campos conforme a estrutura da sua tabela)
class Decision(BaseModel):
    id: str
    data_decisao: str
    texto_decisao: str

@app.get("/search", response_model=List[Decision])
async def search_decisions(query: str = Query(..., description="Termo de busca nas decisões")):
    # Construa a query SQL – cuidado com injeção; considere usar parâmetros
    sql = f"""
        SELECT id, data_decisao, texto_decisao
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        WHERE LOWER(texto_decisao) LIKE '%{query.lower()}%'
        LIMIT 10
    """
    try:
        query_job = client.query(sql)
        results = query_job.result()
        decisions = []
        for row in results:
            decisions.append(Decision(
                id=row.id,
                data_decisao=str(row.data_decisao),
                texto_decisao=row.texto_decisao
            ))
        return decisions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Para rodar a API: uvicorn nome_do_arquivo:app --reload
