FROM python
RUN apt-get update && apt-get install nginx supervisor vim -y
RUN pip install uwsgi
# setup all the configfiles
#RUN echo "daemon off;" >> /etc/nginx/nginx.conf
#COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/

WORKDIR /app
ADD requirements.txt ./
RUN pip install -r requirements.txt

ADD bills bills
ADD numa numa
# ADD templates templates
ADD manage.py ./
ADD uwsgi.ini ./
ADD uwsgi_params ./
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/default

#CMD python manage.py runserver 0.0.0.0:$PORT

#CMD uwsgi --http :$PORT --module numa.wsgi
RUN python manage.py collectstatic
EXPOSE 80
CMD ["supervisord", "-n"]
