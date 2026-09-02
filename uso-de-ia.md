# Técnicas de Engenharia de Prompt Utilizadas Nesta Conversa

Este documento identifica e explica as técnicas de engenharia de prompt que foram efetivamente aplicadas na condução deste chat (desenvolvimento do script de consulta à API ViaCEP), relacionando-as com os conceitos de Zero-Shot, One-Shot, Few-Shot e Chain-of-Thought.

## 1. Role Prompting (Persona Pattern)

Logo no início da conversa, o prompt definiu um papel específico para a IA:

> "Você atuará como um Engenheiro de Software Sênior, Mentor Técnico e Revisor de Projetos de Programação..."

**Por que isso importa:** atribuir uma persona técnica delimita o vocabulário, o nível de rigor e a postura esperada nas respostas. Isso reduz respostas genéricas e aproxima o comportamento do modelo do de um profissional real, incluindo hábitos como não inventar comportamento de API e diagnosticar erros antes de reescrever código.

Mais adiante, o mesmo prompt define uma **segunda persona** para a etapa final ("revisor de processo seletivo" / recrutador), mostrando uso de **múltiplas personas dentro da mesma conversa**, cada uma ativada em um momento específico do processo.

## 2. Decomposição em Etapas (Task Decomposition)

Em vez de pedir a solução completa em um único prompt, a tarefa foi dividida em etapas sequenciais e nomeadas: Entendimento do Requisito → Planejamento → Entradas → Consulta da API → Tratamento de Erros → CSV → Testes → Revisão → Entrega Final.

**Relação com Chain-of-Thought:** essa técnica é conceitualmente próxima ao Chain-of-Thought, mas aplicada no nível da conversa em vez de dentro de uma única resposta. Assim como o CoT força o modelo a expor passos intermediários de raciocínio antes da resposta final, a decomposição em etapas forçou a solução a passar por estágios intermediários explícitos (requisitos, depois planejamento, depois implementação) antes de chegar ao código final — reduzindo a chance de pular etapas de raciocínio e cometer erros de projeto que só apareceriam depois.

Um exemplo concreto dentro da própria conversa: na Etapa 4, o código foi apresentado primeiro em sua forma mais simples (uma única chamada `requests.get`, sem tratamento de erro), testado, e só depois evoluído passo a passo para a função completa com tratamento de exceções. Isso é decomposição de raciocínio aplicada à escrita de código.

## 3. Restrições Negativas (Negative Constraints / Prompting por Exclusão)

O prompt inicial definiu explicitamente o que **não** deveria ser feito:

> "Não crie: banco de dados; interface gráfica; backend desnecessário; arquitetura exageradamente sofisticada; Docker sem necessidade..."

**Por que funciona:** LLMs tendem a "over-engineer" soluções quando não há limites claros. Restrições negativas explícitas ajudam a manter o escopo da solução proporcional à tarefa, evitando que o modelo demonstre conhecimento técnico de forma desnecessária (um risco comum em respostas de IA que tentam parecer mais sofisticadas do que o problema exige).

## 4. Especificação de Formato de Saída (Output Structuring)

Vários pontos do prompt definiram exatamente como as respostas deveriam ser estruturadas: uma tabela com colunas específicas para o CSV, uma estrutura de arquivos fixa, um checklist de requisitos, notas de 0 a 10 em critérios nomeados na entrega final.

**Efeito prático:** isso reduz ambiguidade sobre o que conta como "resposta completa" e permite validação objetiva (por exemplo, comparar diretamente o CSV gerado com as colunas exigidas).

## 5. Grounding / Verificação em Fonte Externa

Antes de assumir o comportamento da API ViaCEP (como ela sinaliza CEP inexistente, se valida formato no servidor etc.), foi feita uma busca ativa na documentação oficial, em vez de responder apenas com base em conhecimento prévio.

**Relação com boas práticas de prompting:** isso é uma aplicação do princípio de **grounding** — instruir explicitamente o modelo a não inventar comportamento e a checar fontes primárias antes de codificar suposições, o que reduz alucinação sobre APIs externas (um erro comum quando o modelo assume que uma API funciona "como a maioria das APIs REST costuma funcionar").

## 6. Recontextualização Incremental (Context Anchoring)

A cada nova etapa, foi solicitado explicitamente que as etapas anteriores fossem recapituladas antes de prosseguir ("recontextualiza as etapas 1 e 2 antes de seguir para a 3").

**Por que isso é uma técnica válida de engenharia de prompt:** em conversas longas, o modelo pode perder precisão sobre decisões tomadas muitas mensagens atrás. Pedir recapitulação explícita antes de cada etapa funciona como uma verificação de consistência (o modelo precisa demonstrar que ainda "sabe" o que foi decidido) e também serve como uma auditoria para o usuário confirmar que nada foi esquecido ou alterado silenciosamente — sem depender de o modelo lembrar espontaneamente.

## 7. Validação Incremental com Humano no Loop (Human-in-the-Loop Verification)

O prompt exigiu, em várias etapas, que o código fosse testado por quem estava conduzindo a conversa antes de a IA prosseguir para a etapa seguinte (por exemplo: rodar a consulta simples da Etapa 4 antes de evoluir para a função completa).

**Por que isso importa:** evita que erros se acumulem silenciosamente em camadas de código construídas sobre suposições não verificadas. Também é coerente com a regra explícita de "não inventar resultados de execução" — como a IA não tinha acesso de rede ao domínio da API neste ambiente, a validação humana em cada etapa era a única forma confiável de confirmar o comportamento real.

## 8. Prompting por Critérios de Aceitação (Acceptance Criteria / Checklist Prompting)

A seção "Critério de Conclusão" do prompt original define uma lista de condições objetivas que precisam ser todas verdadeiras para a tarefa ser considerada concluída (10 entradas processadas, erros registrados, CSV correto, etc.).

**Efeito:** transforma "faça um bom projeto" (vago) em uma lista de condições verificáveis, permitindo que tanto o usuário quanto a IA confirmem objetivamente o progresso, em vez de depender de uma avaliação subjetiva de qualidade.

---

## Relação com os conceitos de Zero-Shot, One-Shot, Few-Shot e Chain-of-Thought

Nenhuma dessas técnicas clássicas foi usada em sua forma "pura" nesta conversa (não houve, por exemplo, exemplos de entrada/saída fornecidos previamente como em Few-Shot). Ainda assim, há uma relação direta:

- A **decomposição em etapas** é o análogo, em escala de conversa, ao raciocínio passo a passo do **Chain-of-Thought**: em vez de pedir a resposta final de imediato (o que seria mais próximo de um prompt Zero-Shot para a tarefa inteira), o processo foi construído expondo cada etapa de raciocínio — requisitos, depois planejamento, depois implementação — antes de chegar ao resultado final.
- A lista de 10 entradas definida na Etapa 3, com exemplos explícitos de cada categoria (válido, inválido, inexistente), funciona de forma semelhante a exemplos em um prompt **Few-Shot**: eles não ensinam o modelo a gerar texto, mas servem como casos de referência que ancoram o comportamento esperado do código em cada cenário.

## Conclusão

A engenharia de prompt usada nesta conversa não se apoiou em uma única técnica isolada, mas em uma combinação: persona técnica definida, decomposição do problema em etapas verificáveis (análoga ao raciocínio passo a passo do Chain-of-Thought), restrições negativas para conter o escopo, formato de saída especificado, grounding em documentação oficial, recontextualização periódica para evitar perda de contexto, e validação humana incremental a cada etapa antes de avançar. Essa combinação é o que permitiu construir a solução de forma gradual, rastreável e sem resultados inventados.