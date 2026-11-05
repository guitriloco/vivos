# ⚠️ CAVEATS — VIVOS_MASTER_BUNDLE (Phase 17)

Defeitos conhecidos, reconstruções e o que **não** está no pacote. Se algo aqui
te incomodar, é porque deveria incomodar: melhor um pacote com defeito declarado
do que um pacote com defeito escondido.

## 1. `V15_1_SOVEREIGN_LOOP.py` — NÃO está neste bundle, e tem reconstrução

O loop mestre (`/home/team/shared/v15_1_master_logic/V15_1_SOVEREIGN_LOOP.py`,
51 KB) **não faz parte deste pacote** — a estrutura aprovada da Fase 17 não o
inclui. Se ele for adicionado depois, isto precisa ir junto:

- o cabeçalho da classe `EvolutionCore` foi **apagado pela corrupção** e
  **reconstruído** a partir do uso observado (`evolution_cycle`,
  `mutation_factor = 0.01`, `codex`);
- o arquivo **compila**, mas essa parte **não é original** — é reconstrução.

## 2. `vivos_master.sh --dry-run` conta arquivos demais (defeito de relatório)

O `--dry-run` conta com `find "$SOURCE" -type f` **antes** de aplicar as
exclusões do `rsync` (`.git`, `__pycache__`, `*.pyc`, `.run`, `.ssh`, `*.pem`,
`*.key`, `.env*`, `.claude*`, `.mcp.json`). Resultado: o número do dry-run é
maior que o número realmente instalado.

Instância histórica: **5.758 no dry-run contra 1.881 realmente instalados**
(incluía `.git` aninhados). Verificado de novo em 2026-11-05:

```
dry-run: copiaria ~12387 arquivos de /home/team/shared
find sem exclusões .................. 12.387
find com as exclusões do rsync ......  8.512
```

**É defeito de relatório, não do instalador:** o `rsync` instala corretamente o
que deve. O número impresso é que engana. Não use a saída do `--dry-run` como
métrica de tamanho de instalação.

## 3. `REGISTRO_AGENTES_V17.md` — contagens com defeito interno

O registro (em `registry/`) já foi corrigido de 34 → 35 agentes e 22 → 23
tarefas, mas **ainda tem uma inconsistência verificável**:

- o cabeçalho da seção TIER C diz **"(21)"**;
- a tabela do TIER C lista **22** agentes;
- 13 agentes numerados (Tier S/A/B) + 22 = **35**, que é o número do roster e o
  número de dossiês em `pantheon/` (35 dossiês + 1 índice = 36 arquivos).

Ou seja: o total (35) está certo, o subtítulo do TIER C está errado por 1. Não
corrigimos o arquivo original aqui — ele é cópia fiel da fonte, e o defeito fica
registrado em vez de maquiado.

## 4. O snapshot da máquina não é produto

O snapshot de ambiente (`612d8d9`, ~39.234 arquivos) é **backup de ambiente**,
não pacote de produto, e **não está** neste bundle. Não confunda os dois: este
bundle tem menos de 200 KB de código e documentação.

## 5. `benchmark/yield_siphon_bridge.py` foi adaptado para ser portátil

A versão original resolvia a biblioteca por caminho absoluto
(`/home/team/shared/V16_TRANSMUTED_CORE/libsiphon_bridge.so`), o que quebraria
em qualquer outra máquina. No bundle a resolução é, nesta ordem:

1. `$VIVOS_SIPHON_LIB`, se definida;
2. `libsiphon_bridge.so` ao lado do próprio arquivo `.py`;
3. o caminho legado absoluto.

**Só a busca mudou.** O caminho de chamada `ctypes` é o mesmo da versão usada na
medição, e a medição foi refeita a partir do bundle: 22,04 – 22,79 ns/op (ver
`TRUTH_REGISTER.md`).

## 6. O `.so` é binário pré-compilado — mas o build é reprodutível

`libsiphon_bridge.so` (16.016 bytes) é enviado já compilado. Verificamos que ele
**corresponde ao fonte do pacote**:

```bash
g++ -O3 -fPIC -shared -I include python_bridge.cpp -o /tmp/rebuild.so
sha256sum /tmp/rebuild.so libsiphon_bridge.so
# 4ea852fed25e57097b96c04248888ea7142e3d8b2f701fcc7b83905e4146bd87  (os dois)
```

Hash idêntico nesta máquina (g++ do container, x86_64). Em outra toolchain o
binário pode diferir — recompile a partir de `python_bridge.cpp` + `include/` +
`src/` antes de confiar no binário.

## 7. A verificação de integridade foi testada por adulteração

Prova, não promessa: copiamos o bundle, alteramos **1 byte** de um arquivo,
rodamos `verify_bundle.sh` e ele **falhou com exit 1**; restauramos o byte e ele
**passou com exit 0**. As duas saídas estão no relatório de entrega e podem ser
reproduzidas assim:

```bash
cp -a VIVOS_MASTER_BUNDLE /tmp/b && cd /tmp/b
printf 'X' | dd of=README.md bs=1 seek=0 conv=notrunc status=none
./verify_bundle.sh ; echo "exit=$?"     # → BUNDLE NÃO VERIFICADO · exit=1
git -C /caminho/do/bundle checkout -- README.md   # ou restaure a cópia original
./verify_bundle.sh ; echo "exit=$?"     # → BUNDLE ÍNTEGRO · exit=0
```

O verificador também falha se alguém **adicionar** um arquivo que não está no
`SHA256SUMS` (arquivo novo não passa despercebido) e se as contagens do
`VIVOS_SUPREME_MANIFEST.json` não baterem com o disco.

## 8. Varredura de segredos — resultado

Antes do commit, varredura por `.env*`, `*.key`, `*.pem`, `.netrc`,
`.git-credentials`, `ghp_`, `gho_`, `ghs_`, `ghu_`, `ghr_`, `sk-` e
`-----BEGIN ... PRIVATE KEY-----`:

**0 achados.** Nenhum arquivo foi removido por conter segredo. O bundle não
contém credencial, chave, token nem `.git` interno.

## 9. O que o instalador faz — e o que ele não faz

`install.sh` roda `verify_bundle.sh` e só depois o instalador, com
`--source` apontando para o próprio bundle. Ele:

- copia o conteúdo do bundle para o destino e cria a estrutura de diretórios
  (`nectars/ fusion/ skills/ powers/ scripts/ docs/ vault/ site/ database/`);
- tenta auto-repair de `git`, `python3`, `rsync`, `tar`, `curl` (precisa de
  `sudo`/apt e de rede — pode falhar em ambiente fechado; falha é reportada, não
  escondida).

Ele **não**: instala dependências de sistema sem permissão, conecta Stripe, cria
produto, publica site, nem envia nada para a rede.

## 10. Estrutura: dois arquivos a mais que o mínimo da especificação

Além da árvore aprovada, o bundle inclui `benchmark/src/transmuted_core.cpp` e
`benchmark/include/*.h` completos — sem eles o `.so` não seria recompilável e a
prova de correspondência binário↔fonte (§6) seria impossível. Nada foi omitido
em relação à especificação.

---

**Um defeito declarado é um ativo. Um defeito escondido é uma dívida.**
