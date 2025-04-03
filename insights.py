import streamlit as st

def display_insights_recommendations(filtered_df, display_option):
    """
    Exibe insights e recomendações baseados nos dados
    """
    # Calcular alguns insights baseados nos dados
    media_eficiencia = filtered_df['TAXA_EFICIENCIA'].mean()
    escolas_abaixo_50 = len(filtered_df[filtered_df['TAXA_EFICIENCIA'] < 50])
    pct_abaixo_50 = escolas_abaixo_50 / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
    escolas_acima_85 = len(filtered_df[filtered_df['TAXA_EFICIENCIA'] >= 85])
    pct_acima_85 = escolas_acima_85 / len(filtered_df) * 100 if len(filtered_df) > 0 else 0

    # Layout para os insights
    insight_cols = st.columns(2)

    with insight_cols[0]:
        st.markdown("""
        <div style="margin-bottom: 15px;">
            <div style="font-weight: 600; margin-bottom: 10px;">Principais Observações</div>
            <ul style="font-size: 0.9rem; padding-left: 20px; margin-top: 0;">
        """, unsafe_allow_html=True)

        # Lista dinâmica de observações baseadas nos dados
        observations = []

        # Observação sobre média geral
        if media_eficiencia >= 85:
            observations.append(f"Desempenho geral excelente com média de {media_eficiencia:.1f}%")
        elif media_eficiencia >= 50:
            observations.append(f"Desempenho geral médio com {media_eficiencia:.1f}% de eficiência")
        else:
            observations.append(f"Desempenho geral abaixo do esperado ({media_eficiencia:.1f}%)")

        # Observação sobre distribuição
        if pct_acima_85 > 50:
            observations.append(f"{pct_acima_85:.1f}% das {display_option.lower()} têm desempenho excelente")
        elif pct_abaixo_50 > 50:
            observations.append(f"{pct_abaixo_50:.1f}% das {display_option.lower()} têm desempenho baixo")

        # Observação sobre potencial de melhoria
        potential_students = filtered_df[filtered_df['TAXA_EFICIENCIA'] < 50]['MATRICULAS'].sum() * 0.5
        observations.append(f"Potencial para aumentar em até {int(potential_students)} inscritos")

        # Exibir observações
        for obs in observations:
            st.markdown(f"<li>{obs}</li>", unsafe_allow_html=True)

        # Finalizar a lista
        st.markdown("</ul></div>", unsafe_allow_html=True)

    with insight_cols[1]:
        st.markdown("""
        <div style="margin-bottom: 15px;">
            <div style="font-weight: 600; margin-bottom: 10px;">Recomendações</div>
            <ul style="font-size: 0.9rem; padding-left: 20px; margin-top: 0;">
        """, unsafe_allow_html=True)

        # Lista de recomendações
        recommendations = [
            "Promover troca de experiências entre escolas com alto e baixo desempenho",
            f"Priorizar ações nas {escolas_abaixo_50} escolas com taxa abaixo de 50%",
            "Avaliar correlação entre infraestrutura escolar e taxa de conversão",
            "Estabelecer metas progressivas por GRE, considerando realidades locais"
        ]

        # Exibir recomendações
        for rec in recommendations:
            st.markdown(f"<li>{rec}</li>", unsafe_allow_html=True)

        # Finalizar a lista
        st.markdown("</ul></div>", unsafe_allow_html=True)