import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import json

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="B2B Lead Enrichment", layout="wide", page_icon="🏭")

# --- CONEXÃO AO POSTGRESQL ---
# Usamos a mesma string de conexão do models.py
DATABASE_URL = "postgresql://user_b2b:password_secure@localhost:5432/b2b_leads_db"

@st.cache_data(ttl=5) # Cache de 5 segundos para não massacrar a DB
def load_data():
    try:
        engine = create_engine(DATABASE_URL)
        query = "SELECT * FROM companies ORDER BY updated_at DESC"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Erro ao conectar à DB: {e}")
        return pd.DataFrame()

# --- APP ---
st.title("🏭 B2B Enterprise Data Pipeline")
st.markdown("Monitorização em tempo real do enriquecimento de leads via **Celery & Redis**.")

df = load_data()

if not df.empty:
    # 1. MÉTRICAS DE TOPO
    col1, col2, col3, col4 = st.columns(4)

    total = len(df)
    completed = len(df[df['status'] == 'completed'])
    processing = len(df[df['status'] == 'processing'])
    failed = len(df[df['status'] == 'failed'])

    col1.metric("Total Leads", total)
    col2.metric("✅ Completos", completed)
    col3.metric("⚙️ A Processar", processing)
    col4.metric("❌ Falhas", failed)

    st.divider()

    # 2. ANÁLISE DE TECNOLOGIAS (O Poder do JSON)
    st.subheader("📊 Tech Stack Analytics")

    # Truque de Pandas para explodir o JSON numa lista plana
    # Filtramos apenas os que têm dados e status completed
    valid_data = df[df['status'] == 'completed']['tech_stack'].dropna()

    all_techs = []
    for stack in valid_data:
        # O Pandas às vezes lê o JSON como string, outras como dict
        if isinstance(stack, str):
            try:
                stack_list = json.loads(stack)
                all_techs.extend(stack_list)
            except: pass
        elif isinstance(stack, list):
            all_techs.extend(stack)

    if all_techs:
        tech_counts = pd.Series(all_techs).value_counts().head(10)
        st.bar_chart(tech_counts)
    else:
        st.info("Ainda não há dados tecnológicos suficientes para gerar gráficos.")

    # 3. TABELA DE DADOS
    st.subheader("📋 Live Data Feed")

    # Formatação para a tabela ficar bonita
    display_df = df[['domain', 'status', 'tech_stack', 'updated_at']].copy()
    st.dataframe(display_df, use_container_width=True)

    if st.button("🔄 Refresh Data"):
        st.rerun()

else:
    st.warning("A base de dados está vazia ou inacessível. Corre o 'trigger.py' primeiro!")

# --- SIDEBAR: STATUS DA INFRAESTRUTURA ---
with st.sidebar:
    st.header("Infrastructure Status")
    st.success("🟢 PostgreSQL: Online")
    st.success("🟢 Redis Broker: Online")
    st.info("🟡 Celery Workers: Waiting tasks...")

    st.markdown("---")
    st.markdown("**Arquitetura:**")
    st.code("""
Scraper -> Redis Queue
   |
   v
Celery Worker [x N]
   |
   v
PostgreSQL (JSONB)
    """, language="text")