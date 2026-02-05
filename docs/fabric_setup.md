# Guide de Déploiement sur Microsoft Fabric

## 🎯 Objectif

Déployer la démo IT Ops & FinOps sur Microsoft Fabric en 6 étapes :
1. Générer les données localement
2. Uploader vers OneLake
3. Créer les tables Delta dans le Lakehouse
4. Configurer le modèle sémantique
5. Configurer le Data Agent
6. Tester et valider

**Durée estimée** : 2-3 heures

---

## 📋 Prérequis

### Infrastructure
- [ ] Workspace Fabric avec capacité **F64 ou supérieure**
- [ ] Lakehouse créé dans le workspace
- [ ] Permissions **Contributor** ou **Admin** sur le workspace

### Local
- [ ] Python 3.9+ installé
- [ ] Packages Python installés (`pip install -r requirements.txt`)
- [ ] Azure Storage Explorer (optionnel, pour upload)
- [ ] Power BI Desktop (optionnel, pour tester le modèle sémantique)

---

## Étape 1 : Génération des Données Locales

### 1.1 Installer les dépendances

```powershell
cd "c:\Users\esigwald\OneDrive - Microsoft\Documents\03_Dev\09_DemoFabricDataAgent\MF_ITOps"
pip install -r requirements.txt
```

### 1.2 Configurer les volumes (optionnel)

Éditer `src/config.yaml` si vous voulez ajuster les volumes :

```yaml
volumes:
  subscriptions: 8
  environments: 15
  workloads: 120  # Augmenter à 150 pour plus de données
  business_units: 6
  teams: 30
  applications: 60
```

### 1.3 Générer les CSV

```powershell
cd src
python generate_data.py
```

**Sortie attendue** :
```
============================================================
🚀 GÉNÉRATION DES DONNÉES IT OPS & FINOPS
============================================================

📋 Génération des subscriptions Azure...
  ✓ 8 subscriptions générées
  💾 subscriptions.csv sauvegardé (8 lignes)

🌍 Génération des environments...
  ✓ 15 environments générés
  💾 environments.csv sauvegardé (15 lignes)

⚙️ Génération des workloads...
  ✓ 120 workloads générés
  💾 workloads.csv sauvegardé (120 lignes)

📊 Génération des usage metrics...
  ✓ 36000 metrics générées
  💾 usage_metrics.csv sauvegardé (36000 lignes)

💰 Génération des cloud costs...
  ✓ 36000 cost records générés
  💾 cloud_costs.csv sauvegardé (36000 lignes)

🏢 Génération des business units...
  ✓ 6 business units générées
  💾 business_units.csv sauvegardé (6 lignes)

👥 Génération des teams...
  ✓ 30 teams générées
  💾 teams.csv sauvegardé (30 lignes)

📱 Génération des applications...
  ✓ 60 applications générées
  💾 applications.csv sauvegardé (60 lignes)

============================================================
✅ GÉNÉRATION TERMINÉE
============================================================
```

### 1.4 Valider les données

```powershell
python validate_schema.py
```

**Sortie attendue** :
```
============================================================
🔍 VALIDATION DES SCHÉMAS - IT OPS & FINOPS
============================================================

📋 Validation des schémas:
  ✓ subscriptions.csv: 8 lignes, 6 colonnes
  ✓ environments.csv: 15 lignes, 7 colonnes
  ✓ workloads.csv: 120 lignes, 11 colonnes
  ✓ usage_metrics.csv: 36000 lignes, 9 colonnes
  ✓ cloud_costs.csv: 36000 lignes, 8 colonnes
  ✓ business_units.csv: 6 lignes, 4 colonnes
  ✓ teams.csv: 30 lignes, 5 colonnes
  ✓ applications.csv: 60 lignes, 6 colonnes

🔗 Validation des relations:
  ✓ environments.subscription_id → subscriptions.subscription_id OK
  ✓ workloads.environment_id → environments.environment_id OK
  ✓ usage_metrics.workload_id → workloads.workload_id OK
  ✓ cloud_costs.workload_id → workloads.workload_id OK
  ✓ teams.business_unit_id → business_units.business_unit_id OK
  ✓ applications.team_id → teams.team_id OK

✨ Validation de la qualité:
  ✓ CPU usage dans la plage [0, 100]
  ✓ Memory usage dans la plage [0, 100]
  ✓ Tous les coûts sont >= 0
  ✓ Storage used <= provisioned

============================================================
✅ VALIDATION RÉUSSIE - Toutes les données sont conformes
============================================================
```

---

## Étape 2 : Upload vers OneLake

### Option A : Via l'interface Fabric (recommandé)

