# Plano de refatoração

## Junho 2019

### Panorama geral:
  
* [ ] Finalizar container que adquire os dados (1m) da binance e os armazena no DB (BinanceStorageDaemon)
* [x] Renomear tabelas
* [x] Renomear funções
* [ ] Iniciar construção do container BinanceTrader

### Por programa:

#### run.py
* [x] Adicionar identação para os "modes"
* [x] Adicionar deleção e cópia da pasta "modules"

#### modules.general_functions.binance_klines_to_postgres_klines
* [ ] Adicionar conversor para UTC (para o cenário em que o servertime da binance não esteja em UTC)

#### modules.general_functions.binance_functions
* [ ] Corrigir contagem de requests com ***response.headers['X-MBX-USED-WEIGHT']***
        Isso propagará para todas as funções que fazem, contam, calculam requests à binance,
        pois eta variável retorna o peso total das requests feitas em 1 min a partir de 1 IP.
        Portanto, ao atingir certo limite, basta qualquer função que realize requests à binance
        parar por 1 min.

#### modules.general_functions.log_handler
* [ ] Melhorar namespacing buscando respectiva pasta de logs, criando-a se náo existir

## Julho 2019