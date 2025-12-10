from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# --- CONFIGURAÇÃO DA CONEXÃO ---
# Formato: postgresql://user:password@localhost:port/database_name
DATABASE_URL = "postgresql://user_b2b:password_secure@localhost:5432/b2b_leads_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- DEFINIÇÃO DAS TABELAS (MODELS) ---

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True, index=True, nullable=False) # ex: stripe.com
    name = Column(String, nullable=True)

    # Dados Enriquecidos (JSONB é super poderoso no Postgres para dados variáveis)
    tech_stack = Column(JSON, nullable=True) # ex: {"cms": "WordPress", "frontend": "React"}
    location_data = Column(JSON, nullable=True) # ex: {"lat": 41.15, "lon": -8.62, "city": "Porto"}

    # Status do Processamento
    status = Column(String, default="pending") # pending, processing, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# --- FUNÇÃO PARA CRIAR AS TABELAS ---
def init_db():
    print("⏳ A conectar ao PostgreSQL e a criar tabelas...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso! A DB está pronta.")
    except Exception as e:
        print(f"❌ Erro ao conectar à DB: {e}")

if __name__ == "__main__":
    init_db()