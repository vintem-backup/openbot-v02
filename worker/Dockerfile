FROM python:3.7
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . /worker
WORKDIR /worker
COPY src/* worker/
CMD python main.py 
#deve acrescentar argumentos ($strategy, $state, $market e $stock_exchange) no comando