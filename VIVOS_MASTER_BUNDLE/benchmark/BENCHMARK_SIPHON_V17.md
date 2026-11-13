# BENCHMARK REAL — C++ Yield Siphon / Arbitrage Engine (FASE 17)

**Status: MEDIDO NESTA MÁQUINA. Substitui o número 0,368 μs, que nunca teve origem.**

## O que foi medido

`run_benchmark(n)` da biblioteca C++ `V16_TRANSMUTED_CORE/libsiphon_bridge.so`,
exposta via `ctypes` em `/home/team/shared/yield_siphon_bridge.py`.

Cada iteração executa o caminho quente do engine C++: atualização de preço
(SOLANA + BASE) e comparação de spread contra o threshold.

## Resultado (5 execuções, 200.000 iterações cada)

| Execução | ns/op |
|---|---|
| 1 | 22,49 |
| 2 | 22,37 |
| 3 | 22,23 |
| 4 | 22,34 |
| 5 | 22,34 |

**Faixa medida: 22,23 – 22,49 ns/op  →  ~22,3 ns/op  (0,0223 μs)**

Uma execução anterior, com apenas 50.000 iterações (aquecimento/carga fria),
deu 58,69 ns/op. O valor estável em regime é o da tabela acima.

## Como reproduzir

```bash
cd /home/team/shared
for i in 1 2 3 4 5; do
  python3 -c "import yield_siphon_bridge as b; print(round(b.run_benchmark(200000),2))"
done
```

## Ambiente da medição

- CPU: Intel(R) Xeon(R) Processor @ 2.90GHz — 2 vCPU
- SO: container Linux, Python 3
- Biblioteca: `libsiphon_bridge.so` (16 KB), build já existente no repositório

## O que este número É — e o que NÃO é

**É:** a latência por operação do comparador de arbitragem em memória, em uma
única thread, medida com o próprio código C++ do pacote.

**NÃO é:** latência de execução de ordem em exchange real, nem throughput de
produção. O engine não envia ordens: `execute_trade()` apenas incrementa um
contador. `siphon_network.h` descreve o componente como *simulação*.

## Como citar em material de produto (texto aprovado)

> Comparador de arbitragem em C++: **~22 ns por operação** (22,23–22,49 ns,
> 5 execuções de 200.000 iterações, Xeon 2,90 GHz, 2 vCPU), medido nesta
> máquina com o benchmark incluído no pacote. É um comparador em memória —
> não é latência de execução em exchange.

Nunca escrever 0,368 μs, "368 ns" ou "sub-microssegundo" em nenhum material.
