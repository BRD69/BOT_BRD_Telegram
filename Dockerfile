FROM python:3.12-alpine
WORKDIR /bot_brd
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . /bot_brd
CMD ["python", "bot_main.py"]