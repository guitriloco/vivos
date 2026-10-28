# ⚜️ AUDITORIA DE REPOSITÓRIOS — OS 79 LINKADOS ⚜️

**Auditor:** agent-repositor-artificial · 2026-10-28

## 0. Método e limite declarado

**O que eu fiz:** verifiquei os **79** repositórios listados no bloco gerenciado de `/home/team/shared/WORKFLOW.md` com
```
while read r; do git ls-remote --heads "https://github.com/$r.git"; done < repos.txt
```
**Resultado: 79 OK / 0 falhas.** Todos os 79 existem e têm pelo menos uma branch remota. Lista completa em `/tmp/lsremote.txt` (artefato de sessão; a fonte canônica é o `WORKFLOW.md`).

**O que eu NÃO fiz:** não clonei os 79 individualmente (952 MB só o `vivos`; o disco `/home` está em 98%). Portanto:

> **A existência de todos os 79 está provada. O conteúdo interno da maioria NÃO foi inspecionado.** Onde eu digo o que existe dentro, é porque há espelho local em `/home/team/shared` ou porque eu clonei. Onde eu não sei, está escrito **"conteúdo não inspecionado"**. Não inventei descrição de repositório.

**Espelhos locais que eu pude inspecionar:**
- `/home/team/shared/fusion/` — **5.077 arquivos**, dos quais **1.354** fora de `.git` (ou seja, 3.723 objetos git). Contém clones de trabalho, incluindo `fusion/cognitive-sdk-vivos/Understand-Anything/` (com scripts de benchmark reais: `benchmark-layout.mjs`, `benchmark-aggregations.mjs`).
- `/home/team/shared/` tem **14 diretórios `.git` aninhados** no total.
- `/home/team/shared/V16_TRANSMUTED_CORE/`, `VIVOS_DIST_V16/`, `vivos_node/` — artefatos do núcleo C++ (espelho de `YIELD-SIPHON`).
- `/home/team/shared/PANTHEON_AGENTES/` — 36 arquivos de dossiês.
- Clone completo de `guitriloco/vivos` em `/tmp/vivos_audit` (952 MB, pack 70,97 MiB).

---

## 1. Agrupamento funcional dos 79

### Grupo A — Núcleo canônico do império (4)

| Repositório | Inspeção | O que genuinamente existe |
|---|---|---|
| **`guitriloco/vivos`** | ✅ **CLONADO E AUDITADO** | **Ativo real.** 6 commits em `main` (HEAD `20d7de1`), + branch `machine-state-snapshot` (`d4e352e`). 39.281 arquivos no HEAD. Contém: `vivos_master.sh` (6.848 B, testado), `PANTHEON_AGENTES/` (35 dossiês), `REGISTRO_AGENTES_V17.md` (8.919 B), `SNAPSHOT_MANIFEST_FULL.md`, `novas/`, `agents/` (34 homes), `database/`, `shared/` |
| `guitriloco/NECTAR_SYNC_TEST` | existência | conteúdo não inspecionado |
| `guitriloco/Sovereign-Imperial-Core` | existência | conteúdo não inspecionado |
| `guitriloco/Sovereign-Intelligence-SDK` | existência | conteúdo não inspecionado |

---

### Grupo B — Os 5 Supreme Cores do catálogo (5)

São exatamente os nomes que aparecem como SKUs em `stripe_products.json`. **Este é o ponto onde catálogo e código deveriam se encontrar — e só um se encontra.**

