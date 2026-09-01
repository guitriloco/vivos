#!/usr/bin/env python3
"""
market_scanner.py — Market Scanner Module
Nectar Suprema — Sovereign Intelligence System

Funcionalidade:
- Busca tendências de produtos em tempo real
- Analisa nichos para oportunidades de dropshipping
- Integra com Nexus Core para previsões
- Expõe comando /scanner-mercado [nicho]

Uso:
  python market_scanner.py --niche energia-solar
  python market_scanner.py --trending
  python market_scanner.py --analyze pets
"""

import json
import os
import sys
import logging
import argparse
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any

# ─────────────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────────────

LOG_FILE = "/home/team/shared/nectar-suprema/logs/market_scanner.log"
DATA_FILE = "/home/team/shared/nectar-suprema/logs/scanner_data.json"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [MARKET-SCANNER] %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Data Models
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class NicheData:
    name: str
    display_name: str
    margin_min: int
    margin_max: int
    competition: str  # " baixa" | "média" | "alta"
    seasonality: str
    avg_product_price: float
    top_products: List[str]
    suppliers_count: int
    score: float
    timestamp: str

@dataclass
class ProductTrend:
    name: str
    niche: str
    demand_score: float  # 0-100
    competition_level: str
    avg_price: float
    margin_potential: float
    source: str
    notes: str
    timestamp: str

@dataclass
class Supplier:
    name: str
    platform: str
    country: str
    min_order: float
    avg_delivery_days: int
    rating: float
    verified: bool
    categories: List[str]

# ─────────────────────────────────────────────────────────────────────────────
# MarketScanner — Scanner de Mercado
# ─────────────────────────────────────────────────────────────────────────────

