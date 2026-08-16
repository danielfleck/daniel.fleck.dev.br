# Conformidade, privacidade e segurança

> **Motivo do documento:** Centralizar a documentação durável de conformidade e orientar manutenção humana/IA.
> **Fundamento:** LGPD arts. 6, 37, 46 e 50; governança técnica do projeto.
> **Regra de manutenção:** cada alteração relevante deve atualizar o motivo/fundamento correspondente e, quando afetar texto público, o racional da seção legal no mesmo commit.


Esta seção registra as decisões de engenharia, privacidade e governança aplicáveis ao site pessoal `daniel.fleck.dev.br`.

Ela foi criada para cumprir quatro objetivos:

1. manter rastreabilidade do motivo de cada regra pública;
2. impedir que uma futura manutenção simplifique textos jurídicos sem compreender o contexto;
3. fornecer procedimentos reproduzíveis para eventos de segurança, pedidos de titulares e requisições;
4. separar evidência pública, evidência restrita e pendências.

## Documentos principais

- [Racional do Aviso de Privacidade V7](racional-aviso-privacidade-v7.md)
- [Racional dos Termos de Uso V6](racional-termos-uso-v6.md)
- [Matriz de fontes e evidências](matriz-fontes-e-evidencias.md)
- [Política interna de privacidade e proteção de dados](politica-interna-privacidade.md)
- [Política de retenção e descarte](politica-retencao-descarte.md)
- [Segurança do e-mail: SPF, DKIM e DMARC](email-seguranca-spf-dkim-dmarc.md)
- [Proteção contra crawlers, spam e mail-bombing](crawler-spam-mailbomb.md)
- [Fornecedores e transferências](fornecedores-transferencias.md)

## Segurança e infraestrutura

- [Transporte seguro, HSTS e security.txt](transporte-https-hsts-security-txt.md)
- [Relato de vulnerabilidade](procedimento-relato-vulnerabilidade.md)
- [Diligência pendente — KingHost](diligencia-kinghost-pendente.md)
- [Pendências da auditoria de qualidade](qualidade-web-2026-08-15.md)

## Procedimentos

- [Direitos dos titulares](procedimento-titulares.md)
- [Resposta a incidentes](procedimento-incidentes.md)
- [Requisições de autoridades](procedimento-requisicoes-autoridades.md)
- [Retenção legal / legal hold](procedimento-legal-hold.md)
- [Revisão periódica](revisao-periodica.md)

## Modelos

Os modelos são **templates em branco**. Nunca preencha um modelo público com dados reais. Salve a cópia preenchida fora do repositório público.

Veja [Modelos e formulários](modelos/README.md).

## Regra para manutenção por IA

Antes de editar Aviso de Privacidade ou Termos:
1. localizar o comentário `LEGAL-RATIONALE` da seção;
2. ler o racional correspondente;
3. conferir o comportamento real do site;
4. conferir a fonte normativa/técnica atual;
5. atualizar texto, racional, histórico e validações no mesmo commit.
