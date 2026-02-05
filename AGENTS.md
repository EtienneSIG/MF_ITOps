# AGENTS.md - Conventions de Développement

## 📋 Contexte du Projet

Ce repository contient une **démo Microsoft Fabric** pour IT Ops & FinOps :
- OneLake + Shortcuts
- Modèle sémantique FinOps (coûts IT + valeur business)
- Fabric Data Agent "IT Finance Analyst"
- Analyses : dérives de coûts, optimisations, workloads surdimensionnés

**Langue principale** : Français (code en anglais, docs en français)

---

## 🏗️ Structure du Repo

```
MF_ITOps/
├── data/
│   └── raw/
│       ├── subscriptions.csv         # 8 abonnements Azure
│       ├── environments.csv          # 15 environnements (prod, dev, test...)
│       ├── workloads.csv             # 120 workloads Fabric/Azure
│       ├── usage_metrics.csv         # ~36k lignes (métriques quotidiennes)
│       ├── cloud_costs.csv           # ~36k lignes (coûts quotidiens)
│       ├── business_units.csv        # 6 BU (Sales, Marketing, Finance, IT, HR, Ops)
│       ├── teams.csv                 # 30 équipes (5 par BU)
│       └── applications.csv          # 60 applications (2 par team)
├── src/
│   ├── generate_data.py              # Script principal de génération
│   ├── validate_schema.py            # Validation des schémas CSV
│   └── config.yaml                   # Configuration (volumes, distributions)
├── docs/
│   ├── schema.md                     # Dictionnaire de données (8 tables)
│   ├── demo_story.md                 # Scénario "Le Coût Fabric qui Explose"
│   ├── questions_demo.md             # 15 questions Data Agent
│   ├── fabric_setup.md               # Guide déploiement Fabric
│   ├── dax_measures.md               # Mesures DAX FinOps
│   ├── data_agent_instructions.md    # Prompt système Data Agent
│   └── data_agent_examples.md        # Exemples de réponses attendues
├── requirements.txt
├── README.md
└── AGENTS.md                         # Ce fichier
```

---

## 🎯 Conventions de Code

### Noms de Variables et Colonnes

- **Colonnes de tables** : `snake_case` (ex: `workload_id`, `cost_usd`, `cpu_usage_percent`)
- **Variables Python** : `snake_case` (ex: `workloads_df`, `daily_costs`)
- **Constantes** : `UPPER_SNAKE_CASE` (ex: `CONFIG_FILE`, `SEED`, `OUTPUT_DIR`)
- **Noms de classes** : `PascalCase` (ex: `FinOpsDataGenerator`)

### Identifiants Métier

Format standardisé :
- Subscriptions : `SUB_XXXXXXXX` (8 caractères hex)
- Environments : `ENV_XXX` (3 chiffres)
- Workloads : `WL_XXXXXXXX` (8 chiffres)
- Applications : `APP_XXXXXX` (6 chiffres)
- Teams : `TEAM_XXX` (3 chiffres)
- Business Units : `BU_XX` (2 chiffres)

### Dates et Formats

- **Dates** : ISO 8601 (`YYYY-MM-DD`) pour les dates, (`YYYY-MM-DD HH:MM:SS`) pour les timestamps
- **Encoding** : UTF-8 (tous les fichiers)
- **CSV separator** : virgule (`,`)
- **Decimal separator** : point (`.`)
- **Devise** : USD (pour cohérence avec facturation Azure)

---

## 🔧 Commandes Fréquentes

### Génération de Données

```powershell
# Générer toutes les données avec config par défaut
cd src
python generate_data.py

# Modifier les volumes : éditer src/config.yaml puis relancer
```

### Vérifications

```powershell
# Vérifier le nombre de lignes générées
Get-ChildItem ..\data\raw\*.csv | ForEach-Object { 
    Write-Host "$($_.Name): $((Get-Content $_.FullName | Measure-Object -Line).Lines - 1) lignes"
}

# Vérifier l'encodage UTF-8
Get-Content ..\data\raw\workloads.csv -Encoding UTF8 | Select-Object -First 5

# Calculer la taille totale des données
(Get-ChildItem ..\data\raw\*.csv | Measure-Object -Property Length -Sum).Sum / 1MB
```

### Validation du Schéma

```powershell
# Valider que les CSV respectent le schéma
python validate_schema.py

# Sortie attendue :
# ✓ subscriptions.csv : 8 lignes, 6 colonnes
# ✓ environments.csv : 15 lignes, 7 colonnes
# ✓ workloads.csv : 120 lignes, 10 colonnes
# ✓ usage_metrics.csv : ~36000 lignes, 9 colonnes
# ✓ cloud_costs.csv : ~36000 lignes, 7 colonnes
# ✓ business_units.csv : 6 lignes, 4 colonnes
# ✓ teams.csv : 30 lignes, 5 colonnes
# ✓ applications.csv : 60 lignes, 6 colonnes
```

---

## 📊 Données Métier - Contexte FinOps

