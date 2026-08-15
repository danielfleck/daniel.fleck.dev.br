# Proteção do e-mail público contra crawlers, spam e mail-bombing

> **Motivo do documento:** Reduzir coleta automatizada simples do endereço e mitigar spam, phishing e flooding sem criar formulário/terceiro desnecessário.
> **Fundamento:** LGPD arts. 6, III, VII e VIII, e 46; segurança proporcional; boas práticas anti-automação.
> **Regra de manutenção:** cada alteração relevante deve atualizar o motivo/fundamento correspondente e, quando afetar texto público, o racional da seção legal no mesmo commit.


## Modelo de ameaça

Um endereço literal em HTML, `mailto:`, repositório público ou cache pode ser coletado por scrapers. Depois de conhecido, o endereço pode receber:
- spam;
- phishing;
- engenharia social;
- anexos maliciosos;
- inscrição abusiva em listas;
- mail-bombing/flooding;
- tentativas de descobrir contas administrativas.

## Decisão desta release

### 1. Página `/contato/`

O rodapé e CTAs deixam de conter `mailto:` estático e passam a apontar para `/contato/`.

A página mostra:

```text
contato [arroba] fleck.dev.br
```

O JavaScript reconstrói o `mailto:` somente quando a pessoa aciona o botão e confirma o aviso.

### 2. Limite da ofuscação

Isso reduz crawlers simples baseados em regex. Não impede:
- crawler com JavaScript;
- análise semântica;
- leitura do repositório/histórico Git;
- cache antigo;
- listas em que o endereço já exista.

O e-mail deve ser considerado **publicamente descobrível**.

### 3. Separação de identidades

`contato@...` não deve ser:
- recuperação do GitHub;
- login administrativo da KingHost;
- recuperação do registrador de domínio;
- e-mail bancário;
- e-mail de MFA;
- conta administrativa principal.

Use um endereço administrativo não publicado para essas funções.

### 4. Provedor

Verificar no plano:
- antispam/Spaminator;
- treinamento ao mover mensagens entre spam e caixa;
- lista de bloqueio;
- bloqueio por remetente/domínio;
- limites e quotas;
- comportamento diante de volume excepcional;
- canal de escalonamento para mail-bombing.

### 5. Não usar auto-resposta genérica

Auto-responder a toda mensagem pode confirmar a existência da caixa e aumentar backscatter/loops. Usar somente se houver necessidade operacional.

### 6. Formulário/captcha

Não criar nesta etapa. Um formulário pode reduzir exposição do endereço, mas cria um endpoint suscetível a abuso e um novo tratamento direto. CAPTCHA de terceiro também adiciona scripts/processamento externos.

Reavaliar apenas se os controles do provedor e a ofuscação forem insuficientes.

### 7. Em caso de flood

1. não responder aos remetentes;
2. preservar amostra mínima de evidência, sem arquivar milhares de cópias;
3. registrar início, volume aproximado e efeito;
4. alterar senha somente se houver indício de comprometimento, não apenas por volume recebido;
5. acionar KingHost para filtro/rate limit/bloqueio conforme recursos do serviço;
6. checar disponibilidade da caixa e quota;
7. aplicar filtros locais/servidor;
8. executar procedimento de incidente se houver exposição, comprometimento ou indisponibilidade relevante;
9. se o alias se tornar inutilizável, planejar substituição controlada do endereço público.

## Robots.txt

`robots.txt` não é controle de segurança para endereço de e-mail. Crawlers maliciosos podem ignorá-lo.
