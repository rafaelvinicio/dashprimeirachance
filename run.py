import os
import sys
import subprocess

# Garantir que o diretório atual esteja no PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Criar diretório .streamlit se não existir
streamlit_dir = os.path.join(current_dir, ".streamlit")
if not os.path.exists(streamlit_dir):
    os.makedirs(streamlit_dir)
    print(f"Diretório criado: {streamlit_dir}")

# Verificar se o arquivo config.toml existe
config_file = os.path.join(streamlit_dir, "config.toml")
if not os.path.exists(config_file):
    with open(config_file, "w") as f:
        f.write("""[theme]
primaryColor="#0050B3"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#FFFFFF"
textColor="#2E3A59"
font="Segoe UI"
base="light"

[server]
enableStaticServing = true
""")
    print(f"Arquivo de configuração do tema criado: {config_file}")

# Executar streamlit diretamente usando subprocess
if __name__ == "__main__":
    print("Iniciando o dashboard...")
    subprocess.run(["streamlit", "run", "app.py"])