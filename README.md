
# 🤖 S3nsei: Bot de Discord para Estudiantes de AWS

**S3nsei** es un bot creado para ayudar a estudiantes del curso **AWS re/Start**, recordando tareas, compartiendo tips, respondiendo comandos y motivando la participación dentro de Discord. Fue construido con `discord.py` y utiliza servicios de **AWS** como Lambda, DynamoDB, Lex, S3, CloudWatch y más, integrando tecnologías en la nube de forma educativa.

---

## 🚀 Requisitos

- Cuenta de Discord (con permisos para crear un bot)
- Cuenta de AWS con permisos para usar Secrets Manager, ECS, ECR, Lambda, etc.
- Docker (para ejecución local o en la nube)

---

## 🔐 Manejo de secretos

Las credenciales y configuraciones del bot (como el token de Discord) están almacenadas de forma segura en **AWS Secrets Manager**. El bot accede al secreto automáticamente al iniciar, por lo que **no es necesario usar un archivo `.env`**.

---

## 🐳 Ejecutar con Docker

### 📍 Opción 1: Localmente

1. Clona el repositorio:

```bash
git clone https://github.com/tu_usuario/s3nsei.git
cd s3nsei
```

2. Construye la imagen Docker:

```bash
docker build -t s3nsei-bot .
```

3. Ejecuta el contenedor:

```bash
docker run s3nsei-bot
```

Asegúrate de tener credenciales de AWS configuradas localmente (`~/.aws/credentials`) o usar un role/usuario con permisos necesarios para acceder al secreto y servicios de AWS.

---

### ☁️ Opción 2: En una instancia EC2

1. Conéctate a tu instancia EC2.
2. Asegúrate de tener Docker instalado.
3. Clona este repositorio o transfiere el código.
4. Ejecuta los mismos comandos para construir y correr el contenedor.
5. Asegúrate de asociar un **IAM Role** con permisos adecuados a la instancia.

---

### ☁️ Opción 3: En Amazon ECS con Fargate

1. Sube la imagen a Amazon ECR:

```bash
aws ecr create-repository --repository-name s3nsei
docker tag s3nsei-bot:latest <tu_id>.dkr.ecr.<region>.amazonaws.com/s3nsei
docker push <tu_id>.dkr.ecr.<region>.amazonaws.com/s3nsei
```

2. Crea un servicio ECS (tipo Fargate) que apunte a esa imagen.
3. Configura la tarea para que use un **IAM Role** con permisos para acceder a Secrets Manager y otros servicios de AWS.

---

## ✅ Comandos disponibles

- `/tareas` → Muestra las tareas pendientes del curso
- `/recursos` → Muestra tips, links o materiales de apoyo
- `/ayuda` → Muestra una lista de comandos y funciones disponibles
- Puedes interactuar con el bot directamente preguntando sobre **servicios de AWS**, y él te responderá con explicaciones, significados y tips relacionados.

---

## 🌱 En desarrollo

- Automatización de tips por medio de Lambda y Eventbridge.
- Tips personalizados por estudiantes.
- Integración con sitio web educativo y otros servicios como AWS Personalize.

---

## 👩‍🏫 Autor

Creado por **Veruzka B.**, estudiante de AWS re/Start 2025.

---

## 📄 Licencia

MIT © Veruzka B.