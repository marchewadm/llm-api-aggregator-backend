ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION} AS build

WORKDIR /app

COPY requirements/requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . ./

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]