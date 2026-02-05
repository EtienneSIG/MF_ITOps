# Schéma de données - IT Ops & FinOps

## Vue d'ensemble

Ce schéma décrit toutes les tables de données pour la démo Microsoft Fabric IT Ops & FinOps.
Les données sont organisées en trois domaines principaux :
- **Infrastructure** : subscriptions, environments, workloads
- **Métriques & Coûts** : usage_metrics, cloud_costs
- **Business Mapping** : business_units, teams, applications

## Diagramme relationnel

```
┌────────────────┐
│ SUBSCRIPTIONS  │
└────────────────┘
        │
        │ 1:N
        ▼
┌────────────────┐
│ ENVIRONMENTS   │
└────────────────┘
        │
        │ 1:N
        ▼
┌────────────────┐         ┌────────────────┐
│   WORKLOADS    │────────▶│ USAGE_METRICS  │
└────────────────┘  1:N    └────────────────┘
        │
        │ 1:N
        ▼
┌────────────────┐
│  CLOUD_COSTS   │
└────────────────┘
        ▲
        │
        │
┌────────────────┐         ┌────────────────┐         ┌────────────────┐
│ APPLICATIONS   │────────▶│     TEAMS      │────────▶│ BUSINESS_UNITS │
└────────────────┘  N:1    └────────────────┘  N:1    └────────────────┘
        │
        │ N:N (via workload_ids)
        ▼
┌────────────────┐
│   WORKLOADS    │
└────────────────┘
```

---

## Tables Infrastructure

### 1. `subscriptions`

Abonnements Azure organisés par type (dev, test, prod, shared).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `subscription_id` | VARCHAR(20) | Identifiant unique de la subscription | **PK**, format `SUB_XXXXXXXX` (8 hex) |
| `subscription_name` | VARCHAR(100) | Nom de la subscription | NOT NULL, ex: `PROD-01` |
| `subscription_type` | VARCHAR(20) | Type de subscription | `dev`, `test`, `prod`, `shared` |
| `owner` | VARCHAR(200) | Propriétaire/responsable | |
| `status` | VARCHAR(20) | Statut | `active`, `suspended`, `cancelled` |
| `created_date` | DATE | Date de création | Format ISO 8601 |

**Cardinalité** : 8 lignes

**Types de subscriptions** :
- `dev` (2) : Développement
- `test` (2) : Test/UAT
- `prod` (3) : Production (par criticité)
- `shared` (1) : Services partagés

**Index recommandés** :
- `subscription_id` (PK)
- `subscription_type`

---

### 2. `environments`

Environnements déployés dans les subscriptions (prod, preprod, dev, sandbox).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `environment_id` | VARCHAR(20) | Identifiant unique de l'environment | **PK**, format `ENV_XXX` |
| `environment_name` | VARCHAR(100) | Nom de l'environment | NOT NULL, ex: `prod-critical` |
| `environment_type` | VARCHAR(20) | Type d'environment | `production`, `preproduction`, `development`, `sandbox` |
| `subscription_id` | VARCHAR(20) | Référence vers subscription | **FK** → subscriptions |
| `region` | VARCHAR(50) | Région Azure | ex: `eastus`, `westeurope` |
| `tags` | VARCHAR(500) | Tags (key=value pairs) | Format: `env=prod,managed=true` |
| `created_date` | DATE | Date de création | Format ISO 8601 |

**Cardinalité** : 15 lignes

**Répartition par type** :
- Production (5) : `prod-critical`, `prod-standard`, `prod-low`, `prod-dr`, `prod-backup`
- Pre-production (3) : `preprod`, `staging`, `uat`
- Development (5) : `dev-team1`, `dev-team2`, `dev-shared`, `integration`, `perf-test`
- Sandbox (2) : `sandbox-innovation`, `sandbox-poc`

**Index recommandés** :
- `environment_id` (PK)
- `subscription_id` (FK)
- `environment_type`

---

### 3. `workloads`

