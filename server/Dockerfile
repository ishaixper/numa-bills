FROM python
WORKDIR /app
ADD requirements.txt ./
RUN pip install -r requirements.txt

ADD bills bills
ADD numa numa
ADD templates templates
ADD manage.py ./
CMD python manage.py runserver 0.0.0.0:$PORT
