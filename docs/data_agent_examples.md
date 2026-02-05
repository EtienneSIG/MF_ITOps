# Exemples de Réponses - Data Agent IT Finance Analyst

## 📋 Vue d'ensemble

Ces exemples montrent les réponses attendues du Data Agent pour les questions fréquentes.
Utilisez-les pour :
- **Tester** le Data Agent après configuration
- **Former** les utilisateurs (CFO, FinOps)
- **Comparer** avec les réponses réelles (quality check)
- **Améliorer** les instructions système si écarts

---

## 💰 Catégorie : Analyse Globale

### Exemple 1 : Coût Total Mensuel

**Question** :
```
Quel est le coût total Fabric + Azure pour janvier 2026 ?
```

**Réponse Attendue** :
```
Le coût total pour janvier 2026 est de **$487,350**.

Répartition par composant :
• Compute : $341,145 (70%)
• Storage : $121,838 (25%)
• Network : $24,367 (5%)

Évolution :
• vs décembre 2025 : **+$126,350 (+35%)**
• vs janvier 2025 : **+$167,350 (+52%)**

⚠️ ALERTE : Augmentation anormale de 35% en un mois.

Causes identifiées :
1. Scaling-up de 5 Fabric Capacities (+$78K)
2. Croissance organique attendue (+$7K)
3. Accumulation d'archives storage (+$12K)
4. Workloads sandbox non nettoyés (+$20K)

🎯 RECOMMANDATION : Audit immédiat des Fabric Capacities et suppression des sandbox zombies.
```

**Métriques de Qualité** :
- ✅ Chiffre principal en gras
- ✅ Décomposition claire
- ✅ Comparaison temporelle
- ✅ Alerte + causes
- ✅ Recommandation actionnable

---

### Exemple 2 : Évolution sur 12 Mois

**Question** :
```
Comment ont évolué les coûts IT sur les 12 derniers mois ?
```

**Réponse Attendue** :
```
Évolution des coûts IT (février 2025 → janvier 2026) :

| Mois | Coût Total | Évolution M/M |
|------|-----------|---------------|
| Fév 2025 | $320,000 | - |
| Mars 2025 | $326,400 | +2.0% |
| Avril 2025 | $333,130 | +2.1% |
| Mai 2025 | $339,900 | +2.0% |
| Juin 2025 | $346,690 | +2.0% |
| Juil 2025 | $353,620 | +2.0% |
| Août 2025 | $360,690 | +2.0% |
| Sept 2025 | $367,900 | +2.0% |
| Oct 2025 | $375,260 | +2.0% |
| Nov 2025 | $382,760 | +2.0% |
| Déc 2025 | $361,000 | -5.7% ⚠️ |
| **Jan 2026** | **$487,350** | **+35.0%** 🚨 |

Tendances :
• **Croissance organique** : +2% par mois (février-novembre)
• **Baisse en décembre** : -5.7% (optimisations de fin d'année)
• **Pic en janvier** : +35% (anormal !)

📊 Sur 12 mois : **+52.3%** de croissance totale

⚠️ ALERTE CRITIQUE : Le pic de janvier (+35%) est 17x supérieur à la croissance mensuelle moyenne (+2%).

🎯 RECOMMANDATION : Analyse détaillée des workloads ajoutés/modifiés en janvier 2026.
```

---

## 🔍 Catégorie : Top Contributeurs

### Exemple 3 : Top 5 Workloads Chers

**Question** :
```
Quels sont les 5 workloads les plus chers en janvier 2026 ?
```

**Réponse Attendue** :
```
Top 5 des workloads les plus chers (janvier 2026) :

**1. fabric-capacity-delta-001**
   • Environment : ENV_001 (prod-critical)
   • Type : Fabric Capacity (128 CU)
   • Coût : **$38,420**
   • Évolution : +142% vs décembre 🚨
   • Usage CPU : 87%
   • Application : Sales Analytics

**2. azure-sql-analytics-003**
   • Environment : ENV_002 (prod-standard)
   • Type : Azure SQL (16 vCPU)
   • Coût : **$31,250**
   • Évolution : +8% vs décembre
   • Usage CPU : 76%
   • Application : CRM Dashboard

**3. fabric-capacity-sales-002**
   • Environment : ENV_001 (prod-critical)
   • Type : Fabric Capacity (64 CU)
   • Coût : **$27,890**
   • Évolution : +128% vs décembre 🚨
   • Usage CPU : 91%
   • Application : Sales Forecasting

**4. azure-vm-web-012**
   • Environment : ENV_002 (prod-standard)
   • Type : Azure VM (32 vCPU)
   • Coût : **$18,340**
   • Évolution : +5% vs décembre
   • Usage CPU : 82%
   • Application : Web Application Backend

**5. fabric-capacity-marketing-004**
   • Environment : ENV_003 (prod-low)
   • Type : Fabric Capacity (32 CU)
   • Coût : **$14,230**
   • Évolution : +95% vs décembre 🚨
   • Usage CPU : 68%
   • Application : Marketing Analytics

💰 Coût combiné : **$129,130** (26.5% du total mensuel)

⚠️ ALERTE : 3 des 5 sont des Fabric Capacities avec doublements de coûts !

🎯 RECOMMANDATION : Audit des configurations Fabric Capacity (possibles sur-provisionnements).
```

