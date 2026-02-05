# Mesures DAX - Modèle Sémantique FinOps

## 📋 Vue d'ensemble

Ce fichier contient **toutes les mesures DAX** à créer dans le modèle sémantique Fabric pour la démo IT Ops & FinOps.

**Organisation** :
1. Mesures de Coûts
2. Mesures d'Usage
3. Mesures d'Efficacité
4. Mesures de Croissance
5. Mesures Business
6. Mesures de Détection d'Anomalies

**Total** : ~30 mesures DAX

---

## 💰 1. Mesures de Coûts

### Total Cost
```dax
Total Cost = 
SUM(cloud_costs[total_cost_usd])
```

**Description** : Coût total sur la période sélectionnée  
**Format** : `$#,##0`  
**Utilisation** : Toutes les analyses de coûts

---

### Compute Cost
```dax
Compute Cost = 
SUM(cloud_costs[compute_cost_usd])
```

**Description** : Coût de compute (CPU, CU)  
**Format** : `$#,##0`

---

### Storage Cost
```dax
Storage Cost = 
SUM(cloud_costs[storage_cost_usd])
```

**Description** : Coût de stockage  
**Format** : `$#,##0`

---

### Network Cost
```dax
Network Cost = 
SUM(cloud_costs[network_cost_usd])
```

**Description** : Coût réseau  
**Format** : `$#,##0`

---

### Total Cost MTD
```dax
Total Cost MTD = 
TOTALMTD([Total Cost], 'calendar'[Date])
```

**Description** : Coût cumulé du mois en cours  
**Format** : `$#,##0`  
**Prérequis** : Table calendrier (`calendar`) avec colonne `Date`

---

### Total Cost YTD
```dax
Total Cost YTD = 
TOTALYTD([Total Cost], 'calendar'[Date])
```

**Description** : Coût cumulé de l'année en cours  
**Format** : `$#,##0`

---

### Average Daily Cost
```dax
Average Daily Cost = 
AVERAGE(cloud_costs[total_cost_usd])
```

**Description** : Coût quotidien moyen  
**Format** : `$#,##0`

---

### Cost per Workload
```dax
Cost per Workload = 
DIVIDE(
    [Total Cost],
    DISTINCTCOUNT(cloud_costs[workload_id])
)
```

**Description** : Coût moyen par workload  
**Format** : `$#,##0`

---

## 📊 2. Mesures d'Usage

### Avg CPU Usage
```dax
Avg CPU Usage = 
AVERAGE(usage_metrics[cpu_usage_percent])
```

**Description** : Utilisation CPU moyenne (%)  
**Format** : `0.0"%"`

---

### Avg Memory Usage
```dax
Avg Memory Usage = 
AVERAGE(usage_metrics[memory_usage_percent])
```

**Description** : Utilisation RAM moyenne (%)  
**Format** : `0.0"%"`

---

### Total Storage Used
```dax
Total Storage Used = 
SUM(usage_metrics[storage_used_gb])
```

**Description** : Stockage total utilisé (GB)  
**Format** : `#,##0" GB"`

---

### Total Storage Provisioned
```dax
Total Storage Provisioned = 
SUM(usage_metrics[storage_provisioned_gb])
```

**Description** : Stockage total provisionné (GB)  
**Format** : `#,##0" GB"`

---

### Storage Utilization Rate
```dax
Storage Utilization Rate = 
DIVIDE(
    [Total Storage Used],
    [Total Storage Provisioned]
)
```

**Description** : Taux d'utilisation du stockage  
**Format** : `0.0%`

---

### Total Queries
```dax
Total Queries = 
SUM(usage_metrics[query_count])
```

**Description** : Nombre total de queries  
**Format** : `#,##0`

---

### Total Data Processed
```dax
Total Data Processed = 
SUM(usage_metrics[data_processed_gb])
```

**Description** : Total de données traitées (GB)  
**Format** : `#,##0" GB"`

---

### Total Active Users
```dax
Total Active Users = 
SUM(usage_metrics[active_users])
```

