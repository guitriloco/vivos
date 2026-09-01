#!/usr/bin/env python3
import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="Terax-AI CLI: A Interface Soberana do Desenvolvedor")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # Comando: distill
    distill_parser = subparsers.add_parser("distill", help="Inicia o loop de destilação de código")
    distill_parser.add_argument("path", help="Caminho para o arquivo ou diretório a ser destilado")

    # Comando: generate
    generate_parser = subparsers.add_parser("generate", help="Gera código soberano a partir de uma intenção")
    generate_parser.add_argument("prompt", help="Descrição do que deve ser gerado")

    # Comando: audit
    audit_parser = subparsers.add_parser("audit", help="Audita o código seguindo o Padrão de Ouro")
    audit_parser.add_argument("path", help="Caminho para o arquivo a ser auditado")

    args = parser.parse_args()

    if args.command == "distill":
        print(f"[*] Iniciando destilação em: {args.path}")
        # Chamar lógica de destilação
    elif args.command == "generate":
        print(f"[*] Gerando código para: {args.prompt}")
        # Chamar lógica de geração
    elif args.command == "audit":
        from auditor import GoldStandardAuditor
        print(f"[*] Auditando código em: {args.path}")
        auditor = GoldStandardAuditor()
        findings = auditor.audit(args.path)
        if findings:
            print("\n--- Resultados da Auditoria Soberana ---")
            for f in findings:
                print(f)
        else:
            print("\nParabéns! Código aprovado no Padrão de Ouro.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