### Subscriptions (Abonnements Azure)
8 subscriptions pour refléter une organisation typique :
- `Dev` (2 subs) : environnements de développement
- `Test` (2 subs) : environnements de test/UAT
- `Prod` (3 subs) : production (segmenté par criticité)
- `Shared` (1 sub) : services partagés (monitoring, logs, IAM)

### Environments
15 environnements avec tags de criticité :
- **Production** (5 env) : `prod-critical`, `prod-standard`, `prod-low`
- **Pre-production** (3 env) : `preprod`, `staging`, `uat`
- **Development** (5 env) : `dev-team1`, `dev-team2`, `dev-shared`, `integration`, `perf-test`
- **Sandbox** (2 env) : `sandbox-innovation`, `sandbox-poc`

### Workloads
120 workloads répartis par type :
- **Fabric Capacity** (40%) : Lakehouses, Warehouses, Semantic Models
- **Azure VMs** (25%) : Compute classique
- **Azure Storage** (15%) : Blob, Files, Data Lake
- **Azure SQL** (10%) : Bases de données managées
- **Azure Functions** (10%) : Serverless

**Attributs clés** :
- `capacity_units` (CU) : 1-128 pour Fabric
- `vcpu_count` : 2-64 pour VMs
- `storage_gb` : 100-50000 GB
- `provisioned_date` : Date de déploiement

### Usage Metrics
Métriques quotidiennes sur 12 mois (~36 000 lignes) :
- `cpu_usage_percent` : 10-100%
- `memory_usage_percent` : 20-95%
- `storage_used_gb` : Variable selon capacité
- `query_count` : 0-100 000 queries/jour
- `data_processed_gb` : 0-5000 GB/jour

**Patterns réalistes** :
- Pics d'usage en semaine (lun-ven)
- Usage faible le weekend
- Tendance croissante sur 12 mois (+15% en moyenne)
- Anomalies ponctuelles (Black Friday, fin de trimestre fiscal)

### Cloud Costs
Coûts quotidiens calculés selon :
- **Fabric** : $8 par CU par jour
- **VMs** : $0.10-$2.00 par vCPU par heure
- **Storage** : $0.02-$0.05 par GB par mois
- **SQL** : $5-$50 par DB par jour
- **Functions** : $0.20 par million d'exécutions

**Dérives simulées** :
- Croissance organique : +2-5% par mois
- Pic janvier 2026 : +35% (pour scénario démo)
- Workloads surdimensionnés : coût élevé, usage < 40%

### Business Mapping
**6 Business Units** :
- Sales : CRM, Sales Analytics, Customer Data
- Marketing : Campaign Management, Web Analytics
- Finance : ERP, Financial Reporting, Budget Planning
- IT : Infrastructure Monitoring, DevOps Tools
- HR : HRIS, Talent Management
- Operations : Supply Chain, Manufacturing Execution

**30 Teams** (5 par BU) :
- Chaque team gère 2 applications en moyenne
- Budget IT alloué : $5K-$50K/mois selon taille

**60 Applications** :
- Chaque app consomme 1-3 workloads
- Mapping app → workload → coût
- Utilisateurs actifs : 10-500 par app

---

## 🎨 Règles de Génération de Données

### Réalisme des Coûts
- **Production** : coûts 3x plus élevés que dev/test (haute disponibilité, redondance)
- **Critical workloads** : coûts 2x plus élevés (SLA, monitoring)
- **Sandbox** : coûts faibles mais souvent gaspillés (usage < 10%)

### Patterns Temporels
- **Jours ouvrés** : usage 60-90%
- **Weekend** : usage 20-40%
- **Nuit** : usage 10-30%
- **Tendance annuelle** : +15% (croissance business)

### Anomalies Réalistes
- **Over-provisioning** : 20% des workloads ont usage < 30% mais coût > $1000/mois
- **Zombie workloads** : 5% des workloads ont usage < 5% (candidats à suppression)
- **Cost spikes** : 3-4 pics de coût sur l'année (événements business)

### Relations Business ↔ IT
- **Application critique** → workload prod → coût justifié
- **POC abandonné** → workload sandbox → coût à optimiser
- **App peu utilisée** → workload surdimensionné → downscale possible

---

## 🧮 Mesures DAX Clés

Ces mesures doivent être créées dans le modèle sémantique Fabric :

### Coûts
```dax
Total Cost = SUM(cloud_costs[cost_usd])
Total Cost MTD = TOTALMTD([Total Cost], 'Date'[Date])
Cost Growth MoM = 
    DIVIDE(
        [Total Cost MTD] - CALCULATE([Total Cost MTD], DATEADD('Date'[Date], -1, MONTH)),
        CALCULATE([Total Cost MTD], DATEADD('Date'[Date], -1, MONTH))
    )
```

### Usage
```dax
Avg CPU Usage = AVERAGE(usage_metrics[cpu_usage_percent])
Avg Storage Usage = AVERAGE(usage_metrics[storage_used_gb])
Total Queries = SUM(usage_metrics[query_count])
```

