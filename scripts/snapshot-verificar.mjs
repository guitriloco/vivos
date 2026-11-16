#!/usr/bin/env node
/* ---------------------------------------------------------------------------
   Snapshot de verificação — roda ANTES do `vite build`.

   O runtime que serve o site ao vivo NÃO enxerga /home/team/shared: tudo o que
   a página /verificar precisa tem de entrar DENTRO do build. Este script lê, no
   momento do build, e escreve src/data/verificar-snapshot.json, que é importado
   pelo endpoint (/api/verificar) e pela página (/verificar) e portanto fica
   embutido no bundle.

   O que entra no snapshot:
     1) o manifesto SHA256SUMS do VIVOS_MASTER_BUNDLE (51 hashes / caminhos);
     2) as últimas 50 linhas datadas do TRUTH_LOG.tsv (histórico do gate);
     3) o commit de origem do manifesto, derivado do repositório canônico.

   Duas regras que este script obedece e que o build herda:

   A) FALHA FECHADA. Se uma fonte não puder ser lida, o snapshot anterior NUNCA
      é reaproveitado. O JSON é reescrito com `status: "falhou"`, evidência
      vazia (arquivos: [], gate: null) e a lista de problemas, e o script sai
      com código 1 — o build para, nada é publicado. Assim um manifesto antigo
      jamais aparece como evidência atual.

   B) COMMIT DERIVADO OU AUSENTE. Não existe id de commit escrito à mão. O
      commit de origem é o último commit do repositório canônico cujo blob de
      VIVOS_MASTER_BUNDLE/SHA256SUMS tem sha256 idêntico ao manifesto lido. Se
      nenhum commit bater (ou não houver clone local), `commit.id` é null com
      `commit.fonte: "ausente"` e o motivo — nunca um palpite.

   Esta é a cópia versionada (guitriloco/vivos). A que roda no build do site é
   /home/team/shared/site/scripts/snapshot-verificar.mjs, byte a byte igual a
   esta — o teste compara as duas quando o site está na máquina.

   Variáveis de ambiente (todas opcionais):
     VIVOS_SHARED_DIR        raiz das fontes            (padrão /home/team/shared)
     VIVOS_BUNDLE_SHA256SUMS manifesto                  (padrão $SHARED/VIVOS_MASTER_BUNDLE/SHA256SUMS)
     VIVOS_TRUTH_LOG         log do gate                (padrão $SHARED/TRUTH_LOG.tsv)
     VIVOS_SNAPSHOT_OUT      arquivo de saída           (padrão src/data/verificar-snapshot.json)
     VIVOS_REPO_DIR          clone do repo canônico     (se definido, é o único candidato)
     VIVOS_REPO_MANIFEST_PATH caminho do manifesto no repo (padrão VIVOS_MASTER_BUNDLE/SHA256SUMS)
   ------------------------------------------------------------------------- */

import { readFile, writeFile, mkdir, readdir } from "node:fs/promises";
import { createHash } from "node:crypto";
import { execFile } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, join } from "node:path";

const AQUI = dirname(new URL(import.meta.url).pathname);
const RAIZ = join(AQUI, "..");

const SHARED = process.env.VIVOS_SHARED_DIR ?? "/home/team/shared";
const MANIFESTO = process.env.VIVOS_BUNDLE_SHA256SUMS ?? join(SHARED, "VIVOS_MASTER_BUNDLE", "SHA256SUMS");
const TRUTH_LOG = process.env.VIVOS_TRUTH_LOG ?? join(SHARED, "TRUTH_LOG.tsv");
const SAIDA = process.env.VIVOS_SNAPSHOT_OUT ?? join(RAIZ, "src", "data", "verificar-snapshot.json");

const CAMINHO_MANIFESTO_NO_REPO = process.env.VIVOS_REPO_MANIFEST_PATH ?? "VIVOS_MASTER_BUNDLE/SHA256SUMS";
const REPO_ENV = process.env.VIVOS_REPO_DIR ?? null;

const LIMITE_GATE = 50;
const COLUNAS_GATE = ["timestamp", "bundle", "tamper", "py_compile", "secrets", "veredito"];

function sha256De(dados) {
  return createHash("sha256").update(dados).digest("hex");
}

