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
from details import display_data_table

# Configurações da página
st.set_page_config(
    page_title="Dashboard Analítico - Programa Primeira Chance 2025",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregar CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Logo e cabeçalho
st.markdown("""
<div class="logo-container">
    <img src="https://i.postimg.cc/dVfZXQv7/Primeira-Chance-PRINCIPAL.png" alt="Programa Primeira Chance 2025">
</div>
""", unsafe_allow_html=True)

# Carregar dados
with st.spinner("Carregando dados..."):
    df = load_data()

# Criar barra lateral e obter filtros
display_option, filtro_gre, filtro_cidade, sort_by, show_details = create_sidebar(df)

# Preparar dados filtrados
filtered_df, grouped_df, column_name = prepare_dataframe(df, filtro_gre, filtro_cidade, display_option)

# Ordenar os dados conforme solicitado (valor padrão)
grouped_df = grouped_df.sort_values('TAXA_EFICIENCIA', ascending=False)

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