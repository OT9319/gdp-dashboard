# Branch Protection Configuration
# 
# This file documents the recommended branch protection settings
# for implementing the "Contrôleur Qualité & Logisticien" workflow.
# 
# GitHub Repository Settings > Branches > Add rule for 'main':

## Required Status Checks:
- CI - Contrôleur Qualité (HYGIE & AEGIS) / quality-control
- CI - Contrôleur Qualité (HYGIE & AEGIS) / security-scan  
- CI - Contrôleur Qualité (HYGIE & AEGIS) / deployment-validation

## Branch Protection Settings:
- ✅ Require a pull request before merging
- ✅ Require approvals (1 minimum)
- ✅ Dismiss stale PR approvals when new commits are pushed
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging
- ✅ Require conversation resolution before merging
- ❌ Require signed commits (optional - depends on team policy)
- ✅ Restrict pushes that create files that have a path longer than this (100)
- ✅ Restrict pushes that update files that have a path longer than this (100)

## Admin Settings:
- ❌ Allow force pushes (disabled for safety)
- ❌ Allow deletions (disabled for safety)

This configuration ensures that the "Barrière Humaine" (Human Barrier) 
works in conjunction with the automated quality controls to maintain
code quality, security, and deployment readiness.