FROM python:3.7.3-alpine3.9
ENV PYTHONUNBUFFERED 1
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev
RUN mkdir /code
COPY requirements.txt /code/
WORKDIR /code
RUN pip install --upgrade pip
RUN pip install -r requirements.txt 
COPY ./${DataHandlerDir} /code/
COPY entrypoint /code/
RUN chmod +x entrypoint
CMD ["sh", "entrypoint"]