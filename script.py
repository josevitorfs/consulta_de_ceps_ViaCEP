import requests
import csv


def validar_formato(cep):
    cep_limpo = cep.replace("-", "").strip()
    return cep_limpo.isdigit() and len(cep_limpo) == 8


def consultar_cep(cep):
    cep_limpo = cep.replace("-", "").strip()

    if not validar_formato(cep_limpo):
        return {
            "entrada": cep, "status": "formato_invalido", "cep": "",
            "logradouro": "", "bairro": "", "localidade": "", "uf": "",
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


def processar_entradas(entradas):
    resultados = []
    for entrada in entradas:
        resultado = consultar_cep(entrada)
        resultados.append(resultado)
    return resultados


def ler_entradas(caminho):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        linhas = [linha.strip() for linha in arquivo.readlines()]
    return [linha for linha in linhas if linha]


def gerar_csv(resultados, caminho):
    colunas = ["entrada", "status", "cep", "logradouro", "bairro", "localidade", "uf", "mensagem_erro"]

    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(resultados)


def main():
    entradas = ler_entradas("entradas.txt")
    resultados = processar_entradas(entradas)
    gerar_csv(resultados, "resultado.csv")

    total = len(resultados)
    sucesso = sum(1 for r in resultados if r["status"] == "sucesso")
    print(f"Processamento concluído: {total} entradas processadas, {sucesso} com sucesso.")


if __name__ == "__main__":
    main()