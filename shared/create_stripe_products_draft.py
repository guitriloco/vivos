import json
import os

def generate_stripe_products():
    base_products = [
        {"name": "YIELD-SIPHON", "price": 499, "interval": "one_time", "description": "C++ arbitrage siphon engine with a Python integration layer. Decision latency is unverified: no benchmark harness ships with this package."},
        {"name": "WRAITH-MESH", "price": 299, "interval": "month", "description": "Zero-Trust Autonomous Firewall & Node routing mesh"},
        {"name": "COGNITIVE-SDK", "price": 99, "interval": "month", "description": "14-Model AI Sovereign Intelligence Orchestration SDK"},
        {"name": "SECURE-VAULT", "price": 199, "interval": "month", "description": "ZKP Immutable Ledger and Encrypted Multi-tenant Vault"},
        {"name": "OMNI-HUB", "price": 999, "interval": "month", "description": "Central Command and Imperial Control Hub"},
        {"name": "MUTANT-NECTAR", "price": 149, "interval": "one_time", "description": "Self-Evolving Code and Mutation Engine (E-LINK)"},
        {"name": "LIFE-SUITE", "price": 49, "interval": "month", "description": "Wealth, Pets, and Health Sovereign Suite Bundle"}
    ]

    niches = [
        {"code": "FIN", "name": "Fintech & Arbitrage"},
        {"code": "CYBER", "name": "Cybersecurity & Defense"},
        {"code": "BIO", "name": "Biotech & Genetic Simulation"},
        {"code": "DEF", "name": "Defense & Sovereign Networks"},
        {"code": "LOG", "name": "Logistics & Supply-Chain Optimization"}
    ]

    catalog = []

    # 1. Generate 7 Core Aggregates
    for bp in base_products:
        item = {
            "product_id": f"prod_v17_{bp['name'].lower()}",
            "name": f"⚜️ {bp['name']} (Supreme Core) ⚜️",
            "description": bp['description'],
            "price_id": f"price_v17_{bp['name'].lower()}",
            "price": bp['price'],
            "currency": "usd",
            "billing_scheme": bp['interval'],
            "checkout_url": f"https://checkout.stripe.com/pay/simulated_v17_{bp['name'].lower()}"
        }
        catalog.append(item)

    # 2. Generate 35 Niche-Fractal Variants
    for bp in base_products:
        for niche in niches:
            n_name = f"VIVOS-{niche['code']}-{bp['name']}"
            item = {
                "product_id": f"prod_v17_{bp['name'].lower()}_{niche['code'].lower()}",
                "name": f"💠 {n_name} ({niche['name']}) 💠",
                "description": (
                    f"Industry preset of {bp['name']} for {niche['name']}. "
                    "Same core code as the base product, shipped as a labelled configuration preset. "
                    "No separate engine and no verified performance gain over the base product."
                ),
                "price_id": f"price_v17_{bp['name'].lower()}_{niche['code'].lower()}",
                "price": int(bp['price'] * 1.25),  # 25% premium for niche specialization
                "currency": "usd",
                "billing_scheme": bp['interval'],
                "checkout_url": f"https://checkout.stripe.com/pay/simulated_v17_{bp['name'].lower()}_{niche['code'].lower()}"
            }
            catalog.append(item)

    output_path = os.environ.get("STRIPE_PRODUCTS_OUT", "/home/team/shared/stripe_products.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "status": "DRAFT_SIMULATED",
            "currency": "usd",
            "products_count": len(catalog),
            "products": catalog,
            "note": (
                "SIMULATED preview of the product catalogue. No Stripe account is connected and no "
                "product here exists at Stripe. Descriptions state only what the shipped code does. "
                "On 2026-10-30 the claims '0.368us decision latency' and 'PHI 1.618 resonance' were "
                "removed: neither is reproduced by any benchmark in this repository."
            ),
        }, f, indent=2, ensure_ascii=True)

    print(f"✅ Product catalog successfully written to: {output_path}")
    print(f"Total products generated: {len(catalog)}")

if __name__ == "__main__":
    generate_stripe_products()