function mensagem(erro) {
  return erro instanceof Error ? erro.message : String(erro);
}

function git(diretorio, argumentos) {
  return new Promise((resolver) => {
    execFile(
      "git",
      ["-C", diretorio, ...argumentos],
      { timeout: 20000, maxBuffer: 16 * 1024 * 1024 },
      (erro, stdout, stderr) => {
        if (erro) {
          const bruto = String(stderr ?? "").trim() || erro.message;
          resolver({ ok: false, motivo: bruto.split("\n")[0] ?? "erro do git" });
          return;
        }
        resolver({ ok: true, saida: String(stdout ?? "") });
      },
    );
  });
}

function lerManifesto(texto) {
  const arquivos = [];
  for (const linha of texto.split("\n")) {
    const limpa = linha.trim();
    if (!limpa || limpa.startsWith("#")) continue;
    const partes = limpa.split(/\s+/);
    if (partes.length < 2) continue;
    const sha256 = (partes[0] ?? "").toLowerCase();
    if (!/^[0-9a-f]{64}$/.test(sha256)) continue;
    // Caminho pode conter espaços: junta tudo depois do hash e remove o "*" do
    // formato binário do sha256sum.
    const caminho = partes.slice(1).join(" ").replace(/^\*/, "");
    arquivos.push({ sha256, caminho });
  }
  if (arquivos.length === 0) throw new Error("manifesto sem nenhum hash válido");
  return arquivos;
}

function lerGate(texto) {
  const linhas = texto
    .split("\n")
    .map((l) => l.trimEnd())
    .filter((l) => l.length > 0);

  // Primeira linha é cabeçalho; o resto é dado.
  const dados = linhas.filter((l) => !/^timestamp\b/i.test(l));
  if (dados.length === 0) throw new Error("log sem nenhuma linha datada de gate");

  const ultimas = dados.slice(-LIMITE_GATE).map((linha) => {
    const c = linha.split("\t").map((v) => v.trim());
    const registro = {};
    COLUNAS_GATE.forEach((nome, i) => {
      registro[nome] = c[i] ?? "";
    });
    return registro;
  });

  const ultima = ultimas[ultimas.length - 1] ?? null;
  return {
    arquivo: "TRUTH_LOG.tsv",
    colunas: COLUNAS_GATE,
    linhas_no_arquivo: dados.length,
    linhas_consideradas: ultimas.length,
    ultima,
    linhas: ultimas,
  };
}

/* Candidatos a clone do repositório canônico. Se VIVOS_REPO_DIR está definido,
   ele é o único candidato (é assim que o teste força o caso "ausente"). */
async function candidatosDeRepo() {
  if (REPO_ENV !== null) return [REPO_ENV];

  const candidatos = [join(SHARED, "vivos")];
  try {
    const entradas = await readdir("/home", { withFileTypes: true });
    for (const entrada of entradas) {
      if (!entrada.isDirectory()) continue;
      const caminho = join("/home", entrada.name, "vivos");
      if (!candidatos.includes(caminho)) candidatos.push(caminho);
    }
  } catch {
    /* sem /home legível: ficam só os candidatos explícitos */
  }
  return candidatos;
}

function slugDoRemoto(url) {
  if (!url) return null;
  const limpo = url.trim().replace(/\.git$/, "");
  const m = /(?:[:/])([^/:]+\/[^/:]+)$/.exec(limpo);
  return m && m[1] ? m[1] : null;
}

/* Deriva o commit de origem: o último commit do repo canônico cujo blob do
   manifesto tem sha256 idêntico ao manifesto lido. Sem palpite. */
