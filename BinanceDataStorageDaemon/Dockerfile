FROM python:3.7.3
RUN mkdir /BinanceDataStorageDaemon
RUN mkdir /BinanceDataStorageDaemon/logs
COPY requirements.txt /BinanceDataStorageDaemon/
WORKDIR /BinanceDataStorageDaemon
RUN pip install --upgrade pip
RUN pip install -r requirements.txt 
COPY . /BinanceDataStorageDaemon/
CMD ["python", "main.py"]