1. **Ouvrir le Lakehouse** dans le workspace Fabric
2. **Aller dans l'onglet "Files"**
3. **Créer un dossier** `finops_demo/raw`
4. **Uploader les 8 CSV** depuis `data/raw/`
   - Drag & drop ou bouton "Upload"
   - Attendre la fin de l'upload (peut prendre 2-3 min pour ~8 MB)

### Option B : Via Azure Storage Explorer

1. **Installer Azure Storage Explorer**
2. **Se connecter** avec votre compte Microsoft
3. **Naviguer vers** OneLake → Workspace → Lakehouse → Files
4. **Créer le dossier** `finops_demo/raw`
5. **Uploader les CSV**

### Option C : Via Shortcut OneLake

Si les données sont déjà dans un Azure Storage Account :

1. Dans Fabric, **créer un Shortcut** : New → Shortcut → Azure Data Lake Storage Gen2
2. **Configurer** le shortcut vers votre container
3. **Mapper** les fichiers CSV

---

## Étape 3 : Créer les Tables Delta

### 3.1 Ouvrir un Notebook dans le Lakehouse

Dans Fabric :
1. **Ouvrir le Lakehouse**
2. **New Notebook**
3. **Attacher au Lakehouse**

### 3.2 Charger les données en tables Delta

Copier/coller ce code dans des cellules du Notebook :

```python
# Cell 1: Load subscriptions
from pyspark.sql.types import *

subscriptions_schema = StructType([
    StructField("subscription_id", StringType(), False),
    StructField("subscription_name", StringType(), False),
    StructField("subscription_type", StringType(), False),
    StructField("owner", StringType(), True),
    StructField("status", StringType(), True),
    StructField("created_date", DateType(), True)
])

df_subscriptions = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "false") \
    .schema(subscriptions_schema) \
    .load("Files/finops_demo/raw/subscriptions.csv")

df_subscriptions.write.format("delta").mode("overwrite").saveAsTable("subscriptions")
print(f"✓ subscriptions: {df_subscriptions.count()} lignes")
```

```python
# Cell 2: Load environments
environments_schema = StructType([
    StructField("environment_id", StringType(), False),
    StructField("environment_name", StringType(), False),
    StructField("environment_type", StringType(), False),
    StructField("subscription_id", StringType(), False),
    StructField("region", StringType(), True),
    StructField("tags", StringType(), True),
    StructField("created_date", DateType(), True)
])

df_environments = spark.read.format("csv") \
    .option("header", "true") \
    .schema(environments_schema) \
    .load("Files/finops_demo/raw/environments.csv")

df_environments.write.format("delta").mode("overwrite").saveAsTable("environments")
print(f"✓ environments: {df_environments.count()} lignes")
```

```python
# Cell 3: Load workloads
workloads_schema = StructType([
    StructField("workload_id", StringType(), False),
    StructField("workload_name", StringType(), False),
    StructField("workload_type", StringType(), False),
    StructField("environment_id", StringType(), False),
    StructField("status", StringType(), True),
    StructField("created_date", DateType(), True),
    StructField("owner", StringType(), True),
    StructField("tags", StringType(), True),
    StructField("capacity_units", IntegerType(), True),
    StructField("vcpu_count", IntegerType(), True),
    StructField("storage_gb", IntegerType(), True)
])

df_workloads = spark.read.format("csv") \
    .option("header", "true") \
    .schema(workloads_schema) \
    .load("Files/finops_demo/raw/workloads.csv")

df_workloads.write.format("delta").mode("overwrite").saveAsTable("workloads")
print(f"✓ workloads: {df_workloads.count()} lignes")
```

```python
# Cell 4: Load usage_metrics
usage_metrics_schema = StructType([
    StructField("workload_id", StringType(), False),
    StructField("date", DateType(), False),
    StructField("cpu_usage_percent", DoubleType(), True),
    StructField("memory_usage_percent", DoubleType(), True),
    StructField("storage_used_gb", DoubleType(), True),
    StructField("storage_provisioned_gb", DoubleType(), True),
    StructField("query_count", IntegerType(), True),
    StructField("data_processed_gb", DoubleType(), True),
    StructField("active_users", IntegerType(), True)
])

df_usage_metrics = spark.read.format("csv") \
    .option("header", "true") \
    .schema(usage_metrics_schema) \
    .load("Files/finops_demo/raw/usage_metrics.csv")

df_usage_metrics.write.format("delta").mode("overwrite").saveAsTable("usage_metrics")
print(f"✓ usage_metrics: {df_usage_metrics.count()} lignes")
```

