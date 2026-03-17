# SECURITY_REPORT - bank-api

| Controle | OWASP | Status |
|----------|-------|--------|
| bcrypt hash | A02 | ok |
| ORM sem raw SQL | A03 | ok |
| JWT com expiracao | A07 | ok |
| Timing-safe login | A07 | ok |
| Stack trace oculto | A09 | ok |
| Docs off em prod | A05 | ok |
| CORS explicito | A05 | ok |
| .env no .gitignore | A02 | ok |
| SECRET_KEY via env | A02 | ok |
| Saldo nao negativo | negocio | ok |

## Teste manual
```
POST /auth/register -> 201
POST /auth/login -> 200 + token
GET  /auth/me (sem JWT) -> 401
POST /accounts/1/withdraw {amount:9999} -> 422 saldo insuficiente
```
