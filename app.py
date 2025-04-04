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

# Função para alternar o tema
def toggle_theme():
    # Obter o tema atual
    theme = st.session_state.get("theme", "auto")

    # Alternar entre tema claro, escuro e automático
    if theme == "auto":
        st.session_state.theme = "light"
    elif theme == "light":
        st.session_state.theme = "dark"
    else:
        st.session_state.theme = "auto"

    # Aplicar o tema conforme a seleção
    apply_theme(st.session_state.theme)

# Função para aplicar o tema
def apply_theme(theme):
    if theme == "light":
        # Tema claro
        st.markdown("""
        <style>
        :root {
            --background-color: #F8FAFC;
            --text-color: #2E3A59;
            --sidebar-bg: #F2F5F9;
            --card-bg: #FFFFFF;
        }
        </style>
        """, unsafe_allow_html=True)
    elif theme == "dark":
        # Tema escuro
        st.markdown("""
        <style>
        :root {
            --background-color: #1E1E1E;
            --text-color: #E0E0E0;
            --sidebar-bg: #252526;
            --card-bg: #2D2D2D;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        # Tema automático (baseado nas preferências do sistema)
        pass

# Inicializar o tema na sessão (padrão: automático)
if "theme" not in st.session_state:
    st.session_state.theme = "auto"

# Carregar CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Aplicar o tema atual
apply_theme(st.session_state.theme)

# Logo e cabeçalho em uma linha com o botão de tema
header_cols = st.columns([3, 1])

with header_cols[0]:
    st.markdown("""
    <div class="logo-container">
        <img src="https://i.postimg.cc/dVfZXQv7/Primeira-Chance-PRINCIPAL.png" alt="Programa Primeira Chance 2025">
    </div>
    """, unsafe_allow_html=True)

with header_cols[1]:
    # Mostrar o tema atual e botão para alternar
    current_theme = {"auto": "Automático", "light": "Claro", "dark": "Escuro"}
    st.button(f"Tema: {current_theme[st.session_state.theme]}", on_click=toggle_theme)

# Título principal
st.markdown("<h1 style='text-align: center;'>Dashboard Analítico - Programa Primeira Chance 2025</h1>", unsafe_allow_html=True)

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

# Cartões de métricas
display_metric_cards(filtered_df, column_name)

# Gráfico principal: Quadrante de Eficiência
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.subheader("Mapa de Eficiência de Conversão")

# Criar e exibir gráfico de eficiência
efficiency_fig = create_efficiency_map(grouped_df, column_name)
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
ranking_fig = create_ranking_chart(grouped_df, column_name, display_option)
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