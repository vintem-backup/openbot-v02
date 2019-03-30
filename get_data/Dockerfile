FROM python:3.7
COPY get_data/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY lib/ lib/
COPY get_data/ /
<<<<<<< HEAD
CMD (python ${stock_exchange}.py)
=======
CMD (python ${stock_exchange}_requester.py)
>>>>>>> 2a5c0de7750ec1dddcde9ff35ee40e771d0cc256
#