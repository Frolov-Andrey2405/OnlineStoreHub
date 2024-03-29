# Use an official Node.js image as a parent image for building frontend assets
FROM node:14 as builder
WORKDIR /code/mysite
COPY mysite/package*.json ./
RUN npm install
COPY mysite/ .
RUN npm run build

# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the backend code to the container
COPY . /code/

# Install Python dependencies
RUN pip install -r /code/requirements.txt

# Copy the built frontend assets from the builder stage
COPY --from=builder /code/mysite/static /code/mysite/static

# Expose the port the app runs on
EXPOSE 8000

# Start the application
CMD ["python", "mysite/manage.py", "runserver", "0.0.0.0:8000"]
