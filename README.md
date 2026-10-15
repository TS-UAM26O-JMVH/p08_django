# Práctica 8: Microservicios con Django REST Framework, PostgreSQL, Docker y Gateway

Proyecto backend basado en una arquitectura de microservicios con Django REST Framework, PostgreSQL, Docker y un API Gateway (Nginx), que incorpora autenticación JWT, múltiples bases de datos y documentación mediante Swagger.
---
## 🚀 Características principales

> Arquitectura de Microservicios: Separación de responsabilidades con servicios independientes (servicio_auth, servicio_usuarios, servicio_productos).

> Enrutamiento Centralizado: Uso de un API Gateway (Nginx) para unificar el acceso a las APIs a través de un único punto de entrada (localhost/api/...).

> Contenedorización con Docker Compose: Orquestación de múltiples contenedores de aplicaciones y bases de datos PostgreSQL aisladas (postgres_auth, postgres_usuarios, postgres_productos).

> Documentación interactiva: Swagger UI integrado para cada microservicio.
---
## 🛠️ Requisitos previos

>Docker y Docker Compose instalados en tu sistema.

>Python 3.11+ (para manejo local con entorno virtual).
---
## 🛠️ Instrucciones de Configuración y Ejecución

Sigue estos pasos en tu terminal para poner en marcha el proyecto en tu equipo local:

### 1. Clonar el repositorio y ubicarse en la ruta del proyecto
```
git clone <url-de-tu-repositorio>
cd <nombre-de-la-carpeta>/back_end_django
```

### 2. Activar el entorno virtual (Opcional para comandos locales)
```
source venv/bin/activate
```

Para desactivar el entorno virtual:
```
deactivate
```

### 3. Configurar los archivos .env

Asegúrate de que cada microservicio (servicio_auth, servicio_usuarios, servicio_productos) cuente con su archivo .env configurado correctamente apuntando a su respectivo contenedor de base de datos (postgres_auth, postgres_usuarios, postgres_productos).

### 4. Construir y levantar los contenedores con Docker Compose
```
docker compose up --build -d
```

### 5. Ejecutar las migraciones de las bases de datos

Aplica las migraciones correspondientes a cada microservicio:
```
docker compose exec servicio_auth python manage.py migrate
docker compose exec servicio_usuarios python manage.py migrate
docker compose exec servicio_productos python manage.py migrate
```
---

## 🛑 Administración de Contenedores

Detener y eliminar los contenedores de forma limpia:
```
docker compose down
```

Ver el estado de los contenedores activos:
```
docker ps
```

Revisar logs de un servicio en específico (ej. autenticación):
```
docker compose logs servicio_auth
```
---

## 🌐 Endpoints y Documentación Swagger

Puedes acceder a la documentación interactiva de cada microservicio a través del Gateway:

>Servicio de Autenticación: http://localhost/api/auth/swagger/

>Servicio de Usuarios: http://localhost/api/usuarios/swagger/ (según configuración)

>Servicio de Productos: http://localhost/api/productos/swagger/ (según configuración)

👨‍💻 Autor

Desarrollado por Juan Valentin.