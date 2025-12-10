import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

HUBSPOT_API_URL = "https://api.hubapi.com/crm/v3/objects/companies"
TOKEN = os.getenv("HUBSPOT_TOKEN")

def send_to_hubspot(domain, tech_stack):
    """
    Envia a empresa enriquecida para o HubSpot CRM.
    Mete as tecnologias encontradas na 'description' da empresa.
    """
    if not TOKEN:
        print("⚠️ [CRM] Token não encontrado. A saltar envio.")
        return False

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    # Converter a lista de tecnologias numa string bonita
    tech_str = ", ".join(tech_stack) if tech_stack else "None detected"

    # Payload: Mapear os nossos dados para os campos do HubSpot
    payload = {
        "properties": {
            "domain": domain,
            "name": domain, # Usamos o domínio como nome provisório
            "description": f"✅ Tech Stack Detected by Bot: {tech_str}",
            "lifecyclestage": "lead"
        }
    }

    try:
        response = requests.post(HUBSPOT_API_URL, headers=headers, json=payload)

        if response.status_code == 201:
            print(f"🚀 [CRM] Sucesso! Empresa {domain} criada no HubSpot.")
            return True
        elif response.status_code == 409:
            print(f"⚠️ [CRM] A empresa {domain} já existe no HubSpot.")
            return True
        else:
            print(f"❌ [CRM] Erro {response.status_code}: {response.text}")
            return False

    except Exception as e:
        print(f"❌ [CRM] Erro de conexão: {e}")
        return False