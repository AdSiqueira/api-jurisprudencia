from fastapi import FastAPI, Query
import requests

app = FastAPI()

def buscar_jurisprudencia_stj(termo):
    url = "https://www.stj.jus.br/api/jurisprudencia"
    params = {"query": termo, "pagina": 1, "tamanhoPagina": 5}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Verifica se há erro HTTP
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"erro": f"Erro ao buscar no STJ: {str(e)}"}

def buscar_jurisprudencia_stf(termo):
    url = "https://dadosabertos.stf.jus.br/api/jurisprudencia"
    params = {"termo": termo, "pagina": 1, "tamanhoPagina": 5}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"erro": f"Erro ao buscar no STF: {str(e)}"}

@app.get("/jurisprudencia")
def obter_jurisprudencia(termo: str = Query(..., description="Termo de busca")):
    resultado_stj = buscar_jurisprudencia_stj(termo)
    resultado_stf = buscar_jurisprudencia_stf(termo)
    return {"STJ": resultado_stj, "STF": resultado_stf}
