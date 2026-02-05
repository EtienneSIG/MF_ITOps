# Scénario de Démo - "Le Coût Fabric qui Explose"

## 🎭 Contexte

**Date** : 5 février 2026  
**Lieu** : Salle de réunion du CFO, Contoso Corp  
**Participants** :
- **Sarah Chen** - CFO (Chief Financial Officer)
- **Marcus Johnson** - CIO (Chief Information Officer)
- **Elena Rodriguez** - FinOps Manager
- **David Kim** - Lead Data Engineer (vous)

---

## 📊 La Situation

### Email du CFO (3 février 2026, 8h30)

```
De: Sarah Chen <sarah.chen@contoso.com>
À: Marcus Johnson <marcus.johnson@contoso.com>
CC: Elena Rodriguez <elena.rodriguez@contoso.com>
Objet: 🚨 URGENT - Explosion des coûts Azure/Fabric en janvier

Marcus,

Je viens de recevoir la facture Azure pour janvier 2026 : $487,350 !

C'est une augmentation de 35% vs décembre ($361,000). 
Sur l'année, on est à +52% vs janvier 2025 ($320,000).

Questions immédiates :
1. Pourquoi cette explosion soudaine ?
2. Quels services/équipes sont responsables ?
3. Est-ce justifié par l'usage business ?
4. Où peut-on optimiser SANS impacter les opérations ?

Réunion de crise demain 9h. Je veux des réponses chiffrées.

Sarah
```

### Réaction du CIO

Marcus est sous pression. Il convoque Elena (FinOps) et David (Data Engineering) pour préparer la réunion.

**Problème** : Les factures Azure sont opaques. On sait combien on paie, mais pas :
- Qui consomme quoi ?
- Pourquoi l'augmentation ?
- Quelle est la valeur business de chaque workload ?
- Où optimiser sans risque ?

**Solution** : Utiliser le **Fabric Data Agent** configuré par David pour interroger les données de coûts et usage.

---

## 🔍 Investigation avec le Data Agent

### 15h30 - Première Analyse

**Elena** : "David, tu as configuré ce fameux Data Agent Fabric pour le FinOps. Peux-tu nous montrer ce qu'il trouve ?"

**David** : "Bien sûr. J'ai consolidé toutes les données : coûts, usage, mapping vers les apps et les équipes. Posons-lui des questions."

---

### Question 1 : Vue d'ensemble

**👤 Utilisateur** : "Quel est le coût total Fabric + Azure pour janvier 2026 ?"

**🤖 Data Agent** :
```
Le coût total pour janvier 2026 est de $487,350.

Répartition :
• Compute : $341,145 (70%)
• Storage : $121,838 (25%)  
• Network : $24,367 (5%)

Par rapport à décembre 2025 ($361,000), c'est une augmentation de $126,350 (+35%).
```

**Elena** : "35% confirmé. Mais pourquoi ?"

---

### Question 2 : Top contributeurs

**👤 Utilisateur** : "Quels sont les 5 workloads les plus chers en janvier ?"

**🤖 Data Agent** :
```
Top 5 des workloads les plus chers (janvier 2026) :

1. fabric-capacity-delta-001 (ENV_001 - prod-critical)
   • Type: Fabric Capacity (128 CU)
   • Coût: $38,420 (+142% vs décembre)
   • Usage CPU: 87%
   
2. azure-sql-analytics-003 (ENV_002 - prod-standard)
   • Type: Azure SQL (16 vCPU)
   • Coût: $31,250 (+8% vs décembre)
   • Usage CPU: 76%

3. fabric-capacity-sales-002 (ENV_001 - prod-critical)
   • Type: Fabric Capacity (64 CU)
   • Coût: $27,890 (+128% vs décembre)
   • Usage CPU: 91%

4. azure-vm-web-012 (ENV_002 - prod-standard)
   • Type: Azure VM (32 vCPU)
   • Coût: $18,340 (+5% vs décembre)
   • Usage CPU: 82%

5. fabric-capacity-marketing-004 (ENV_003 - prod-low)
   • Type: Fabric Capacity (32 CU)
   • Coût: $14,230 (+95% vs décembre)
   • Usage CPU: 68%

ALERTE : Les 3 workloads Fabric Capacity ont doublé en coût !
```

**Marcus** : "Fabric Capacity... Ce sont nos nouveaux lakehouses analytics. Pourquoi ils ont doublé ?"

