# FIORI — Meta Ads Dashboard

Dashboard interativa de campanhas Meta Ads para **FIORI EMPREENDIMENTOS IMOBILIÁRIOS LTDA**.

## Acesso

**Link permanente da dashboard:**
👉 https://renan8989.github.io/fiori-meta-ads-dashboard/

## Sobre

- Exibe dados reais da campanha ativa **Oceana Golf** (Meta Ads)
- Atualização automática diária às 08:00 BRT via GitHub Actions
- Hospedada via GitHub Pages — link permanente e sempre atualizado
- Terminologia conforme padrões oficiais Meta Ads

## Métricas exibidas

| Métrica | Descrição |
|---|---|
| Impressões | Número de vezes que o anúncio foi exibido |
| Alcance | Accounts Center accounts que viram o anúncio |
| Frequência | Média de visualizações por conta |
| Cliques (todos) | Total de cliques no anúncio |
| Link clicks | Cliques em links para destinos do anunciante |
| CTR (todos) | Taxa de cliques sobre impressões |
| Valor usado | Investimento total em BRL |
| CPM | Custo por 1.000 impressões |
| CPC (todos) | Custo médio por clique |
| Leads | Cadastros gerados |
| Custo por lead | Custo médio por lead |

## Estrutura

```
fiori-meta-ads-dashboard/
├── index.html              # Dashboard interativa
├── data/
│   └── campaign_data.json  # Dados da campanha (atualizado automaticamente)
├── update_data.py          # Script de coleta de dados via MCP
└── .github/workflows/
    └── update-dashboard.yml # Automação GitHub Actions
```

---
*Gerado automaticamente por Manus · Meta Ads API*
