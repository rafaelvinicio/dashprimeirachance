import os
import sys

# Adicionar diretório atual ao PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import streamlit as st
import pandas as pd
import numpy as np

# Agora importar os módulos locais
from data_loader import load_data
from utils import prepare_dataframe
from sidebar import create_sidebar
from metrics import display_metric_cards, display_top_performers, display_priority_attention
from visualizations import create_efficiency_map, create_ranking_chart, create_category_distribution, create_gre_analysis_chart
from details import display_category_details, display_data_table

# Configurações da página
st.set_page_config(
    page_title="Dashboard Analítico - Programa Primeira Chance 2025",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregar CSS principal
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carregar CSS específico para a sidebar
try:
    with open("sidebar_theme.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    # Fallback - injeta CSS da sidebar diretamente se o arquivo não existir
    st.markdown("""
    <style>
    /* Fallback para sidebar - fundo branco */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"], [data-testid="stSidebarUserContent"] {
        background-color: white !important;
    }
    [data-testid="stSidebar"] * {
        color: #2E3A59 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Injetar CSS e JavaScript para forçar o tema claro
st.markdown("""
<style>
    /* Forçar tema claro independente das configurações do sistema */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #F8FAFC !important;
    }
    .stApp {
        background-color: #F8FAFC !important;
    }
    .main {
        background-color: #F8FAFC !important;
        color: #2E3A59 !important;
    }
    .st-eb {
        background-color: #FFFFFF !important;
    }
    .st-bb {
        background-color: #0050B3 !important;
    }
    .st-bc {
        color: #0050B3 !important;
    }
    /* Garantir que o texto seja escuro */
    .st-cx, .st-cy, .st-cz, .st-da, .st-db, .st-dc, .st-dd, .st-de,
    .st-cg, .st-ch, .st-ci, .st-cj, .st-ae, .st-af, .st-ag, .st-ai, .st-bu {
        color: #2E3A59 !important;
    }

    /* CORREÇÃO ESPECÍFICA PARA A SIDEBAR - Usando força máxima */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarUserContent"],
    .st-emotion-cache-16txtl3,
    .st-emotion-cache-18ni7ap,
    .st-emotion-cache-1cypcdb,
    .st-emotion-cache-6qob1r,
    .st-emotion-cache-1fttcpj,
    .st-emotion-cache-19rxjzo,
    .st-emotion-cache-z5fcl4,
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        color: #2E3A59 !important;
    }

    /* Garantir que todos os elementos na sidebar sejam da cor certa */
    [data-testid="stSidebar"] *,
    section[data-testid="stSidebar"] * {
        background-color: #FFFFFF !important;
        color: #2E3A59 !important;
    }

    /* Exceções para elementos específicos */
    [data-testid="stSidebar"] .stButton > button,
    [data-testid="stSidebar"] .stDownloadButton > button,
    section[data-testid="stSidebar"] .stButton > button {
        background-color: #0050B3 !important;
        color: white !important;
    }

    /* Agressivamente forçar que todos textos sejam escuros */
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] > div * {
        color: #2E3A59 !important;
    }

    /* Exceção para badges */
    [data-testid="stSidebar"] .efficiency-badge {
        color: white !important;
    }
</style>

<script>
// Script para forçar fundo branco na sidebar
document.addEventListener('DOMContentLoaded', function() {
    // Função para aplicar estilo a todos os elementos da sidebar
    function fixSidebarStyle() {
        // Selecionar a sidebar
        const sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            // Aplicar estilo à sidebar
            sidebar.style.backgroundColor = '#FFFFFF';

            // Aplicar estilo a todos os elementos dentro da sidebar
            const allElements = sidebar.querySelectorAll('*');
            allElements.forEach(el => {
                el.style.backgroundColor = '#FFFFFF';

                // Preservar cores para botões específicos
                if (!el.classList.contains('stButton') &&
                    !el.classList.contains('stDownloadButton') &&
                    !el.classList.contains('efficiency-badge')) {
                    el.style.color = '#2E3A59';
                }
            });
        }
    }

    // Executar imediatamente
    fixSidebarStyle();

    // Executar novamente após um curto atraso para pegar elementos carregados dinamicamente
    setTimeout(fixSidebarStyle, 500);
    setTimeout(fixSidebarStyle, 1000);

    // Criar um observador para mudanças no DOM
    const observer = new MutationObserver(function(mutations) {
        fixSidebarStyle();
    });

    // Observar mudanças em todo o documento
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});
</script>
""", unsafe_allow_html=True)

# Logo e cabeçalho
st.markdown("""
<div class="logo-container">
    <img src="https://i.postimg.cc/dVfZXQv7/Primeira-Chance-PRINCIPAL.png" alt="Programa Primeira Chance 2025">
