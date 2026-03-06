# Iniciar alembic
init:
	alembic init migrations

# Generar migración
migrate:
	alembic revision --autogenerate -m "$(MSG)"

# Aplicar migración
upgrade:
	alembic upgrade head