---

## 🎯 Catégorie : Optimisation

### Exemple 4 : Workloads Surdimensionnés

**Question** :
```
Quels workloads sont surdimensionnés : usage CPU < 40% et coût > $1000/mois ?
```

**Réponse Attendue** :
```
23 workloads surdimensionnés détectés (janvier 2026) :

**PRIORITÉ HAUTE** (5 workloads) - Usage < 20%, Coût > $5K :

1. **azure-vm-legacy-034**
   • Environment : ENV_007 (dev-team2)
   • Usage CPU : 12%
   • Coût : $8,340/mois
   • Utilisateurs : 0
   • Dernière activité : 12 déc 2025
   • **ACTION** : ARRÊTER immédiatement
   • **Économie** : $8,340/mois

2. **fabric-capacity-poc-018**
   • Environment : ENV_014 (sandbox-innovation)
   • Usage CPU : 8%
   • Coût : $6,780/mois
   • Utilisateurs : 0
   • POC terminé : nov 2025
   • **ACTION** : SUPPRIMER
   • **Économie** : $6,780/mois

3. **azure-storage-temp-029**
   • Environment : ENV_015 (sandbox-poc)
   • Storage utilisé : 234 GB / 10,000 GB (2.3%)
   • Coût : $5,120/mois
   • **ACTION** : DOWNSCALE à 500 GB
   • **Économie** : $4,870/mois

... (2 autres workloads similaires)

**PRIORITÉ MOYENNE** (18 workloads) - Usage 20-40%, Coût > $2K :

6. **azure-vm-web-staging-041**
   • Usage CPU : 28%
   • Coût : $4,230/mois
   • **ACTION** : DOWNSCALE 32 → 16 vCPU
   • **Économie** : $2,115/mois

7. **fabric-capacity-test-052**
   • Usage CPU : 32%
   • Coût : $3,890/mois
   • **ACTION** : DOWNSCALE 32 → 16 CU
   • **Économie** : $1,945/mois

... (16 autres workloads)

💰 **ÉCONOMIES TOTALES** :
• Arrêt zombies (5) : $38,450/mois
• Downscale medium (18) : $21,780/mois
• **TOTAL** : **$60,230/mois** ($723K/an)

⚠️ **RISQUES** :
• Haute priorité : Aucun (pas d'utilisateurs)
• Moyenne priorité : Faible (environnements non-prod)

🎯 **PLAN D'ACTION** :
1. J1 : Supprimer les 5 workloads zombies → $38K économisés
2. J7 : Downscale 12 workloads dev/test → $15K économisés
3. J30 : Auditer 6 workloads prod (20-40%) → $7K économisés
```

---

### Exemple 5 : Économies Sandbox

**Question** :
```
Si je supprime tous les workloads sandbox avec usage < 10%, combien j'économise ?
```

**Réponse Attendue** :
```
Impact de la suppression des workloads sandbox (usage < 10%) :

**WORKLOADS CONCERNÉS** (3) :

1. **fabric-capacity-poc-018**
   • Coût : $6,780/mois
   • Usage : 8%
   • Utilisateurs : 0
   • Application : POC AI Vision (terminé nov 2025)

2. **azure-vm-legacy-034**
   • Coût : $8,340/mois
   • Usage : 12%
   • Utilisateurs : 0
   • Application : Dev Environment Legacy (abandonné)

3. **azure-storage-temp-029**
   • Coût : $5,120/mois
   • Storage : 2.3% utilisé
   • Application : Sandbox Storage (temporaire)

💰 **ÉCONOMIES** :
• Mensuel : **$20,240**
• Annuel : **$242,880**

📊 **IMPACT BUSINESS** : **AUCUN**
• Aucun utilisateur actif (0)
• Aucune dépendance applicative
• Données archivables en cold storage (~$50/mois)

✅ **RISQUE** : **Aucun**

🎯 **RECOMMANDATION** : Suppression immédiate dès demain.

**ACTIONS** :
1. Archiver les 234 GB de données temporaires → Azure Blob Cold Storage
2. Supprimer les 3 workloads
3. Communiquer aux équipes (aucune objection attendue)

**PLANNING** :
• J0 (aujourd'hui) : Validation CFO
• J1 : Archivage données + suppression workloads
• J2 : Vérification facture (économie visible)
```

