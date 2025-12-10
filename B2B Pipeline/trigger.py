from tasks import analyze_domain
import time

domains_to_scan = [
    "github.com",
    "stackoverflow.com",
    "python.org",
    "docker.com",
    "airbnb.com",
    "uber.com",
    "spotify.com",
    "netflix.com"
]

print(f"🚀 A enviar {len(domains_to_scan)} tarefas para a fila...")

start_time = time.time()

for domain in domains_to_scan:
    # O segredo está aqui: .delay()
    # Isto envia a tarefa para o Redis e o script CONTINUA imediatamente.
    analyze_domain.delay(domain)

end_time = time.time()

print(f"🏁 Enviadas em {end_time - start_time:.4f} segundos!")
print("👀 Olha para o outro terminal para veres o trabalho a acontecer.")