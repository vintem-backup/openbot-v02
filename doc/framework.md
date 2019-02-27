# Framework
>*The pandazord structure*

[Pandazord](../README.md)

```


├── php-app
├   ├── index.php
│   └── static.html
└── proxy
    └── conf.d
        └── default.conf



```

        root/
            README.md
                        
            app/
                __init__.py
                app.py
                environment
                requirements.txt

                getdata/
                    Dockerfile
                    getdata.py
                    requirements.txt
            
                src/
                    __init__.py
                    strategies/
                        <strategy_1>/
                            __init__.py
                            <strategy_1>.py
                            <strategy_1_BT>.py
                            <strategy_1>.yml
                        ...
                        charlie/
                            __init__.py
                            charlie.py
                            charlie_BT.py
                            charlie.yml

                worker/
                    Dockerfile
                    worker.py
                    requirements.txt
            
            dev/
                notebooks/
            
            setup/
                aws/

> ### app/
- **app.py** | Dá *"start"* na aplicação:
>>1 - Checka se o banco de dados está ativado e o ativa, caso não esteja.  
>>2 - Faz a leitura, a partir do banco de dados, do index **master***    
        *Por hora um "container provisório" escreverá as alterações no index master.