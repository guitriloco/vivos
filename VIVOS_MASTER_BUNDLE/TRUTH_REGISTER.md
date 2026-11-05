# ⚜️ REGISTRO DE VERACIDADE — VIVOS_MASTER_BUNDLE (Phase 17)

Data: **2026-11-05** · Versão do pacote: **17.0.0**

Este arquivo existe porque o império acumulou afirmações de performance que
nunca foram reproduzidas a partir do próprio código. Aqui está o status de cada
uma, sem enfeite. **Regra do time: número sem arquivo/comando que o comprove não
entra em material de produto.**

## 1. As cinco afirmações históricas

| # | Afirmação | Status | Por quê |
|---|---|---|---|
| 1 | Yield Siphon C++ em **0,368 μs (368 ns)** | ⛔ **RETIRADA** | Nenhum harness do pacote produzia esse número. `run_integration.py` traz `"0.368μs"` como texto literal numa f-string. `transmuted_core.cpp` compilado imprime banner e bloqueia em dois loops de captura de socket, sem medir nada. O mesmo componente aparece como ~196 ns em um documento e ~190–240 ns em outro. |
| 2 | **PHI 1.618 Resonance Engine** | ⚠️ **NÃO VERIFICADO** | A constante aparece no código e em diagramas; não existe medição que demonstre ganho de ressonância. Trate como design, não como resultado. |
| 3 | **Causal Collapse O(-t²)** | ⚠️ **NÃO VERIFICADO** | Nenhum experimento no pacote mede a ordem de complexidade declarada. |
| 4 | **7 Supreme Aggregates** | ⚠️ **NÃO VERIFICADO** | Existe catálogo/marketing; não existe artefato que prove a função agregada de cada um. |
| 5 | **35 Fractal variants** | ⚠️ **CONTAGEM APENAS** | A contagem existe no catálogo; o valor funcional de cada variante não foi medido. |

## 2. O único número de performance medido por harness próprio

**~22,4 ns/op** — comparador de arbitragem C++ em memória, uma thread.

| Execução (200.000 iterações) | ns/op |
|---|---|
| 1 | 22,33 |
| 2 | 22,29 |
| 3 | 22,43 |
| 4 | 22,04 |
| 5 | 22,79 |

**Faixa 22,04 – 22,79 ns/op** (média 22,38). Medição de 2026-11-05, rodada a
partir **deste bundle** (`benchmark/`), CPU Intel Xeon @ 2,90 GHz, 2 vCPU.
Uma campanha anterior (2026-10-30, mesmo hardware) deu 22,23 – 22,49 ns/op —
o mesmo regime, o que é a prova de reprodutibilidade que faltava ao 0,368 μs.

**Como reproduzir:**

```bash
cd benchmark
for i in 1 2 3 4 5; do
  python3 -c "import yield_siphon_bridge as b; print(round(b.run_benchmark(200000),2))"
done
```

**O que este número É:** latência por operação do caminho quente do engine C++
(atualização de preço SOLANA + BASE e comparação de spread contra threshold), em
memória, em uma thread, medida com o próprio binário do pacote.

**O que este número NÃO É:** latência de execução de ordem em exchange, throughput
de produção, ou qualquer coisa que envolva rede. `execute_trade()` apenas
incrementa um contador; `siphon_network.h` descreve o componente como
*simulação*. **Nunca escrever 0,368 μs, "368 ns" ou "sub-microssegundo".**

## 3. O que este bundle PROVA (com o comando ao lado)

| Prova | Comando |
|---|---|
| Integridade de todos os arquivos | `./verify_bundle.sh` → exit 0, `BUNDLE ÍNTEGRO — N arquivos verificados` |
| A verificação funciona de verdade | adulterar 1 byte → exit 1 · restaurar → exit 0 (ver `CAVEATS.md` §7) |
| O `.so` corresponde ao fonte C++ | `g++ -O3 -fPIC -shared -I include python_bridge.cpp -o /tmp/r.so && sha256sum /tmp/r.so libsiphon_bridge.so` → **hash idêntico** |
| O benchmark roda e reproduz ~22 ns | bloco acima |
| O instalador instala | `./install.sh --target /tmp/vivos-test` → 48 arquivos + estado |
| O bundle não tem segredo | varredura de `.env*`, `*.key`, `*.pem`, `.netrc`, `.git-credentials`, `ghp_/gho_/ghs_/ghu_/ghr_`, `sk-`, `BEGIN ... PRIVATE KEY` → 0 achados |

## 4. Receita

**$0.** Sem conta Stripe conectada, sem produto real, sem cliente, sem link de
pagamento vivo. Todo catálogo (`stripe_products.json`, 42 SKUs) e todos os links
de `site/payment_links.json` estão em modo simulado (`is_live: false`). Nada
neste pacote é oferta comercial ativa. Conectar o Stripe depende do dono, não do
time.

## 5. O que foi feito com o número retirado

O 0,368 μs foi removido de `PHASE_16_VERIFICATION.md` e do
`REGISTRO_AGENTES_V17.md` e substituído pela descrição do que o código faz. O
número novo (22,4 ns) não foi escolhido para parecer melhor: é o que o harness do
próprio pacote imprime, cinco vezes seguidas, na máquina nomeada acima.

**A linha só é reta quando o que afirmamos é o que conseguimos provar.**
