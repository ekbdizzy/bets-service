FROM python:3.10
ENV PYTHONUNBUFFERED 1

WORKDIR /bet-maker

COPY requirements.txt /bet-maker/requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 8099

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8099", "--reload"]