```python
# Cell 5: Load cloud_costs
cloud_costs_schema = StructType([
    StructField("workload_id", StringType(), False),
    StructField("date", DateType(), False),
    StructField("compute_cost_usd", DoubleType(), True),
    StructField("storage_cost_usd", DoubleType(), True),
    StructField("network_cost_usd", DoubleType(), True),
    StructField("total_cost_usd", DoubleType(), True),
    StructField("currency", StringType(), True),
    StructField("billing_period", StringType(), True)
])

df_cloud_costs = spark.read.format("csv") \
    .option("header", "true") \
    .schema(cloud_costs_schema) \
    .load("Files/finops_demo/raw/cloud_costs.csv")

df_cloud_costs.write.format("delta").mode("overwrite").saveAsTable("cloud_costs")
print(f"✓ cloud_costs: {df_cloud_costs.count()} lignes")
```

```python
# Cell 6: Load business_units
business_units_schema = StructType([
    StructField("business_unit_id", StringType(), False),
    StructField("business_unit_name", StringType(), False),
    StructField("budget_monthly_usd", DoubleType(), True),
    StructField("head_of_unit", StringType(), True)
])

df_business_units = spark.read.format("csv") \
    .option("header", "true") \
    .schema(business_units_schema) \
    .load("Files/finops_demo/raw/business_units.csv")

df_business_units.write.format("delta").mode("overwrite").saveAsTable("business_units")
print(f"✓ business_units: {df_business_units.count()} lignes")
```

```python
# Cell 7: Load teams
teams_schema = StructType([
    StructField("team_id", StringType(), False),
    StructField("team_name", StringType(), False),
    StructField("business_unit_id", StringType(), False),
    StructField("team_size", IntegerType(), True),
    StructField("budget_monthly_usd", DoubleType(), True)
])

df_teams = spark.read.format("csv") \
    .option("header", "true") \
    .schema(teams_schema) \
    .load("Files/finops_demo/raw/teams.csv")

df_teams.write.format("delta").mode("overwrite").saveAsTable("teams")
print(f"✓ teams: {df_teams.count()} lignes")
```

```python
# Cell 8: Load applications
applications_schema = StructType([
    StructField("application_id", StringType(), False),
    StructField("application_name", StringType(), False),
    StructField("team_id", StringType(), False),
    StructField("application_type", StringType(), True),
    StructField("active_users", IntegerType(), True),
    StructField("workload_ids", StringType(), True)
])

df_applications = spark.read.format("csv") \
    .option("header", "true") \
    .schema(applications_schema) \
    .load("Files/finops_demo/raw/applications.csv")

df_applications.write.format("delta").mode("overwrite").saveAsTable("applications")
print(f"✓ applications: {df_applications.count()} lignes")
```

```python
# Cell 9: Verification
print("\n📊 Tables Delta créées:")
print(f"  • subscriptions: {spark.table('subscriptions').count()} lignes")
print(f"  • environments: {spark.table('environments').count()} lignes")
print(f"  • workloads: {spark.table('workloads').count()} lignes")
print(f"  • usage_metrics: {spark.table('usage_metrics').count()} lignes")
print(f"  • cloud_costs: {spark.table('cloud_costs').count()} lignes")
print(f"  • business_units: {spark.table('business_units').count()} lignes")
print(f"  • teams: {spark.table('teams').count()} lignes")
print(f"  • applications: {spark.table('applications').count()} lignes")
```

**Exécuter toutes les cellules** et vérifier qu'il n'y a pas d'erreur.

---

## Étape 4 : Configurer le Modèle Sémantique

### 4.1 Créer le Semantic Model

1. Dans le Lakehouse, **cliquer sur "New semantic model"**
2. **Sélectionner les 8 tables** Delta
3. **Nommer** le modèle : `FinOps_SemanticModel`
4. **Create**

### 4.2 Définir les Relations

Dans l'interface du Semantic Model :

**Relations à créer** :
- `environments[subscription_id]` → `subscriptions[subscription_id]` (Many-to-One)
- `workloads[environment_id]` → `environments[environment_id]` (Many-to-One)
- `usage_metrics[workload_id]` → `workloads[workload_id]` (Many-to-One)
- `cloud_costs[workload_id]` → `workloads[workload_id]` (Many-to-One)
- `teams[business_unit_id]` → `business_units[business_unit_id]` (Many-to-One)
- `applications[team_id]` → `teams[team_id]` (Many-to-One)

**Cardinality** : Many-to-One pour toutes  
**Cross-filter direction** : Single (sauf si besoin de bi-directionnel)

### 4.3 Créer les Mesures DAX

