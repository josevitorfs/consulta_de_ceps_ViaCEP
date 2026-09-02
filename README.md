# Consulta de CEPs — ViaCEP

Script em Python que consulta uma lista de 10 CEPs na API pública ViaCEP e gera um CSV com os resultados, tratando erros de entrada inválida ou falha de comunicação sem interromper a execução.

## Objetivo

Demonstrar consumo de uma API REST pública, tratamento de erros e geração de um arquivo CSV organizado a partir de uma lista de entradas.

## API utilizada

- **ViaCEP** — API pública e gratuita de consulta de CEPs do Brasil.
- Documentação oficial: https://viacep.com.br
- Endpoint usado: `https://viacep.com.br/ws/{cep}/json/`

## Como funciona

Para cada CEP em `entradas.txt`, o script:

1. Valida o formato localmente (8 dígitos numéricos, com ou sem hífen). A ViaCEP não valida formato no servidor, então essa checagem é feita pelo próprio script antes de qualquer requisição.
2. Se o formato for válido, consulta a API.
3. Interpreta a resposta:
   - **sucesso** — CEP encontrado, dados retornados;
   - **nao_encontrado** — CEP com formato válido, mas inexistente na base (a ViaCEP responde com `{"erro": true}`);
   - **erro_comunicacao** — timeout, falha de conexão ou status HTTP inesperado.
4. Registra o resultado (sucesso ou erro) e segue para a próxima entrada — nenhum erro interrompe o processamento das demais.

Ao final, todos os resultados são gravados em `resultado.csv`, um por linha, na ordem em que foram processados.

## Tecnologias e dependências

- Python 3.8+
- Biblioteca `requests` (única dependência externa)
- Biblioteca padrão `csv`

Instalar a dependência:

```bash
pip install requests
```

## Estrutura de arquivos

```
uso-de-api/
├── script.py        # código principal
├── entradas.txt      # 10 CEPs usados como entrada
├── resultado.csv      # gerado após a execução
├── prompts.txt       # histórico de uso de IA no desenvolvimento
└── README.md
```

## Como executar

1. Certifique-se de ter Python 3.8+ instalado.
2. Instale a dependência:
   ```bash
   pip install requests
   ```
3. Garanta que o arquivo `entradas.txt` está na mesma pasta do `script.py`, com um CEP por linha (10 linhas).
4. Execute:
   ```bash
   python script.py
   ```
5. O arquivo `resultado.csv` será criado (ou sobrescrito) na mesma pasta, e um resumo será exibido no terminal, por exemplo:
   ```
   Processamento concluído: 10 entradas processadas, 7 com sucesso.
   ```

## Tratamento de erros

O script nunca interrompe a execução por causa de uma entrada com problema. Três cenários são tratados explicitamente:

| Cenário | Status no CSV | Exemplo de entrada |
|---|---|---|
| Formato inválido (não numérico ou tamanho incorreto) | `formato_invalido` | `ABC123`, `123` |
| Formato válido, mas CEP inexistente | `nao_encontrado` | `99999999` |
| Timeout, falha de conexão ou status HTTP inesperado | `erro_comunicacao` | (depende da disponibilidade da rede/API no momento) |

Em todos os casos, a entrada permanece registrada no CSV com seu status e, quando aplicável, uma mensagem de erro — nenhuma entrada é descartada silenciosamente.

## Exemplo de saída (`resultado.csv`)

```
entrada,status,cep,logradouro,bairro,localidade,uf,mensagem_erro
01001000,sucesso,01001-000,Praça da Sé,Sé,São Paulo,SP,
ABC123,formato_invalido,,,,,,Formato de CEP inválido (esperado 8 dígitos numéricos).
99999999,nao_encontrado,,,,,,CEP não encontrado na base de dados.
```

## Observações

- As 10 entradas usadas neste exercício foram escolhidas propositalmente para cobrir os três cenários de erro exigidos, além de casos de sucesso.
- O histórico de prompts usados durante o desenvolvimento com apoio de IA está documentado em `prompts.txt`.