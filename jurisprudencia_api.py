from fastapi import FastAPI, Query
import requests

app = FastAPI()

def buscar_jurisprudencia_stj(termo):
    url = "https://www.stj.jus.br/api/jurisprudencia"
    params = {"query": termo, "pagina": 1, "tamanhoPagina": 5}
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else {"erro": "Erro na busca STJ"}

def buscar_jurisprudencia_stf(termo):
    url = "https://dadosabertos.stf.jus.br/api/jurisprudencia"
    params = {"termo": termo, "pagina": 1, "tamanhoPagina": 5}
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else {"erro": "Erro na busca STF"}

@app.get("/jurisprudencia")
def obter_jurisprudencia(termo: str = Query(..., description="Termo de busca")):
    resultado_stj = buscar_jurisprudencia_stj(termo)
    resultado_stf = buscar_jurisprudencia_stf(termo)
    return {"STJ": resultado_stj, "STF": resultado_stf}
