# Use Node.js base image
FROM node:18

# Set the working directory
WORKDIR /app

# Copy the frontend files
COPY ./frontend /app

# Install dependencies
RUN npm install

# Expose port 3000 for the React app
EXPOSE 3000

# Start the React app
CMD ["npm", "start"]
