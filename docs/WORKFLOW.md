# Workflow de Gouvernance - Pull Request

## Vue d'ensemble

Ce document décrit le processus opérationnel pour les contributions de code dans le repository "cerebrum-1", conformément à la Constitution du Repository.

## Phases du Workflow

### 1. Phase de Développement

#### Préparation
- Créer une branche feature depuis `main`
- Respecter l'architecture de dossiers (`/src`, `/docs`, `/tests`, `/prompts`)
- Suivre les principes constitutionnels (AEGIS, PORTABILITÉ, HYGIE, CHRONOS)

#### Développement
- Écrire du code clair avec commentaires explicatifs
- Documenter les nouvelles fonctions/APIs
- Implémenter les tests correspondants
- Vérifier l'absence d'informations sensibles

### 2. Phase de Commit

#### Contrôles Automatisés
- **Sécurité (AEGIS)** : Scan des secrets et informations sensibles
- **Tests (HYGIE)** : Exécution des tests unitaires
- **Qualité** : Vérification du style de code
- **Documentation** : Validation de la documentation

#### Standards de Commit
```
type(scope): description

- feat: nouvelle fonctionnalité
- fix: correction de bug
- docs: mise à jour documentation
- test: ajout/modification tests
- refactor: refactoring code
- security: correction sécurité
```

### 3. Phase de Pull Request

#### Création de la PR
1. Créer la PR avec description détaillée
2. Inclure les tests et documentation
3. Référencer les issues liées
4. Ajouter les labels appropriés

#### Analyse Automatisée (Agent IA)
L'agent IA sert de **copilote** et fournit :
- Revue de code automatisée
- Vérification des standards
- Suggestions d'amélioration
- Détection de problèmes potentiels

#### Revue Humaine (Barrière Humaine)
La **Barrière Humaine** effectue :
- Revue fonctionnelle
- Validation de l'architecture
- Vérification de la cohérence
- **Décision finale de merge**

### 4. Phase d'Intégration

#### Conditions de Merge
- [ ] Tous les tests passent
- [ ] Revue de code complète
- [ ] Documentation à jour
- [ ] Pas de secrets exposés
- [ ] Approbation de la Barrière Humaine

#### Post-Merge
- Surveillance des métriques
- Mise à jour de la documentation
- Communication des changements

## Responsabilités

### Agent IA (Copilote)
- ✅ Analyse automatisée du code
- ✅ Suggestions d'amélioration
- ✅ Vérification des standards
- ❌ Décision de merge

### Barrière Humaine (Humain)
- ✅ Revue fonctionnelle finale
- ✅ Décision de merge
- ✅ Validation architecturale
- ✅ Supervision globale

## Outils et Intégrations

### Vérifications Automatiques
- Tests unitaires et d'intégration
- Analyse de sécurité (secrets scanning)
- Vérification de style de code
- Analyse de couverture de tests

### Métriques de Qualité
- Couverture de tests
- Complexité cyclomatique
- Dette technique
- Vulnérabilités de sécurité

---

*Ce workflow garantit la conformité aux principes constitutionnels tout en maintenant l'efficacité du processus de développement.*