FROM python:3.11

WORKDIR /api

RUN apt update -y && apt install -y ghostscript python3-tk libgl1 libglib2.0-0 locales
RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen && sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
RUN update-locale


# Add metadata to the image to describe that the container is listening on port 8000
EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --reload --workers 1