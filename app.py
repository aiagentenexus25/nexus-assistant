import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import plotly.express as px
import os
import re
import docx
from io import BytesIO
import time

# ================= CONFIGURATION =================

# Configuração da página
st.set_page_config(
    page_title="NEXUS - Assistente de Comunicação de Projetos",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Definindo paleta de cores
nexus_colors = {
    "purple": "#6247AA",
    "orange": "#FF6D2A",
    "teal": "#00C1D5",
    "dark_purple": "#231A41",
    "background": "#F5F5F7",
    "text_primary": "#1D1D1F",
    "text_secondary": "#86868B"
}

st.markdown("""
<style>
    /* Ocultar completamente a sidebar */
    [data-testid="collapsedControl"] {
        display: none;
    }
    section[data-testid="stSidebar"] {
        display: none;
    }
    /* Ajustar a área principal para ocupar toda a largura */
    .main .block-container {
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 1200px;
    }
</style>
""", unsafe_allow_html=True)

# Base de conhecimento sobre PMBOK 7
PMBOK7_KNOWLEDGE_BASE = {
    "princípios": [
        "1. Ser um administrador diligente, respeitoso e cuidadoso",
        "2. Criar um ambiente colaborativo da equipe do projeto",
        "3. Envolver efetivamente as partes interessadas",
        "4. Focar no valor",
        "5. Reconhecer, avaliar e responder às interações do sistema",
        "6. Demonstrar comportamentos de liderança",
        "7. Adaptar com base no contexto",
        "8. Incorporar qualidade nos processos e resultados",
        "9. Navegar na complexidade",
        "10. Otimizar respostas a riscos",
        "11. Abraçar adaptabilidade e resiliência",
        "12. Permitir mudança para alcançar o estado futuro previsto"
    ],
    
    "domínios": [
        "1. Stakeholders (Partes Interessadas)",
        "2. Team (Equipe)",
        "3. Development Approach and Life Cycle (Abordagem de Desenvolvimento e Ciclo de Vida)",
        "4. Planning (Planejamento)",
        "5. Project Work (Trabalho do Projeto)",
        "6. Delivery (Entrega)",
        "7. Measurement (Mensuração)",
        "8. Uncertainty (Incerteza)"
    ],
    
    "metodologias": {
        "preditiva": "Abordagem tradicional (cascata) com fases sequenciais",
        "adaptativa": "Abordagens ágeis e iterativas (Scrum, Kanban, etc.)",
        "híbrida": "Combinação de elementos preditivos e adaptativos"
    },
    
    "mudancas_principais": [
        "1. Transição de processos para princípios e domínios de performance",
        "2. Foco em entrega de valor em vez de apenas escopo, tempo e custo",
        "3. Maior ênfase em adaptabilidade e contexto",
        "4. Abordagem de sistemas em vez de processos isolados",
        "5. Reconhecimento de múltiplas abordagens (adaptativa, preditiva, híbrida)",
        "6. Maior ênfase na liderança e soft skills",
        "7. Visão holística do gerenciamento de projetos"
    ]
}

# Limites ampliados para melhor experiência do usuário
TOKEN_LIMIT = 100000    # Aumentado para permitir interações mais longas
REQUEST_LIMIT = 50      # Aumentado para permitir mais consultas por sessão

# CSS Personalizado
st.markdown("""
<style>
    /* Variáveis de cores */
    :root {
        --purple: #6247AA;
        --orange: #FF6D2A;
        --teal: #00C1D5;
        --dark-purple: #231A41;
        --background: #F5F5F7;
        --text-primary: #1D1D1F;
        --text-secondary: #86868B;
    }

    
    /* Reset e estilos gerais */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'SF Pro Text', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Corpo principal */
    .main {
        background-color: var(--background);
        padding: 1rem;
    }
    
    .stApp {
        background-color: var(--background);
    }
    
    /* Cabeçalho gradiente */
    .header-gradient {
        background: linear-gradient(90deg, var(--purple) 0%, var(--orange) 50%, var(--teal) 100%);
        padding: 1rem 2rem;
        color: white;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Cartões para funcionalidades */
    .card-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .feature-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.2rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        flex: 1;
        min-width: 200px;
        border: 1px solid #E2E8F0;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .card-purple {
        border-left: 4px solid var(--purple);
    }
    
    .card-orange {
        border-left: 4px solid var(--orange);
    }
    
    .card-teal {
        border-left: 4px solid var(--teal);
    }

    /* Formulários */
    .form-container {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .form-title {
        font-size: 1.5rem;
        color: var(--dark-purple);
        margin-bottom: 1rem;
    }
    
    /* Campos de entrada */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        padding: 10px 15px;
        background-color: var(--background);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--purple);
        box-shadow: 0 0 0 2px rgba(98, 71, 170, 0.2);
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        padding: 10px 15px;
        background-color: var(--background);
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--purple);
        box-shadow: 0 0 0 2px rgba(98, 71, 170, 0.2);
    }
    
    /* Botões */
    .button-primary {
        background-color: var(--purple);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
        width: 100%;
        text-align: center;
        display: inline-block;
    }
    
    .button-secondary {
        background-color: #f0f0f0;
        color: var(--text-primary);
        border: 1px solid #ddd;
        border-radius: 50px;
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
        width: 100%;
        text-align: center;
        display: inline-block;
    }
    
    .button-primary:hover {
        filter: brightness(1.1);
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }
    
    .button-secondary:hover {
        background-color: #e0e0e0;
    }
    
    /* Resultado e área de resposta */
    .result-area {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid #E2E8F0;
    }
    
    /* Sidebar */
    .sidebar-content {
        padding: 20px 10px;
    }
    
    /* Métricas e cartões */
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Análise de tom */
    .tone-analysis-section {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        border: 1px solid #E2E8F0;
    }
    
    .tone-current {
        background-color: var(--background);
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    
    .tone-optimized {
        background-color: #F0FFF4;
        padding: 10px;
        border-radius: 5px;
        border-left: 3px solid var(--teal);
    }

    /* Design responsivo */
    @media (max-width: 768px) {
        .header-gradient {
            padding: 1rem;
        }
        
        .feature-card {
            min-width: 100%;
        }
        
        .card-container {
            flex-direction: column;
        }
    }
    
    /* Esconder elementos default do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Estilo aprimorado para o histórico */
    .history-item {
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        background-color: white;
        border: 1px solid #E2E8F0;
    }
    
    .history-item:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Definição de funcionalidades disponíveis (incluindo PMBOK 7)
feature_options = {
    "Gerador de Comunicações Estruturadas": {
        "description": "Crie comunicações profissionais a partir de pontos-chave.",
        "icon": "📧",
        "color": "purple",
        "subtypes": ["E-mail Profissional", "Relatório de Status", "Comunicado Formal"]
    },
    "Assistente de Reuniões": {
        "description": "Gere agendas detalhadas, atas de reuniões e mensagens de follow-up estruturadas.",
        "icon": "📅",
        "color": "orange",
        "subtypes": ["Agenda de Reunião", "Ata/Resumo de Reunião", "Follow-up de Reunião"]
    },
    "Simplificador de Linguagem Técnica": {
        "description": "Simplifique linguagem técnica e adapte comunicações para diferentes públicos.",
        "icon": "🔄",
        "color": "teal",
        "subtypes": ["Simplificação de Documento Técnico", "Adaptação para Executivos", "Adaptação para Clientes", "Adaptação para Equipe Técnica"]
    },
    "Facilitador de Feedback": {
        "description": "Estruture feedback construtivo e prepare roteiros para conversas difíceis.",
        "icon": "💬",
        "color": "purple",
        "subtypes": ["Feedback de Desempenho", "Feedback sobre Entregáveis", "Roteiro para Conversa Difícil"]
    },
    "Detector de Riscos de Comunicação": {
        "description": "Analise comunicações para identificar ambiguidades e problemas potenciais.",
        "icon": "🔍",
        "color": "orange",
        "subtypes": ["Análise de E-mail", "Análise de Comunicado", "Análise de Proposta", "Análise de Documento de Requisitos"]
    },
    "Consultor PMBOK 7": {
        "description": "Esclareça dúvidas sobre gerenciamento de projetos conforme o PMBOK 7.",
        "icon": "📚",
        "color": "teal",
        "subtypes": ["Princípios de Gerenciamento", "Domínios de Performance", "Adaptação de Metodologias", "Ferramentas e Técnicas", "Melhores Práticas"]
    }
}

# ================= SESSION STATE INITIALIZATION =================

# Inicialização da sessão
if 'api_key_configured' not in st.session_state:
    st.session_state.api_key_configured = True
    # Configurar API key automaticamente a partir dos secrets
    if st.secrets.get("OPENAI_API_KEY"):
        st.session_state.api_key = st.secrets.get("OPENAI_API_KEY")
    else:
        st.session_state.api_key = None
        st.session_state.api_key_configured = False

if 'usage_data' not in st.session_state:
    st.session_state.usage_data = []
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = ""
if 'history' not in st.session_state:
    st.session_state.history = []
if 'token_count' not in st.session_state:
    st.session_state.token_count = 0
if 'request_count' not in st.session_state:
    st.session_state.request_count = 0
if 'last_request_time' not in st.session_state:
    st.session_state.last_request_time = 0
if 'session_id' not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%d%H%M%S") + str(hash(datetime.now()))[:5]
if 'current_feature' not in st.session_state:
    st.session_state.current_feature = ""
if 'optimized_content' not in st.session_state:
    st.session_state.optimized_content = ""
if 'previous_screen' not in st.session_state:
    st.session_state.previous_screen = None

# ================= HELPER FUNCTIONS =================

def header():
    """Renderiza o cabeçalho com gradiente apenas com o título NEXUS"""
    
    st.markdown("""
    <div class="header-gradient">
        <h1 style="margin:0; font-weight:600; font-size:32px; color:white;">NEXUS</h1>
        <div style="display: flex; align-items: center;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width:8px; height:8px; border-radius:50%; background:#28C840;"></div>
                <span style="font-size:12px; color:white; opacity:0.9;">API</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def enrich_pmbok_prompt(prompt, pmbok_topic):
    """Enriquece o prompt com informações relevantes do PMBOK 7 baseado no tópico selecionado"""
    
    additional_info = ""
    
    if "Princípios" in pmbok_topic:
        additional_info += "\n\nPrincípios de Gerenciamento do PMBOK 7:\n"
        additional_info += "\n".join(PMBOK7_KNOWLEDGE_BASE["princípios"])
        
    elif "Domínios" in pmbok_topic:
        additional_info += "\n\nDomínios de Performance do PMBOK 7:\n"
        additional_info += "\n".join(PMBOK7_KNOWLEDGE_BASE["domínios"])
        
    elif "Adaptação" in pmbok_topic:
        additional_info += "\n\nAbordagens de Desenvolvimento no PMBOK 7:\n"
        for k, v in PMBOK7_KNOWLEDGE_BASE["metodologias"].items():
            additional_info += f"- {k.capitalize()}: {v}\n"
            
    elif "Melhores Práticas" in pmbok_topic:
        additional_info += "\n\nMudanças Principais no PMBOK 7:\n"
        additional_info += "\n".join([f"- {item}" for item in PMBOK7_KNOWLEDGE_BASE["mudancas_principais"]])
    
    # Adicionar a informação relevante ao prompt
    enhanced_prompt = prompt + additional_info
    return enhanced_prompt

# Função para exportar conteúdo como DOCX
def export_as_docx(content, filename="documento"):
    doc = docx.Document()
    
    # Adicionar título
    doc.add_heading(f"{filename}", 0)
    
    # Dividir por linhas e adicionar parágrafos
    paragraphs = content.split('\n')
    for para in paragraphs:
        if para.strip() == "":
            continue
        
        # Verificar se é um cabeçalho
        if re.match(r'^#{1,6}\s+', para):
            # Extrair o nível do cabeçalho e o texto
            header_match = re.match(r'^(#{1,6})\s+(.*)', para)
            if header_match:
                level = min(len(header_match.group(1)), 9)  # Limitar a 9 para evitar erro
                text = header_match.group(2)
                doc.add_heading(text, level)
        else:
            doc.add_paragraph(para)
    
    # Salvar para um buffer em memória
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    
    return buffer

# Função para gerar conteúdo via API OpenAI
def generate_content(prompt, model="gpt-3.5-turbo", temperature=0.7):
    if not st.session_state.api_key_configured or not st.session_state.api_key:
        return "API não configurada. Por favor, contate o administrador."
    
    # Verificar limites
    if st.session_state.token_count >= TOKEN_LIMIT:
        return "Você atingiu o limite de tokens para esta sessão. Por favor, tente novamente mais tarde."
    
    if st.session_state.request_count >= REQUEST_LIMIT:
        return "Você atingiu o limite de requisições para esta sessão. Por favor, tente novamente mais tarde."
    
    try:
        with st.spinner("Gerando conteúdo..."):
            # Atualizar o timestamp da última requisição
            st.session_state.last_request_time = time.time()
            
            # Incrementar contador de requisições
            st.session_state.request_count += 1
            
            # Configurar requisição direta à API
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {st.session_state.api_key}"
            }
            
            # System prompt (versão resumida para exemplificação)
            system_prompt = """
            Você é o NEXUS, um sistema de IA especializado em comunicação estratégica e gerenciamento de projetos.
            Forneça respostas profissionais, estruturadas e detalhadas, adaptadas ao contexto específico.
            """
            
            # Adicionar mensagem do sistema e prompt do usuário
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": temperature,
                "max_tokens": 4000  # Aumentado para respostas mais completas
            }
            
            # Fazer a requisição à API
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                data=json.dumps(payload),
                timeout=60
            )
            
            # Processar a resposta
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Atualizar contadores de tokens
                prompt_tokens = result['usage']['prompt_tokens']
                completion_tokens = result['usage']['completion_tokens']
                total_tokens = result['usage']['total_tokens']
                st.session_state.token_count += total_tokens
                
                # Registrar uso
                st.session_state.usage_data.append({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'feature': st.session_state.current_feature,
                    'tokens': total_tokens,
                    'model': model,
                    'session_id': st.session_state.session_id
                })
                
                # Adicionar ao histórico
                st.session_state.history.append({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'feature': st.session_state.current_feature,
                    'input': prompt[:100] + "..." if len(prompt) > 100 else prompt,  # Resumido para economizar espaço
                    'output': content,
                    'model': model,
                    'session_id': st.session_state.session_id
                })
                
                return content
            else:
                return f"Erro na API (Status {response.status_code}): {response.text}"
        
    except Exception as e:
        return f"Erro ao gerar conteúdo: {str(e)}"

  # Função para criar cartões de funcionalidades
