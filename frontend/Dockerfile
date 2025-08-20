# Build stage
FROM node:20 as build
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json* frontend/yarn.lock* /app/
RUN npm i
COPY frontend /app
RUN npm run build

# Serve stage
FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
# Simple SPA fallback
RUN rm -f /etc/nginx/conf.d/default.conf
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 5173
CMD ["nginx", "-g", "daemon off;"]
