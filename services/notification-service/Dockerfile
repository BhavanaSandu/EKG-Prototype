# ===== Build Stage =====
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies (production only)
RUN npm install --only=production

# Copy application code
COPY . .

# ===== Production Stage =====
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy only production dependencies and app code from build stage
COPY --from=build /app .

# Expose port (adjust for your service)
EXPOSE 8085   
# Start the application
CMD ["node", "index.js"]
