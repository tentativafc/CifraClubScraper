# -*- coding: utf-8 -*-
__author__ = 'marcelo'

from pymongo import MongoClient

from DadosMusicaisScraper.settings import *
from utils import *


client = MongoClient(MONGODB_URI)
db = client[MONGODB_DATABASE]
colecao_dicionario = db[MONGODB_COLLECTION_DA]

import logging

LOG_FILENAME = 'atualizador.log'
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.ERROR)

# TODO Talvez tenha que trazer o tom, caso haja diferencas entre os acordes e os acordes especificos do tom.


def traduzir_acordes(registros):
    for registro in registros:
        id = registro['_id']

        try:
            # atualizamos o registro com os dados dos ratings do youtube.
            desenho_acorde, lista_idx_notas, lista_notas, foi_sucesso, mensagem = obter_desenho_lista_idx_notas(id)
            dictUpdate = {"desenho_acorde": desenho_acorde, "lista_idx_notas": lista_idx_notas,
                          "lista_notas": lista_notas,
                          "foi_sucesso": foi_sucesso, "mensagem": mensagem}

        except BaseException as exc:
            dictUpdate = {"desenho_acorde": desenho_acorde, "lista_idx_notas": [],
                          "foi_sucesso": False, lista_notas: [], "mensagem": mensagem}

            logging.error("Erro ao processar o registro <%s>. Detalhes: %s..." % (id, exc))

        finally:
            colecao_dicionario.update({"_id": id}, {'$set': dictUpdate}, upsert=True)


if __name__ == "__main__":
    # # REGISTROS QUE NAO FORAM PROCESSADOS OU QUE FORAM PROCESSADAS COM ERRO
    # query = {"$or": [{"foi_sucesso": {"$exists": 0}}, {"foi_sucesso": False}]}
    # # REGISTROS QUE NAO FORAM PROCESSADOS
    # query = {"desenho_acorde": {"$exists": 0}}
    # REGISTROS QUE FORAM PROCESSADOS COM SUCESSO
    query = {"foi_sucesso": True}

    registros = colecao_dicionario.find(query)
    qtd_registros = registros.count()

    import concurrent.futures

    qtd_registros_por_thread = 50
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(0, qtd_registros, qtd_registros_por_thread):
            idx = 0
            lista_processar = []
            for registro in registros:
                lista_processar.append(registro)
                idx = idx + 1
                if idx >= qtd_registros_por_thread:
                    break

            executor.submit(traduzir_acordes, lista_processar)





