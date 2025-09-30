# syntax=docker/dockerfile:1

# Development target
FROM node:20-alpine AS dev
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . /app
EXPOSE 5173
# Make Vite listen on all interfaces (container)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# Prodction build
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . /app

ARG VITE_API_URL=/api
ENV VITE_API_URL=${VITE_API_URL}
RUN npm run build

FROM nginx:1.27-alpine AS prod
# Copy build output
COPY --from=build /app/dist /usr/share/nginx/html
# Nginx config to proxy /api -> backend:8000
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