Voir le fichier [dax_measures.md](dax_measures.md) pour toutes les mesures.

**Mesures essentielles à créer** :
- Total Cost
- Total Cost MTD
- Cost Growth MoM
- Avg CPU Usage
- Cost per Query
- Wasted Capacity

---

## Étape 5 : Configurer le Data Agent

### 5.1 Créer le Data Agent

1. Dans le workspace, **New → Data Agent**
2. **Nommer** : `IT Finance Analyst`
3. **Sélectionner** le Semantic Model : `FinOps_SemanticModel`

### 5.2 Configurer les Instructions Système

Copier/coller les instructions depuis [data_agent_instructions.md](data_agent_instructions.md) dans la section **System Instructions**.

**Résumé des instructions** :
- Persona : Analyste FinOps expert
- Ton : Professionnel, concis, orienté action
- Focus : Coûts, optimisations, ROI, mapping business
- Langage : Français

### 5.3 Ajouter des Exemples (optionnel)

Copier quelques exemples depuis [data_agent_examples.md](data_agent_examples.md) pour améliorer la précision.

### 5.4 Sauvegarder et Publier

1. **Save**
2. **Publish** pour rendre le Data Agent accessible

---

## Étape 6 : Tester et Valider

### 6.1 Tester les 15 Questions

Ouvrir le Data Agent et poser les 15 questions depuis [questions_demo.md](questions_demo.md).

**Checklist** :
- [ ] Q1 : Coût total janvier 2026
- [ ] Q4 : Top 5 workloads chers
- [ ] Q7 : Workloads surdimensionnés
- [ ] Q11 : Coût par Business Unit
- [ ] Q14 : Justification workload cher

### 6.2 Vérifier la Cohérence

Les réponses doivent être :
- **Précises** : Chiffres corrects (±5%)
- **Complètes** : Toutes les dimensions demandées
- **Actionnables** : Recommandations claires
- **En français** : Pas d'anglais sauf termes techniques

### 6.3 Créer un Dashboard Power BI (optionnel)

1. **Ouvrir Power BI Desktop**
2. **Se connecter** au Semantic Model Fabric
3. **Créer des visuels** :
   - Coût total par mois (line chart)
   - Top 10 workloads (bar chart)
   - Coût par BU (pie chart)
   - Workloads surdimensionnés (table)
   - Usage vs Coût (scatter plot)
4. **Publier** vers le workspace Fabric

---

## ✅ Validation Finale

Avant de déclarer la démo prête :

- [ ] Les 8 CSV sont générés et validés
- [ ] Les 8 tables Delta existent dans le Lakehouse
- [ ] Le Semantic Model a les 6 relations configurées
- [ ] Au moins 10 mesures DAX sont créées
- [ ] Le Data Agent répond correctement aux 15 questions
- [ ] Les réponses sont en français et actionnables
- [ ] Le scénario de démo est répété (demo_story.md)

---

## 🐛 Troubleshooting

### Problème : "Table not found" lors de la création Delta

**Cause** : Schéma incorrect ou fichier CSV mal formé

**Solution** :
```python
# Vérifier le schéma du CSV
df_test = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("Files/finops_demo/raw/subscriptions.csv")
df_test.printSchema()
df_test.show(5)
```

### Problème : Data Agent répond en anglais

**Cause** : Instructions système mal configurées

**Solution** :
- Vérifier que les instructions contiennent "Réponds TOUJOURS en français"
- Ajouter des exemples en français dans les "Sample Q&A"

### Problème : Relations cassées dans le Semantic Model

**Cause** : Clés primaires/étrangères incorrectes

**Solution** :
```python
# Vérifier les FK
df_envs = spark.table("environments")
df_subs = spark.table("subscriptions")

orphans = df_envs.join(df_subs, df_envs.subscription_id == df_subs.subscription_id, "left_anti")
orphans.show()  # Doit être vide
```

### Problème : Coûts incohérents

**Cause** : Données générées avec seed différent

**Solution** :
- Vérifier que `config.yaml` a `seed: 42`
- Régénérer les données : `python generate_data.py`
- Re-charger en Delta

---

## 📚 Ressources

- [Microsoft Fabric Documentation](https://learn.microsoft.com/fabric/)
- [Data Agent Documentation](https://learn.microsoft.com/fabric/data-science/data-agent)
- [DAX Reference](https://dax.guide/)
- [Delta Lake Guide](https://learn.microsoft.com/fabric/data-engineering/lakehouse-and-delta-tables)

---

**🎉 Félicitations !** Votre démo IT Ops & FinOps est prête. Testez-la plusieurs fois avant de la présenter.
