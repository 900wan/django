# Use an official Python runtime as a parent image
FROM python:2.7-slim
# No need to set WORKDIR
# Copy the current directory contents into the container at /app
COPY . .
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 80
# Define environment variable
CMD ["python", "manage.py", "runserver"]