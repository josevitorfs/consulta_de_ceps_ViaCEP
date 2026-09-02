import requests

def consultar_cep(cep):
    """
    Consulta um CEP na API ViaCEP e retorna um dicionário padronizado
    com o resultado da consulta (sucesso ou erro).
    """
    cep_limpo = cep.replace("-", "").strip()

    if not validar_formato(cep_limpo):
        return {
            "entrada": cep,
            "status": "formato_invalido",
            "cep": "",
            "logradouro": "",
            "bairro": "",
            "localidade": "",
            "uf": "",
            "mensagem_erro": "Formato de CEP inválido (esperado 8 dígitos numéricos)."
        }

    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.Timeout:
        return {
            "entrada": cep, "status": "erro_comunicacao", "cep": "",
            "logradouro": "", "bairro": "", "localidade": "", "uf": "",
            "mensagem_erro": "Timeout ao tentar acessar a API."
        }
    except requests.exceptions.ConnectionError:
        return {
            "entrada": cep, "status": "erro_comunicacao", "cep": "",
            "logradouro": "", "bairro": "", "localidade": "", "uf": "",
            "mensagem_erro": "Falha de conexão com a API."
        }
    except requests.exceptions.RequestException as e:
        return {
            "entrada": cep, "status": "erro_comunicacao", "cep": "",
            "logradouro": "", "bairro": "", "localidade": "", "uf": "",
            "mensagem_erro": f"Erro inesperado na requisição: {e}"
        }

    if response.status_code != 200:
        return {
            "entrada": cep, "status": "erro_comunicacao", "cep": "",
            "logradouro": "", "bairro": "", "localidade": "", "uf": "",
            "mensagem_erro": f"Status HTTP inesperado: {response.status_code}"
        }

    dados = response.json()

    if dados.get("erro"):
        return {
            "entrada": cep, "status": "nao_encontrado", "cep": "",
            "logradouro": "", "bairro": "", "localidade": "", "uf": "",
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

def validar_formato(cep):
    """
    Verifica se o CEP tem exatamente 8 dígitos numéricos.
    Aceita entradas com ou sem hífen (ex.: "01001-000" ou "01001000").
    """
    cep_limpo = cep.replace("-", "").strip()
    return cep_limpo.isdigit() and len(cep_limpo) == 8


def processar_entradas(entradas):
    """
    Processa uma lista de CEPs, chamando consultar_cep para cada um.
    Nenhuma exceção interrompe o loop: cada resultado (sucesso ou erro)
    é adicionado à lista final.
    """
    resultados = []
    for entrada in entradas:
        resultado = consultar_cep(entrada)
        resultados.append(resultado)
    return resultados

entradas = ["01001000","20040020","30130010","70150900","80010000","ABC123","123","99999999","01310930","40010000"]

print(processar_entradas(entradas))