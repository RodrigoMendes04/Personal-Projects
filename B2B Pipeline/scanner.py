import requests
from bs4 import BeautifulSoup
import re

class TechScanner:
    def __init__(self):
        # Configurar headers para fingir ser um browser real (evita bloqueios 403)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # --- DEFINIÇÃO DAS REGRAS (FINGERPRINTS) ---
        # Podes adicionar mais regras aqui facilmente.
        self.rules = {
            "WordPress": {
                "html": [r"/wp-content/", r"wp-includes", r'name="generator" content="WordPress"'],
                "headers": []
            },
            "Shopify": {
                "html": [r"cdn.shopify.com", r"Shopify.shop"],
                "headers": []
            },
            "React": {
                "html": [r"react-dom", r"data-reactid", r"_reactInternalInstance"],
                "headers": []
            },
            "Google Analytics": {
                "html": [r"UA-[0-9]+-[0-9]", r"googletagmanager"],
                "headers": []
            },
            "Stripe": {
                "html": [r"js.stripe.com"],
                "headers": []
            },
            "Nginx": {
                "html": [],
                "headers": [r"nginx"]
            },
            "Cloudflare": {
                "html": [],
                "headers": [r"cloudflare"]
            }
        }

    def scan_url(self, url):
        """
        Recebe um URL, faz o request e retorna um JSON com as tecnologias encontradas.
        """
        if not url.startswith("http"):
            url = f"https://{url}"

        print(f"🕵️  A analisar: {url} ...")

        detected_tech = []

        try:
            # 1. Fazer o Request
            response = requests.get(url, headers=self.headers, timeout=10)

            # 2. Analisar Headers HTTP
            # Convertemos headers para string para facilitar a busca
            headers_str = str(response.headers).lower()

            # 3. Analisar HTML (Body)
            soup = BeautifulSoup(response.text, 'html.parser')
            html_str = str(soup).lower() # Convertemos tudo para minúsculas

            # 4. Aplicar as Regras
            for tech_name, patterns in self.rules.items():
                found = False

                # Check HTML patterns
                for pattern in patterns['html']:
                    if re.search(pattern.lower(), html_str):
                        detected_tech.append(tech_name)
                        found = True
                        break # Se já achou um padrão desta tech, passa à próxima

                # Check Header patterns (se ainda não encontrou no HTML)
                if not found:
                    for pattern in patterns['headers']:
                        if re.search(pattern.lower(), headers_str):
                            detected_tech.append(tech_name)
                            break

            return list(set(detected_tech)) # Remove duplicados e retorna lista

        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao aceder ao site: {e}")
            return ["Error: Unreachable"]