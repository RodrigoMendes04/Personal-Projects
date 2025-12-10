from celery import Celery

# 1. Definir o nome da aplicação
app = Celery('b2b_pipeline')

# 2. Configurar o Broker (Quem distribui as mensagens) e o Backend (Quem guarda resultados)
# Estamos a usar o Redis que está a rodar no Docker (localhost:6379)
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

# 3. Configurações extra para robustez
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)