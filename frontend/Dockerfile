# Этап 1: Сборка приложения
FROM node:20-alpine AS builder

# Рабочая директория
WORKDIR /app

# Копируем конфиги и index.html
COPY package.json pnpm-lock.yaml ./
COPY tsconfig*.json vite.config.ts ./
COPY index.html .

# Устанавливаем pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Устанавливаем зависимости
RUN pnpm install

# Копируем оставшиеся файлы
COPY public ./public
COPY src ./src
ARG VITE_API
ENV VITE_API=$VITE_API

# Сборка проекта
RUN pnpm run build

# Этап 2: Продакшен сервер на Nginx
FROM nginx:alpine AS production

# Копируем собранный фронт
COPY --from=builder /app/dist /usr/share/nginx/html

# Настраиваем Nginx (опционально — если нужно SPA rewrite)
# RUN echo 'server { listen 80; root /usr/share/nginx/html; index index.html; location / { try_files $uri $uri/ /index.html; } }' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
