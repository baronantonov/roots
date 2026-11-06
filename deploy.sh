#!/usr/bin/env bash
set -e

# Единая команда для коммита и мгновенного деплоя ROOTS на GitHub Pages
MSG="${1:-update roots archive}"

cd "$(dirname "$0")"

git add index.html photos/ BIOGRAPHIES.md final-report.md person-register.csv claims-register.csv artifact-register.csv relationship-register.csv roots.ged scripts/ 2>/dev/null || git add .
if ! git diff --cached --quiet; then
  git commit -m "$MSG"
fi

git push origin main