| Repositório | SKU correspondente | O que existe |
|---|---|---|
| **`guitriloco/YIELD-SIPHON`** | $499 `prod_v17_yield-siphon` | ✅ **Código existe** (espelho em `V16_TRANSMUTED_CORE/`): `transmuted_core.cpp` (53 L), `arbitrage_engine.h` (60 L), `siphon_network.h` (59 L), `python_bridge.cpp`, `yield_siphon_bridge.py`, `performance_audit.py`, `libyieldsiphon.so`, `libsiphon_bridge.so`. **Compila limpo; não benchmark; mede 0,17x.** Ver `AUDITORIA_VERACIDADE.md` §1 |
| `guitriloco/WRAITH-MESH` | $299 | existência confirmada; **conteúdo não inspecionado**; **nenhum artefato executável identificado** em `/home/team/shared` |
| `guitriloco/COGNITIVE-SDK` | $99 | existência confirmada; espelho local em `fusion/cognitive-sdk-vivos/` contém `Understand-Anything` com **dois scripts de benchmark reais** (`benchmark-layout.mjs`, `benchmark-aggregations.mjs`) — mas são benchmarks de dashboard/layout, **não** de capacidade cognitiva. Nenhum "SDK cognitivo" próprio identificado |
| `guitriloco/SECURE-VAULT` | $199 | existência confirmada; **conteúdo não inspecionado**; **nenhum artefato identificado** |
| `guitriloco/OMNI-HUB` | $999 | existência confirmada; **conteúdo não inspecionado**; **nenhum artefato identificado** |

> **Este quadro é a auditoria inteira em miniatura:** 5 produtos de $99 a $999 à venda; **1** tem código, e esse código não sustenta a alegação. Os outros 4 são nomes de repositório.

---

### Grupo C — Linhagem "Nectar" / "Mutante" / "Império" (17)

`nectar-suprema` · `nectar-suprema-soberano` · `Nectar_Empire_Lattice` · `Nectar-Global-Info-Hybrid-Mastery` · `Nectar-Omni-Verticals` · `Mutante-Nectar-Sovereignty` · `Mutante-Apex-Functions` · `Imperio-Mutante` · `Imperio-Mutante-v15-Vault` · `Imperio-Mutante-v3-Core` · `Imperio_mutante` · `vvv` · `premium`→(`Premium`) · `Nectar_Wealth` · `Nectar_Pets` · `Nectar_Health` · `Nectar_Dev`

**Estado:** **79/79 existem**. **Conteúdo não inspecionado** (exceto `vvv`/`Imperio-Mutante-v15-Vault`, que o plano descreve como vault/ledger — não verifiquei).

**Observação de nomenclatura (fato observável, não opinião):** existem **três grafias** do mesmo conceito de "Imperio Mutante" (`Imperio-Mutante`, `Imperio-Mutante-v3-Core`, `Imperio_mutante`) e **quatro** do "nectar supremo" (`nectar-suprema`, `nectar-suprema-soberano`, `Nectar_Empire_Lattice`, `Nectar-Global-Info-Hybrid-Mastery`). Isso é dívida de organização: não há como um comprador saber qual é canônico. **Não pude determinar qual é o ativo principal de cada família sem clonar — não afirmo qual é.**

---

### Grupo D — Verticais de negócio (Forks/CLIs e ferramentas de terceiros) (26)

`opencode` · `cline` · `OpenHands` · `continue` · `gemini-cli` · `gemini` · `supercli` · `aider` · `free-claude-code` · `deepseek-harness` · `savant-code` · `great_cto` · `cto.new` · `openhuman` · `terax-ai` · `Lite-Server` · `script` · `projets` · `project-2.0` · `project-2.0-backup` · `AfiliPainel` · `SwiftCommerce` · `MoneyPrinterTurbo` · `Automatic`→(`Auto`) · `olocoo` · `oi` · `ooi` · `Yes` · `Nov` · `kok`

**Estado:** existem; **conteúdo não inspecionado**.

**Fato importante e verificável:** vários destes são **projetos open-source de terceiros** (opencode, cline, OpenHands, continue, gemini-cli, aider, free-claude-code, MoneyPrinterTurbo, prompts.chat, discourse, silverbullet, AionUi, OpenCut, OpenMontage, awesome-*). Eles estão **forkados** na conta. **Forkar não é construir**, e **licença de terceiro não é ativo vendável** — vários têm licenças (AGPL, Apache, MIT) que impõem obrigações a quem redistribui comercialmente. **Não auditei as licenças de cada um; isso precisa ser feito antes de empacotar qualquer coisa que os contenha.**

---