### Efficacité
```dax
Cost per Query = DIVIDE([Total Cost], [Total Queries])
Utilization Rate = DIVIDE([Avg CPU Usage], 100)
Wasted Capacity = 
    CALCULATE(
        [Total Cost],
        FILTER(workloads, [Avg CPU Usage] < 40 && [Total Cost] > 1000)
    )
```

### Business Value
```dax
Cost per Team = 
    CALCULATE([Total Cost], RELATEDTABLE(applications))
Cost per Active User = 
    DIVIDE([Total Cost], SUM(applications[active_users]))
```

---

## 🔍 Validation des Données Générées

Avant de déployer sur Fabric, vérifier :

### Cohérence Volumétrique
```powershell
# Nombre de lignes attendu
subscriptions.csv     : 8 lignes
environments.csv      : 15 lignes
workloads.csv         : 120 lignes
usage_metrics.csv     : ~36,000 lignes (120 workloads × 365 jours × 80% couverture)
cloud_costs.csv       : ~36,000 lignes (même volumétrie)
business_units.csv    : 6 lignes
teams.csv             : 30 lignes
applications.csv      : 60 lignes
```

### Cohérence Relationnelle
```python
# Vérifier les FK (Foreign Keys)
assert len(environments[~environments['subscription_id'].isin(subscriptions['subscription_id'])]) == 0
assert len(workloads[~workloads['environment_id'].isin(environments['environment_id'])]) == 0
assert len(usage_metrics[~usage_metrics['workload_id'].isin(workloads['workload_id'])]) == 0
assert len(applications[~applications['team_id'].isin(teams['team_id'])]) == 0
```

### Cohérence Métier
```python
# Vérifier les ranges de valeurs
assert usage_metrics['cpu_usage_percent'].between(0, 100).all()
assert cloud_costs['cost_usd'].min() >= 0
assert workloads['capacity_units'].between(1, 128).all()
```

---

## 💡 Tips pour la Démo

### Points Clés à Montrer
1. **Mapping coût → business** : Du workload à la business unit via applications et teams
2. **Détection anomalies** : Workloads avec coût croissant mais usage stable
3. **Optimisations chiffrées** : "Supprimer les 5 sandbox non utilisés économiserait $X/mois"
4. **Justification business** : "Le coût de 'Sales Analytics' est justifié par 500 users actifs"

### Questions Impressionnantes pour le Data Agent
- "Compare le coût par utilisateur actif entre les apps Marketing et Finance"
- "Quels workloads en production ont un usage < 50% sur les 30 derniers jours ?"
- "Si je downscale tous les workloads dev/test à 50% de leur capacité, combien j'économise ?"
- "Quel est le ROI (coût IT / revenus générés) par business unit ?"

### Pièges à Éviter
- Ne pas créer trop de workloads "parfaits" (usage = 100%) → pas réaliste
- Ne pas oublier les coûts de stockage (souvent sous-estimés)
- Ne pas négliger les petits coûts qui s'accumulent (zombie resources)

---

## 🚀 Workflow de Développement

### 1. Modification de la Config
```yaml
# src/config.yaml
volumes:
  workloads: 150  # Augmenter de 120 à 150
```

### 2. Régénération
```powershell
cd src
python generate_data.py
```

### 3. Validation
```powershell
python validate_schema.py
```

### 4. Upload vers Fabric
- Via Azure Storage Explorer (shortcuts OneLake)
- Ou upload direct dans Lakehouse Files

### 5. Refresh du Modèle Sémantique
- Refresh des tables Delta
- Vérifier les relations
- Tester les mesures DAX

### 6. Test du Data Agent
- Poser les 15 questions de référence
- Vérifier la cohérence des réponses
- Ajuster les instructions si nécessaire

---

## 📚 Références Utiles

- [Microsoft Fabric Docs](https://learn.microsoft.com/fabric/)
- [FinOps Foundation](https://www.finops.org/)
- [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)
- [DAX Guide](https://dax.guide/)

---

## ✅ Checklist avant Démo

- [ ] Données générées (8 CSV)
- [ ] Validation schéma OK (validate_schema.py)
- [ ] Upload vers OneLake
- [ ] Tables Delta créées dans Lakehouse
- [ ] Modèle sémantique configuré (relations + mesures)
- [ ] Data Agent configuré avec instructions
- [ ] 15 questions testées
- [ ] Dashboard Power BI (optionnel)
- [ ] Scénario démo répété (demo_story.md)

---

## 🤝 Contribution

Pour améliorer cette démo :
1. Fork le repo
2. Créer une branche (`feature/amelioration-xyz`)
3. Commiter les changements
4. Pousser et créer une Pull Request

**Règles** :
- Respecter les conventions de nommage
- Ajouter des tests dans `validate_schema.py`
- Mettre à jour la documentation
- Maintenir le seed=42 pour reproductibilité

---

## 📞 Support

Pour questions ou problèmes :
- Lire d'abord la documentation dans `docs/`
- Vérifier les issues GitHub
- Contacter l'auteur

---

**Happy FinOps with Fabric! 💰🚀**
