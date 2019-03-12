# Data structure
>*Data what we need and the data what we are producing*

[Pandazord](../README.md)

[PT_br]

## 1 - master

Deve ser um index do elasticsearch cujos documentos agrupam parâmetros de cada uma das operações rodando ou que já rodaram no sistema (nota para a possibildade desse dado poder ser apagado, opcionalmente). A id deste documento deve ser o nome da estratégia.

### Exemplo

master/doc/charlie/_source

        {   
            "state": "<off>","<bt>","<trade>","<both>",
            "market": "btcusdt",
            "stock_exchenge": "binance",
            "position": "<buy_side>","<sell_side>",
            "allotment":"1000",
            "n_trades":"0",
            "parameters": {
                "price": {
                    "source": "close",
                    "n_samples": "3",
                    "from_samples": "5"
                },
                "indicators_values": {
                    "short_ma": "23",
                    "long_ma": "2345"
                },
                "stop_config": {
                    "stop_price": "3400.45",
                    "stop_tolerance": "5",
                    "price":{
                        "source": "high",
                        "n_samples": "3",
                        "from_samples": "5"
                    },
                    "tranding_stop": {
                        "source": "low",
                        "n_samples": "3",
                        "from_samples": "5"
                    }
                }



            }

    
        }
#