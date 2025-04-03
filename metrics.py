import streamlit as st

def display_metric_cards(filtered_df, column_name):
    """
    Exibe os cartões de métricas principais
    """
    metric_cols = st.columns(4)

    # Total de inscritos
    with metric_cols[0]:
        total_inscritos = int(filtered_df['INSCRITOS'].sum())
        total_matriculas = int(filtered_df['MATRICULAS'].sum())
        taxa_global = (total_inscritos / total_matriculas * 100) if total_matriculas > 0 else 0

        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Total de Inscritos</div>
            <div class="stat-value">{:,}</div>
            <div class="stat-trend">
                <span>Taxa global: <b>{:.1f}%</b></span>
            </div>
        </div>
        """.format(total_inscritos, taxa_global), unsafe_allow_html=True)

    # Total de escolas/cidades/GREs analisadas
    with metric_cols[1]:
        display_option = column_name.upper() + 'S' if column_name != 'GRE' else 'GREs'
        total_entidades = len(filtered_df[column_name].unique())

        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Total de {}</div>
            <div class="stat-value">{:,}</div>
            <div class="stat-trend">
                <span>Em análise</span>
            </div>
        </div>
        """.format(display_option, total_entidades), unsafe_allow_html=True)

    # Distribuição de categorias
    with metric_cols[2]:
        excelentes = len(filtered_df[filtered_df['CATEGORIA'] == 'Excelente'])
        pct_excelentes = (excelentes / len(filtered_df) * 100) if len(filtered_df) > 0 else 0

        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Desempenho Excelente</div>
            <div class="stat-value">{:,}</div>
            <div class="stat-trend trend-up">
                <span>{:.1f}% do total</span>
            </div>
        </div>
        """.format(excelentes, pct_excelentes), unsafe_allow_html=True)

    # Melhores desempenhos
    with metric_cols[3]:
        taxa_max = filtered_df['TAXA_EFICIENCIA'].max()
        melhor_entidade_idx = filtered_df['TAXA_EFICIENCIA'].idxmax()
        melhor_entidade = filtered_df.loc[melhor_entidade_idx, column_name]

        if len(melhor_entidade) > 20:
            melhor_entidade = melhor_entidade[:18] + "..."

        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">Melhor Desempenho</div>
            <div class="stat-value">{:.1f}%</div>
            <div class="stat-trend">
                <span><b>{}</b></span>
            </div>
        </div>
        """.format(taxa_max, melhor_entidade), unsafe_allow_html=True)

def display_summary_card(filtered_df):
    """
    Exibe o cartão de resumo com estatísticas principais
    """
    # Resumo do estado atual
    taxa_media = filtered_df['TAXA_EFICIENCIA'].mean()
    taxa_mediana = filtered_df['TAXA_EFICIENCIA'].median()

    # Determinar status com base na média
    if taxa_media >= 85:
        status_color = "#36B37E"  # Verde
        status_text = "Excelente"
    elif taxa_media >= 50:
        status_color = "#FFAB00"  # Amarelo
        status_text = "Médio"
    else:
        status_color = "#FF5630"  # Vermelho
        status_text = "Preocupante"

    # Exibir status geral
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 15px;'>
        <div style='font-size: 0.85rem; color: #4B5563; margin-bottom: 5px;'>
            Status Geral do Programa
        </div>
        <div style='font-size: 1.3rem; font-weight: 700; color: {status_color};'>
            {status_text}
        </div>
        <div style='font-size: 0.9rem; color: #6B7280; margin-top: 5px;'>
            Taxa média de {taxa_media:.1f}%
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Distribuição estatística
    st.markdown("""
    <div style='margin: 15px 0;'>
        <div style='font-size: 0.85rem; font-weight: 600; color: #4B5563; margin-bottom: 10px;'>
            Distribuição Estatística
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Estatísticas lado a lado
    stat_cols = st.columns(2)

    with stat_cols[0]:
        st.metric("Média", f"{taxa_media:.1f}%")
        st.metric("Mínima", f"{filtered_df['TAXA_EFICIENCIA'].min():.1f}%")

    with stat_cols[1]:
        st.metric("Mediana", f"{taxa_mediana:.1f}%")
        st.metric("Máxima", f"{filtered_df['TAXA_EFICIENCIA'].max():.1f}%")

def display_top_performers(filtered_df, column_name):
    """
    Exibe a lista das entidades com melhor desempenho
    """
    top_entities = filtered_df.nlargest(5, 'TAXA_EFICIENCIA')

    for i, (_, entity) in enumerate(top_entities.iterrows(), 1):
        entity_name = entity[column_name]
        taxa = entity['TAXA_EFICIENCIA']

        # Exibir entidade com estilo de ranking
        st.markdown(f"""
        <div style='display: flex; align-items: center; margin-bottom: 10px; padding: 8px; background-color: {"#F9FAFB" if i % 2 == 0 else "white"}; border-radius: 4px;'>
            <div style='width: 25px; height: 25px; background-color: {"gold" if i == 1 else "silver" if i == 2 else "#CD7F32" if i == 3 else "#0050B3"}; color: white; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: 600; margin-right: 10px;'>
                {i}
            </div>
            <div style='flex-grow: 1;'>
                <div style='font-weight: 600; font-size: 0.9rem;'>{entity_name}</div>
                <div style='font-size: 0.8rem; color: #6B7280;'>
                    {entity['INSCRITOS']} inscritos de {entity['MATRICULAS']} matriculados
                </div>
            </div>
            <div style='font-weight: 700; font-size: 1.1rem; color: #36B37E; text-align: right;'>
                {taxa:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_priority_attention(filtered_df, column_name):
    """
    Exibe as entidades que precisam de atenção prioritária
    """
    # Filtrar apenas entidades com baixo desempenho, com mais de 50 matriculados
    low_performers = filtered_df[
        (filtered_df['CATEGORIA'] == 'Baixo') &
        (filtered_df['MATRICULAS'] > 50)
    ].nlargest(5, 'MATRICULAS')

    if not low_performers.empty:
        for _, entity in low_performers.iterrows():
            entity_name = entity[column_name]
            taxa = entity['TAXA_EFICIENCIA']

            # Potencial de melhoria (diferença até atingir 50%)
            gap = 50 - taxa
            potential_increase = int((gap / 100) * entity['MATRICULAS'])

            # Exibir entidade com potencial de melhoria
            st.markdown(f"""
            <div style='margin-bottom: 12px; padding: 10px; background-color: #FFF5F5; border-left: 3px solid #FF5630; border-radius: 4px;'>
                <div style='font-weight: 600; font-size: 0.9rem;'>{entity_name}</div>
                <div style='display: flex; justify-content: space-between; margin-top: 5px;'>
                    <div style='font-size: 0.8rem;'>
                        <span style='color: #6B7280;'>Taxa atual:</span>
                        <span style='font-weight: 600; color: #FF5630;'>{taxa:.1f}%</span>
                    </div>
                    <div style='font-size: 0.8rem;'>
                        <span style='color: #6B7280;'>Matriculados:</span>
                        <span style='font-weight: 600;'>{entity['MATRICULAS']}</span>
                    </div>
                </div>
                <div style='font-size: 0.8rem; margin-top: 5px;'>
                    <span style='color: #6B7280;'>Potencial de melhoria:</span>
                    <span style='font-weight: 600; color: #FFAB00;'>+{potential_increase} inscritos</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Não há entidades de baixo desempenho com mais de 50 matriculados.")