### Grupo E — Conteúdo, mídia e front-end (6)
`OpenCut` · `OpenMontage` · `fabrica-conteudo` · `AionUi` · `YouBGram_WebApp` · `-imaginastudio`
**Estado:** existem; **conteúdo não inspecionado**.

### Grupo F — Infra, rede e segurança (6)
`proxy_mutante` · `proxy` · `StegoForge` · `FreeDomain` · `WRAITH-MESH`(já contado em B) · `SECURE-VAULT`(idem)
**Estado:** existem; **conteúdo não inspecionado**. Nenhum teste de segurança foi executado por mim.

### Grupo G — Skills, prompts e catálogos de IA (7)
`agent-skills` · `ui-ux-pro-max-skill` · `prompts.chat` · `awesome-ai-tools` · `awesome-free-llm-apis` · `Understand-Anything` · `OpenCut`(dup)
**Estado:** existem; **conteúdo não inspecionado**. `agent-skills` é citado no resultado da tarefa `f782c3cb` (COLONIZATION) como um dos três repos fusionados no MUTANT-NECTAR.

### Grupo H — Diversos / sem categoria aparente (8)
`Organizacoes` · `Sovereign-L2-Arbitrage` · `StegoForge`(dup) · `Ai`→(`AionUi` dup) · `quantum-*` (não é repo; é agente) · `database` (não é repo) · `novos` (repo separado, distinto da pasta `novas/` do `vivos`)
**Estado:** existem; **conteúdo não inspecionado**.

---

## 2. Resumo quantitativo

| Grupo | Nº de repos | Existência verificada | Conteúdo inspecionado | Com artefato executável que eu executei |
|---|---|---|---|---|
| A — Núcleo canônico | 4 | ✅ | **1** (`vivos`) | **1** (`vivos_master.sh`) |
| B — Supreme Cores | 5 | ✅ | **1** (`YIELD-SIPHON`) | **1** (compila; benchmark falha) |
| C — Linhagem Nectar/Mutante | 17 | ✅ | **0** | **0** |
| D — Ferramentas/forks | ~30 | ✅ | **0** | **0** |
| E — Mídia/front | 6 | ✅ | **0** | **0** |
| F — Infra/rede | 4 | ✅ | **0** | **0** |
| G — Skills/catálogos | 6 | ✅ | ~**0,5** (scripts de benchmark vistos em `Understand-Anything`) | **0** |
| H — Diversos | 7 | ✅ | **0** | **0** |
| **Total** | **79** | **79 / 79** | **~3** | **2** |

---

## 3. Três conclusões que a lista de repos sustenta

1. **79 repositórios é uma medida de atividade, não de produto.** Nenhum deles é um pacote que um comprador possa instalar e usar, exceto o `vivos` (que entrega um backup de ambiente de trabalho de 39 mil arquivos, não um produto).
2. **O catálogo comercial (42 SKUs) e o inventário técnico (79 repos) não se mapeiam.** Dos 7 "Supreme Cores" à venda, **1** tem código. Os 35 "fractal variants" não têm repositório próprio — são o mesmo produto com preço multiplicado.
3. **A nomenclatura duplicada é um risco comercial concreto.** Três "Imperio Mutante", quatro "nectar suprema". Um comprador que peça "o produto" não tem como saber qual receber, e o time não tem como garantir qual é o canônico sem uma decisão explícita do lead.

---

## 4. O que eu recomendo para uma próxima auditoria de repo

Para cada um dos 79, em ordem de valor comercial:
1. `git ls-tree -r --name-only <ref> | wc -l` (tamanho real)
2. `git log -1 --format='%H %ad %s'` (último commit real, não o relatado)
3. Existência de `README.md`, `package.json`/`pyproject.toml`/`Cargo.toml`/`CMakeLists.txt` (é construível?)
4. `LICENSE` (é redistribuível comercialmente?)
5. Um comando de teste que rode e produza saída verificável

**Nenhum desses 5 passos foi feito para 76 dos 79.** Isso é o trabalho que falta, e é mecânico.

*A LINHA É RETA QUANDO O QUE AFIRMAMOS É O QUE CONSEGUIMOS PROVAR.*
