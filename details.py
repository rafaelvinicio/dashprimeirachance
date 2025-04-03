import streamlit as st
import pandas as pd

def display_category_details(filtered_df):
    """
    Exibe informações detalhadas sobre as categorias
    """
    st.subheader("Informações por Categoria")

    for cat in ["Excelente", "Médio", "Baixo"]:
        cat_data = filtered_df[filtered_df['CATEGORIA'] == cat]

        if len(cat_data) > 0:
            cat_inscritos = cat_data['INSCRITOS'].sum()
            cat_matriculas = cat_data['MATRICULAS'].sum()
            cat_taxa = (cat_inscritos / cat_matriculas * 100) if cat_matriculas > 0 else 0
            cat_count = len(cat_data)

            st.markdown(f"""
            <div style='margin-bottom: 15px; padding: 12px; background-color: {"#F0FFF4" if cat == "Excelente" else "#FFFBEB" if cat == "Médio" else "#FFF5F5"}; border-radius: 6px;'>
                <div style='font-weight: 600; color: {"#36B37E" if cat == "Excelente" else "#FFAB00" if cat == "Médio" else "#FF5630"}; margin-bottom: 8px;'>
                    {cat} ({cat_count} registros)
                </div>
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.85rem;'>
                    <div>
                        <div style='color: #6B7280;'>Inscritos:</div>
                        <div style='font-weight: 600;'>{cat_inscritos:,}</div>
                    </div>
                    <div>
                        <div style='color: #6B7280;'>Matriculados:</div>
                        <div style='font-weight: 600;'>{cat_matriculas:,}</div>
                    </div>
                    <div>
                        <div style='color: #6B7280;'>Taxa Média:</div>
                        <div style='font-weight: 600;'>{cat_taxa:.1f}%</div>
                    </div>
                    <div>
                        <div style='color: #6B7280;'>% do Total:</div>
                        <div style='font-weight: 600;'>{(cat_count / len(filtered_df) * 100):.1f}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def display_data_table(table_df, column_name, display_option):
    """
    Exibe a tabela de dados com formatação
    """
    # Remover colunas desnecessárias e renomear para exibição
    display_columns = []
    if display_option == "Escolas" and 'GRE' in table_df.columns:
        display_columns.append('GRE')
    if display_option == "Escolas" and 'CIDADE' in table_df.columns:
        display_columns.append('CIDADE')

    display_columns.extend([column_name, 'MATRICULAS', 'INSCRITOS', 'TAXA_EFICIENCIA', 'CATEGORIA'])
    table_df = table_df[display_columns].copy()

    column_mapping = {
        'GRE': 'GRE',
        'CIDADE': 'Cidade',
        'ESCOLA': 'Escola',
        column_name: display_option.rstrip('s'),
        'MATRICULAS': 'Matriculados',
        'INSCRITOS': 'Inscritos',
        'TAXA_EFICIENCIA': 'Taxa (%)',
        'CATEGORIA': 'Categoria'
    }

    # Aplicar mapeamento de colunas
    valid_mapping = {col: new_col for col, new_col in column_mapping.items() if col in table_df.columns}
    table_df = table_df.rename(columns=valid_mapping)

    # Formatar a taxa para exibição
    table_df['Taxa (%)'] = table_df['Taxa (%)'].round(1)

    # Exibir tabela
    st.dataframe(
        table_df.sort_values('Taxa (%)', ascending=False),
        hide_index=True,
        use_container_width=True,
        height=min(400, 100 + len(table_df) * 35)
    )