**Description** : Nombre total d'utilisateurs actifs  
**Format** : `#,##0`

---

## ⚡ 3. Mesures d'Efficacité

### Cost per Query
```dax
Cost per Query = 
DIVIDE(
    [Total Cost],
    [Total Queries],
    0
)
```

**Description** : Coût moyen par query  
**Format** : `$0.0000`

---

### Cost per GB Processed
```dax
Cost per GB Processed = 
DIVIDE(
    [Total Cost],
    [Total Data Processed],
    0
)
```

**Description** : Coût par GB de données traitées  
**Format** : `$0.00`

---

### Cost per Active User
```dax
Cost per Active User = 
DIVIDE(
    [Total Cost],
    [Total Active Users],
    0
)
```

**Description** : Coût par utilisateur actif  
**Format** : `$#,##0`

---

### Utilization Rate (CPU)
```dax
Utilization Rate = 
DIVIDE(
    [Avg CPU Usage],
    100
)
```

**Description** : Taux d'utilisation CPU (0-1)  
**Format** : `0.0%`

---

### Efficiency Score
```dax
Efficiency Score = 
VAR UtilizationScore = [Utilization Rate]
VAR CostPerUserScore = 
    DIVIDE(
        150, -- Target: $150/user
        [Cost per Active User],
        0
    )
RETURN
    (UtilizationScore + CostPerUserScore) / 2
```

**Description** : Score d'efficacité global (0-1)  
**Format** : `0.0%`  
**Interprétation** : > 70% = Efficace, < 50% = Inefficace

---

## 📈 4. Mesures de Croissance

### Cost Previous Month
```dax
Cost Previous Month = 
CALCULATE(
    [Total Cost],
    DATEADD('calendar'[Date], -1, MONTH)
)
```

**Description** : Coût du mois précédent  
**Format** : `$#,##0`

---

### Cost Growth MoM
```dax
Cost Growth MoM = 
VAR CurrentMonth = [Total Cost MTD]
VAR PreviousMonth = [Cost Previous Month]
RETURN
    DIVIDE(
        CurrentMonth - PreviousMonth,
        PreviousMonth
    )
```

**Description** : Croissance mois/mois (%)  
**Format** : `+0.0%;-0.0%`

---

### Cost Growth MoM ($)
```dax
Cost Growth MoM ($) = 
[Total Cost MTD] - [Cost Previous Month]
```

**Description** : Croissance mois/mois en dollars  
**Format** : `$#,##0;-$#,##0`

---

### Cost Previous Year
```dax
Cost Previous Year = 
CALCULATE(
    [Total Cost],
    SAMEPERIODLASTYEAR('calendar'[Date])
)
```

**Description** : Coût même période année précédente  
**Format** : `$#,##0`

---

### Cost Growth YoY
```dax
Cost Growth YoY = 
VAR CurrentYear = [Total Cost]
VAR PreviousYear = [Cost Previous Year]
RETURN
    DIVIDE(
        CurrentYear - PreviousYear,
        PreviousYear
    )
```

**Description** : Croissance année/année (%)  
**Format** : `+0.0%;-0.0%`

---

### Projected Cost Next Month
```dax
Projected Cost Next Month = 
VAR AvgGrowthRate = 
    CALCULATE(
        AVERAGE([Cost Growth MoM]),
        DATESINPERIOD('calendar'[Date], MAX('calendar'[Date]), -6, MONTH)
    )
RETURN
    [Total Cost MTD] * (1 + AvgGrowthRate)
```

**Description** : Projection coût mois prochain (tendance 6 mois)  
**Format** : `$#,##0`

---

## 💼 5. Mesures Business

### Total Budget Allocated
```dax
Total Budget Allocated = 
SUMX(
    business_units,
    business_units[budget_monthly_usd]
)
```

**Description** : Budget IT total alloué  
**Format** : `$#,##0`

---

### Budget Variance
```dax
Budget Variance = 
[Total Cost] - [Total Budget Allocated]
```

