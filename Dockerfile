FROM python:3.9

COPY requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code
CMD ["fastapi", "run", "main.py", "--port", "80"]