async function derivarCommit(shaDoManifesto) {
  const tentativas = [];
  const candidatos = await candidatosDeRepo();

  for (const diretorio of candidatos) {
    if (!existsSync(diretorio)) {
      tentativas.push(`${diretorio}: caminho não existe`);
      continue;
    }
    const log = await git(diretorio, [
      "log",
      "--all",
      "--format=%H",
      "-n",
      "400",
      "--",
      CAMINHO_MANIFESTO_NO_REPO,
    ]);
    if (!log.ok) {
      tentativas.push(`${diretorio}: não é repositório git (${log.motivo})`);
      continue;
    }
    const commits = log.saida
      .split("\n")
      .map((l) => l.trim())
      .filter(Boolean);
    if (commits.length === 0) {
      tentativas.push(`${diretorio}: nenhum commit toca ${CAMINHO_MANIFESTO_NO_REPO}`);
      continue;
    }

    const remoto = await git(diretorio, ["config", "--get", "remote.origin.url"]);
    const repositorio = remoto.ok ? slugDoRemoto(remoto.saida) : null;

    for (const commit of commits) {
      const blob = await git(diretorio, ["show", `${commit}:${CAMINHO_MANIFESTO_NO_REPO}`]);
      if (!blob.ok) continue;
      if (sha256De(Buffer.from(blob.saida, "utf8")) === shaDoManifesto) {
        return {
          id: commit,
          curto: commit.slice(0, 7),
          repositorio,
          fonte: `git log -- ${CAMINHO_MANIFESTO_NO_REPO} · blob com sha256 idêntico (${diretorio})`,
          motivo: null,
        };
      }
    }
    tentativas.push(`${diretorio}: nenhum commit tem este manifesto byte a byte`);
  }

  return {
    id: null,
    curto: null,
    repositorio: null,
    fonte: "ausente",
    motivo: tentativas.length > 0 ? tentativas.join("; ") : "nenhum clone do repositório canônico encontrado",
  };
}

async function main() {
  const problemas = [];
  let arquivos = null;
  let gate = null;
  let shaDoManifesto = null;

  try {
    const bruto = await readFile(MANIFESTO);
    shaDoManifesto = sha256De(bruto);
    arquivos = lerManifesto(bruto.toString("utf8"));
  } catch (erro) {
    problemas.push(`manifesto indisponível: ${mensagem(erro)}`);
  }

  try {
    gate = lerGate(await readFile(TRUTH_LOG, "utf8"));
  } catch (erro) {
    problemas.push(`TRUTH_LOG indisponível: ${mensagem(erro)}`);
  }

  const commit =
    shaDoManifesto === null
      ? {
          id: null,
          curto: null,
          repositorio: null,
          fonte: "ausente",
          motivo: "manifesto ilegível: commit de origem não derivável",
        }
      : await derivarCommit(shaDoManifesto);

  const falhou = arquivos === null || gate === null;

  const snapshot = {
    schema: 2,
    status: falhou ? "falhou" : "ok",
    gerado_em: new Date().toISOString(),
    origem: {
      manifesto: MANIFESTO,
      manifesto_rotulo: "VIVOS_MASTER_BUNDLE/SHA256SUMS",
      truth_log: "TRUTH_LOG.tsv",
    },
    commit,
    manifesto:
      arquivos === null
        ? null
        : { total_arquivos: arquivos.length, algoritmo: "sha256", sha256_do_manifesto: shaDoManifesto },
    arquivos: arquivos ?? [],
    gate: gate ?? null,
    fontes: {
      manifesto: arquivos === null ? "falhou" : "ok",
      truth_log: gate === null ? "falhou" : "ok",
      commit: commit.id === null ? "ausente" : "derivado",
    },
    problemas_no_build: problemas,
  };

  try {
    await mkdir(dirname(SAIDA), { recursive: true });
    await writeFile(SAIDA, JSON.stringify(snapshot, null, 2) + "\n", { encoding: "utf8", mode: 0o664 });
  } catch (erro) {
    console.error(
      `[snapshot-verificar] FALHA ao gravar ${SAIDA} (${mensagem(erro)}): sem snapshot gravado, o build para.`,
    );
    process.exitCode = 1;
    return;
  }

  if (falhou) {
    console.error(
      `[snapshot-verificar] FALHA FECHADA: ${problemas.join("; ")}. Snapshot marcado como "falhou", evidência vazia, build interrompido — nenhum dado antigo é reaproveitado.`,
    );
    process.exitCode = 1;
    return;
  }

  console.log(
    `[snapshot-verificar] ok · ${String(arquivos.length)} hashes · ${String(gate.linhas_consideradas)} linhas de gate · commit ${commit.id ?? "ausente (não derivável)"}`,
  );
}

await main();
