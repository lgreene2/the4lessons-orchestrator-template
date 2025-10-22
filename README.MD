# 🧩 The 4 Lessons Orchestrator Template  
> A standardized GitHub template for 4 Lessons projects — preconfigured with automated CI, formatting, linting, and testing.

[![CI (format → lint → tests)](https://github.com/lgreene2/the4lessons-orchestrator-template/actions/workflows/ci.yml/badge.svg)](https://github.com/lgreene2/the4lessons-orchestrator-template/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.10%20|%203.11%20|%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🧠 Overview

The **4 Lessons Orchestrator Template** provides a ready-to-use foundation for all 4 Lessons projects.  
Every new repo created from this template automatically includes the same verified CI/CD pipeline as the main Orchestrator framework.

**Preconfigured automation includes:**
- ✅ **Black** for code formatting  
- ✅ **Ruff** for linting and style enforcement  
- ✅ **Pytest** for testing and coverage  
- ✅ **GitHub Actions** for CI and dependency management  
- ✅ **Dependabot** support for auto-updates  

---

## ⚙️ Built-in Workflows

| 🧩 Workflow | ⚙️ Purpose |
| :-- | :-- |
| **CI (`ci.yml`)** | Runs Format → Lint → Tests across Python 3.10–3.12 |
| **Dependabot (`dependabot.yml`)** | Keeps dependencies and GitHub Actions up to date |
| **Pre-commit (`.pre-commit-config.yaml`)** | Local developer hooks mirror the same checks as CI |
| **Security / Code of Conduct** | Automatically included for open collaboration |

---

## 💻 Local Developer Setup

```bash
# Clone your new project (after using this template)
git clone <your-new-repo-url>
cd <your-new-repo>

# Create and activate a virtual environment
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt

# Run the same checks that CI runs
python -m black .
ruff check .
pytest
