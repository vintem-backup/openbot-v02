FROM python:3.7
COPY worker/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY lib/ lib/
COPY get_data/ /
CMD (python ${stock_exchange}.py)