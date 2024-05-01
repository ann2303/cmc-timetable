FROM python:3.11

WORKDIR /api

COPY requirements.txt requirements.txt
RUN apt update -y && apt install -y ghostscript python3-tk libgl1 libglib2.0-0
RUN pip install --upgrade pip setuptools wheel

RUN pip install -r requirements.txt


# Add metadata to the image to describe that the container is listening on port 8000
EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --reload --workers 1