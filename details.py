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
    # Verificar e mostrar as colunas disponíveis para debug
    # st.write(f"Colunas disponíveis: {table_df.columns.tolist()}")

    # Verificar primeiro se o DataFrame está vazio ou inválido
    if table_df is None or len(table_df) == 0 or len(table_df.columns) == 0:
        st.warning(f"Não há dados disponíveis para exibir a tabela de {display_option}.")
        return

    # Criar uma cópia do DataFrame para evitar modificar o original
    table_df = table_df.copy()

    # Encontrar apenas as colunas que realmente existem no DataFrame
    # Verificar se column_name existe no DataFrame
    if column_name not in table_df.columns:
        st.error(f"A coluna {column_name} não existe nos dados.")
        return

    # Lista para armazenar as colunas existentes que vamos usar
    columns_to_use = [column_name]  # Garantir que a coluna principal está presente

    # Verificar e adicionar colunas extras se existirem
    for col in ['GRE', 'CIDADE', 'MATRICULAS', 'INSCRITOS', 'TAXA_EFICIENCIA', 'CATEGORIA']:
        if col in table_df.columns and col != column_name:  # Evitar duplicação
            columns_to_use.append(col)

    # Se temos poucas colunas, mostrar uma mensagem informativa
    if len(columns_to_use) < 2:
        st.warning(f"Dados insuficientes para exibir uma tabela completa de {display_option}.")

    # Filtrar apenas as colunas existentes
    table_df = table_df[columns_to_use]

    # Se estamos visualizando por GREs, adicionar "GRE" antes do número
    if column_name == 'GRE' and 'GRE' in table_df.columns:
        table_df['GRE'] = "GRE " + table_df['GRE'].astype(str)

    # Mapeamento de nomes de colunas para exibição
    column_mapping = {
        'GRE': 'GRE',
        'CIDADE': 'Cidade',
        'ESCOLA': 'Escola',
        'MATRICULAS': 'Matriculados',
        'INSCRITOS': 'Inscritos',
        'TAXA_EFICIENCIA': 'Taxa (%)',
        'CATEGORIA': 'Categoria'
    }

    # Adicionar o mapeamento para o column_name dinâmico
    if column_name not in column_mapping:
        column_mapping[column_name] = display_option.rstrip('s')

    # Aplicar mapeamento apenas às colunas disponíveis
    valid_mapping = {col: column_mapping.get(col, col) for col in table_df.columns}
    table_df = table_df.rename(columns=valid_mapping)

    # Determinar a coluna para ordenação
    sort_col = None

    # Tentar usar Taxa (%) para ordenação se existir
    if 'Taxa (%)' in table_df.columns:
        sort_col = 'Taxa (%)'
        table_df['Taxa (%)'] = table_df['Taxa (%)'].round(1)
    # Tentar usar Matriculados ou Inscritos se existirem
    elif 'Matriculados' in table_df.columns:
        sort_col = 'Matriculados'
    elif 'Inscritos' in table_df.columns:
        sort_col = 'Inscritos'
    # Caso contrário, usar a primeira coluna (que deve ser o nome da entidade)
    else:
        sort_col = table_df.columns[0]

    # Ordenar e exibir tabela
    if sort_col:
        # Ordenação descendente para números, ascendente para texto
        ascending = not (sort_col in ['Taxa (%)', 'Matriculados', 'Inscritos'])
        table_df = table_df.sort_values(sort_col, ascending=ascending)

    # Exibir tabela
    st.dataframe(
        table_df,
        hide_index=True,
        use_container_width=True,
        height=min(400, 100 + len(table_df) * 35)
    )