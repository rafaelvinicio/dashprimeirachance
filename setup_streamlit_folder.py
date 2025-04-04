import os

# Criar diretório .streamlit se não existir
streamlit_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".streamlit")
if not os.path.exists(streamlit_dir):
    os.makedirs(streamlit_dir)
    print(f"Diretório criado: {streamlit_dir}")
else:
    print(f"Diretório já existe: {streamlit_dir}")

# Verificar se o arquivo config.toml existe
config_file = os.path.join(streamlit_dir, "config.toml")
if not os.path.exists(config_file):
    with open(config_file, "w") as f:
        f.write("""[theme]
primaryColor="#0050B3"
backgroundColor="#F8FAFC"
secondaryBackgroundColor="#FFFFFF"
textColor="#2E3A59"
font="Segoe UI"
base="light"

[server]
enableStaticServing = true
""")
    print(f"Arquivo criado: {config_file}")
else:
    print(f"Arquivo já existe: {config_file}")