# GitHub Workflows Documentation

## Contents
- [Project Automation Overview](#project-automation-overview)
- [Enforcement](#enforcement)

## Project Automation Overview
This project uses GitHub Actions workflows to enforce code quality, testing standards, and branch protection. There are two primary workflows:

1. [Development PR Pipeline](#development-pr-pipeline-pryml)
2. [Merge into Main](#merge-into-main-merge-into-mainyml)

### Development PR Pipeline (`pr.yml`)
**Trigger:** 
- Pull requests targeting the `development` branch
- Manual trigger via workflow dispatch

**Purpose:**
Enforces code quality standards and runs tests before code can be merged into `development`.

**Quality Gates:**
- Code formatting (Black)
- Linting (Flake8)
- Static typing (MyPy)
- Dependency checks
- Code complexity analysis
- Security scans
- Test execution with coverage
- Coverage reporting to Codecov

### Merge into Main (`merge-into-main.yml`)
**Trigger:**
- Pull requests targeting `main`
- Direct pushes to `main` (blocked)
- Manual trigger via workflow dispatch

**Purpose:**
Controls merges into the `main` branch and enforces proper workflow.

**Key Checks:**
- Only allows merges from `development` to `main`
- Blocks direct pushes or PRs from other branches to `main`
- Requires PR CI Pipeline to pass before allowing merge
- Provides manual merge capability for administrators

---

## Enforcement
- All code must pass PR CI Pipeline before merging to `development`
- Only `development` can be merged into `main`
- Direct pushes to `main` are blocked
- Requires passing development pipeline
- Provides controlled merge process
- Administrators can manually trigger merges when needed
