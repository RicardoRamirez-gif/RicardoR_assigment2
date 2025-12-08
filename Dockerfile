# Dockerfile content
# Usamos la imagen oficial de Playwright con el tag que coincide con requirements.txt (1.50.0).
FROM mcr.microsoft.com/playwright/python:v1.50.0-jammy

WORKDIR /app
COPY requirements.txt .

# 1. Instala dependencias del Sistema Operativo necesarias manualmente (INCLUYE FUENTES)
# Esto soluciona los problemas de fuentes y librerías que Playwright necesita para ejecutar Chromium.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libnss3 libxss1 libasound2 libatk1.0-0 libgtk-3-0 \
    libgbm-dev libnss3-dev libcups2-dev libxkbcommon-x11-dev \
    ca-certificates \
    fonts-unifont \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 2. Instala librerías Python
RUN pip install --no-cache-dir -r requirements.txt

# 3. INSTALA SOLO LOS BINARIOS DEL NAVEGADOR CHROMIUM. 
# Omite la verificación de dependencias del SO (--with-deps) porque ya las instalamos.
RUN playwright install chromium

# 4. Copia el código fuente restante al contenedor
COPY . .