---

## 💼 Catégorie : Mapping Business

### Exemple 6 : Coût par Business Unit

**Question** :
```
Combien coûte chaque Business Unit en infrastructure IT pour janvier 2026 ?
```

**Réponse Attendue** :
```
Coûts IT par Business Unit (janvier 2026) :

| BU | Coût Réalisé | Budget Alloué | Écart | % Écart |
|----|--------------|---------------|-------|---------|
| **Sales** | **$206,030** | $50,000 | +$156,030 | **+312%** 🚨 |
| **IT** | $98,340 | $60,000 | +$38,340 | +64% ⚠️ |
| **Finance** | $72,450 | $40,000 | +$32,450 | +81% ⚠️ |
| **Marketing** | $54,120 | $35,000 | +$19,120 | +55% ⚠️ |
| **Operations** | $38,890 | $45,000 | -$6,110 | -14% ✅ |
| **HR** | $17,520 | $25,000 | -$7,480 | -30% ✅ |

**TOTAL** : $487,350

📊 **Analyse** :
• **2 BU sous budget** : Operations, HR ✅
• **4 BU en dépassement** : Sales (+312%), Finance (+81%), IT (+64%), Marketing (+55%) ⚠️

🚨 **ALERTE CRITIQUE : Sales**
• Dépassement : +$156K (+312%)
• Cause : Déploiement CRM + Sales Analytics en janvier
• Applications : 
  - CRM Dashboard : $82,340
  - Sales Analytics : $54,670
• **Action** : Renégociation budget ou optimisation workloads

💡 **INSIGHT : Operations & HR**
• Seules BU efficaces (sous budget)
• Bonnes pratiques : downscale systématique dev/test, archivage régulier
• **Recommandation** : Partager best practices avec autres BU

🎯 **ACTIONS** :
1. Audit Sales : justifier le dépassement (+312%)
2. Review Finance & IT : possibilités d'optimisation
3. Chargebacks : facturer coûts réels aux BU (responsabilisation)
```

---

## 🏆 Catégorie : Justification & ROI

### Exemple 7 : Justification d'un Workload Cher

**Question** :
```
Le coût du workload 'fabric-capacity-sales-002' ($27,890/mois) est-il justifié ?
```

**Réponse Attendue** :
```
Analyse de justification : **fabric-capacity-sales-002**

**CONFIGURATION** :
• Type : Fabric Capacity (64 CU)
• Environment : prod-critical
• Coût : **$27,890/mois**
• Évolution : +128% vs décembre (⚠️ forte augmentation)

**USAGE** :
• CPU : **91%** (très élevé) ✅
• Mémoire : 85%
• Queries : 2.4M/mois
• Data processed : 18.7 TB/mois
• Utilisateurs actifs : **387**

**APPLICATIONS ASSOCIÉES** :
• Sales Analytics (APP_000002)
• Sales Forecasting (APP_000015)

**BUSINESS VALUE** :
• Revenus générés (Sales Analytics) : **$8.2M/trimestre**
• Coût IT : $27,890 × 3 mois = **$83,670/trimestre**
• **ROI** : **98x** (revenus / coût IT)

**COÛT PAR UTILISATEUR** :
• $27,890 / 387 users = **$72/user/mois**

**COMPARAISON** (workloads similaires) :
| Workload | Type | Users | Coût/user | Usage CPU |
|----------|------|-------|-----------|-----------|
| sales-002 | Fabric 64 CU | 387 | **$72** | 91% |
| marketing-004 | Fabric 32 CU | 124 | $115 | 68% |
| finance-007 | Fabric 32 CU | 89 | $130 | 62% |

📊 **ANALYSE** :
• Usage **très élevé** (91%) → capacité bien utilisée ✅
• Coût/user **compétitif** ($72 vs $115-$130) ✅
• ROI **exceptionnel** (98x) ✅
• Workload **critique** pour le business (Sales Analytics) ✅

✅ **VERDICT : JUSTIFIÉ**

Le coût de $27,890/mois est pleinement justifié par :
1. Usage optimal (91%)
2. Efficacité économique ($72/user, meilleur que Marketing/Finance)
3. Valeur business exceptionnelle (ROI 98x)
4. Criticité business (Sales est priorité #1)

🎯 **RECOMMANDATION** : 
• **Conserver** ce workload sans optimisation
• **Monitorer** l'usage : si > 95%, envisager upgrade à 96 CU
• **Répliquer** les bonnes pratiques Sales vers Marketing/Finance
```

