import os
import sys

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database.seed import seed_database

if __name__ == "__main__":
    print("Iniciando seed do banco de dados...")
    seed_database()
    print("Seed concluído com sucesso!") 