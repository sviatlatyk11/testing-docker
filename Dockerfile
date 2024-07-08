# Base image
FROM node:14.17.0-alpine

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy rest of the application
COPY . .

# Build the React app
RUN npm run build

# Expose port 3000 (default for React)
EXPOSE 3000

# Command to run the React app
CMD ["npm", "start"]