Workloads déployés (Fabric Capacity, VMs, Storage, SQL, Functions).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `workload_id` | VARCHAR(20) | Identifiant unique du workload | **PK**, format `WL_XXXXXXXX` |
| `workload_name` | VARCHAR(200) | Nom du workload | NOT NULL |
| `workload_type` | VARCHAR(50) | Type de workload | `fabric_capacity`, `azure_vm`, `azure_storage`, `azure_sql`, `azure_functions` |
| `environment_id` | VARCHAR(20) | Référence vers environment | **FK** → environments |
| `status` | VARCHAR(20) | Statut du workload | `running`, `stopped`, `paused` |
| `created_date` | DATE | Date de création | Format ISO 8601 |
| `owner` | VARCHAR(200) | Propriétaire/responsable | |
| `tags` | VARCHAR(500) | Tags métier | |
| `capacity_units` | INTEGER | Capacity Units Fabric (F2-F128) | NULL si non Fabric |
| `vcpu_count` | INTEGER | Nombre de vCPU | NULL si non VM/SQL |
| `storage_gb` | INTEGER | Stockage provisionné (GB) | |

**Cardinalité** : 120 lignes

**Répartition par type** :
- Fabric Capacity (40%) : 48 workloads
- Azure VMs (25%) : 30 workloads
- Azure Storage (15%) : 18 workloads
- Azure SQL (10%) : 12 workloads
- Azure Functions (10%) : 12 workloads

**Répartition par environnement** :
- Production : 50%
- Pre-production : 20%
- Development : 25%
- Sandbox : 5%

**Index recommandés** :
- `workload_id` (PK)
- `environment_id` (FK)
- `workload_type`
- `status`

---

## Tables Métriques & Coûts

### 4. `usage_metrics`

Métriques d'utilisation quotidiennes par workload.

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `workload_id` | VARCHAR(20) | Référence vers workload | **FK** → workloads |
| `date` | DATE | Date de la métrique | Format ISO 8601 |
| `cpu_usage_percent` | DECIMAL(5,2) | Usage CPU (%) | 0-100 |
| `memory_usage_percent` | DECIMAL(5,2) | Usage RAM (%) | 0-100 |
| `storage_used_gb` | DECIMAL(10,2) | Stockage utilisé (GB) | >= 0 |
| `storage_provisioned_gb` | DECIMAL(10,2) | Stockage provisionné (GB) | >= storage_used_gb |
| `query_count` | INTEGER | Nombre de queries (Fabric/SQL) | >= 0 |
| `data_processed_gb` | DECIMAL(10,2) | Données traitées (GB) | >= 0, principalement Fabric |
| `active_users` | INTEGER | Utilisateurs actifs | >= 0 |

**Cardinalité** : ~36 000 lignes (120 workloads × 365 jours × ~80% couverture)

**Clé composite** : (`workload_id`, `date`)

**Patterns réalistes** :
- **Jours ouvrés** : CPU 60-90%, Memory 50-85%
- **Weekend** : CPU 20-40%, Memory 30-50%
- **Over-provisioned** (20%) : CPU < 30%, coût > $1000/mois
- **Zombie** (5%) : CPU < 10%, candidats à suppression
- **Croissance annuelle** : +15% (tendance organique)

**Index recommandés** :
- (`workload_id`, `date`) (Composite PK)
- `date`

---

### 5. `cloud_costs`

Coûts quotidiens par workload (compute, storage, network).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `workload_id` | VARCHAR(20) | Référence vers workload | **FK** → workloads |
| `date` | DATE | Date du coût | Format ISO 8601 |
| `compute_cost_usd` | DECIMAL(10,2) | Coût compute (USD) | >= 0, ~70% du total |
| `storage_cost_usd` | DECIMAL(10,2) | Coût storage (USD) | >= 0, ~25% du total |
| `network_cost_usd` | DECIMAL(10,2) | Coût network (USD) | >= 0, ~5% du total |
| `total_cost_usd` | DECIMAL(10,2) | Coût total journalier (USD) | sum(compute, storage, network) |
| `currency` | VARCHAR(10) | Devise | Toujours `USD` |
| `billing_period` | VARCHAR(10) | Période de facturation | Format `YYYY-MM` |

