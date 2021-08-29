FROM python:3.9

ENV PYTHONUNBUFFERED=1
RUN mkdir /workspace
COPY ./requirements.txt /workspace/requirements.txt
COPY . /workspace/
WORKDIR /workspace
RUN pip install -r requirements.txt
EXPOSE 5000