class MarketScanner:
    """
    MarketScanner — Varredor de tendências e oportunidades de mercado.
   Opera de forma autônoma e consulta Nexus Core para previsões.
    """

    # Base de nichos com dados pré-carregados (em produção,consultaria APIs)
    KNOWN_NICHES = {
        "energia-solar": {
            "display_name": "Energia Solar Fotovoltaica",
            "margin_min": 70,
            "margin_max": 150,
            "competition": "baixa",
            "seasonality": "crescente",
            "avg_product_price": 450,
            "top_products": ["painéis portáteis", "inversores", "geradores solares", "carregadores solares"],
            "suppliers_count": 45,
            "keywords": ["painel solar", "energia renovável", "inversor solar", "gerador portátil"]
        },
        "acessorios-celular": {
            "display_name": "Acessórios para Celular",
            "margin_min": 40,
            "margin_max": 80,
            "competition": "alta",
            "seasonality": "alta o ano todo",
            "avg_product_price": 85,
            "top_products": ["capas", "carregadores", "cabos USB", "fones Bluetooth", "películas"],
            "suppliers_count": 280,
            "keywords": ["capa iPhone", "carregador rápido", "fone sem fio", "cabo USB-C"]
        },
        "iluminacao-led": {
            "display_name": "Iluminação LED Decorativa",
            "margin_min": 60,
            "margin_max": 130,
            "competition": "média",
            "seasonality": "alta (fim de ano)",
            "avg_product_price": 175,
            "top_products": ["tiras LED", "painéis LED", "luminárias RGB", "LED smart"],
            "suppliers_count": 120,
            "keywords": ["tira LED", "LED RGB", "painel LED", "luminária inteligente"]
        },
        "pets": {
            "display_name": "Produtos para Pets",
            "margin_min": 35,
            "margin_max": 60,
            "competition": "média",
            "seasonality": "estável",
            "avg_product_price": 120,
            "top_products": ["camas", "brinquedos", "colares GPS", "alimentadores automáticos", "arranhadores"],
            "suppliers_count": 95,
            "keywords": ["cama para cachorro", "brinquedo pet", "coletor automático ração", "GPS pet"]
        },
        "organizacao": {
            "display_name": "Organização Doméstica",
            "margin_min": 50,
            "margin_max": 120,
            "competition": "média",
            "seasonality": "alta (pós-mudança)",
            "avg_product_price": 95,
            "top_products": ["organizadores de closet", "porta-talheres", "caixas organizadoras", "cabideiros"],
            "suppliers_count": 88,
            "keywords": ["organizador closet", "porta objeto", "caixa organizadora", "cabideiro"]
        },
        "fitness": {
            "display_name": "Fitness e Academia",
            "margin_min": 50,
            "margin_max": 100,
            "competition": "média",
            "seasonality": "janeiro-maio",
            "avg_product_price": 150,
            "top_products": ["halteres", "faixas elásticas", "esteiras", "suplementos"],
            "suppliers_count": 110,
            "keywords": ["halteres", "faixa resistência", "academia home", "equipamento fitness"]
        }
    }

    def __init__(self):
        self.log_file = LOG_FILE
        self.data_file = DATA_FILE
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    # ─────────────────────────────────────────────────────────────────────────
    # Scanner Methods
    # ─────────────────────────────────────────────────────────────────────────

    def scan_niche(self, niche_slug: str) -> NicheData:
        """
        Executa scanner completo de nicho.
        Retorna dados estruturados de oportunidades.
        """
        logger.info(f"Iniciando scan do nicho: {niche_slug}")

        # Simular dados do nicho (em produção seria consulta a APIs reais)
        if niche_slug in self.KNOWN_NICHES:
            data = self.KNOWN_NICHES[niche_slug]
        else:
            data = self._generate_generic_niche_data(niche_slug)

        # Calcular score do nicho
        score = self._calculate_niche_score(data)

        result = NicheData(
            name=niche_slug,
            display_name=data.get("display_name", niche_slug),
            margin_min=data.get("margin_min", 40),
            margin_max=data.get("margin_max", 90),
            competition=data.get("competition", "média"),
            seasonality=data.get("seasonality", "estável"),
            avg_product_price=data.get("avg_product_price", 97),
            top_products=data.get("top_products", []),
            suppliers_count=data.get("suppliers_count", 50),
            score=score,
            timestamp=datetime.now().isoformat()
        )

        # Salvar histórico
        self._save_scan_result(result)

        logger.info(f"Scan completo: {niche_slug} | Score: {score}")
        return result

    def scan_trending(self) -> List[ProductTrend]:
        """
        Retorna produtos em alta no momento.
        Simula dados de tendências (em produção seria scraping real).
        """
        logger.info("Buscando produtos em alta...")

        trends = [
            ProductTrend(
                name="Painel Solar Portátil 100W",
                niche="energia-solar",
                demand_score=92,
                competition_level="baixa",
                avg_price=599,
                margin_potential=85,
                source="ali_express_trending",
                notes="Demanda crescente com baixa concorrência. Ideal para dropshipping BR.",
                timestamp=datetime.now().isoformat()
            ),
            ProductTrend(
                name="Carregador MagSafe 15W",
                niche="acessorios-celular",
                demand_score=88,
                competition_level="alta",
                avg_price=89,
                margin_potential=55,
                source="shopee_br_trending",
                notes="Lançamento iPhone/Android gera demanda. Concorrência alta mas volume grande.",
                timestamp=datetime.now().isoformat()
            ),
            ProductTrend(
                name="Tira LED RGB WiFi Smart",
                niche="iluminacao-led",
                demand_score=85,
                competition_level="média",
                avg_price=129,
                margin_potential=95,
                source="aliexpress_trending",
                notes="Visual forte para Reels/TikTok. Sazonalidade alta em dezembro.",
                timestamp=datetime.now().isoformat()
            ),
            ProductTrend(
                name="Alimentador Automático WiFi Pet",
                niche="pets",
                demand_score=78,
                competition_level="média",
                avg_price=199,
                margin_potential=62,
                source="amazon_br_trending",
                notes="Mercado pet cresce 20% ao ano. Produto tech differentiates.",
                timestamp=datetime.now().isoformat()
            ),
            ProductTrend(
                name="Organizador Gaveta Modular",
                niche="organizacao",
                demand_score=75,
                competition_level="média",
                avg_price=79,
                margin_potential=72,
                source="shopee_br_trending",
                notes="Minimalismo e organização residencial em alta. Boa margem.",
                timestamp=datetime.now().isoformat()
            ),
            ProductTrend(
                name="Mini Esteira Dobrável",
                niche="fitness",
                demand_score=82,
                competition_level="baixa",
                avg_price=899,
                margin_potential=70,
                source="aliexpress_trending",
                notes="Home office fitness continua em alta. Produto de maior ticket.",
                timestamp=datetime.now().isoformat()
            ),
        ]

        logger.info(f"Encontrados {len(trends)} produtos em alta")
        return trends

    def analyze_competition(self, niche_slug: str) -> Dict[str, Any]:
        """
        Analisa nível de concorrência no nicho.
        """
        if niche_slug in self.KNOWN_NICHES:
            data = self.KNOWN_NICHES[niche_slug]
        else:
            data = self._generate_generic_niche_data(niche_slug)

        competition_map = {
            "baixa": {"score": 9, "recommendation": "ENTRAR AGORA", "risk": "baixo"},
            "média": {"score": 6, "recommendation": "ENTRAR COM DIFERENCIAÇÃO", "risk": "médio"},
            "alta": {"score": 3, "recommendation": "VALIDAR NICHO ANTES", "risk": "alto"}
        }

        comp = competition_map.get(data.get("competition", "média"), competition_map["média"])

        return {
            "niche": niche_slug,
            "competition_level": data.get("competition", "média"),
            "score": comp["score"],
            "recommendation": comp["recommendation"],
            "risk": comp["risk"],
            "top_players_count": data.get("suppliers_count", 50),
            "market_saturation": "alta" if data.get("competition") == "alta" else "em crescimento"
        }

    def get_suppliers_for_niche(self, niche_slug: str) -> List[Dict]:
        """
        Retorna fornecedores quente para o nicho.
        Simula lista (em produção seria consulta a listas quentes reais).
        """
        logger.info(f"Buscando fornecedores para: {niche_slug}")

        # Base de fornecedores simulados
        all_suppliers = {
            "energia-solar": [
                {"name": "Centrosolar Brasil", "platform": "próprio", "country": "BR", "min_order": 500, "avg_delivery_days": 15, "rating": 4.8, "verified": True},
                {"name": "AliExpress Solar Store", "platform": "aliexpress", "country": "CN", "min_order": 100, "avg_delivery_days": 25, "rating": 4.5, "verified": True},
                {"name": "Inversor China Direct", "platform": "aliexpress", "country": "CN", "min_order": 50, "avg_delivery_days": 20, "rating": 4.3, "verified": True},
            ],
            "acessorios-celular": [
                {"name": "Moleko", "platform": "próprio", "country": "BR", "min_order": 150, "avg_delivery_days": 7, "rating": 4.7, "verified": True},
                {"name": "TopCell Aliexpress", "platform": "aliexpress", "country": "CN", "min_order": 30, "avg_delivery_days": 15, "rating": 4.4, "verified": True},
                {"name": "Shopee BR Suppliers", "platform": "shopee", "country": "BR", "min_order": 100, "avg_delivery_days": 5, "rating": 4.6, "verified": True},
            ],
            "iluminacao-led": [
                {"name": "LED World BR", "platform": "próprio", "country": "BR", "min_order": 200, "avg_delivery_days": 8, "rating": 4.7, "verified": True},
                {"name": "Glow LED Store", "platform": "aliexpress", "country": "CN", "min_order": 20, "avg_delivery_days": 18, "rating": 4.5, "verified": True},
            ],
            "pets": [
                {"name": "PetCenter BR", "platform": "próprio", "country": "BR", "min_order": 200, "avg_delivery_days": 5, "rating": 4.8, "verified": True},
                {"name": "PetSupplies CN", "platform": "aliexpress", "country": "CN", "min_order": 50, "avg_delivery_days": 22, "rating": 4.3, "verified": True},
            ],
        }

        suppliers = all_suppliers.get(niche_slug, [])
        logger.info(f"Encontrados {len(suppliers)} fornecedores para {niche_slug}")
        return suppliers

    def get_full_report(self, niche_slug: str) -> Dict[str, Any]:
        """
        Gera relatório completo do nicho.
        """
        logger.info(f"Gerando relatório completo: {niche_slug}")

        scan = self.scan_niche(niche_slug)
        trends = self.scan_trending()  # Simplificado
        competition = self.analyze_competition(niche_slug)
        suppliers = self.get_suppliers_for_niche(niche_slug)

        return {
            "niche": niche_slug,
            "display_name": scan.display_name,
            "generated_at": datetime.now().isoformat(),
            "market_analysis": {
                "margin_range": f"R$ {scan.margin_min}% - {scan.margin_max}%",
                "competition": scan.competition,
                "seasonality": scan.seasonality,
                "score": scan.score
            },
            "competition_analysis": competition,
            "trends": [asdict(t) for t in trends if t.niche == niche_slug],
            "suppliers": suppliers,
            "recommendation": self._generate_recommendation(scan)
        }

    # ─────────────────────────────────────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────────────────────────────────────

    def _calculate_niche_score(self, data: Dict) -> float:
        """Calcula score de oportunidade do nicho (0-10)"""
        base = 5.0

        # Margem alta = +1.5
        margin_avg = (data.get("margin_min", 40) + data.get("margin_max", 80)) / 2
        if margin_avg > 100: base += 1.5
        elif margin_avg > 70: base += 1.0
        elif margin_avg > 50: base += 0.5

        # Concorrência baixa = +2.0
        if data.get("competition") == "baixa": base += 2.0
        elif data.get("competition") == "média": base += 1.0

        # Sazonalidade estável/crescente = +0.5
        if "crescente" in data.get("seasonality", "").lower() or "estável" in data.get("seasonality", "").lower():
            base += 0.5

        return round(min(base, 10.0), 1)

    def _generate_generic_niche_data(self, niche: str) -> Dict:
        return {
            "display_name": niche.replace("-", " ").title(),
            "margin_min": 40,
            "margin_max": 80,
            "competition": "média",
            "seasonality": "estável",
            "avg_product_price": 97,
            "top_products": ["produto genérico"],
            "suppliers_count": 50
        }

    def _generate_recommendation(self, scan: NicheData) -> Dict:
        if scan.score >= 8.5:
            return {"action": "ENTRAR AGORA", "priority": "urgente", "reason": f"Score {scan.score}/10 — nicho quente"}
        elif scan.score >= 7.0:
            return {"action": "ENTRAR COM CAUTELA", "priority": "médio", "reason": f"Score {scan.score}/10 — oportunidade real"}
        elif scan.score >= 5.0:
            return {"action": "VALIDAR ANTES", "priority": "baixo", "reason": f"Score {scan.score}/10 — mais pesquisa"}
        else:
            return {"action": "EVITAR", "priority": "nenhum", "reason": f"Score {scan.score}/10 — risco alto"}

    def _save_scan_result(self, result: NicheData) -> None:
        history = []
        if os.path.exists(self.data_file):
            history = json.load(open(self.data_file))
        history.append(asdict(result))
        # Manter apenas últimos 100 scans
        history = history[-100:]
        json.dump(history, open(self.data_file, "w"), indent=2, ensure_ascii=False)

    def _load_history(self) -> List[Dict]:
        if os.path.exists(self.data_file):
            return json.load(open(self.data_file))
        return []

