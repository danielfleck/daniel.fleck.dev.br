# Privacidade por arquitetura

A redução de dados tratados começa na arquitetura.

A aplicação não oferece:

- cadastro ou conta de visitante;
- autenticação pública;
- comentários;
- upload de arquivos;
- formulários próprios de captação;
- publicidade programática;
- pixel próprio de marketing;
- ferramenta própria de analytics comportamental;
- banco próprio de histórico individual de visitantes.

Scripts, imagens, fontes e folhas de estilo do site principal são servidos pelo próprio domínio. Links externos são acionados pelo visitante e não representam, por si só, carregamento automático do recurso de terceiro.

A política `no-referrer` reduz o envio da URL de origem ao navegar para outro site. O código também não combina deliberadamente IPs com dados de outras fontes para identificar visitantes.

## Limite desta documentação

Essas são características técnicas. A qualificação de controlador/operador, bases legais, direitos dos titulares e retenções legais não são inferidas automaticamente a partir da arquitetura e permanecem na documentação de governança apropriada.
