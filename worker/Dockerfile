FROM python:3.7
COPY worker/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY lib/ lib/
COPY worker/ /
CMD (python ${strategy}.py)
#