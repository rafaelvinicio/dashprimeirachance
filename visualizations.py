import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import CATEGORY_COLORS

def create_efficiency_map(plot_data, column_name):
    """
    Cria o mapa de eficiência (gráfico de dispersão com quadrantes)
    """
    # Criar o gráfico de dispersão com quadrantes
    fig = px.scatter(
        plot_data,
        x='MATRICULAS',
        y='TAXA_EFICIENCIA',
        color='CATEGORIA',
        color_discrete_map=CATEGORY_COLORS,
        size=[12] * len(plot_data),
        size_max=15,
        hover_name=column_name,
        hover_data={
            'MATRICULAS': True,
            'INSCRITOS': True,
            'TAXA_EFICIENCIA': ':.1f',
            'CATEGORIA': False
        },
        labels={
            'MATRICULAS': 'Total de Matriculados',
            'TAXA_EFICIENCIA': 'Taxa de Eficiência (%)',
            'CATEGORIA': 'Categoria'
        },
        height=500
    )

    # Adicionar rótulos para os pontos
    fig.update_traces(
        textposition='top center',
        textfont=dict(size=10, color="#333333"),
        text=plot_data[column_name],
        marker=dict(line=dict(width=1, color='white'))
    )

    # Adicionar linhas de referência para os quadrantes
    x_min = plot_data['MATRICULAS'].min() * 0.8
    x_max = plot_data['MATRICULAS'].max() * 1.2

    # Linha para 50%
    fig.add_shape(
        type="line", line=dict(dash="dash", width=1, color="#697386"),
        x0=x_min, y0=50, x1=x_max, y1=50
    )

    # Linha para 85%
    fig.add_shape(
        type="line", line=dict(dash="dash", width=1, color="#697386"),
        x0=x_min, y0=85, x1=x_max, y1=85
    )

    # Rótulos dos quadrantes
    fig.add_annotation(
        x=x_max * 0.95, y=92,
        text="Excelente (≥85%)",
        showarrow=False,
        font=dict(color="#36B37E", size=12),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#36B37E",
        borderwidth=2,
        borderpad=4
    )

    fig.add_annotation(
        x=x_max * 0.95, y=67.5,
        text="Médio (50-85%)",
        showarrow=False,
        font=dict(color="#FFAB00", size=12),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#FFAB00",
        borderwidth=2,
        borderpad=4
    )

    fig.add_annotation(
        x=x_max * 0.95, y=25,
        text="Baixo (<50%)",
        showarrow=False,
        font=dict(color="#FF5630", size=12),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="#FF5630",
        borderwidth=2,
        borderpad=4
    )

    # Ajustar layout do gráfico
    fig.update_layout(
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            title=None
        ),
        margin=dict(l=10, r=10, t=60, b=60),
        xaxis=dict(
            title=dict(
                font=dict(size=12)
            ),
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            title=dict(
                font=dict(size=12)
            ),
            tickfont=dict(size=11),
            range=[0, 105]
        )
    )

    return fig

def create_ranking_chart(display_df, column_name, display_option):
    """
    Cria o gráfico de ranking de eficiência
    """
    if display_option == "Escolas":
        # Para escolas, usamos gráfico horizontal devido ao potencial número de itens
        fig_bar = px.bar(
            display_df.sort_values('TAXA_EFICIENCIA', ascending=True),  # Removido .tail(num_items)
            y=column_name,
            x='TAXA_EFICIENCIA',
            color='CATEGORIA',
            color_discrete_map=CATEGORY_COLORS,
            orientation='h',
            labels={
                column_name: display_option.rstrip('s'),
                'TAXA_EFICIENCIA': 'Taxa de Eficiência (%)'
            },
            text='TAXA_EFICIENCIA',
            height=min(500, 100 + len(display_df) * 25),  # Usar comprimento de display_df em vez de num_items
            hover_data=['INSCRITOS', 'MATRICULAS']
        )

        # Formatação dos textos nas barras
        fig_bar.update_traces(
            texttemplate='%{x:.1f}%',
            textposition='outside',
            cliponaxis=False
        )

    else:  # Para Cidades ou GREs, usamos barras verticais
        fig_bar = px.bar(
            display_df.sort_values('TAXA_EFICIENCIA', ascending=False),
            x=column_name,
            y='TAXA_EFICIENCIA',
            color='CATEGORIA',
            color_discrete_map=CATEGORY_COLORS,
            labels={
                column_name: display_option.rstrip('s'),
                'TAXA_EFICIENCIA': 'Taxa de Eficiência (%)'
            },
            text='TAXA_EFICIENCIA',
            height=400,
            hover_data=['INSCRITOS', 'MATRICULAS']
        )

        # Formatação para texto nas barras
        fig_bar.update_traces(
            texttemplate='%{y:.1f}%',
            textposition='outside',
            cliponaxis=False
        )

        # Rotação dos rótulos do eixo X para facilitar leitura
        fig_bar.update_layout(
            xaxis_tickangle=-45
        )

    # Layout comum para ambos os tipos de gráfico
    fig_bar.update_layout(
        template="plotly_white",
        showlegend=False,
        margin=dict(l=10, r=20, t=10, b=10),
        yaxis=dict(
            title=None if display_option == "Escolas" else "Taxa de Eficiência (%)"
        ),
        xaxis=dict(
            title="Taxa de Eficiência (%)" if display_option == "Escolas" else None
        )
    )

    return fig_bar
