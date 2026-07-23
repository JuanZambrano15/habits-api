# Habits API

API REST para gestión de hábitos con recordatorios automáticos y analíticas de cumplimiento, construida con Django REST Framework y PostgreSQL.

🔗 **API en vivo:** https://habits-api-sr2u.onrender.com/api/docs/
> Nota: al estar en el plan gratuito de Render, el servicio "duerme" tras 15 minutos sin tráfico — la primera petición puede tardar hasta 1 minuto en responder.

## Qué demuestra este proyecto

- Modelado de datos relacional normalizado (catálogo de días, M2M, registros con estado)
- API REST completa con autenticación JWT (rotación + blacklist de tokens)
- Tarea programada en background con Celery + Redis (revisión diaria de recordatorios)
- Analíticas calculadas (rachas de cumplimiento, % de cumplimiento por hábito)
- Tests automatizados (unitarios + integración) con pytest y factory_boy
- Containerización con Docker multi-stage (usuario sin privilegios, imagen optimizada)
- CI/CD con GitHub Actions (tests + build de imagen en cada PR)
- Documentación OpenAPI autogenerada (Swagger UI + Redoc)
- Deploy en producción (Render, PostgreSQL administrado)

## Stack técnico

Django 5.2 · Django REST Framework · PostgreSQL · Redis · Celery · JWT (SimpleJWT) · pytest + factory_boy · Docker · GitHub Actions · drf-spectacular

## Decisiones técnicas y por qué

**Modelo de usuario personalizado desde el inicio.** Cambiar `AUTH_USER_MODEL` después de la primera migración es costoso en Django; extenderlo desde el día 1 (con un campo de zona horaria pensado para los recordatorios) evita esa migración riesgosa más adelante.

**Frecuencia de hábitos como relación M2M, no como campo de texto.** Permite hábitos con días específicos (ej. lunes/miércoles/viernes) en vez de solo "diario/semanal", y refleja mejor una relación muchos-a-muchos real en el diseño.

**Separación en apps `accounts`, `habits` y `analytics`.** Cada una con una responsabilidad clara; la lógica de cálculo de rachas vive en un módulo `services.py` separado de las vistas, para que sea testeable de forma aislada sin necesitar un request HTTP.

**JWT con rotación y blacklist**, en vez de solo tokens de larga duración. Limita la ventana de exposición si un token es comprometido, sin sacrificar la experiencia de uso.

**Rachas y porcentajes calculados al vuelo**, no cacheados. Para el volumen de datos de un usuario individual, el costo de recalcular es insignificante, y se evita el riesgo de que un valor cacheado quede desincronizado. Con mayor escala, sería razonable cachear estos valores y actualizarlos vía signals.

**Dockerfile multi-stage con usuario sin privilegios.** Reduce el tamaño de la imagen final (las herramientas de compilación quedan solo en la etapa de build) y evita correr el proceso como root dentro del contenedor.

**Celery/Redis probados localmente, no desplegados en producción.** Los background workers no están disponibles en el plan gratuito de Render (arrancan en $7/mes); el ciclo completo de recordatorios está verificado en el entorno de Docker Compose local (ver sección de evidencia abajo).

## Cómo correrlo localmente

\`\`\`bash
git clone https://github.com/JuanZambrano15/habits-api.git
cd habits-api
cp .env.example .env   # completa las variables

docker compose up --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
\`\`\`

La API queda disponible en `http://localhost:8000/api/docs/`.

## Tests

\`\`\`bash
pytest --cov=apps
\`\`\`

## CI/CD

Cada Pull Request corre automáticamente la suite de tests con PostgreSQL y Redis como servicios de GitHub Actions, y construye la imagen Docker si los tests pasan. Ver `.github/workflows/ci.yml`.