**Cardinalité** : ~36 000 lignes (même que usage_metrics)

**Clé composite** : (`workload_id`, `date`)

**Pricing modèle (simplifié)** :
- **Fabric** : $8/CU/jour
- **VM** : $0.15/vCPU/heure
- **Storage** : $0.03/GB/mois
- **SQL** : $10/DB/jour (base)
- **Functions** : $0.20/million exécutions

**Multiplicateurs de coût** :
- **Production** : ×3 (HA, redondance)
- **Pre-production** : ×1.5
- **Development** : ×1
- **Sandbox** : ×0.5

**Dérive de coûts (pour scénario démo)** :
- Croissance organique : +2%/mois
- **Spike janvier 2026** : +35% (5 workloads responsables)

**Index recommandés** :
- (`workload_id`, `date`) (Composite PK)
- `date`
- `billing_period`

---

## Tables Business Mapping

### 6. `business_units`

Unités business de l'entreprise (6 BU).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `business_unit_id` | VARCHAR(20) | Identifiant unique de la BU | **PK**, format `BU_XX` |
| `business_unit_name` | VARCHAR(100) | Nom de la BU | NOT NULL |
| `budget_monthly_usd` | DECIMAL(10,2) | Budget IT mensuel (USD) | >= 0 |
| `head_of_unit` | VARCHAR(200) | Responsable de la BU | |

**Cardinalité** : 6 lignes

**Business Units** :
- `BU_01` : Sales (budget $50K/mois)
- `BU_02` : Marketing ($35K/mois)
- `BU_03` : Finance ($40K/mois)
- `BU_04` : IT ($60K/mois)
- `BU_05` : HR ($25K/mois)
- `BU_06` : Operations ($45K/mois)

**Index recommandés** :
- `business_unit_id` (PK)

---

### 7. `teams`

Équipes organisées par business unit (30 teams, 5 par BU).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `team_id` | VARCHAR(20) | Identifiant unique de la team | **PK**, format `TEAM_XXX` |
| `team_name` | VARCHAR(200) | Nom de la team | NOT NULL |
| `business_unit_id` | VARCHAR(20) | Référence vers BU | **FK** → business_units |
| `team_size` | INTEGER | Nombre de membres | 5-50 |
| `budget_monthly_usd` | DECIMAL(10,2) | Budget IT mensuel (USD) | $5K-$50K |

**Cardinalité** : 30 lignes

**Exemples de noms** :
- Sales Analytics Team
- Marketing Operations Team
- Finance Platform Team
- IT Infrastructure Team
- HR Data Team
- Operations Engineering Team

**Index recommandés** :
- `team_id` (PK)
- `business_unit_id` (FK)

---

### 8. `applications`

Applications métier (60 apps, 2 par team en moyenne).

| Colonne | Type | Description | Contraintes |
|---------|------|-------------|-------------|
| `application_id` | VARCHAR(20) | Identifiant unique de l'app | **PK**, format `APP_XXXXXX` |
| `application_name` | VARCHAR(200) | Nom de l'application | NOT NULL |
| `team_id` | VARCHAR(20) | Référence vers team | **FK** → teams |
| `application_type` | VARCHAR(50) | Type d'application | ex: `CRM`, `ERP`, `Analytics Dashboard` |
| `active_users` | INTEGER | Utilisateurs actifs | 10-500 |
| `workload_ids` | VARCHAR(500) | Liste des workload IDs | Format: `WL_001,WL_002,WL_003` |

**Cardinalité** : 60 lignes

**Types d'applications** :
- CRM
- ERP
- Analytics Dashboard
- Data Pipeline
- Web Application
- Mobile Backend
- API Gateway
- Reporting Tool
- Monitoring Platform
- ML/AI Workload

**Relation N:N avec workloads** :
- Une application consomme 1-3 workloads
- Un workload peut être partagé par plusieurs applications (rare)
- ~50% des workloads sont mappés à des applications (les autres sont infra/shared)

**Index recommandés** :
- `application_id` (PK)
- `team_id` (FK)
- `application_type`

---

