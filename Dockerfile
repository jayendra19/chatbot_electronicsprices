# Use an official Python runtime as the base image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy requirements.txt to the working directory
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# Copy the rest of the application code to the working directory
COPY . .

# Copy the NER model to the working directory
COPY ./NER /app/NER



# Set build arguments
ARG API_KEY='my_build key'

# Set environment variables using build arguments
ENV API_KEY=$API_KEY

# Make port 5000 available outside the container

EXPOSE 8501


# Define the command to run the application
CMD ["streamlit", "run", "app.py"]

#if u put -d it ur stramlit will be running on background docker run  -p 8501:8501 -d my-chatbot and 