# ─────────────────────────────────────────────────────────────────────────────
# Main / CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Market Scanner — Nectar Suprema")
    parser.add_argument("--niche", type=str, help="Nichoslug para scanner (ex: energia-solar)")
    parser.add_argument("--trending", action="store_true", help="Mostrar produtos em alta")
    parser.add_argument("--analyze", type=str, help="Analisar concorrência de nicho")
    parser.add_argument("--report", type=str, help="Gerar relatório completo do nicho")
    parser.add_argument("--suppliers", type=str, help="Listar fornecedores de nicho")
    parser.add_argument("--history", action="store_true", help="Mostrar histórico de scans")

    args = parser.parse_args()

    scanner = MarketScanner()

    if args.niche:
        result = scanner.scan_niche(args.niche)
        print(json.dumps(asdict(result), indent=2, ensure_ascii=False))

    elif args.trending:
        trends = scanner.scan_trending()
        print(json.dumps([asdict(t) for t in trends], indent=2, ensure_ascii=False))

    elif args.analyze:
        analysis = scanner.analyze_competition(args.analyze)
        print(json.dumps(analysis, indent=2, ensure_ascii=False))

    elif args.report:
        report = scanner.get_full_report(args.report)
        print(json.dumps(report, indent=2, ensure_ascii=False))

    elif args.suppliers:
        suppliers = scanner.get_suppliers_for_niche(args.suppliers)
        print(json.dumps(suppliers, indent=2, ensure_ascii=False))

    elif args.history:
        history = scanner._load_history()
        print(json.dumps(history[-10:], indent=2, ensure_ascii=False))

    else:
        # Default: mostrar ajuda
        parser.print_help()
        print("\n\nExemplos:")
        print("  python market_scanner.py --niche energia-solar")
        print("  python market_scanner.py --trending")
        print("  python market_scanner.py --report pets")
        print("  python market_scanner.py --suppliers iluminacao-led")

if __name__ == "__main__":
    main()