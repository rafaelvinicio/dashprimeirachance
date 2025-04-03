import streamlit as st

def create_sidebar(df):
    """
    Cria a barra lateral com filtros e opções
    Retorna os valores de filtro selecionados
    """
    with st.sidebar:
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        st.markdown('<div class="filter-title">Configuração do Dashboard</div>', unsafe_allow_html=True)

        # Seleção de visão principal
        display_option = st.radio(
            "Visualizar por:",
            ["Escolas", "Cidades", "GREs"],
            index=0,
            help="Escolha como deseja visualizar os dados"
        )

        # Filtro de GRE
        all_gres = sorted(df['GRE'].unique().tolist())
        filtro_gre = st.selectbox(
            "Filtrar por GRE:",
            ["Todas"] + all_gres,
            help="Selecione uma GRE específica ou 'Todas'"
        )

        # Aplicar filtro de GRE para o filtro condicional de cidades
        temp_df = df.copy()
        if filtro_gre != "Todas":
            temp_df = temp_df[temp_df['GRE'] == filtro_gre]

        # Filtro condicional para cidades
        filtro_cidade = "Todas"
        if display_option == "Escolas":
            cidades_disponiveis = sorted(temp_df['CIDADE'].unique().tolist())
            filtro_cidade = st.selectbox(
                "Filtrar por Cidade:",
                ["Todas"] + cidades_disponiveis,
                help="Selecione uma cidade específica ou 'Todas'"
            )

        # Tipo de ordenação
        sort_by = st.radio(
            "Ordenar por:",
            ["Taxa de Eficiência", "Número de Inscritos", "Número de Matriculados"],
            index=0
        )

        # Checkbox para exibir detalhes adicionais
        show_details = st.checkbox("Exibir detalhes avançados", value=False)

        # Preparar o dataframe para download - corrigindo a formatação da taxa de eficiência
        download_df = df.copy()
        # Garantir que TAXA_EFICIENCIA seja um número decimal normal
        download_df['TAXA_EFICIENCIA'] = download_df['TAXA_EFICIENCIA'].astype(float).round(1)

        # Botão de download
        st.download_button(
            "📥 Baixar Dados como CSV",
            download_df.to_csv(index=False, encoding='utf-8-sig', decimal='.', sep=',').encode('utf-8-sig'),
            f"primeira_chance_dados.csv",
            "text/csv",
            key='download-csv'
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # Informações sobre as categorias
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        st.markdown('<div class="filter-title">Legenda de Categorias</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="margin-bottom: 10px;">
            <span class="efficiency-badge efficiency-high">Excelente</span>
            <span style="font-size: 0.8rem; margin-left: 5px;">Taxa ≥ 85%</span>
        </div>
        <div style="margin-bottom: 10px;">
            <span class="efficiency-badge efficiency-medium">Médio</span>
            <span style="font-size: 0.8rem; margin-left: 5px;">Taxa entre 50% e 85%</span>
        </div>
        <div>
            <span class="efficiency-badge efficiency-low">Baixo</span>
            <span style="font-size: 0.8rem; margin-left: 5px;">Taxa < 50%</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    return display_option, filtro_gre, filtro_cidade, sort_by, show_details