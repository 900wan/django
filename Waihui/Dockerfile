FROM python:2.7.13
COPY . .
RUN pip intall --trusted-host pypi.python.org -r requirements.txt
EXPOSE 80
CMD ["python", "manage.py", "runserver"]