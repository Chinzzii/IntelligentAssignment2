# Set the base image to Python 3.8
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all the files from your project into the container
COPY . /app

# Install the necessary Python dependencies
RUN pip install -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Run the Flask application using python app.py
CMD ["python", "app/app.py"]
