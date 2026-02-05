# Questions de Démo - Data Agent IT Finance Analyst

## 📋 Vue d'ensemble

Ces 15 questions permettent de tester le **Fabric Data Agent** configuré pour le FinOps.
Elles couvrent tous les cas d'usage : analyse globale, détection d'anomalies, optimisation, mapping business, ROI.

**Ordre recommandé** : Suivre la numérotation pour un storytelling cohérent.

---

## 🎯 Questions par Catégorie

### 1️⃣ Analyse Globale des Coûts

#### Q1 : Coût total mensuel
**Question** :
```
Quel est le coût total Fabric + Azure pour janvier 2026 ?
```

**Réponse attendue** :
- Coût total : ~$487K
- Répartition compute/storage/network (70/25/5%)
- Comparaison vs décembre (-35%)
- Tendance sur 12 mois

**Utilité** : Vue d'ensemble pour cadrer la discussion avec le CFO.

---

#### Q2 : Évolution mensuelle
**Question** :
```
Comment ont évolué les coûts IT mois par mois sur les 12 derniers mois ?
```

**Réponse attendue** :
- Tableau mois par mois (févr 2025 → janv 2026)
- Croissance M/M (%) pour chaque mois
- Identification du pic en janvier 2026
- Croissance annuelle totale (~+52%)

**Utilité** : Détecter les tendances et les anomalies temporelles.

---

#### Q3 : Répartition par type de workload
**Question** :
```
Quelle est la répartition des coûts par type de workload (Fabric, VM, Storage, SQL, Functions) ?
```

**Réponse attendue** :
- Fabric Capacity : ~45% des coûts
- Azure VMs : ~25%
- Azure Storage : ~15%
- Azure SQL : ~10%
- Azure Functions : ~5%

**Utilité** : Identifier les postes de dépenses dominants.

---

### 2️⃣ Top Contributeurs & Détection d'Anomalies

#### Q4 : Top 5 workloads les plus chers
**Question** :
```
Quels sont les 5 workloads les plus chers en janvier 2026 ?
```

**Réponse attendue** :
- Liste des 5 workloads avec :
  - Nom, type, environment
  - Coût mensuel
  - Évolution vs décembre (%)
  - Usage CPU moyen
- Alerte sur les Fabric Capacities surdimensionnées

**Utilité** : Focus sur les gros postes de dépenses.

---

#### Q5 : Workloads avec croissance anormale
**Question** :
```
Quels workloads ont augmenté de plus de 30% en janvier 2026 vs décembre 2025 ?
```

**Réponse attendue** :
- Liste de 10-15 workloads
- Catégorisation par type
- Identification des causes (scaling-up, usage accru, erreur de config)
- Priorisation par impact ($)

**Utilité** : Détection des dérives de coûts.

---

#### Q6 : Coûts par environnement
**Question** :
```
Quelle est la répartition des coûts par type d'environnement (production, preproduction, development, sandbox) ?
```

**Réponse attendue** :
- Production : ~70% (justifié par criticité)
- Pre-production : ~15%
- Development : ~12%
- Sandbox : ~3% (mais candidats à optimisation)

**Utilité** : Vérifier que le budget est bien alloué (prod >> dev/test).

---

### 3️⃣ Optimisation & Inefficacités

#### Q7 : Workloads surdimensionnés
**Question** :
```
Quels workloads sont surdimensionnés : usage CPU < 40% et coût > $1000/mois ?
```

**Réponse attendue** :
- Liste de 20-25 workloads
- Catégorisation par gravité :
  - Critiques : usage < 20%, coût > $5K
  - Moyens : usage 20-40%, coût > $2K
  - Faibles : usage 40-50%, coût > $1K
- Économies potentielles chiffrées par workload

**Utilité** : Identifier les quick wins d'optimisation.

---

#### Q8 : Workloads zombies (non utilisés)
**Question** :
```
Quels workloads ont un usage < 10% et n'ont aucun utilisateur actif ?
```

**Réponse attendue** :
- Liste de 5-8 workloads "zombies"
- Principalement en sandbox/dev
- Date de dernière activité
- Coût total gaspillé (~$20-30K/mois)

**Utilité** : Candidats à suppression immédiate.

---

#### Q9 : Storage sous-utilisé
**Question** :
```
Quels workloads de type Storage ont un taux d'utilisation < 30% (storage_used / storage_provisioned) ?
```

**Réponse attendue** :
- Liste de 8-12 workloads Storage
- Capacité provisionnée vs utilisée
- Coût mensuel
- Recommandation de downscale avec économies

**Utilité** : Optimiser les coûts de stockage (souvent négligés).

---

#### Q10 : Calcul des économies potentielles
**Question** :
```
Si je supprime tous les workloads sandbox avec usage < 10%, combien j'économise par mois ?
```

