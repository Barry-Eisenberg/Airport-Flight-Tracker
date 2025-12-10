# Frontend Dockerfile for Railway deployment
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Set the backend API URL for the build
ARG VITE_API_URL=https://airport-flight-tracker-production.up.railway.app/api/v1
ENV VITE_API_URL=$VITE_API_URL

# Build the application
RUN npm run build

# Production stage with nginx
FROM nginx:alpine

# Copy custom nginx config as template
COPY nginx.conf /etc/nginx/templates/default.conf.template

# Copy built files from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Railway provides PORT env var - nginx will substitute it
ENV PORT=80

# Start nginx (entrypoint handles envsubst on templates)
CMD ["nginx", "-g", "daemon off;"]