def create_category_distribution(filtered_df):
    """
    Cria o gráfico de distribuição por categoria
    """
    # Dados para o gráfico de distribuição
    category_counts = filtered_df['CATEGORIA'].value_counts().reset_index()
    category_counts.columns = ['Categoria', 'Quantidade']

    # Adicionar percentuais
    total = category_counts['Quantidade'].sum()
    category_counts['Percentual'] = category_counts['Quantidade'] / total * 100

    # Garantir que as categorias estejam na ordem correta
    category_order = ["Excelente", "Médio", "Baixo"]
    category_counts['Categoria'] = pd.Categorical(
        category_counts['Categoria'],
        categories=category_order,
        ordered=True
    )
    category_counts = category_counts.sort_values('Categoria')

    # Criar gráfico de pizza moderno
    fig_pie = px.pie(
        category_counts,
        values='Quantidade',
        names='Categoria',
        color='Categoria',
        color_discrete_map=CATEGORY_COLORS,
        hole=0.4,
        height=350
    )

    # Personalizar layout do gráfico
    fig_pie.update_traces(
        textinfo='percent+label',
        textposition='outside',
        textfont=dict(size=14),
        marker=dict(line=dict(color='white', width=2))
    )

    return fig_pie, category_counts, category_order

def create_mini_histogram(filtered_df):
    """
    Cria um mini histograma para a distribuição das taxas
    """
    fig_hist = px.histogram(
        filtered_df,
        x='TAXA_EFICIENCIA',
        nbins=20,
        color_discrete_sequence=['#0050B3'],
        height=150
    )

    fig_hist.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        xaxis_title=None,
        yaxis_title=None,
        showlegend=False,
        template="plotly_white"
    )

    # Adicionar linhas verticais para referência
    fig_hist.add_vline(x=50, line_width=1, line_dash="dash", line_color="#6B7280")
    fig_hist.add_vline(x=85, line_width=1, line_dash="dash", line_color="#6B7280")

    return fig_hist

def create_gre_analysis_chart(filtered_df):
    """
    Cria gráfico de análise por GRE
    """
    if 'GRE' not in filtered_df.columns:
        return None

    gre_analysis = filtered_df.groupby('GRE').agg({
        'TAXA_EFICIENCIA': 'mean',
        'INSCRITOS': 'sum',
        'MATRICULAS': 'sum',
        'ESCOLA': 'count'
    }).reset_index()

    gre_analysis = gre_analysis.rename(columns={'ESCOLA': 'Quantidade'})
    gre_analysis['TAXA_EFICIENCIA'] = gre_analysis['TAXA_EFICIENCIA'].round(1)

    # Criar um gráfico de barras horizontal com as GREs
    fig_gre = px.bar(
        gre_analysis.sort_values('TAXA_EFICIENCIA', ascending=True),
        y='GRE',
        x='TAXA_EFICIENCIA',
        text='TAXA_EFICIENCIA',
        color='TAXA_EFICIENCIA',
        color_continuous_scale=[[0, CATEGORY_COLORS["Baixo"]],
                                [0.5, CATEGORY_COLORS["Médio"]],
                                [0.85, CATEGORY_COLORS["Excelente"]]],
        range_color=[0, 100],
        height=min(400, 50 + len(gre_analysis) * 25),
        labels={'TAXA_EFICIENCIA': 'Taxa Média (%)'}
    )

    fig_gre.update_traces(
        texttemplate='%{x:.1f}%',
        textposition='outside'
    )

    fig_gre.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        yaxis_title=None,
        xaxis_title="Taxa Média (%)",
        coloraxis_showscale=False,
        template="plotly_white"
    )

    # Adicionar linhas verticais para referência
    fig_gre.add_vline(x=50, line_width=1, line_dash="dash", line_color="#6B7280")
    fig_gre.add_vline(x=85, line_width=1, line_dash="dash", line_color="#6B7280")

    return fig_gre