**Réponse attendue** :
- Liste des workloads concernés (5-8)
- Coût mensuel total : ~$20-25K
- Projection annuelle : ~$240-300K
- Impact business : AUCUN (pas d'utilisateurs actifs)

**Utilité** : Chiffrer l'optimisation pour convaincre le CFO.

---

### 4️⃣ Mapping Business & Chargebacks

#### Q11 : Coût par Business Unit
**Question** :
```
Combien coûte chaque Business Unit en infrastructure IT pour janvier 2026 ?
```

**Réponse attendue** :
- Tableau des 6 BU :
  - Sales : ~$206K
  - IT : ~$98K
  - Finance : ~$72K
  - Marketing : ~$54K
  - Operations : ~$38K
  - HR : ~$19K
- Comparaison budget alloué vs réalisé
- Identification des dépassements

**Utilité** : Chargebacks et responsabilisation des BU.

---

#### Q12 : Coût par équipe (top 5)
**Question** :
```
Quelles sont les 5 équipes les plus dépensières en IT ?
```

**Réponse attendue** :
- Sales Analytics Team : ~$52K
- IT Infrastructure Team : ~$48K
- Finance Platform Team : ~$41K
- Sales Operations Team : ~$38K
- Marketing Operations Team : ~$31K

**Utilité** : Focus sur les équipes à fort impact financier.

---

#### Q13 : Applications les plus chères
**Question** :
```
Quelles sont les 5 applications les plus chères et combien d'utilisateurs actifs ont-elles ?
```

**Réponse attendue** :
- CRM Dashboard : $82K, 387 users → $212/user
- Sales Analytics : $54K, 245 users → $220/user
- ERP Platform : $47K, 412 users → $114/user
- Finance Reporting : $38K, 156 users → $244/user
- Marketing Analytics : $31K, 124 users → $250/user

**Utilité** : Calculer le coût par utilisateur et identifier les apps inefficaces.

---

### 5️⃣ Justification & ROI

#### Q14 : Justification d'un workload cher
**Question** :
```
Le coût du workload 'fabric-capacity-sales-002' ($27,890/mois) est-il justifié vu l'usage et la valeur business ?
```

**Réponse attendue** :
- Configuration : 64 CU, prod-critical
- Usage : 91% CPU (très élevé) ✅
- Utilisateurs : 387 actifs
- Coût par utilisateur : $72/mois (compétitif)
- Applications : Sales Analytics (génère $8.2M/trimestre)
- ROI : 295x (revenus / coût IT)
- **Verdict** : ✅ JUSTIFIÉ

**Utilité** : Défendre les workloads critiques face au CFO.

---

#### Q15 : Comparaison efficacité entre BU
**Question** :
```
Compare le coût par utilisateur actif entre les Business Units Sales, Marketing et Finance.
```

**Réponse attendue** :
- **Sales** : $206K / 1,234 users = $167/user
- **Marketing** : $54K / 418 users = $129/user ✅ (meilleur)
- **Finance** : $72K / 389 users = $185/user

**Insight** : 
- Marketing est la plus efficace (apps bien dimensionnées)
- Finance est la moins efficace (apps sur-provisionnées)

**Recommandation** : Auditer les apps Finance pour optimisation.

**Utilité** : Benchmarking interne pour amélioration continue.

---

## 🎓 Bonnes Pratiques pour la Démo

### Préparation
1. **Tester les 15 questions** avant la démo live
2. **Vérifier les chiffres** (coûts, pourcentages, tendances)
3. **Préparer des variantes** si une question échoue
4. **Avoir un backup** (screenshots des réponses attendues)

### Pendant la Démo
1. **Commencer par Q1-Q3** (vue d'ensemble) pour planter le décor
2. **Montrer Q7-Q10** (optimisations) pour l'impact business
3. **Utiliser Q14-Q15** (ROI) pour justifier l'investissement Fabric
4. **Laisser l'audience poser des questions** et les traiter en live avec le Data Agent

### Pièges à Éviter
- ❌ Ne pas enchainer trop vite (laisser le temps de lire les réponses)
- ❌ Ne pas sauter les étapes (vue d'ensemble → détails → actions)
- ❌ Ne pas se concentrer que sur les problèmes (montrer aussi les succès)
- ❌ Ne pas oublier de conclure sur les économies potentielles ($60K/mois)

---

## 📊 Checklist de Validation

Avant la démo, vérifier que le Data Agent répond correctement à :

- [ ] Q1 : Coût total janvier 2026
- [ ] Q2 : Évolution mensuelle sur 12 mois
- [ ] Q3 : Répartition par type de workload
- [ ] Q4 : Top 5 workloads chers
- [ ] Q5 : Workloads avec croissance > 30%
- [ ] Q6 : Coûts par environnement
- [ ] Q7 : Workloads surdimensionnés
- [ ] Q8 : Workloads zombies
- [ ] Q9 : Storage sous-utilisé
- [ ] Q10 : Économies potentielles sandbox
- [ ] Q11 : Coût par Business Unit
- [ ] Q12 : Top 5 équipes dépensières
- [ ] Q13 : Applications les plus chères + users
- [ ] Q14 : Justification workload cher
- [ ] Q15 : Comparaison coût/user entre BU

---

## 🚀 Questions Bonus (Avancées)

Si le temps le permet, questions plus avancées :

#### B1 : Prédiction de coûts
```
Si la tendance actuelle continue, quel sera le coût total en juin 2026 ?
```

#### B2 : Impact d'un downscale
```
Si je downscale tous les workloads dev/test à 50% de leur capacité, combien j'économise sans impacter la production ?
```

#### B3 : Analyse de corrélation
```
Y a-t-il une corrélation entre le nombre de queries et le coût pour les workloads Fabric Capacity ?
```

#### B4 : Détection de fraude/erreur
```
Quels workloads ont un coût anormalement élevé par rapport à leur usage (outliers) ?
```

#### B5 : Recommandations d'archivage
```
Quels workloads Storage ont des données de plus de 12 mois qui pourraient être archivées en cold storage ?
```

---

**💡 Conseil final** : Le Data Agent est puissant, mais la préparation est clé. Testez toutes les questions, comprenez les données sous-jacentes, et soyez prêt à adapter le discours selon l'audience (CFO, CIO, FinOps, Engineering).
