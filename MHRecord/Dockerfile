# Use Python base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /Record

# Copy the backend files to the container
COPY ./backend /Record

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the backend
EXPOSE 8000

# Start the backend server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
