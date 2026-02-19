ARG AIRFLOW_VERSION=slim-2.11.1rc2
ARG PYTHON_BASE_VERSION=3.12

FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_BASE_VERSION}

ENV AIRFLOW_HOME=/opt/airflow

COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt