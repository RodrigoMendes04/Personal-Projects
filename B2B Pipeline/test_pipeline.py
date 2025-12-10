from models import SessionLocal, Company, init_db
from scanner import TechScanner

def process_domain(domain):
    # 1. Iniciar Sessão na DB
    db = SessionLocal()
    scanner = TechScanner()

    try:
        # 2. Verificar se a empresa já existe, se não, cria
        company = db.query(Company).filter(Company.domain == domain).first()
        if not company:
            print(f"📝 Criando registo para: {domain}")
            company = Company(domain=domain, status="processing")
            db.add(company)
            db.commit()
            db.refresh(company) # Atualiza o objeto com o ID gerado
        else:
            print(f"🔄 Atualizando registo existente: {domain}")

        # 3. Rodar o Scanner (A magia acontece aqui)
        tech_stack = scanner.scan_url(domain)

        # 4. Atualizar a Base de Dados
        company.tech_stack = tech_stack

        if "Error: Unreachable" in tech_stack:
            company.status = "failed"
        else:
            company.status = "completed"

        db.commit()
        print(f"✅ Sucesso! Tecnologias de {domain}: {tech_stack}")

    except Exception as e:
        print(f"💥 Erro crítico: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Garante que as tabelas existem
    init_db()

    # Lista de domínios para testar
    targets = [
        "wordpress.org",   # Deve detetar WordPress
        "shopify.com",     # Deve detetar Shopify/Cloudflare
        "react.dev",       # Deve detetar React
        "stripe.com"       # Deve detetar Stripe
    ]

    print("--- 🚀 INICIANDO PIPELINE DE TESTE ---")
    for domain in targets:
        process_domain(domain)
        print("-" * 30)