# 🚀 Production Readiness Report: Equity Valuation Engine

Embora o teu projeto tenha uma excelente **Arquitetura Hexagonal** (Domain, Application, Ports, Adapters), o código atual foi desenhado como um script *CLI (Command Line Interface)* local. 

Para passar este motor de avaliação para um ambiente de **Produção** (escalável, seguro, disponível na web e robusto), precisas de abordar as seguintes 8 áreas críticas:

## 1. Exposição Web (A API)
Atualmente, a execução é feita localmente no `main.py`. Para servires isto em produção (ex: para alimentar um Frontend em React/Next.js ou para venderes como um serviço), precisas de um servidor Web.
> [!IMPORTANT]
> **Ação:** Implementar o **FastAPI**. 
> - Cria novos *Input Adapters* (os *Controllers* do FastAPI) que recebam pedidos HTTP (ex: `GET /api/v1/valuation/META`).
> - Substitui os teus atuais Input Adapters (que usam `print()`) por rotas que devolvam os DTOs diretamente como JSON.

## 2. Assincronia (Async I/O)
Neste momento, as tuas chamadas à API da AlphaVantage e ao Gemini são **síncronas** (bloqueantes). Se 5 utilizadores pedirem uma análise ao mesmo tempo, o teu servidor vai processar um a um.
> [!WARNING]
> **Ação:** Mudar para chamadas Assíncronas.
> - Trocar a biblioteca `requests` por `httpx` para chamadas assíncronas ao AlphaVantage.
> - Assegurar que os teus Use Cases são `async def` e utilizam o `await`.

## 3. Persistência e Cache Partilhada (O Adeus aos Ficheiros)
Estás a usar o disco local para a cache (`alpha_vantage_cache.sqlite` e a pasta `.gemini_cache`). Em produção (ex: Docker, AWS, Render), o disco é efémero (apaga-se quando o servidor reinicia) e não pode ser partilhado se tiveres 2 ou 3 servidores ligados ao mesmo tempo.
> [!CAUTION]
> **Ação:** Usar Bases de Dados e Cache Distribuída.
> - **Redis:** Para substituir as caches do AlphaVantage e do Gemini. O Redis partilha a cache instantaneamente por todos os teus servidores.
> - **PostgreSQL:** Para guardar análises a longo prazo (persistência real do teu Output Adapter), o histórico dos utilizadores, e relatórios que já não mudam.

## 4. Gestão de Filas (Filas de Trabalho / Background Jobs)
A análise de Earnings e de Valuation demora algum tempo (devido ao raciocínio do LLM e aos limites de taxa da AlphaVantage). Se um utilizador clicar no botão num website, a ligação HTTP vai dar *Timeout* antes do Gemini terminar a resposta.
> [!TIP]
> **Ação:** Implementar processamento em Background (Worker Queues).
> - Ferramentas como **Celery**, **RQ** ou **TaskIQ**. O utilizador pede a análise, o servidor responde `{"status": "processing", "job_id": 123}`, e um processo em *background* faz o trabalho pesado, notificando o Frontend quando terminar.

## 5. Resiliência e Limites de Taxa (Rate Limits)
O teu código tem `time.sleep(1.5)` no AlphaVantage. Isto é perigoso em produção e não escala. Além disso, se o Gemini falhar, o teu código aborta (embora com mensagem bonita).
> [!TIP]
> **Ação:** Usar *Exponential Backoff*.
> - Instalar a biblioteca **`tenacity`**. Ela permite tentar novamente chamadas à API de forma inteligente (ex: espera 2s, se falhar espera 4s, se falhar espera 8s) antes de devolver erro ao utilizador.

## 6. Logs e Monitorização (Observability)
Atualmente usas `print()` para debugar e apanhar erros. Em produção, os `prints` perdem-se e não tens forma de saber se o sistema falhou às 4 da manhã.
> [!IMPORTANT]
> **Ação:** Estruturar os Logs.
> - Usar a biblioteca padrão `logging` de Python ou, melhor ainda, **`structlog`** para formatar os logs em JSON.
> - Integrar o **Sentry** (uma ferramenta gratuita de monitorização) que te envia um email/alerta sempre que um utilizador encontra um erro grave (como aquele de faltar o Balance Sheet de 2008).

## 7. Configuração e Dependency Injection
O teu `main.py` faz a injeção manual das dependências e carrega as chaves usando `os.getenv()`.
> [!NOTE]
> **Ação:** Usar *Pydantic Settings* e Contentores DI.
> - O **`pydantic-settings`** deve ser usado para validar as variáveis de ambiente. Se faltar uma API Key no arranque do servidor, ele crasha imediatamente, evitando que falhe só quando um cliente o usa.
> - Frameworks como o FastAPI já trazem sistemas nativos de Injeção de Dependências (o `Depends()`) para substituir as tuas linhas gigantes de instanciação de `Adapters` e `UseCases`.

## 8. Dockerização e CI/CD
Por fim, o código precisa de ser embalado de forma estandardizada.
> [!IMPORTANT]
> **Ação:** Criar a Infraestrutura como Código.
> - Criar um **`Dockerfile`** (usa a imagem `python:3.12-slim` ou mais recente) e um **`docker-compose.yml`** que levanta a tua API juntamente com o Redis e o PostgreSQL de uma só vez.
> - Configurar **GitHub Actions** para correr o `pytest` e o linter (`Ruff`) automaticamente sempre que fazes um commit.
