import requests

def consultar_cep(cep):
    """
    Consulta um CEP na API ViaCEP e retorna um dicionário padronizado
    com o resultado da consulta (sucesso ou erro).
    """
    url = f"https://viacep.com.br/ws/{cep}/json/"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        return {
            "entrada": cep,
            "status": "erro_comunicacao",
            "mensagem_erro": "Timeout ao tentar acessar a API."
        }
    except requests.exceptions.ConnectionError:
        return {
            "entrada": cep,
            "status": "erro_comunicacao",
            "mensagem_erro": "Falha de conexão com a API."
        }
    except requests.exceptions.RequestException as e:
        return {
            "entrada": cep,
            "status": "erro_comunicacao",
            "mensagem_erro": f"Erro inesperado na requisição: {e}"
        }

    if response.status_code != 200:
        return {
            "entrada": cep,
            "status": "erro_comunicacao",
            "mensagem_erro": f"Status HTTP inesperado: {response.status_code}"
        }

    dados = response.json()

    if dados.get("erro"):
        return {
            "entrada": cep,
            "status": "nao_encontrado",
            "mensagem_erro": "CEP não encontrado na base de dados."
        }

    return {
        "entrada": cep,
        "status": "sucesso",
        "cep": dados.get("cep"),
        "logradouro": dados.get("logradouro"),
        "bairro": dados.get("bairro"),
        "localidade": dados.get("localidade"),
        "uf": dados.get("uf"),
        "mensagem_erro": ""
    }