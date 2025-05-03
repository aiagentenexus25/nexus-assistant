# nexus-assistant
Educational Version of an IA Assistant
# NEXUS - Assistente de Comunicação de Projetos

NEXUS é um assistente de IA especializado em comunicação de projetos, projetado para ajudar gerentes de projetos, líderes de equipe e outros profissionais a comunicar-se de forma clara, eficaz e profissional.

## Funcionalidades Principais

### 1. Gerador de Comunicações Estruturadas
* **Gera e-mails profissionais**: Transforma pontos-chave em e-mails bem estruturados para equipes, clientes e stakeholders
* **Cria relatórios de status**: Produz atualizações de progresso de projetos em formato adequado
* **Elabora comunicados formais**: Formata anúncios importantes como mudanças de escopo ou cronograma

### 2. Assistente de Reuniões
* **Gera agendas detalhadas**: Cria estruturas de reuniões com tópicos, tempo e responsáveis
* **Produz atas e resumos**: Formata documentação pós-reunião com decisões e pontos de ação
* **Estrutura follow-ups**: Ajuda a criar comunicações de acompanhamento após reuniões

### 3. Tradutor de Jargão Técnico
* **Simplifica linguagem técnica**: Converte termos e conceitos técnicos em linguagem acessível
* **Adapta comunicações para diferentes públicos**: Reformula a mesma informação para diferentes stakeholders (executivos, clientes, equipe técnica)
* **Traduz requisitos técnicos**: Ajuda a explicar conceitos complexos em termos mais simples

### 4. Facilitador de Feedback
* **Estrutura feedback construtivo**: Ajuda gerentes a formular feedback equilibrado e específico
* **Transforma críticas em sugestões**: Reformula críticas para focar em soluções construtivas
* **Cria roteiros de conversas difíceis**: Prepara estruturas para discussões delicadas com equipes

### 5. Detector de Riscos de Comunicação
* **Analisa comunicações importantes**: Identifica potenciais problemas, ambiguidades ou mal-entendidos
* **Sugere alternativas mais claras**: Propõe reformulações para reduzir riscos de interpretação errada
* **Avalia adequação ao público**: Verifica se a linguagem e tom são apropriados para o destinatário

## Requisitos

- Python 3.8 ou superior
- Streamlit
- Chave API da OpenAI (formatos sk-proj-, sk-svca- ou sk-)
- Outras dependências listadas em requirements.txt

## Instalação

1. Clone este repositório:
```
git clone https://github.com/seu-usuario/nexus-assistant.git
cd nexus-assistant
```

2. Instale as dependências:
```
pip install -r requirements.txt
```

3. Execute a aplicação:
```
streamlit run app.py
```

## Uso

1. Acesse a aplicação em seu navegador (geralmente em http://localhost:8501)
2. Insira sua chave API da OpenAI na barra lateral
3. Selecione a funcionalidade desejada
4. Preencha os campos específicos para sua necessidade
5. Clique no botão "Gerar" para criar o conteúdo
6. Baixe o resultado como texto ou documento Word

## Como funciona na prática?

1. **Interface simples**: O usuário acessa o aplicativo através de uma interface web criada com Streamlit
2. **Seleção de função**: Escolhe qual das cinco funcionalidades principais deseja utilizar
3. **Entrada de informações**: Preenche campos específicos para cada função (contexto, público-alvo, pontos-chave, etc.)
4. **Processamento pela IA**: O aplicativo faz uma chamada à API da OpenAI para gerar o conteúdo personalizado
5. **Resultado e download**: O usuário recebe o texto formatado e pode baixá-lo ou copiá-lo

## Exemplo concreto

Um gerente de projetos precisa comunicar um atraso de três dias a um cliente importante. Ele:
1. Acessa o NEXUS
2. Seleciona "Gerador de Comunicações"
3. Escolhe o tipo "E-mail"
4. Preenche:
   * Contexto: "Projeto de desenvolvimento do aplicativo mobile, fase de testes"
   * Público: "Cliente, diretor de marketing da empresa XYZ"
   * Pontos-chave: "Atraso de 3 dias devido a bugs na integração com API de pagamentos; Plano de recuperação com recursos adicionais; Impacto mínimo no prazo final"
5. Clica em "Gerar Comunicação"
6. Recebe um e-mail profissional, equilibrado, que comunica o problema de forma transparente mas construtiva, preservando a relação com o cliente

## Notas sobre limites de uso

Para controlar custos e garantir disponibilidade para todos os usuários, o NEXUS inclui:
- Limite de solicitações por sessão
- Limite de tokens utilizados por sessão
- Rastreamento de uso para transparência

## Implantação

Este projeto pode ser facilmente implantado no Streamlit Community Cloud:

1. Faça fork deste repositório no GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Configure um novo aplicativo usando o repositório
4. Adicione sua API key como segredo nas configurações avançadas
5. Implante e compartilhe com sua equipe

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## Créditos

Desenvolvido com Streamlit e API da OpenAI.
Elaborado por [Ricardo Brigante]
