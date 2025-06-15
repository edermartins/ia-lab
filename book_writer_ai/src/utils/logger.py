import logging
import sys
from datetime import datetime

# Configurar o logger
def setup_logger():
    logger = logging.getLogger('book_writer')
    logger.setLevel(logging.DEBUG)

    # Criar formato do log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Handler para arquivo
    log_file = f'logs/book_writer_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Adicionar handlers ao logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Criar diretório de logs se não existir
import os
os.makedirs('logs', exist_ok=True)

# Criar instância do logger
logger = setup_logger() 