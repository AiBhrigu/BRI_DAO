#!/bin/bash

echo "🔧 Setting up devlog structure..."

mkdir -p docs/devlog

cat > docs/devlog/index.md <<EOF
# 🕰 DevLog — Хроника BRI DAO

Добро пожаловать в DevLog — здесь публикуются ключевые события, обновления, улучшения и планы развития проекта.

## 📅 Последние события
<!-- devlog_entries will be inserted here -->

EOF

cat > .github/workflows/devlog.yml <<EOF
name: Update DevLog

on:
  push:
    paths:
      - 'docs/devlog/*.md'

jobs:
  update-devlog:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Append latest commit to DevLog
        run: |
          DATE=$(date "+%Y-%m-%d")
          COMMIT_MSG=$(git log -1 --pretty=%B)
          echo "- [$DATE] $COMMIT_MSG" >> docs/devlog/\$(date "+%Y-%m").md

      - name: Auto-commit DevLog update
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "Update DevLog from latest commit"
          file_pattern: docs/devlog/*.md
        env:
          GITHUB_TOKEN: \${{ secrets.GH_TOKEN_AUTOBOT }}
EOF

echo "✅ DevLog setup complete."
