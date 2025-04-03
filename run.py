import os
import sys
import subprocess

# Garantir que o diretório atual esteja no PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Executar streamlit diretamente usando subprocess
if __name__ == "__main__":
    subprocess.run(["streamlit", "run", "app.py"])