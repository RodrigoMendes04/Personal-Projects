from celery_config import app
from models import SessionLocal, Company, init_db
from scanner import TechScanner
from crm_connector import send_to_hubspot


# Inicializa a DB quando o Worker arranca
init_db()

@app.task(name='tasks.analyze_domain')
def analyze_domain(domain):
    """
    Esta função vai ser executada pelo Worker, não pelo teu script principal.
    """
    print(f"⚙️ [WORKER] A iniciar processamento de: {domain}")

    # Cada tarefa tem de abrir a sua própria sessão de DB
    db = SessionLocal()
    scanner = TechScanner()

    try:
        # 1. Buscar ou Criar Empresa
        company = db.query(Company).filter(Company.domain == domain).first()
        if not company:
            company = Company(domain=domain, status="processing")
            db.add(company)
            db.commit()
            db.refresh(company)

        # 2. Executar o Scanner (A parte lenta!)
        tech_stack = scanner.scan_url(domain)

        # 3. Guardar Resultados
        company.tech_stack = tech_stack

        if "Error: Unreachable" in tech_stack:
            company.status = "failed"
        else:
            company.status = "completed"

        db.commit()
        print(f"✅ [WORKER] Concluído: {domain}")

        if company.status == "completed":
            print(f"📤 [WORKER] A enviar {domain} para o CRM...")
            send_to_hubspot(domain, tech_stack)

        return f"Processed {domain}"


    except Exception as e:
        print(f"❌ [WORKER] Erro em {domain}: {e}")
        db.rollback()
        return f"Error {domain}"
    finally:
        db.close()