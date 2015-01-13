CifraClubScraper
================

Obtém os dados das cifras do cifraclub e exporta para csv.

Pré-requisitos
--------------

1. Ter o mongodb instalado.

Teste com o comando ```mongo  -version``` ex:
 ```C:\Users\user>mongo -version```

 ```MongoDB shell version: 2.6.4```

Instalação dos pacotes python
-----------------------------
1. No diretório do projeto executar: ```pip install -r requirements.py```

Criação da base no mongod
-------------------------

1. Inicializar o serviço ```mongod```
2. Executar o comando mongo ```mongo```
3. Criar a base de dados ```use scrapy```
4. Sair ``` quit() ```

Scrape dos dados
----------------

1. No diretório do projeto executar: ```python main.py```

Exportação dos dados
--------------------

1. ```mongoexport --db scrapy --collection musicas --csv --fieldFile ./fields.txt --out ./musicas.csv```
