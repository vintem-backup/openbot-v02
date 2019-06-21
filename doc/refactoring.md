# Plano de refatoração

## Junho 2019

### Panorama geral:
  
* [ ] Finalizar container que adquire os dados (1m) da binance e os armazena no DB (BinanceStorageDaemon)
* [x] Renomear tabelas
* [x] Renomear funções
* [ ] Iniciar construção do container BinanceTrader

### Por programa:

#### run.py
* [ ] Adicionar identação para os "modes"
* [ ] Adicionar cópia da pasta "modules"

#### modules.general_functions.binance_klines_to_postgres_klines
* [ ] Adicionar conversor para UTC (para o cenário em que o servertime da binance não esteja em UTC)

## Julho 2019