---

## 📈 Catégorie : Comparaisons

### Exemple 8 : Comparaison Coût/User entre BU

**Question** :
```
Compare le coût par utilisateur actif entre Sales, Marketing et Finance.
```

**Réponse Attendue** :
```
Comparaison Coût par Utilisateur Actif (janvier 2026) :

| BU | Coût Total | Users Actifs | Coût/User | Rang |
|----|-----------|--------------|-----------|------|
| **Marketing** | $54,120 | 418 | **$129** | 🥇 1er |
| **Sales** | $206,030 | 1,234 | **$167** | 🥈 2e |
| **Finance** | $72,450 | 389 | **$186** | 🥉 3e |

📊 **ANALYSE** :

**🥇 Marketing : Le plus efficace**
• Coût/user : $129 (baseline)
• Raison : Apps bien dimensionnées, downscale agressif dev/test
• Top app : Marketing Analytics ($31K, 124 users) → $250/user
• **Best practice** : Pause automatique sandbox après 7j

**🥈 Sales : Intermédiaire**
• Coût/user : $167 (+29% vs Marketing)
• Raison : Workloads critiques (prod-critical), haute capacité
• Top app : CRM Dashboard ($82K, 387 users) → $212/user
• **Justification** : ROI 98x, criticité business

**🥉 Finance : Le moins efficace**
• Coût/user : $186 (+44% vs Marketing)
• Raison : Over-provisioning (usage moyen 62%)
• Top app : ERP Platform ($47K, 156 users) → $301/user
• **Problème** : Apps sur-provisionnées, peu d'optimisation

💡 **INSIGHTS** :
• Marketing est **44% plus efficace** que Finance
• Sales justifie son coût par la valeur business (ROI 98x)
• Finance a un potentiel d'optimisation important

🎯 **RECOMMANDATIONS** :
1. **Finance** : Audit des apps → objectif $150/user (-20%)
   - Downscale ERP Platform
   - Optimiser Finance Reporting Tool
   - Économie estimée : ~$14K/mois

2. **Sales** : Conserver (justifié par ROI)

3. **Marketing** : Partager best practices avec Finance & IT
   - Pause auto sandbox
   - Downscale systématique dev/test
   - Archivage mensuel

**OBJECTIF GLOBAL** : Coût/user moyen < $150 (économie $40K/mois)
```

---

## ✅ Checklist de Qualité

Une bonne réponse du Data Agent doit avoir :

- [ ] **Chiffre principal** en gras dès le début
- [ ] **Contexte** (période, périmètre, comparaison)
- [ ] **Décomposition** si > 3 catégories
- [ ] **Alerte** si anomalie détectée (⚠️ ou 🚨)
- [ ] **Recommandation** actionnable (🎯)
- [ ] **Chiffrage** des économies potentielles (💰)
- [ ] **Évaluation du risque** pour les optimisations
- [ ] **Langage français** (sauf termes techniques)
- [ ] **Ton professionnel** mais accessible
- [ ] **Émojis modérés** (2-3 par réponse)

---

## 🚀 Utilisation de ces Exemples

### Pour tester le Data Agent
1. Poser la question exacte de l'exemple
2. Comparer la réponse obtenue vs réponse attendue
3. Identifier les écarts (contenu, format, ton)
4. Ajuster les instructions système si nécessaire

### Pour former les utilisateurs
1. Montrer 2-3 exemples de bonnes réponses
2. Expliquer la structure (chiffre → contexte → alerte → recommandation)
3. Laisser les utilisateurs poser leurs propres questions
4. Corriger si réponses trop vagues ou hors sujet

### Pour améliorer le Data Agent
Si les réponses réelles diffèrent :
- **Trop vagues** → Ajouter "Détaille toujours..." dans instructions
- **Manque d'alertes** → Ajouter "Sois proactif dans la détection d'anomalies"
- **Pas de recommandations** → Ajouter "Termine TOUJOURS par une action"
- **Mauvais format** → Ajouter des exemples de formatting dans instructions

---

**Version** : 1.0  
**Dernière mise à jour** : Février 2026  
**Alignement** : Instructions Système v1.0
