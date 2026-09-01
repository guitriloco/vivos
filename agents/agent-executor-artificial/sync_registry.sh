#!/bin/bash
cd /home/agent-executor-artificial/OMNI-RESULTADO
git remote remove origin || true
git remote add origin https://x-access-token:$GITHUB_TOKEN@github.com/guitriloco/Auto.git
git push origin main:MASTER-OMNI-RESULTADO --force
cd /home/agent-executor-artificial/OMNI-RESULTADO
git remote remove origin || true
git remote add origin https://x-access-token:REDACTED_GITHUB_APP_TOKEN@github.com/guitriloco/Auto.git
git push origin main:MASTER-OMNI-RESULTADO --force