---

### Question 3 : Détection d'anomalies

**👤 Utilisateur** : "Quels workloads ont augmenté de plus de 50% en janvier vs décembre ?"

**🤖 Data Agent** :
```
12 workloads ont augmenté de plus de 50% :

FABRIC CAPACITY (5 workloads) :
• fabric-capacity-delta-001 : +142% ($38,420)
• fabric-capacity-sales-002 : +128% ($27,890)
• fabric-capacity-marketing-004 : +95% ($14,230)
• fabric-capacity-finance-007 : +87% ($11,560)
• fabric-capacity-hr-009 : +73% ($8,940)

AZURE STORAGE (4 workloads) :
• azure-storage-archive-018 : +215% ($6,780)
• azure-storage-datalake-023 : +102% ($5,120)
• azure-storage-backup-031 : +89% ($4,230)
• azure-storage-logs-042 : +64% ($3,890)

AZURE FUNCTIONS (3 workloads) :
• azure-functions-etl-054 : +156% ($2,340)
• azure-functions-api-067 : +78% ($1,890)
• azure-functions-trigger-078 : +62% ($1,450)

Cause probable : Scaling-up des Fabric Capacities + augmentation du storage archive.
```

**Elena** : "C'est clair maintenant. Les capacités Fabric ont été surdimensionnées en janvier."

---

### Question 4 : Mapping vers le business

**👤 Utilisateur** : "Combien coûte l'équipe Sales en infrastructure IT ?"

**🤖 Data Agent** :
```
Coût IT de la Business Unit "Sales" (janvier 2026) :

Teams Sales (5 équipes) :
• Sales Analytics Team : $52,340
• Sales Operations Team : $38,120
• Sales Platform Team : $41,890
• Sales Engineering Team : $29,450
• Sales Data Team : $44,230

TOTAL Sales BU : $206,030

Applications principales :
• CRM Dashboard (APP_000001) : $82,340
• Sales Analytics (APP_000002) : $54,670
• Customer Data Platform (APP_000008) : $37,220
• Lead Scoring Engine (APP_000012) : $21,890
• Sales Forecasting (APP_000015) : $9,910

Workloads associés :
• fabric-capacity-sales-002 : $27,890
• azure-sql-crm-003 : $31,250
• azure-vm-sales-app-019 : $12,340
• ... (15 workloads au total)

Budget alloué : $50,000/mois
DÉPASSEMENT : +$156,030 (+312% !!!)
```

**Sarah** (CFO) : "312% de dépassement sur Sales ?! Marcus, c'est quoi cette histoire ?"

**Marcus** : "On a déployé le nouveau CRM et les analytics en janvier. Apparemment on a trop provisionné..."

---

### Question 5 : Workloads surdimensionnés

**👤 Utilisateur** : "Quels workloads sont surdimensionnés : usage CPU < 40% et coût > $1000/mois ?"

**🤖 Data Agent** :
```
23 workloads surdimensionnés détectés (janvier 2026) :

CANDIDATS PRIORITAIRES (usage < 20%, coût > $5000) :
1. azure-vm-legacy-034 (ENV_007 - dev-team2)
   • Usage CPU: 12%  |  Coût: $8,340
   • Recommandation: ARRÊTER (environnement dev non utilisé)

2. fabric-capacity-poc-018 (ENV_014 - sandbox-innovation)
   • Usage CPU: 8%  |  Coût: $6,780
   • Recommandation: ARRÊTER (POC terminé en novembre)

3. azure-storage-temp-029 (ENV_015 - sandbox-poc)
   • Usage CPU: N/A  |  Coût: $5,120
   • Storage utilisé: 234 GB / 10,000 GB (2.3%)
   • Recommandation: DOWNSCALE à 500 GB

OPTIMISATION MEDIUM (usage 20-40%, coût > $2000) :
4. azure-vm-web-staging-041 : 28% CPU, $4,230
5. fabric-capacity-test-052 : 32% CPU, $3,890
6. azure-sql-reporting-063 : 35% CPU, $3,450
... (17 autres workloads)

ÉCONOMIES POTENTIELLES :
• Arrêt des zombies (usage < 20%) : $38,450/mois
• Downscale (usage 20-40%) : $21,780/mois
• TOTAL : $60,230/mois (~$723,000/an)
```

**Elena** : "60K$/mois d'économies sans rien casser ! Il faut agir vite."

