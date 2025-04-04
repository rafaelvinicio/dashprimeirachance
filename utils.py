import pandas as pd
import numpy as np

# Constantes globais
CATEGORY_COLORS = {
    "Excelente": "#36B37E",
    "Médio": "#FFAB00",
    "Baixo": "#FF5630"
}

# Função para criar dados de exemplo
def create_sample_data():
    """
    Cria dados fictícios mais robustos para quando não for possível acessar a fonte real
    """
    # Criar dados fictícios para GREs
    gres = [f"{i}" for i in range(1, 17)]  # GREs de 1 a 16

    # Lista de cidades
    cidades = [
        "Recife", "Olinda", "Jaboatão", "Paulista", "Caruaru", "Petrolina",
        "Garanhuns", "Vitória", "Cabo", "Serra Talhada", "Salgueiro",
        "Araripina", "Goiana", "Bezerros", "Gravatá", "Carpina"
    ]

    # Criar dados de 150 escolas
    data = []
    for i in range(1, 151):
        gre = np.random.choice(gres)
        cidade = np.random.choice(cidades)
        escola = f"Escola Estadual {i}"
        matriculas = np.random.randint(30, 300)

        # Distribuição de categorias (excelente: 25%, médio: 45%, baixo: 30%)
        categoria = np.random.choice([1, 2, 3], p=[0.3, 0.45, 0.25])

        if categoria == 3:  # Excelente (>= 85%)
            taxa = 85 + np.random.random() * 15
            inscritos = int(matriculas * (taxa / 100))
        elif categoria == 2:  # Médio (50-85%)
            taxa = 50 + np.random.random() * 35
            inscritos = int(matriculas * (taxa / 100))
        else:  # Baixo (< 50%)
            taxa = 10 + np.random.random() * 40
            inscritos = int(matriculas * (taxa / 100))

        data.append({
            'GRE': gre,
            'CIDADE': cidade,
            'ESCOLA': escola,
            'MATRICULAS': matriculas,
            'INSCRITOS': inscritos,
            'TAXA_EFICIENCIA': taxa,
            'CATEGORIA': "Excelente" if categoria == 3 else "Médio" if categoria == 2 else "Baixo"
        })

    return pd.DataFrame(data)

# Função para calcular categoria de eficiência
def calculate_efficiency_category(taxa):
    """
    Determina a categoria de eficiência com base na taxa
    """
    if taxa >= 85:
        return "Excelente"
    elif taxa >= 50:
        return "Médio"
    else:
        return "Baixo"

# Função para preparar dataframe para visualização
def prepare_dataframe(df, filtro_gre="Todas", filtro_cidade="Todas", display_option="Escolas"):
    """
    Prepara e filtra o dataframe conforme os filtros selecionados
    """
    # Aplicar filtro de GRE
    filtered_df = df.copy()
    if filtro_gre != "Todas":
        filtered_df = filtered_df[filtered_df['GRE'] == filtro_gre]

    # Aplicar filtro de cidade
    if display_option == "Escolas" and filtro_cidade != "Todas":
        filtered_df = filtered_df[filtered_df['CIDADE'] == filtro_cidade]

    # Preparar dados agrupados conforme visualização selecionada
    if display_option == "Escolas":
        # Para escolas, usamos os dados já filtrados
        grouped_df = filtered_df.copy()
        column_name = 'ESCOLA'
    elif display_option == "Cidades":
        # Agrupar por cidade
        grouped_df = filtered_df.groupby('CIDADE').agg({
            'INSCRITOS': 'sum',
            'MATRICULAS': 'sum'
        }).reset_index()
        grouped_df['TAXA_EFICIENCIA'] = (grouped_df['INSCRITOS'] / grouped_df['MATRICULAS'] * 100).clip(0, 100)
        column_name = 'CIDADE'
    else:  # GREs
        # Agrupar por GRE
        grouped_df = filtered_df.groupby('GRE').agg({
            'INSCRITOS': 'sum',
            'MATRICULAS': 'sum'
        }).reset_index()
        grouped_df['TAXA_EFICIENCIA'] = (grouped_df['INSCRITOS'] / grouped_df['MATRICULAS'] * 100).clip(0, 100)
        column_name = 'GRE'

    # Adicionar categorias aos dados agrupados
    conditions = [
        (grouped_df['TAXA_EFICIENCIA'] < 50),
        (grouped_df['TAXA_EFICIENCIA'] >= 50) & (grouped_df['TAXA_EFICIENCIA'] < 85),
        (grouped_df['TAXA_EFICIENCIA'] >= 85)
    ]
    categories = ["Baixo", "Médio", "Excelente"]
    grouped_df['CATEGORIA'] = np.select(conditions, categories, default="N/A")

    return filtered_df, grouped_df, column_name