**Description** : Écart budget (réalisé - alloué)  
**Format** : `$#,##0;-$#,##0`

---

### Budget Variance %
```dax
Budget Variance % = 
DIVIDE(
    [Budget Variance],
    [Total Budget Allocated]
)
```

**Description** : Écart budget en %  
**Format** : `+0.0%;-0.0%`

---

### Cost per Business Unit
```dax
Cost per Business Unit = 
DIVIDE(
    [Total Cost],
    DISTINCTCOUNT(business_units[business_unit_id])
)
```

**Description** : Coût moyen par BU  
**Format** : `$#,##0`

---

### Cost per Team
```dax
Cost per Team = 
DIVIDE(
    [Total Cost],
    DISTINCTCOUNT(teams[team_id])
)
```

**Description** : Coût moyen par équipe  
**Format** : `$#,##0`

---

## 🚨 6. Mesures de Détection d'Anomalies

### Wasted Capacity (Count)
```dax
Wasted Capacity (Count) = 
CALCULATE(
    DISTINCTCOUNT(workloads[workload_id]),
    FILTER(
        workloads,
        [Avg CPU Usage] < 40 && [Total Cost] > 1000
    )
)
```

**Description** : Nombre de workloads surdimensionnés  
**Format** : `#,##0`

---

### Wasted Capacity ($)
```dax
Wasted Capacity ($) = 
CALCULATE(
    [Total Cost],
    FILTER(
        workloads,
        [Avg CPU Usage] < 40 && [Total Cost] > 1000
    )
)
```

**Description** : Coût des workloads surdimensionnés  
**Format** : `$#,##0`

---

### Zombie Workloads (Count)
```dax
Zombie Workloads (Count) = 
CALCULATE(
    DISTINCTCOUNT(workloads[workload_id]),
    FILTER(
        workloads,
        [Avg CPU Usage] < 10 && [Total Active Users] = 0
    )
)
```

**Description** : Nombre de workloads zombies (non utilisés)  
**Format** : `#,##0`

---

### Zombie Workloads ($)
```dax
Zombie Workloads ($) = 
CALCULATE(
    [Total Cost],
    FILTER(
        workloads,
        [Avg CPU Usage] < 10 && [Total Active Users] = 0
    )
)
```

**Description** : Coût des workloads zombies  
**Format** : `$#,##0`

---

### Over-Provisioned Storage ($)
```dax
Over-Provisioned Storage ($) = 
CALCULATE(
    [Total Cost],
    FILTER(
        workloads,
        workloads[workload_type] = "azure_storage" &&
        [Storage Utilization Rate] < 0.30
    )
)
```

**Description** : Coût des storage sous-utilisés (< 30%)  
**Format** : `$#,##0`

---

### Cost Spike Alert
```dax
Cost Spike Alert = 
IF(
    [Cost Growth MoM] > 0.30, -- 30% threshold
    "🚨 ALERTE: +" & FORMAT([Cost Growth MoM], "0%"),
    IF(
        [Cost Growth MoM] > 0.20, -- 20% threshold
        "⚠️ WARNING: +" & FORMAT([Cost Growth MoM], "0%"),
        "✅ Normal"
    )
)
```

**Description** : Alerte sur pic de coût M/M  
**Format** : Texte

---

### Optimization Potential ($)
```dax
Optimization Potential ($) = 
[Wasted Capacity ($)] + 
[Zombie Workloads ($)] + 
[Over-Provisioned Storage ($)]
```

**Description** : Total des économies potentielles  
**Format** : `$#,##0`

---

## 🎯 Mesures Avancées (Optionnelles)

### Cost Forecast (3 months)
```dax
Cost Forecast (3 months) = 
VAR AvgGrowthRate = 
    CALCULATE(
        AVERAGE([Cost Growth MoM]),
        DATESINPERIOD('calendar'[Date], MAX('calendar'[Date]), -6, MONTH)
    )
VAR CurrentCost = [Total Cost MTD]
RETURN
    CurrentCost * POWER(1 + AvgGrowthRate, 3)
```

