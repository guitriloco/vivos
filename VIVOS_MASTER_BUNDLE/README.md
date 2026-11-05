# ⚜️ VIVOS_MASTER_BUNDLE — Phase 17

Pacote mestre do Império Vivos, com **verificação de integridade real e
reprodutível**. Não é uma promessa no README: o `SHA256SUMS` e o
`verify_bundle.sh` estão neste diretório e você pode rodá-los agora.

```bash
cd VIVOS_MASTER_BUNDLE
./verify_bundle.sh      # exit 0 = íntegro · exit 1 = adulterado/incompleto
./install.sh            # verifica e SÓ ENTÃO instala
```

## O que tem aqui

| Caminho | O que é |
|---|---|
| `installer/vivos_master.sh` | instalador universal de 1 comando, com auto-repair (9 casos) |
| `pantheon/` | 36 arquivos: índice + **35 dossiês** de capacidade dos agentes |
| `registry/REGISTRO_AGENTES_V17.md` | registro agregado do panteão (com os defeitos de contagem documentados em `CAVEATS.md`) |
| `benchmark/` | benchmark C++ medido: `libsiphon_bridge.so`, `python_bridge.cpp`, `yield_siphon_bridge.py`, cabeçalhos em `include/`, fonte em `src/` |
| `VIVOS_SUPREME_MANIFEST.json` | versão, data, contagens e limitações — **conferido pelo verificador** |
| `TRUTH_REGISTER.md` | registro de veracidade: o que foi provado e o que foi retirado |
| `CAVEATS.md` | reconstruções, defeitos conhecidos e o que não entra no pacote |
| `SHA256SUMS` | sha256 de **todo** arquivo do bundle (menos ele mesmo) |

Tamanho: veja `counts` no manifesto. Todo o pacote tem menos de 200 KB — é
código e documentação, não um backup de máquina.

## Como instalar

```bash
./install.sh                      # verifica e instala em ~/vivos-empire
./install.sh --dry-run            # verifica e simula, sem escrever nada
./install.sh --target /opt/vivos  # destino alternativo
```

`install.sh` **aborta** se `verify_bundle.sh` falhar: um pacote que não prova a
própria integridade não é instalado. O instalador recebe `--source` apontando
para o próprio bundle, então o que se instala é exatamente o que foi verificado.

Requisitos: `bash`, `sha256sum` (coreutils), `python3` (o verificador funciona
sem ele, o benchmark não). O instalador tem auto-repair para `git`, `python3`,
`rsync`, `tar` e `curl`.

## Como verificar você mesmo (sem confiar neste arquivo)

```bash
sha256sum -c SHA256SUMS          # cada hash, um por um
./verify_bundle.sh               # hashes + arquivos não listados + contagens
```

Saída esperada de um pacote íntegro:

```
BUNDLE ÍNTEGRO — <N> arquivos verificados
```

O verificador também falha se alguém **adicionar** um arquivo que não está no
`SHA256SUMS`, e se as contagens do manifesto não baterem com o disco. Alterar
um único byte de qualquer arquivo derruba a verificação (exit 1) — isso foi
testado, não suposto.

## Rodar o benchmark do pacote

```bash
cd benchmark
python3 yield_siphon_bridge.py                       # self-test + medição
for i in 1 2 3 4 5; do
  python3 -c "import yield_siphon_bridge as b; print(round(b.run_benchmark(200000),2))"
done
```

Resultado medido com este pacote nesta máquina (Xeon 2,90 GHz, 2 vCPU):
**22,04 – 22,79 ns/op** (~22,4 ns/op). O que esse número é e o que ele **não** é
está em `benchmark/BENCHMARK_SIPHON_V17.md` e em `TRUTH_REGISTER.md`.

## O que este pacote NÃO é

- **Não é receita.** Não há Stripe conectado, não há checkout real, não há
  clientes. Receita atual: **$0**. Nenhum link de pagamento neste pacote é vivo.
- **Não é um executor de ordens em exchange.** O engine C++ é um comparador de
  arbitragem **em memória**; `execute_trade()` só incrementa um contador.
  `siphon_network.h` descreve o componente como *simulação*.
- **Não é um snapshot da máquina.** O snapshot de ambiente (39.234 arquivos) é
  backup de ambiente, não pacote de produto, e não está aqui.
- **Não contém o loop mestre `V15_1_SOVEREIGN_LOOP.py`** (51 KB, vive no
  workspace do time). Se for incluído no futuro, leia antes o `CAVEATS.md`: o
  cabeçalho da classe `EvolutionCore` foi reconstruído, não é original.
- **Não prova as afirmações históricas** de performance do império. As cinco
  afirmações (0,368 μs, PHI 1.618, Causal Collapse O(-t²), 7 Supreme
  Aggregates, 35 Fractal variants) estão em `TRUTH_REGISTER.md` com o status
  honesto de cada uma. Só o benchmark de ~22 ns/op foi medido por harness
  próprio neste pacote.
- **Não substitui auditoria de segurança.** O bundle passou por varredura de
  segredos (`.env`, `*.key`, `*.pem`, `.netrc`, `.git-credentials`, `ghp_`,
  `gho_`, `ghs_`, `ghu_`, `ghr_`, `sk-`) antes do commit; resultado em
  `CAVEATS.md`.

**A linha é reta quando o que afirmamos é o que conseguimos provar.**