def create_feature_cards():
    """Cria os cartões de seleção de funcionalidades na interface principal"""
    
    col1, col2 = st.columns(2)
    features_list = list(feature_options.items())
    
    # Distribuir as funcionalidades em duas colunas
    for i, (name, details) in enumerate(features_list):
        current_col = col1 if i % 2 == 0 else col2
        with current_col:
            color = details["color"]
            icon = details["icon"]
            description = details["description"]
            
            # Use um container para o estilo do cartão
            with st.container():
                st.markdown(f"""
                <div style="background-color: white; padding: 15px; border-radius: 10px; 
                            margin-bottom: 15px; border-left: 4px solid var(--{color});">
                    <h3 style="margin:0; color:var(--dark-purple); font-size:18px;">
                        {icon} {name}
                    </h3>
                    <p style="margin:5px 0 0 0; color:var(--text-secondary); font-size:14px;">
                        {description}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Simplificar para apenas um botão
                if st.button(f"Selecionar", key=f"select_{name}"):
                    st.session_state.current_feature = name
                    st.session_state.previous_screen = "home"
                    st.experimental_rerun()

# Função para configurar e exibir a sidebar
def setup_sidebar():
    """Configura a barra lateral do aplicativo"""
    
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        
        # Logo ou imagem
        st.markdown("""
        <div style="text-align:center; padding:20px 0;">
            <svg width="120" height="40">
                <defs>
                    <linearGradient id="sidebarGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#6247AA"/>
                        <stop offset="50%" stop-color="#FF6D2A"/>
                        <stop offset="100%" stop-color="#00C1D5"/>
                    </linearGradient>
                </defs>
                <rect width="120" height="40" rx="5" fill="url(#sidebarGradient)"/>
                <text x="60" y="25" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="white" text-anchor="middle">NEXUS</text>
            </svg>
            <p style="color:#86868B; margin-top:5px; font-size:12px;">Assistente de Comunicação IA</p>
        </div>
        """, unsafe_allow_html=True)

  # Função para criar cartões de funcionalidades
def create_feature_cards():
    """Cria os cartões de seleção de funcionalidades na interface principal"""
    
    col1, col2 = st.columns(2)
    features_list = list(feature_options.items())
    
    # Distribuir as funcionalidades em duas colunas
    for i, (name, details) in enumerate(features_list):
        current_col = col1 if i % 2 == 0 else col2
        with current_col:
            color = details["color"]
            icon = details["icon"]
            description = details["description"]
            
            # Use um container para o estilo do cartão
            with st.container():
                st.markdown(f"""
                <div style="background-color: white; padding: 15px; border-radius: 10px; 
                            margin-bottom: 15px; border-left: 4px solid var(--{color});">
                    <h3 style="margin:0; color:var(--dark-purple); font-size:18px;">
                        {icon} {name}
                    </h3>
                    <p style="margin:5px 0 0 0; color:var(--text-secondary); font-size:14px;">
                        {description}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Simplificar para apenas um botão
                if st.button(f"Selecionar", key=f"select_{name}"):
                    st.session_state.current_feature = name
                    st.session_state.previous_screen = "home"
                    st.experimental_rerun()

# Função para configurar e exibir a sidebar
def setup_sidebar():
    """Configura a barra lateral do aplicativo"""
    
    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        
        # Logo ou imagem
        st.markdown("""
        <div style="text-align:center; padding:20px 0;">
            <svg width="120" height="40">
                <defs>
                    <linearGradient id="sidebarGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#6247AA"/>
                        <stop offset="50%" stop-color="#FF6D2A"/>
                        <stop offset="100%" stop-color="#00C1D5"/>
                    </linearGradient>
                </defs>
                <rect width="120" height="40" rx="5" fill="url(#sidebarGradient)"/>
                <text x="60" y="25" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="white" text-anchor="middle">NEXUS</text>
            </svg>
            <p style="color:#86868B; margin-top:5px; font-size:12px;">Assistente de Comunicação IA</p>
        </div>
        """, unsafe_allow_html=True)

 # Interface principal do aplicativo
def main():
    # Renderizar o cabeçalho com gradiente
    header()
    
    # Configurar a sidebar
    setup_sidebar()
    
    # Exibir mensagem sobre versão aprimorada
    with st.expander("ℹ️ Sobre esta versão", expanded=False):
        st.markdown(f"""
        **Versão NEXUS Aprimorada**
        Esta versão possui interface moderna e limites expandidos:
        * Até {REQUEST_LIMIT} requisições por sessão
        * Até {TOKEN_LIMIT} tokens por sessão
        * Design responsivo para todos os dispositivos
        * Análise avançada de tom comunicacional
        """)
    
    # Botão VOLTAR quando estiver em uma funcionalidade
    if st.session_state.current_feature:
        if st.button("◀️ VOLTAR", key="back_to_home"):
            st.session_state.current_feature = ""
            st.session_state.previous_screen = None
            st.experimental_rerun()
    
    # Histórico de gerações recentes
    if st.session_state.history:
        with st.expander("Histórico de Gerações Recentes", expanded=False):
            for i, item in enumerate(reversed(st.session_state.history[-5:])):  # 5 itens mais recentes
                st.markdown(f"""
                <div class="history-item">
                    <p><strong>{item['timestamp']} - {item['feature']}</strong></p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Carregar este conteúdo ↩️", key=f"load_{i}"):
                    st.session_state.current_feature = item['feature']
                    st.session_state.generated_content = item['output']
                    st.experimental_rerun()
                st.markdown("---")
    
    # Se nenhuma funcionalidade selecionada, mostrar as opções
    if not st.session_state.current_feature:
        st.markdown("## Selecione uma funcionalidade")
        create_feature_cards()
    else:
        # Interface específica da funcionalidade selecionada
        current_feature = st.session_state.current_feature
        feature_details = feature_options[current_feature]
        
        # Título da funcionalidade
        st.markdown(f"## {feature_details['icon']} {current_feature}")
        
        # Verificar limites antes de mostrar a interface
        if st.session_state.token_count >= TOKEN_LIMIT:
            st.error(f"Você atingiu o limite de {TOKEN_LIMIT} tokens para esta sessão. Por favor, tente novamente mais tarde.")
        elif st.session_state.request_count >= REQUEST_LIMIT:
            st.error(f"Você atingiu o limite de {REQUEST_LIMIT} requisições para esta sessão. Por favor, tente novamente mais tarde.")
        else:
            # Interface específica da funcionalidade
            with st.form(key=f"{current_feature}_form"):
                st.markdown(f'<div class="form-container">', unsafe_allow_html=True)
                st.markdown(f'<p class="form-title">{feature_details["description"]}</p>', unsafe_allow_html=True)
                
                # Campo de subtipo
                subtype = st.selectbox("Tipo de Comunicação", feature_details['subtypes'])
                
                # Campos comuns a todas as funcionalidades (exceto PMBOK que tem campos específicos)
                context = ""
                if current_feature != "Consultor PMBOK 7":
                    context = st.text_area("Contexto do Projeto", 
                                        help="Descreva o projeto, fase atual e informações relevantes",
                                        height=100,
                                        placeholder="Ex: Projeto de desenvolvimento do aplicativo mobile, fase de testes")
                
                # Campos específicos por funcionalidade
                prompt = ""
                
                if current_feature == "Gerador de Comunicações Estruturadas":
                    audience = st.text_input("Público-alvo", 
                                        help="Para quem esta comunicação será enviada (equipe, cliente, stakeholder)",
                                        placeholder="Ex: Cliente, diretor de marketing da empresa XYZ")
                    key_points = st.text_area("Pontos-chave", 
                                            help="Liste os principais pontos que devem ser incluídos na comunicação",
                                            height=150,
                                            placeholder="Ex: Atraso de 3 dias devido a bugs na integração; Plano de recuperação com recursos adicionais")
                    tone = st.select_slider("Tom da Comunicação", 
                                        options=["Muito Formal", "Formal", "Neutro", "Amigável", "Casual"],
                                        value="Neutro")
                    
                    prompt = f"""
                    Gere um {subtype} com base nas seguintes informações:
                    
                    Contexto do Projeto: {context}
                    Público-alvo: {audience}
                    Pontos-chave: {key_points}
                    Tom desejado: {tone}
                    
                    Formate a saída adequadamente para um {subtype}, incluindo assunto/título e estrutura apropriada.
                    """
                
                elif current_feature == "Assistente de Reuniões":
                    participants = st.text_area("Participantes", 
                                            help="Liste os participantes e suas funções",
                                            height=100,
                                            placeholder="Ex: João Silva (Gerente de Projeto), Maria Costa (Desenvolvedora Frontend)")
                    topics = st.text_area("Tópicos a serem abordados", 
                                        help="Liste os tópicos que precisam ser discutidos",
                                        height=150,
                                        placeholder="Ex: Atualização do cronograma, Bugs pendentes, Feedback do cliente")
                    duration = st.number_input("Duração (minutos)", min_value=15, max_value=240, value=60, step=15)
                    
                    if subtype == "Agenda de Reunião":
                        prompt = f"""
                        Crie uma agenda detalhada para uma reunião de {duration} minutos com base nas seguintes informações:
                        
                        Contexto do Projeto: {context}
                        Participantes: {participants}
                        Tópicos a serem abordados: {topics}
                        
                        Inclua alocação de tempo para cada item, responsáveis e objetivos claros.
                        """
                    elif subtype == "Ata/Resumo de Reunião":
                        decisions = st.text_area("Decisões tomadas", 
                                            help="Liste as principais decisões tomadas durante a reunião",
                                            height=100,
                                            placeholder="Ex: Aprovação do novo design, Extensão do prazo em 1 semana")
                        actions = st.text_area("Ações acordadas", 
                                            help="Liste as ações acordadas, responsáveis e prazos",
                                            height=100,
                                            placeholder="Ex: João irá corrigir o bug #123 até amanhã, Maria criará novos componentes até sexta")
                        
                        prompt = f"""
                        Crie uma ata/resumo detalhado para uma reunião de {duration} minutos com base nas seguintes informações:
                        
                        Contexto do Projeto: {context}
                        Participantes: {participants}
                        Tópicos abordados: {topics}
                        Decisões tomadas: {decisions}
                        Ações acordadas: {actions}
                        
                        Organize por tópicos, destacando claramente decisões e próximos passos com responsáveis.
                        """
                    else:  # Follow-up
                        meeting_outcome = st.text_area("Resultado da reunião", 
                                                help="Resuma os principais resultados da reunião",
                                                height=100,
                                                placeholder="Ex: Definidas as prioridades para o próximo sprint e resolvidos os bloqueios atuais")
                        action_items = st.text_area("Itens de ação", 
                                                help="Liste os itens de ação, responsáveis e prazos",
                                                height=100,
                                                placeholder="Ex: João: revisão de código até 25/03; Maria: implementação da nova feature até 27/03")
                        
                        prompt = f"""
                        Crie uma mensagem de follow-up para uma reunião com base nas seguintes informações:
                        
                        Contexto do Projeto: {context}
                        Participantes: {participants}
                        Tópicos abordados: {topics}
                        Resultado da reunião: {meeting_outcome}
                        Itens de ação: {action_items}
                        
                        A mensagem deve agradecer a participação, resumir os principais pontos, detalhar próximos passos
                        com responsáveis e prazos, e solicitar confirmação/feedback conforme apropriado.
                        """
                        
                elif current_feature == "Simplificador de Linguagem Técnica":
                    technical_content = st.text_area("Conteúdo Técnico", 
                                                help="Cole aqui o texto técnico que precisa ser traduzido",
                                                height=200,
                                                placeholder="Ex: A implementação do Redux utiliza reducers imutáveis para gerenciar o estado global da aplicação...")
                    audience = st.selectbox("Público-alvo", 
                                        ["Executivos", "Clientes não-técnicos", "Equipe de Negócios", "Equipe Técnica Junior"])
                    key_concepts = st.text_input("Conceitos-chave a preservar", 
                                            help="Liste conceitos técnicos que devem ser mantidos mesmo se simplificados",
                                            placeholder="Ex: gerenciamento de estado, API, front-end")
                    
                    prompt = f"""
                    Traduza/adapte o seguinte conteúdo técnico para um público de {audience} com base nas seguintes informações:
                    
                    Contexto do Projeto: {context}
                    Conteúdo Técnico Original: {technical_content}
                    Conceitos-chave a preservar: {key_concepts}
                    
                    Para {audience}, foque em: 
                    - {'Impacto nos negócios e resultados de alto nível' if audience == 'Executivos' else ''}
                    - {'Benefícios e funcionalidades em linguagem acessível' if audience == 'Clientes não-técnicos' else ''}
                    - {'Conexão com objetivos de negócios e processos' if audience == 'Equipe de Negócios' else ''}
                    - {'Explicações técnicas mais detalhadas, mas com conceitos explicados' if audience == 'Equipe Técnica Junior' else ''}
                    
                    Mantenha a precisão conceitual mesmo simplificando a linguagem.
                    Forneça uma explicação completa e detalhada, com exemplos e analogias apropriadas para o público.
                    """
                
                elif current_feature == "Facilitador de Feedback":
                    situation = st.text_area("Situação", 
                                        help="Descreva a situação específica para a qual você precisa fornecer feedback",
                                        height=150,
                                        placeholder="Ex: Atraso na entrega de componentes para o projeto principal...")
                    strengths = st.text_area("Pontos Fortes", 
                                        help="Liste aspectos positivos que devem ser destacados",
                                        height=100,
                                        placeholder="Ex: Qualidade do código entregue, comunicação proativa de desafios")
                    areas_for_improvement = st.text_area("Áreas para Melhoria", 
                                                    help="Liste aspectos que precisam ser melhorados",
                                                    height=100,
                                                    placeholder="Ex: Estimativas de tempo irrealistas, falha em pedir ajuda quando bloqueado")
                    relationship = st.selectbox("Relação com o Receptor", 
                                            ["Membro da equipe direto", "Colega de mesmo nível", "Superior hierárquico", "Cliente", "Fornecedor"])
                    
                    prompt = f"""
                    Estruture um {subtype} construtivo e eficaz com base nas seguintes informações:
                    
                    Contexto do Projeto: {context}
                    Situação específica: {situation}
                    Pontos fortes a destacar: {strengths}
                    Áreas para melhoria: {areas_for_improvement}
                    Relação com o receptor: {relationship}
                    
                    O feedback deve:
                    - Ser específico e baseado em comportamentos observáveis
                    - Equilibrar aspectos positivos e áreas de melhoria
                    - Incluir exemplos concretos
                    - Oferecer sugestões acionáveis
                    - Usar tom apropriado para a relação ({relationship})
                    - Focar em crescimento e desenvolvimento, não em crítica
                    
                    Formate como um roteiro/script detalhado que o usuário pode seguir na conversa ou adaptar para uma comunicação escrita.
                    Adicione observações e dicas de comunicação não-verbal quando relevante.
                    """
                
                elif current_feature == "Detector de Riscos de Comunicação":
                    content_to_analyze = st.text_area("Conteúdo para Análise", 
                                                    help="Cole aqui o texto que você deseja analisar quanto a riscos de comunicação",
                                                    height=200,
                                                    placeholder="Ex: Devido a circunstâncias imprevistas no desenvolvimento, alguns recursos podem sofrer atrasos...")
                    audience = st.text_input("Público-alvo", 
                                        help="Descreva quem receberá esta comunicação",
                                        placeholder="Ex: Cliente executivo com pouco conhecimento técnico")
                    stakes = st.select_slider("Importância da Comunicação", 
                                            options=["Baixa", "Média", "Alta", "Crítica"],
                                            value="Média")
                    
                    prompt = f"""
                    Analise o seguinte {subtype} quanto a riscos de comunicação:
                    
                    Contexto do Projeto: {context}
                    Público-alvo: {audience}
                    Importância da comunicação: {stakes}
                    
                    Conteúdo para análise:
                    ---
                    {content_to_analyze}
                    ---
                    
                    Sua análise deve:
                    1. Identificar ambiguidades, informações incompletas ou confusas
                    2. Apontar possíveis mal-entendidos baseados no público-alvo
                    3. Detectar problemas de tom ou linguagem inapropriada
                    4. Identificar informações sensíveis ou potencialmente problemáticas
                    5. Sugerir reformulações específicas para cada problema identificado
                    6. Analisar a estrutura geral e propor melhorias organizacionais
                    7. Verificar se há informações críticas ausentes
                    
                    Organize sua análise em forma de tabela com colunas para: Trecho problemático, Risco potencial, Sugestão de melhoria.
                    Ao final, forneça uma avaliação geral dos riscos de comunicação (Baixo/Médio/Alto) e um resumo das principais recomendações.
                    Forneça também uma versão revisada completa do texto.
                    """
                
                elif current_feature == "Consultor PMBOK 7":
                    pmbok_topic = subtype  # Já definido pelo selectbox de subtypes
                    
                    project_context = st.text_area("Contexto do Projeto", 
                                            help="Descreva brevemente o projeto ou a situação para contextualizar sua dúvida",
                                            height=100,
                                            placeholder="Ex: Estamos iniciando um projeto de desenvolvimento de software com metodologia híbrida...")
                    
                    specific_question = st.text_area("Sua Dúvida Específica", 
                                                help="Detalhe sua dúvida ou o que você precisa saber sobre o tema selecionado",
                                                height=150,
                                                placeholder="Ex: Como aplicar os princípios de valor do PMBOK 7 em um ambiente que tradicionalmente usava metodologias em cascata?")
                    
                    experience_level = st.select_slider("Seu Nível de Experiência", 
                                                    options=["Iniciante", "Intermediário", "Avançado", "Especialista"],
                                                    value="Intermediário")
                    
                    organization_context = st.text_input("Contexto Organizacional", 
                                                    help="Descreva brevemente o contexto organizacional (opcional)",
                                                    placeholder="Ex: Empresa de médio porte do setor financeiro com cultura tradicional")
                    
                    base_prompt = f"""
                    Forneça uma orientação detalhada sobre o tema "{pmbok_topic}" do PMBOK 7 com base nas seguintes informações:
                    
                    Contexto do Projeto: {project_context}
                    Dúvida Específica: {specific_question}
                    Nível de Experiência do Usuário: {experience_level}
                    Contexto Organizacional: {organization_context}
                    
                    Sua resposta deve:
                    1. Explicar os conceitos relevantes do PMBOK 7 relacionados à dúvida
                    2. Fornecer orientações práticas adaptadas ao contexto específico
                    3. Apresentar exemplos concretos de aplicação
                    4. Destacar boas práticas e recomendações
                    5. Considerar o nível de experiência do usuário ({experience_level})
                    6. Fazer conexões com outros domínios ou princípios relevantes do PMBOK 7
                    7. Incluir dicas de implementação prática
                    8. Mencionar possíveis desafios e como superá-los
                    
                    Formate a resposta de maneira estruturada, com seções claras e, se apropriado, inclua referências aos elementos específicos do PMBOK 7.
                    """
                    
                    # Enriquecemos o prompt com informações relevantes do PMBOK 7
                    prompt = enrich_pmbok_prompt(base_prompt, pmbok_topic)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Substituir os três botões por um único botão GERAR
                st.markdown("""
                <style>
                    /* Estilo para o botão submit roxo */
                   .stButton > button {
                        background-color: #6247AA !important;
                        color: white !important;
                        border: none !important;
                        border-radius: 4px;
                        padding: 0.5rem 1rem;
                        font-weight: 500;
                   }
                </style>
                """, unsafe_allow_html=True)
                
                submit_button = st.form_submit_button("GERAR")

# Processamento após o envio do formulário
            if submit_button:
                if not st.session_state.api_key_configured:
                    st.error("API não configurada. Por favor, contate o administrador.")
                elif st.session_state.token_count >= TOKEN_LIMIT:
                    st.error(f"Você atingiu o limite de {TOKEN_LIMIT} tokens para esta sessão.")
                elif st.session_state.request_count >= REQUEST_LIMIT:
                    st.error(f"Você atingiu o limite de {REQUEST_LIMIT} requisições para esta sessão.")
                else:
                    # Gerar conteúdo
                    generated_content = generate_content(prompt, model="gpt-3.5-turbo", temperature=0.7)
                    st.session_state.generated_content = generated_content
                    
                    # Exibir resultado
                    st.markdown("### Resultado")
                    st.markdown('<div class="result-area">', unsafe_allow_html=True)
                    st.markdown(generated_content)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Adicionar botão VOLTAR após exibir o resultado
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if st.button("◀️ VOLTAR", key="back_from_result"):
                            # Manter o current_feature, apenas limpar o resultado
                            st.session_state.generated_content = ""
                            st.experimental_rerun()
                    
                    # Opções de download
                    col1, col2 = st.columns(2)
                    with col1:
                        # Download como texto
                        st.download_button(
                            label="📄 Baixar como TXT",
                            data=generated_content,
                            file_name=f"{current_feature.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
                    
                    with col2:
                        # Download como DOCX
                        docx_buffer = export_as_docx(generated_content)
                        st.download_button(
                            label="📝 Baixar como DOCX",
                            data=docx_buffer,
                            file_name=f"{current_feature.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                    
                    # Comentando a parte de análise de tom, já que você decidiu não incluir por enquanto
                    # # Análise de Tom (para todos os tipos de conteúdo exceto PMBOK)
                    # if current_feature != "Consultor PMBOK 7":
                    #     create_tone_analysis_section(generated_content)
                    
                    
# Iniciar a aplicação
if __name__ == "__main__":
    main()
