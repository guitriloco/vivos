import re
import os

class GoldStandardAuditor:
    def __init__(self):
        self.rules = [
            {"id": "DOC001", "desc": "Nomes de funções devem ser explicativos (mínimo 3 caracteres)", "regex": r"def \w{1,2}\("},
            {"id": "ERR001", "desc": "Captura de exceção genérica detectada", "regex": r"except:"},
            {"id": "LOG001", "desc": "Uso de print em vez de logging sugerido", "regex": r"print\("},
            {"id": "SEC001", "desc": "Possível exposição de segredo (API_KEY)", "regex": r"(?i)api_key\s*=\s*['\"].+['\"]"}
        ]

    def audit(self, file_path):
        results = []
        if not os.path.exists(file_path):
            return [f"Erro: Arquivo {file_path} não encontrado."]

        with open(file_path, 'r') as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, 1):
            for rule in self.rules:
                if re.search(rule["regex"], line):
                    results.append(f"[{rule['id']}] Linha {line_num}: {rule['desc']}")

        return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        auditor = GoldStandardAuditor()
        findings = auditor.audit(sys.argv[1])
        if findings:
            print("--- Resultados da Auditoria Soberana ---")
            for f in findings:
                print(f)
        else:
            print("Parabéns! Código aprovado no Padrão de Ouro.")