**Description** : Prévision de coût dans 3 mois  
**Format** : `$#,##0`

---

### ROI (Return on Investment)
```dax
ROI = 
VAR ITCost = [Total Cost]
VAR BusinessValue = 
    SUMX(
        applications,
        applications[active_users] * 500 -- $500 de valeur par user/mois (à ajuster)
    )
RETURN
    DIVIDE(BusinessValue, ITCost, 0)
```

**Description** : ROI simplifié (valeur business / coût IT)  
**Format** : `0.0"x"`  
**Note** : Ajuster le multiplicateur ($500) selon contexte

---

### Peak Usage Hour
```dax
Peak Usage Hour = 
MAXX(
    VALUES(usage_metrics[date]),
    [Avg CPU Usage]
)
```

**Description** : Utilisation CPU maximale  
**Format** : `0.0%`

---

### Average Cost per CU (Fabric)
```dax
Average Cost per CU = 
VAR FabricWorkloads = 
    FILTER(
        workloads,
        workloads[workload_type] = "fabric_capacity"
    )
VAR TotalCU = SUMX(FabricWorkloads, workloads[capacity_units])
VAR FabricCost = 
    CALCULATE(
        [Total Cost],
        FabricWorkloads
    )
RETURN
    DIVIDE(FabricCost, TotalCU, 0)
```

**Description** : Coût moyen par Capacity Unit Fabric  
**Format** : `$#,##0`

---

## 📐 Création dans Fabric

### Méthode 1 : Via l'interface Semantic Model

1. **Ouvrir le Semantic Model** dans Fabric
2. **Cliquer sur "New measure"**
3. **Copier/coller** la formule DAX
4. **Renommer** la mesure (nom exact comme ci-dessus)
5. **Formater** selon le format recommandé
6. **Sauvegarder**

### Méthode 2 : Via Power BI Desktop

1. **Se connecter** au Semantic Model Fabric
2. **Onglet "Modeling"** → **New Measure**
3. **Copier/coller** la formule
4. **Formater** et **sauvegarder**
5. **Publier** vers Fabric

---

## ✅ Checklist de Validation

Après création des mesures :

- [ ] Les 30+ mesures sont créées dans le Semantic Model
- [ ] Aucune erreur DAX (syntax, références)
- [ ] Les formats sont appliqués (devise, %, GB)
- [ ] Les mesures de base fonctionnent (Total Cost, Avg CPU Usage)
- [ ] Les mesures calculées fonctionnent (Cost Growth MoM, Wasted Capacity)
- [ ] Les mesures avancées fonctionnent (Optimization Potential, ROI)
- [ ] Le Data Agent peut utiliser ces mesures dans ses réponses

---

## 🎓 Bonnes Pratiques DAX

### Nommage
- **Mesures** : PascalCase avec espaces (`Total Cost`, `Cost Growth MoM`)
- **Colonnes calculées** : snake_case (`total_cost_usd`)
- **Tables** : snake_case (`cloud_costs`, `usage_metrics`)

### Performance
- Utiliser `DIVIDE()` avec 3e paramètre (évite erreur /0)
- Préférer `SUMX()` à `SUM()` + filtres complexes
- Éviter les `FILTER()` imbriqués dans les mesures fréquentes

### Lisibilité
- Utiliser `VAR` pour stocker les calculs intermédiaires
- Commenter les formules complexes
- Grouper les mesures par catégorie (dossiers)

---

## 📚 Ressources DAX

- [DAX Guide](https://dax.guide/) - Référence complète
- [SQLBI](https://www.sqlbi.com/articles/) - Articles et patterns
- [Microsoft Learn - DAX](https://learn.microsoft.com/power-bi/transform-model/desktop-quickstart-learn-dax-basics)

---

**Version** : 1.0  
**Dernière mise à jour** : Février 2026  
**Compatibilité** : Fabric Semantic Model, Power BI
