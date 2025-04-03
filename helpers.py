# Funções auxiliares para o dashboard
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Constantes globais
CATEGORY_COLORS = {
    "Excelente": "#36B37E",
    "Médio": "#FFAB00",
    "Baixo": "#FF5630"
}

# Mova as funções auxiliares para cá:
# - create_heatmap
# - create_gauge_chart
# - create_progress_timeline
# etc.