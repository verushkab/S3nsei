
# 🤖 S3nsei: Bot de Discord para Estudiantes de AWS

S3nsei es un bot creado para ayudar a estudiantes del curso **AWS re/Start**, recordando tareas, compartiendo tips, respondiendo comandos y motivando la participación dentro de Discord. Fue construido con `discord.py`, y se le añadió AWS para hacerlo mas natural al momento de responder preguntas sobre servicios y utilizar almacenamiento en la nube.

---

## 🚀 Requisitos

- Python 3.8+
- Cuenta de Discord (con permisos para crear un bot)
- Cuenta de AWS

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
BOT_ID=el_bot_id_aqui
BOTALIAS_ID=tu_bot_alias_aqui
LOCALE_ID=tu_locale_id_aqui
```

⚠️ No lo compartas ni lo subas a GitHub.

---

## ▶️ Ejecutar el bot

```bash
python3 run.py
```

---

## ✅ Comandos disponibles

- `/tarea` → Muestra la tarea próxima
- `/recordatorio` → Envía un mensaje corto con la tarea
- Puede responder información sobre `AWS` 

---

## 🌟 En desarrollo

- Automatización de tips y recordatorios
- Comandos personalizados por estudiante

---

## 👩‍🏫 Autor

Creado por Veruzka B, estudiante de AWS re/Start 2025.