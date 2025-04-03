import sys
print("Python path:", sys.path)

try:
    import utils
    print("Utils importado com sucesso")
    print("CATEGORY_COLORS:", utils.CATEGORY_COLORS)
except Exception as e:
    print("Erro ao importar utils:", e)

try:
    import visualizations
    print("Visualizations importado com sucesso")
except Exception as e:
    print("Erro ao importar visualizations:", str(e))

print("Teste concluído")