
# 🤖 S3nsei: Bot de Discord para Estudiantes de AWS

S3nsei es un bot creado para ayudar a estudiantes del curso **AWS re/Start**, recordando tareas, compartiendo tips, respondiendo comandos y motivando la participación dentro de Discord. Fue construido con `discord.py`, y empaquetado con Docker para facilitar su despliegue.

---

## 🚀 Requisitos

- Python 3.8+
- Docker (opcional para empaquetado)
- Cuenta de Discord (con permisos para crear un bot)
- Cuenta de AWS (si deseas conectarlo con servicios en la nube)

---

## 🐍 Crear entorno virtual

```bash
cd Bot/
python3 -m venv venv
source venv/bin/activate
```

---

## 📦 Instalar dependencias

```bash
pip install -r requirements.txt
```

Contenido de `requirements.txt`:

```
discord.py
python-dotenv
```

---

## 🔐 Configurar variables de entorno

Crear un archivo `.env` en la carpeta `Bot/` con el siguiente contenido:

```
DISCORD_TOKEN=tu_token_secreto_aqui
```

⚠️ No lo compartas ni lo subas a GitHub.

---

## ▶️ Ejecutar el bot

```bash
python bot.py
```

---

## 🐳 Docker (opcional)

### Crear imagen Docker:

```bash
docker build -t s3nsei-bot .
```

### Ejecutar contenedor:

```bash
docker run --env-file .env s3nsei-bot
```

---

## ✅ Comandos disponibles

- `!hola` → Responde con un saludo
- `!tarea` → Muestra la tarea próxima
- `!recordatorio` → Envía un mensaje corto con la tarea
- `!tip` → Muestra un tip de AWS
- `!agregar_tarea` (solo para roles permitidos) → Añade tareas a la lista

---

## 🌟 En desarrollo

- Respuestas automáticas con Amazon Lex
- Conexión con servicios de AWS como S3 o DynamoDB
- Automatización de tips y recordatorios
- Comandos personalizados por estudiante

---

## 👩‍🏫 Autor

Creado por [tu nombre], estudiante de AWS re/Start 2025.