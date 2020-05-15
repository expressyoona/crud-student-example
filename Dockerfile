# Use an official Python runtime as a parent image
FROM python:3.6-slim

RUN apt update
RUN apt install -y libpq-dev python3-dev build-essential

# Set the working directory to /app
WORKDIR /app

COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

EXPOSE 5000


# Run app.py when the container launches
CMD ["python", "app.py"]
# CMD ["FLASK_DEBUG=1", "flask", "run", "--host=0.0.0.0"]