---

### Question 6 : Impact business des optimisations

**👤 Utilisateur** : "Si je supprime les 3 workloads sandbox non utilisés, quel sera l'impact ?"

**🤖 Data Agent** :
```
Impact de la suppression des 3 workloads sandbox :

WORKLOADS CONCERNÉS :
1. fabric-capacity-poc-018 ($6,780/mois)
   • Application: POC AI Vision (APP_000047) - TERMINÉ
   • Utilisateurs actifs: 0
   • Dernière activité: 28 nov 2025

2. azure-vm-legacy-034 ($8,340/mois)
   • Application: Dev Environment Legacy (APP_000051) - ABANDONNÉ
   • Utilisateurs actifs: 0
   • Dernière activité: 12 déc 2025

3. azure-storage-temp-029 ($5,120/mois)
   • Application: Sandbox Storage (APP_000053) - TEMPORAIRE
   • Utilisateurs actifs: 0
   • Données: 234 GB (archivables)

ÉCONOMIES : $20,240/mois ($242,880/an)

IMPACT BUSINESS : AUCUN
• Aucun utilisateur actif
• Aucune dépendance applicative
• Données archivables dans cold storage ($50/mois)

RECOMMANDATION : Suppression immédiate sans risque.
```

**Marcus** : "Parfait. On les coupe dès demain."

---

### Question 7 : Justification des coûts

**👤 Utilisateur** : "Le coût du workload 'fabric-capacity-sales-002' ($27,890/mois) est-il justifié vu l'usage ?"

**🤖 Data Agent** :
```
Analyse du workload 'fabric-capacity-sales-002' :

CONFIGURATION :
• Type: Fabric Capacity (64 CU)
• Environment: prod-critical
• Coût: $27,890/mois (janvier 2026)

USAGE :
• CPU: 91% (très élevé)
• Queries: 2.4M/mois
• Data processed: 18.7 TB/mois
• Utilisateurs actifs: 387

APPLICATIONS ASSOCIÉES :
• Sales Analytics (APP_000002)
• Sales Forecasting (APP_000015)

BUSINESS VALUE :
• Utilisateurs actifs: 387
• Coût par utilisateur: $72/mois
• Revenus générés (Sales Analytics): $8.2M/trimestre
• ROI: 295x (revenus / coût IT)

COMPARAISON :
• Marketing similaire (fabric-capacity-marketing-004) : $14,230, 68% CPU, 124 users → $115/user
• Finance similaire (fabric-capacity-finance-007) : $11,560, 62% CPU, 89 users → $130/user

VERDICT : ✅ JUSTIFIÉ
• Usage très élevé (91%)
• Coût par utilisateur compétitif ($72 vs $115-$130 ailleurs)
• ROI exceptionnel (295x)
• Workload critique pour le business

RECOMMANDATION : Conserver. Possibilité d'upgrade à 96 CU si usage > 95%.
```

**Sarah** : "OK, celui-là est justifié. Par contre, Marketing et Finance semblent chers par utilisateur..."

---

## 💡 Conclusions de l'Investigation

### 16h45 - Synthèse

**Elena** présente les conclusions :

### Causes de l'augmentation (+35%)
1. **Scaling-up Fabric Capacities** : 5 capacités augmentées en janvier (+$78K)
2. **Croissance organique** : +2%/mois attendu (+$7K)
3. **Archives oubliées** : Storage qui s'accumule (+$12K)
4. **Workloads zombies** : Sandbox/POC non nettoyés (+$20K)

### Plan d'Action Immédiat

| Action | Économies | Risque | Délai |
|--------|-----------|--------|-------|
| Supprimer 3 sandbox zombies | $20,240/mois | Aucun | 1 jour |
| Downscale 12 workloads dev/test | $21,780/mois | Faible | 1 semaine |
| Archiver storage ancien (>12 mois) | $8,450/mois | Aucun | 2 semaines |
| Optimiser Fabric Capacities | $9,760/mois | Moyen | 1 mois |
| **TOTAL** | **$60,230/mois** | | |

### Plan à 6 Mois

1. **Gouvernance FinOps** :
   - Alertes automatiques sur dépassements de budget
   - Review mensuel des workloads par équipe
   - Tags obligatoires (owner, BU, env, criticality)

2. **Right-sizing automatique** :
   - Downscale auto des dev/test le weekend
   - Pause automatique des sandbox après 7j d'inactivité
   - Archivage auto du storage > 6 mois

