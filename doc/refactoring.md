# Plano de refatoração

### Panorama geral:
  
* [x] Finalizar container que adquire os dados (1m) da binance e os armazena no DB (BinanceStorageDaemon)
* [x] Renomear tabelas
* [x] Renomear funções
* [x] Mudar os horários dos logs de utc para local
* [x] Iniciar construção do container BinanceTrader
  * [x] Concepção do algoritmo de backtest
  * [x] Concepção dos modelos de dados
* [ ]Container BinanceTrader
  * [ ] Main
    * [ ] Algoritmo
    * [ ] Código
  * [x] Função indicador
  * [x] Função estratégia
  * [ ] Parse de candles
  * [ ] Logger (?)
  * [ ] Disparador de ordens
  * [ ] Calculadora de montantes

* [ ] Colocar TODOS os nomes de tabelas e afins, que figuram nos códigos, como variáveis de ambiente
* [ ] Adicionar os novos indicadores:
  * [ ] Novo indicador 1
  * [ ] Novo idicador 2
* [ ] Criar os views e models no controller para ajuste de parâmetros e afins
* [ ] Buscar uma solução para visualização dos dados
  * [ ] Plotly
  * [ ] Matplotlib
  * [ ] Tradingview
* [ ] Revisar as docstrings, fazer as que não existirem

### Por programa:

#### run.py
* [x] Adicionar identação para os "modes"
* [x] Adicionar deleção e cópia da pasta "modules"

#### modules.general_functions.binance_klines_to_postgres_klines
* [x] Adicionar conversor para UTC (para o cenário em que o servertime da binance não esteja em UTC)

#### modules.general_functions.binance_functions
* [x] Corrigir contagem de requests com ***response.headers['X-MBX-USED-WEIGHT']***
        Isso propagará para todas as funções que fazem, contam, calculam requests à binance,
        pois eta variável retorna o peso total das requests feitas em 1 min a partir de 1 IP.
        Portanto, ao atingir certo limite, basta qualquer função que realize requests à binance
        parar por 1 min.

#### modules.general_functions.log_handler
* [ ] Melhorar namespacing buscando respectiva pasta de logs, criando-a se não existir