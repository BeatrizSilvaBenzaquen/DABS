# Dockerfile

FROM python:3

LABEL maintainer="beatrizsilvabenzaquen.com"

COPY requirements.txt ./

RUN apt update
RUN apt install python3 -y
RUN pip install --no-cache-dir -r requirements.txt

COPY DevAssBCS.py ./

ENTRYPOINT ["python","./DevAssBCS.py"]