3. **Chargebacks** :
   - Facturation interne par BU (responsabilisation)
   - Budgets par équipe avec alertes à 80%
   - Dashboard FinOps temps réel

### Projection Budget 2026

- **Scénario sans action** : $6.2M/an
- **Avec optimisations** : $5.5M/an
- **Économies** : $700K/an (-11%)

---

## 🎯 Réunion du 5 février - Présentation au CFO

### 9h00 - Sarah Chen (CFO) entre dans la salle

**Sarah** : "Alors, Marcus, j'espère que vous avez des réponses ?"

**Marcus** : "Oui Sarah. Elena et David ont fait une analyse complète avec notre Data Agent Fabric. On a identifié les causes et les solutions."

**Elena** (démonstration live du Data Agent) :
- Montre les 5 workloads les plus chers
- Explique le spike Fabric Capacity
- Détaille les 23 workloads surdimensionnés
- Présente le plan d'optimisation : $60K/mois d'économies

**Sarah** : "Impressionnant. Donc vous me dites qu'on peut économiser $720K/an sans impacter le business ?"

**Elena** : "Exactement. Et avec la gouvernance FinOps qu'on va mettre en place, on évitera ce genre de dérive à l'avenir."

**Sarah** : "Parfait. Je veux un rapport mensuel avec ce Data Agent. Et les chargebacks par BU : en place avant fin mars."

**Marcus** : "Ce sera fait, Sarah."

---

## 🏆 Résultats (Mars 2026)

### Après 1 mois d'optimisations

- **Coût mars 2026** : $412,000 (vs $487K en janvier)
- **Économies réalisées** : $75,000 (-15%)
- **Workloads supprimés** : 8 (zombies)
- **Workloads downsizés** : 18
- **Satisfaction business** : Inchangée (aucun impact)

### Indicateurs FinOps

| Métrique | Janvier | Mars | Évolution |
|----------|---------|------|-----------|
| Coût total | $487K | $412K | -15% ✅ |
| Workloads actifs | 120 | 112 | -7% |
| Taux d'utilisation moyen | 58% | 71% | +13% ✅ |
| Workloads surdimensionnés | 23 | 8 | -65% ✅ |
| Coût par utilisateur actif | $142 | $118 | -17% ✅ |

### Feedback CFO (Email du 28 mars 2026)

```
De: Sarah Chen <sarah.chen@contoso.com>
À: Marcus Johnson <marcus.johnson@contoso.com>
CC: Elena Rodriguez <elena.rodriguez@contoso.com>; David Kim <david.kim@contoso.com>
Objet: 👏 Bravo pour les optimisations IT

Marcus, Elena, David,

Facture mars : $412K. Objectif dépassé !

Non seulement on a récupéré les $126K de dérive, mais on a en plus optimisé $75K.

Le Data Agent Fabric est un game-changer pour le FinOps. 
Je veux que toutes les BU l'utilisent pour piloter leurs coûts.

Bravo à l'équipe.

Sarah
```

---

## 📚 Leçons Apprises

### Ce qui a fonctionné ✅
1. **Data Agent Fabric** : Réponses en langage naturel, accessibles au CFO
2. **Mapping IT ↔ Business** : Lien direct coût → app → team → BU
3. **Détection automatique** : Workloads surdimensionnés identifiés en 1 clic
4. **Chiffrage précis** : Économies calculées, ROI prouvé
5. **Action rapide** : Plan d'optimisation en 48h

### Erreurs évitées ❌
1. ~~"C'est Azure, c'est complexe, on ne peut pas expliquer"~~ 
   → **Data Agent explique tout en français**
2. ~~"Optimiser = risque pour le business"~~
   → **Impact business évalué par workload**
3. ~~"On verra le mois prochain"~~
   → **Action immédiate, résultats en 1 mois**

### Recommandations
- Implémenter un Data Agent FinOps dès le déploiement de Fabric
- Former les équipes finance ET IT à l'utilisation
- Automatiser les alertes et les actions (pause auto, downscale)
- Chargebacks pour responsabiliser les BU

---

**🎬 FIN DU SCÉNARIO**

_Cette démonstration montre comment Microsoft Fabric Data Agent transforme la gestion des coûts IT en permettant des analyses complexes via des questions en langage naturel, accessible à tous les stakeholders (CFO, CIO, FinOps)._
