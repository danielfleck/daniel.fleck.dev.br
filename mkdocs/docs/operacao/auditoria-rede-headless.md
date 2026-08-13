# Auditoria de rede em navegador headless

## Problema

Inspecionar apenas `src="https://..."` não detecta requisições criadas dinamicamente pelo JavaScript.

Exemplo real observado durante a revisão: o Material for MkDocs pode consultar a API do GitHub quando `repo_url` está configurado, mesmo que o HTML carregue apenas JavaScript local.

## Solução

`scripts/audit_network.py` executa Chromium headless com Playwright, intercepta as requisições e permite somente hosts autorizados.

Uma tentativa para host não permitido:

1. é registrada;
2. é abortada antes de ser concluída;
3. aparece em `dist/network-audit.json`;
4. faz o comando retornar erro.

## Uso

```bash
python scripts/audit_network.py --all
```

Produção:

```bash
python scripts/audit_network.py   --base-url https://daniel.fleck.dev.br   --all   --report dist/network-audit-production.json
```

## Git

O `pre-push` executa a auditoria automaticamente. Isso coloca a checagem dinâmica imediatamente antes do envio das mudanças ao repositório remoto.