</div>
<h1 style="text-align: center;">Dashboard Analítico - Programa Primeira Chance 2025</h1>
""", unsafe_allow_html=True)

# Carregar dados
with st.spinner("Carregando dados..."):
    df = load_data()

# Criar barra lateral e obter filtros
display_option, filtro_gre, filtro_cidade, sort_by, show_details = create_sidebar(df)

# Preparar dados filtrados
filtered_df, grouped_df, column_name = prepare_dataframe(df, filtro_gre, filtro_cidade, display_option)

# Ordenar os dados conforme solicitado
if sort_by == "Taxa de Eficiência":
    grouped_df = grouped_df.sort_values('TAXA_EFICIENCIA', ascending=False)
elif sort_by == "Número de Inscritos":
    grouped_df = grouped_df.sort_values('INSCRITOS', ascending=False)
else:  # Número de Matriculados
    grouped_df = grouped_df.sort_values('MATRICULAS', ascending=False)

# Usar todos os dados disponíveis
display_df = grouped_df

# Cartões de métricas
display_metric_cards(filtered_df, column_name)

# Gráfico principal: Quadrante de Eficiência
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.subheader("Mapa de Eficiência de Conversão")

# Criar e exibir gráfico de eficiência
efficiency_fig = create_efficiency_map(display_df, column_name)
st.plotly_chart(efficiency_fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Lista das entidades de melhor desempenho
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header">Top 5 Melhores Desempenhos</div>', unsafe_allow_html=True)
display_top_performers(filtered_df, column_name)
st.markdown('</div>', unsafe_allow_html=True)

# Entidades que precisam de atenção
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header">Atenção Prioritária</div>', unsafe_allow_html=True)
display_priority_attention(filtered_df, column_name)
st.markdown('</div>', unsafe_allow_html=True)

# Gráfico secundário: Ranking de Eficiência
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.subheader(f"Ranking de Eficiência - {display_option}")

# Criar e exibir gráfico de ranking
ranking_fig = create_ranking_chart(display_df, column_name, display_option)
st.plotly_chart(ranking_fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Gráfico comparativo: Distribuição de Categorias
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.subheader("Distribuição por Categoria de Desempenho")

# Criar gráfico de distribuição
pie_fig, category_counts, category_order = create_category_distribution(filtered_df)

# Criar um layout de duas colunas para o gráfico e estatísticas
dist_cols = st.columns([3, 2])

with dist_cols[0]:
    # Exibir gráfico de pizza
    st.plotly_chart(pie_fig, use_container_width=True)

with dist_cols[1]:
    # Exibir estatísticas detalhadas em um formato mais elegante
    st.markdown("<div style='padding: 20px 0;'>", unsafe_allow_html=True)

    for i, cat in enumerate(category_order):
        cat_data = category_counts[category_counts['Categoria'] == cat]
        if not cat_data.empty:
            quantidade = int(cat_data['Quantidade'].values[0])
            percentual = cat_data['Percentual'].values[0]

            # Definir cor para cada categoria
            cat_color = "#36B37E" if cat == "Excelente" else "#FFAB00" if cat == "Médio" else "#FF5630"

            # Estilo colorido para cada categoria
            st.markdown(f"""
            <div style='margin-bottom: 20px;'>
                <div style='font-size: 16px; font-weight: 600; color: {cat_color};'>
                    {cat} ({quantidade})
                </div>
                <div style='background-color: #F3F4F6; height: 8px; border-radius: 4px; margin: 8px 0;'>
                    <div style='width: {percentual}%; height: 8px; background-color: {cat_color}; border-radius: 4px;'></div>
                </div>
                <div style='font-size: 14px; color: #4B5563;'>
                    {percentual:.1f}% dos {display_option.lower()}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Detalhes adicionais, se opção habilitada
if show_details:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-header">Análise Detalhada</div>', unsafe_allow_html=True)

    # Comparação da taxa média por GRE
    if 'GRE' in filtered_df.columns:
        st.subheader("Taxa Média por GRE")

        # Criar gráfico de análise de GRE
        gre_fig = create_gre_analysis_chart(filtered_df)
        if gre_fig:
            st.plotly_chart(gre_fig, use_container_width=True)
        else:
            st.info("Dados insuficientes para gerar a análise por GRE.")

    # Adicionando informações detalhadas sobre as categorias
    display_category_details(filtered_df)

    st.markdown('</div>', unsafe_allow_html=True)

# Visualização tabulada dos dados
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.subheader(f"Dados Completos - {display_option}")

# Exibir tabela de dados
display_data_table(grouped_df, column_name, display_option)

st.markdown('</div>', unsafe_allow_html=True)

# Nota de atualização dos dados no rodapé
st.markdown("""
<div style="text-align: center; margin-top: 30px; padding: 10px; font-size: 0.8rem; color: #6B7280;">
    Dashboard desenvolvido para análise de dados do Programa Primeira Chance 2025.<br>
</div>
""", unsafe_allow_html=True)