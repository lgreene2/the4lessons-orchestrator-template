# 🧩 The 4 Lessons Orchestrator  
> A base automation template for all **4 Lessons** projects — self-maintaining, verified, and Dependabot-backed.

[![Format](https://github.com/lgreene2/the4lessons-orchestrator/actions/workflows/format.yml/badge.svg)](https://github.com/lgreene2/the4lessons-orchestrator/actions/workflows/format.yml)
[![Dev Hygiene](https://github.com/lgreene2/the4lessons-orchestrator/actions/workflows/bootstrap-dev-hygiene.yml/badge.svg)](https://github.com/lgreene2/the4lessons-orchestrator/actions/workflows/bootstrap-dev-hygiene.yml)
[![Pre-commit Auto-update](https://github.com/lgreene2/the4lessons-orchestrator/actions/workflows/auto-update-precommit.yml/badge.svg)](https://github.com/lgreene2/the4lessons-orchestrator/actions/workflows/auto-update-precommit.yml)
[![Release](https://github.com/lgreene2/the4lessons-orchestrator/actions/workflows/release.yml/badge.svg)](https://github.com/lgreene2/the4lessons-orchestrator/actions/workflows/release.yml)
[![Verified Builds](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Flgreene2%2Fthe4lessons-orchestrator%2Fmain%2Fbadges%2Fverified.json)](https://github.com/lgreene2/the4lessons-orchestrator)
[![Latest Tag](https://img.shields.io/github/v/tag/lgreene2/the4lessons-orchestrator?label=latest&color=blue)](https://github.com/lgreene2/the4lessons-orchestrator/releases)

---

### 🧠 Overview

The **4 Lessons Orchestrator** is the central automation framework for all 4 Lessons projects.  
It handles formatting, linting, dependency management, version tagging, bundle packaging, and release publishing — automatically.

**Built for:**  
- Books, guides, and companion curricula  
- AI-powered game/app projects  
- DEI, education, and development pipelines  
- Any Python-based project needing verified, repeatable automation

---

## 🌱 Developer Hygiene Automation

This repository includes a **self-maintaining developer hygiene system** powered by GitHub Actions and Dependabot.  
It ensures consistent formatting, testing, and configuration management automatically.

| 🧩 Workflow | 🧰 Purpose | ⏱️ Schedule |
|:------------|:-----------|:------------|
| 🧼 **Format (`format.yml`)** | Runs Black + pre-commit formatters on all PRs. Auto-commits fixes or leaves comments on forks. | Every PR |
| 🧹 **Bootstrap Dev Hygiene (`bootstrap-dev-hygiene.yml`)** | Ensures configuration files (`pyproject.toml`, `.pre-commit-config.yaml`, `.editorconfig`, `requirements-dev.txt`, etc.) are present and correct. | Weekly (Monday 06:00 UTC) |
| 🔁 **Auto-Update Pre-commit (`auto-update-precommit.yml`)** | Refreshes all hook versions and opens a PR with updates. | Monthly (1st of each month) |
| 🤖 **Dependabot (`dependabot.yml`)** | Keeps `requirements-dev.txt` and GitHub Actions versions up-to-date. | Weekly |
| 🧩 **Branch Protection + CODEOWNERS** | Ensures all PRs pass checks and assigns appropriate reviewers automatically. | Continuous |

---

## 💻 Local Developer Setup

Developers can replicate the same environment locally:

```bash
# Create and activate a virtual environment
python -m venv .venv && source .venv/bin/activate

# Install developer dependencies
pip install -r requirements-dev.txt

# Initialize pre-commit hooks
pre-commit install
