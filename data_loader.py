import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse
import gspread
from google.oauth2 import service_account
from gspread_dataframe import get_as_dataframe
from utils import create_sample_data

@st.cache_data(ttl=600)
def load_data():
    """
    Carrega os dados da planilha do Google Sheets ou cria dados de exemplo
    em caso de falha. Faz a limpeza e preparação dos dados.
    """
    try:
        # Conectar com Google Sheets
        sheet_id = "1TGUZU3v9ysTEgx_e8UHkSPl_MHxH9iNXf3AXuJCVVRU"
        sheet_name = "Balanço Atualizado"
        encoded_sheet_name = urllib.parse.quote(sheet_name)
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={encoded_sheet_name}"

        try:
            # Tentativa via pandas
            df = pd.read_csv(url)
        except Exception as e:
            # Falha silenciosa, tentativa via gspread
            try:
                if "gcp_service_account" in st.secrets:
                    credentials = service_account.Credentials.from_service_account_info(
                        st.secrets["gcp_service_account"]
                    )
                    gc = gspread.authorize(credentials)
                    sh = gc.open_by_key(sheet_id)
                    worksheet = sh.worksheet(sheet_name)
                    df = get_as_dataframe(worksheet, evaluate_formulas=True)
                else:
                    # Se não tiver credenciais, use dados de exemplo
                    return create_sample_data()
            except Exception:
                # Criar dados de exemplo sem alertar o usuário
                return create_sample_data()

        # Limpeza e preparação dos dados
        df = df.dropna(how='all')

        # Garantir colunas corretas
        if 'GRE' not in df.columns or 'CIDADE' not in df.columns:
            if len(df) > 0:
                # Primeira linha como cabeçalho
                df.columns = df.iloc[0]
                df = df.drop(df.index[0])

        # Mapeamento padrão
        column_mapping = {
            'GRE': 'GRE',
            'CIDADE': 'CIDADE',
            'ESCOLA': 'ESCOLA',
            'INSCRITOS': 'INSCRITOS',
            'MATRÍCULAS DE 3ª SÉRIE': 'MATRICULAS'
        }

        # Aplicar mapeamento para colunas existentes
        valid_mapping = {col: new_col for col, new_col in column_mapping.items() if col in df.columns}
        df = df.rename(columns=valid_mapping)

        # Converter GRE para string sem decimal
        if 'GRE' in df.columns:
            df['GRE'] = df['GRE'].astype(str).str.replace('.0', '', regex=False)

        # Converter colunas numéricas
        numeric_cols = ['INSCRITOS', 'MATRICULAS']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Remover registros inválidos e GRE 0
        df = df[df['MATRICULAS'] > 0]
        if 'GRE' in df.columns:
            df = df[df['GRE'] != '0']

        # Preenchimento de NaN
        df = df.fillna(0)

        # Calcular a taxa de eficiência
        df['TAXA_EFICIENCIA'] = (df['INSCRITOS'] / df['MATRICULAS'] * 100).clip(0, 100)

        # Categorizar eficiência
        conditions = [
            (df['TAXA_EFICIENCIA'] < 50),
            (df['TAXA_EFICIENCIA'] >= 50) & (df['TAXA_EFICIENCIA'] < 85),
            (df['TAXA_EFICIENCIA'] >= 85)
        ]
        categories = ["Baixo", "Médio", "Excelente"]
        df['CATEGORIA'] = np.select(conditions, categories, default="N/A")

        return df

    except Exception as e:
        # Em caso de erro, retornar dados de exemplo
        return create_sample_data()