#!/usr/bin/env python3
"""
Script de atualização automática dos dados do Meta Ads para a dashboard FIORI.
Executado diariamente via GitHub Actions.
"""

import json
import subprocess
import sys
from datetime import datetime, timezone, timedelta

BRT = timezone(timedelta(hours=-3))

def run_mcp(tool_name, input_json):
    """Executa uma chamada ao MCP do Meta Ads."""
    result = subprocess.run(
        ['manus-mcp-cli', 'tool', 'call', tool_name,
         '--server', 'meta-marketing',
         '--input', json.dumps(input_json)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"Erro ao chamar {tool_name}: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    # Encontrar o arquivo de resultado salvo
    for line in result.stdout.splitlines():
        if line.startswith('MCP tool invocation result saved to:'):
            path = line.split(':', 1)[1].strip()
            with open(path) as f:
                return json.load(f)
    print(f"Resultado não encontrado para {tool_name}", file=sys.stderr)
    sys.exit(1)


def main():
    print("Iniciando atualização dos dados do Meta Ads...")

    # Buscar insights da campanha ativa Oceana Golf
    CAMPAIGN_ID = "120245166124370671"
    insights_data = run_mcp("meta_marketing_get_insights", {
        "object_id": CAMPAIGN_ID,
        "object_type": "campaign",
        "date_preset": "maximum",
        "limit": 1
    })

    insights = insights_data.get("result", {}).get("insights", [])
    if not insights:
        print("Nenhum dado retornado pela API.", file=sys.stderr)
        sys.exit(1)

    c = insights[0]

    # Extrair leads e custo por lead
    leads = 0
    cost_per_lead = 0.0
    for action in c.get("actions", []):
        if action.get("action_type") == "lead":
            leads = int(action.get("value", 0))
    for cpa in c.get("cost_per_action_type", []):
        if cpa.get("action_type") == "lead":
            cost_per_lead = float(cpa.get("value", 0))

    # Montar JSON de saída
    output = {
        "account": {
            "id": "act_1453008295739427",
            "name": "MICHEL - FIORI EMPREENDIMENTOS IMOBILIARIOS LTDA",
            "currency": "BRL"
        },
        "last_updated": datetime.now(BRT).isoformat(),
        "date_range": {
            "start": c.get("date_start", ""),
            "end": c.get("date_stop", "")
        },
        "campaigns": [
            {
                "id": CAMPAIGN_ID,
                "name": c.get("campaign_name", ""),
                "status": "ACTIVE",
                "impressions": int(c.get("impressions", 0)),
                "reach": int(c.get("reach", 0)),
                "frequency": float(c.get("frequency", 0)),
                "clicks_all": int(c.get("clicks", 0)),
                "link_clicks": int(c.get("inline_link_clicks", 0)),
                "ctr_all": float(c.get("ctr", 0)),
                "link_click_ctr": float(c.get("inline_link_click_ctr", 0)),
                "spend": float(c.get("spend", 0)),
                "cpc_all": float(c.get("cpc", 0)),
                "cost_per_link_click": float(c.get("cost_per_inline_link_click", 0)),
                "cpm": float(c.get("cpm", 0)),
                "leads": leads,
                "cost_per_lead": cost_per_lead,
                "quality_ranking": c.get("quality_ranking", "UNKNOWN"),
                "engagement_rate_ranking": c.get("engagement_rate_ranking", "UNKNOWN"),
                "conversion_rate_ranking": c.get("conversion_rate_ranking", "UNKNOWN")
            }
        ]
    }

    # Salvar JSON
    output_path = "data/campaign_data.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Dados atualizados com sucesso em {output_path}")
    print(f"Período: {output['date_range']['start']} → {output['date_range']['end']}")
    print(f"Impressões: {output['campaigns'][0]['impressions']:,}")
    print(f"Leads: {output['campaigns'][0]['leads']}")
    print(f"Valor usado: R$ {output['campaigns'][0]['spend']:,.2f}")


if __name__ == "__main__":
    main()
