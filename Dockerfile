FROM python:3.12.2

# Setting Working Directory
WORKDIR /app

# Requirement Files into Container
COPY requirements.txt /app/


# Installation of dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Copy the current directory contents into the folder
COPY . /app/


# Expose the port flask runs on
EXPOSE 5000

# Settings the flask app file
ENV FLASK_APP=run.py 

# Setting the current environment type of project
ENV FLASK_ENV=development

# To Run the application
CMD [ "flask", "run", "--host=0.0.0.0"]