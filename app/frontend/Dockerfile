# ETAPA 1: Construcción (Build)
FROM node:22-slim AS build

# Instalamos pnpm globalmente
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

WORKDIR /app

# Copiamos solo los archivos de dependencias para aprovechar el cache
COPY package.json pnpm-lock.yaml ./

# Instalamos dependencias
RUN pnpm install --frozen-lockfile

# Copiamos el resto del código y compilamos
COPY . .
RUN pnpm build

# ETAPA 2: Servidor de Producción (Nginx)
FROM nginx:stable-alpine

# Copiamos los archivos compilados desde la etapa anterior al directorio de Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Opcional: Copiamos una configuración de nginx si tenés rutas con React Router
# (Para que las rutas del SPA funcionen bien al recargar)

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]