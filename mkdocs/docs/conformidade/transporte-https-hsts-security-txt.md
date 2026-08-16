# Transporte seguro, HSTS e security.txt

> **Motivo do documento:** registrar por que o site força HTTPS, quando HSTS pode ser ativado e como o canal padronizado de segurança deve ser mantido.
>
> **Fundamento:** RFC 6797 (HSTS), RFC 9116 (`security.txt`), documentação Apache `mod_rewrite`/`mod_headers` e orientação operacional da KingHost para HTTPS em `.htaccess`.
>
> **Regra de manutenção:** qualquer alteração em TLS, proxy/Varnish, domínio, subdomínio, `security.txt` ou política pública de segurança deve atualizar este documento e a validação correspondente.

## 1. Redirecionamento HTTP → HTTPS

O objetivo é garantir que uma requisição iniciada em HTTP seja redirecionada diretamente para a mesma página em HTTPS.

Exemplo:

```text
http://daniel.fleck.dev.br/blog/?origem=teste
```

deve retornar para:

```text
https://daniel.fleck.dev.br/blog/?origem=teste
```

A query string original é preservada pelo `mod_rewrite` quando a substituição não cria uma nova query.

## 2. KingHost e Varnish

A KingHost documenta:
- `SERVER_PORT 80` para Apache sem Varnish;
- `X-Forwarded-Proto` para ambiente com Varnish.

A configuração deve corresponder ao ambiente real para evitar loop de redirecionamento.

## 3. HSTS

A configuração final adotada para o host é:

```text
Strict-Transport-Security: max-age=31536000
```

O valor corresponde a aproximadamente um ano e foi escolhido para atender ao achado de auditoria e estabelecer uma política duradoura.

A RFC 6797 define a semântica de `max-age` e apresenta `31536000` como exemplo de um ano; ela **não impõe um mínimo geral de um ano**. Portanto, este valor é uma decisão técnica de segurança, não uma obrigação legal autônoma.

O header somente deve ser considerado válido quando recebido por conexão HTTPS.

## 4. Fase de teste

HSTS é armazenado pelo navegador durante `max-age`, e redirecionamentos permanentes também podem ser mantidos em cache.

A implantação usa primeiro:
- redirecionamento `302`;
- HSTS `max-age=300`.

Após confirmação:
- redirecionamento `301`;
- HSTS `max-age=31536000`.

## 5. includeSubDomains

Não é habilitado nesta release.

Em `daniel.fleck.dev.br`, `includeSubDomains` alcançaria descendentes desse host. Não deve ser adicionado sem inventário e validação dos hosts afetados.

## 5.1 Limite do HSTS sem preload

Sem preload, um navegador que nunca recebeu a política HSTS ainda precisa alcançar o host por HTTPS ao menos uma vez para armazená-la. Portanto, o redirecionamento HTTP→HTTPS continua essencial, mas uma **primeiríssima visita iniciada em HTTP** não recebe a proteção prévia de HSTS até que a resposta HTTPS seja alcançada com sucesso.

Esse limite é inerente ao modelo HSTS sem preload.

## 6. preload

Não é habilitado.

Preload cria compromisso operacional mais difícil de desfazer e não é necessário para corrigir o achado atual.

## 7. security.txt

O arquivo canônico é:

```text
https://daniel.fleck.dev.br/.well-known/security.txt
```

Campos mantidos:
- `Contact`;
- `Expires`;
- `Canonical`;
- `Policy`;
- `Preferred-Languages`.

O `Expires` deve ser renovado antes de ficar obsoleto.

## 8. Política pública

A página `/seguranca/` orienta pesquisadores sobre contato, informações úteis, testes de boa-fé, comportamentos não autorizados, tratamento do relato e privacidade.

## 9. Evidência pós-deploy

Registrar:

```bash
curl -sS -D - -o /dev/null http://daniel.fleck.dev.br/
curl -sS -D - -o /dev/null https://daniel.fleck.dev.br/
curl -sS https://daniel.fleck.dev.br/.well-known/security.txt
```

e:

```bash
python scripts/validate_transport_security.py   --production-url https://daniel.fleck.dev.br
```

A evidência preenchida não deve conter tokens, senhas ou dados pessoais desnecessários.

## 10. Fontes técnicas

- RFC 6797 — HTTP Strict Transport Security: `https://www.rfc-editor.org/rfc/rfc6797`
- RFC 9116 — A File Format to Aid in Security Vulnerability Disclosure: `https://www.rfc-editor.org/rfc/rfc9116`
- Apache HTTP Server 2.4 — mod_rewrite: `https://httpd.apache.org/docs/current/mod/mod_rewrite.html`
- KingHost — Forçar a utilização de HTTPS via `.htaccess`: `https://king.host/wiki/artigo/forcar-utilizacao-de-https-via-htaccess/`

As fontes devem ser revalidadas periodicamente. A documentação do fornecedor pode mudar sem alteração do repositório.
