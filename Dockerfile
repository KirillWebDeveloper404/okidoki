FROM python

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000

CMD [ "python", "-u", "manage.py", "runserver", "0.0.0.0:8000" ]