## Relations Clés

### Infrastructure (hiérarchie)
```sql
subscriptions (1) ──< environments (N)
environments (1) ──< workloads (N)
workloads (1) ──< usage_metrics (N)
workloads (1) ──< cloud_costs (N)
```

### Business (hiérarchie)
```sql
business_units (1) ──< teams (N)
teams (1) ──< applications (N)
```

### IT ↔ Business (mapping)
```sql
applications (N) ──< workloads (N) via workload_ids (CSV list)
```

**Calcul du coût IT par BU** :
```
business_unit → teams → applications → workloads → cloud_costs
```

---

## Exemples de Requêtes

### Coût total par Business Unit (janvier 2026)
```sql
SELECT 
    bu.business_unit_name,
    SUM(cc.total_cost_usd) as total_cost
FROM business_units bu
JOIN teams t ON bu.business_unit_id = t.business_unit_id
JOIN applications app ON t.team_id = app.team_id
JOIN cloud_costs cc ON cc.workload_id IN (SELECT value FROM STRING_SPLIT(app.workload_ids, ','))
WHERE cc.billing_period = '2026-01'
GROUP BY bu.business_unit_name
ORDER BY total_cost DESC
```

### Workloads surdimensionnés (low usage, high cost)
```sql
SELECT 
    w.workload_name,
    w.workload_type,
    AVG(um.cpu_usage_percent) as avg_cpu,
    SUM(cc.total_cost_usd) as total_cost
FROM workloads w
JOIN usage_metrics um ON w.workload_id = um.workload_id
JOIN cloud_costs cc ON w.workload_id = cc.workload_id
WHERE um.date >= '2026-01-01' AND um.date <= '2026-01-31'
GROUP BY w.workload_id, w.workload_name, w.workload_type
HAVING AVG(um.cpu_usage_percent) < 40 AND SUM(cc.total_cost_usd) > 1000
ORDER BY total_cost DESC
```

### Évolution des coûts mois par mois
```sql
SELECT 
    billing_period,
    SUM(total_cost_usd) as monthly_cost,
    LAG(SUM(total_cost_usd)) OVER (ORDER BY billing_period) as previous_month,
    (SUM(total_cost_usd) - LAG(SUM(total_cost_usd)) OVER (ORDER BY billing_period)) / 
        LAG(SUM(total_cost_usd)) OVER (ORDER BY billing_period) * 100 as growth_percent
FROM cloud_costs
GROUP BY billing_period
ORDER BY billing_period
```

---

## Notes Techniques

### Encodage et Format
- **Encoding** : UTF-8
- **CSV separator** : `,` (virgule)
- **Decimal separator** : `.` (point)
- **Date format** : `YYYY-MM-DD` (ISO 8601)
- **NULL values** : Chaîne vide ou NULL selon type

### Qualité des Données
- Pas de duplicates sur les clés primaires
- Toutes les FK ont une valeur correspondante dans la table parent
- Les valeurs numériques sont dans des plages réalistes
- Les pourcentages sont entre 0 et 100
- Les coûts sont >= 0
- storage_used <= storage_provisioned

### Performance
- Les tables `usage_metrics` et `cloud_costs` sont les plus volumineuses (~36K lignes chacune)
- Prévoir des index sur (`workload_id`, `date`) pour les requêtes temporelles
- Partitioning recommandé sur `billing_period` ou `date` pour Fabric

---

## Annexe : Calcul des Métriques FinOps

### Taux d'utilisation
```
Utilization Rate = AVG(cpu_usage_percent) / 100
```

### Coût par Query
```
Cost per Query = SUM(total_cost_usd) / SUM(query_count)
```

### Capacité gaspillée
```
Wasted Capacity = SUM(total_cost_usd) WHERE avg_cpu < 40% AND total_cost > $1000
```

### Coût par utilisateur actif
```
Cost per Active User = SUM(total_cost_usd) / SUM(active_users)
```

### Croissance M/M (Month-over-Month)
```
MoM Growth = (Cost_Current_Month - Cost_Previous_Month) / Cost_Previous_Month * 100
```
