# Этап 1: Сборка Vue приложения
FROM node:22-alpine as builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Этап 2: Раздача статики через nginx
FROM nginx:alpine

# Копируем кастомный конфиг nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Копируем собранные файлы
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
