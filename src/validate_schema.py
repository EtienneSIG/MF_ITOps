"""
Validation des schémas de données générées
Démo Microsoft Fabric - IT Ops & FinOps

Usage:
    python validate_schema.py
"""

import pandas as pd
from pathlib import Path
import sys

# Chemins
BASE_PATH = Path(__file__).parent.parent
DATA_PATH = BASE_PATH / "data" / "raw"

# Schémas attendus
EXPECTED_SCHEMAS = {
    'subscriptions.csv': {
        'columns': ['subscription_id', 'subscription_name', 'subscription_type', 'owner', 'status', 'created_date'],
        'min_rows': 8,
        'max_rows': 8
    },
    'environments.csv': {
        'columns': ['environment_id', 'environment_name', 'environment_type', 'subscription_id', 'region', 'tags', 'created_date'],
        'min_rows': 15,
        'max_rows': 15
    },
    'workloads.csv': {
        'columns': ['workload_id', 'workload_name', 'workload_type', 'environment_id', 'status', 
                   'created_date', 'owner', 'tags', 'capacity_units', 'vcpu_count', 'storage_gb'],
        'min_rows': 100,
        'max_rows': 150
    },
    'usage_metrics.csv': {
        'columns': ['workload_id', 'date', 'cpu_usage_percent', 'memory_usage_percent', 
                   'storage_used_gb', 'storage_provisioned_gb', 'query_count', 'data_processed_gb', 'active_users'],
        'min_rows': 30000,
        'max_rows': 50000
    },
    'cloud_costs.csv': {
        'columns': ['workload_id', 'date', 'compute_cost_usd', 'storage_cost_usd', 
                   'network_cost_usd', 'total_cost_usd', 'currency', 'billing_period'],
        'min_rows': 30000,
        'max_rows': 50000
    },
    'business_units.csv': {
        'columns': ['business_unit_id', 'business_unit_name', 'budget_monthly_usd', 'head_of_unit'],
        'min_rows': 6,
        'max_rows': 6
    },
    'teams.csv': {
        'columns': ['team_id', 'team_name', 'business_unit_id', 'team_size', 'budget_monthly_usd'],
        'min_rows': 30,
        'max_rows': 30
    },
    'applications.csv': {
        'columns': ['application_id', 'application_name', 'team_id', 'application_type', 
                   'active_users', 'workload_ids'],
        'min_rows': 60,
        'max_rows': 60
    }
}


def validate_file(filename: str, schema: dict) -> tuple[bool, str]:
    """Valide un fichier CSV selon son schéma."""
    filepath = DATA_PATH / filename
    
    # Vérifier que le fichier existe
    if not filepath.exists():
        return False, f"❌ Fichier introuvable: {filename}"
    
    try:
        # Charger le CSV
        df = pd.read_csv(filepath, encoding='utf-8')
        
        # Vérifier les colonnes
        expected_cols = set(schema['columns'])
        actual_cols = set(df.columns)
        
        if expected_cols != actual_cols:
            missing = expected_cols - actual_cols
            extra = actual_cols - expected_cols
            msg = f"❌ {filename}: Colonnes incorrectes"
            if missing:
                msg += f"\n    Manquantes: {missing}"
            if extra:
                msg += f"\n    En trop: {extra}"
            return False, msg
        
        # Vérifier le nombre de lignes
        if not (schema['min_rows'] <= len(df) <= schema['max_rows']):
            return False, f"❌ {filename}: {len(df)} lignes (attendu: {schema['min_rows']}-{schema['max_rows']})"
        
        return True, f"✓ {filename}: {len(df)} lignes, {len(df.columns)} colonnes"
        
    except Exception as e:
        return False, f"❌ {filename}: Erreur de lecture - {e}"


def validate_relationships(data_path: Path) -> list[tuple[bool, str]]:
    """Valide les relations entre tables."""
    results = []
    
    try:
        # Charger les tables
        subscriptions = pd.read_csv(data_path / 'subscriptions.csv')
        environments = pd.read_csv(data_path / 'environments.csv')
        workloads = pd.read_csv(data_path / 'workloads.csv')
        usage_metrics = pd.read_csv(data_path / 'usage_metrics.csv')
        cloud_costs = pd.read_csv(data_path / 'cloud_costs.csv')
        business_units = pd.read_csv(data_path / 'business_units.csv')
        teams = pd.read_csv(data_path / 'teams.csv')
        applications = pd.read_csv(data_path / 'applications.csv')
        
        # Vérifier environments.subscription_id → subscriptions.subscription_id
        orphan_envs = environments[~environments['subscription_id'].isin(subscriptions['subscription_id'])]
        if len(orphan_envs) > 0:
            results.append((False, f"❌ {len(orphan_envs)} environments avec subscription_id invalide"))
        else:
            results.append((True, "✓ environments.subscription_id → subscriptions.subscription_id OK"))
        
        # Vérifier workloads.environment_id → environments.environment_id
        orphan_wl = workloads[~workloads['environment_id'].isin(environments['environment_id'])]
        if len(orphan_wl) > 0:
            results.append((False, f"❌ {len(orphan_wl)} workloads avec environment_id invalide"))
        else:
            results.append((True, "✓ workloads.environment_id → environments.environment_id OK"))
        
        # Vérifier usage_metrics.workload_id → workloads.workload_id
        orphan_metrics = usage_metrics[~usage_metrics['workload_id'].isin(workloads['workload_id'])]
        if len(orphan_metrics) > 0:
            results.append((False, f"❌ {len(orphan_metrics)} metrics avec workload_id invalide"))
        else:
            results.append((True, "✓ usage_metrics.workload_id → workloads.workload_id OK"))
        
        # Vérifier cloud_costs.workload_id → workloads.workload_id
        orphan_costs = cloud_costs[~cloud_costs['workload_id'].isin(workloads['workload_id'])]
        if len(orphan_costs) > 0:
            results.append((False, f"❌ {len(orphan_costs)} costs avec workload_id invalide"))
        else:
            results.append((True, "✓ cloud_costs.workload_id → workloads.workload_id OK"))
        
        # Vérifier teams.business_unit_id → business_units.business_unit_id
        orphan_teams = teams[~teams['business_unit_id'].isin(business_units['business_unit_id'])]
        if len(orphan_teams) > 0:
            results.append((False, f"❌ {len(orphan_teams)} teams avec business_unit_id invalide"))
        else:
            results.append((True, "✓ teams.business_unit_id → business_units.business_unit_id OK"))
        
        # Vérifier applications.team_id → teams.team_id
        orphan_apps = applications[~applications['team_id'].isin(teams['team_id'])]
        if len(orphan_apps) > 0:
            results.append((False, f"❌ {len(orphan_apps)} applications avec team_id invalide"))
        else:
            results.append((True, "✓ applications.team_id → teams.team_id OK"))
        
    except Exception as e:
        results.append((False, f"❌ Erreur lors de la validation des relations: {e}"))
    
    return results


def validate_data_quality(data_path: Path) -> list[tuple[bool, str]]:
    """Valide la qualité des données."""
    results = []
    
    try:
        # Charger usage_metrics et cloud_costs
        usage_metrics = pd.read_csv(data_path / 'usage_metrics.csv')
        cloud_costs = pd.read_csv(data_path / 'cloud_costs.csv')
        
        # Vérifier que CPU usage est entre 0 et 100
        invalid_cpu = usage_metrics[(usage_metrics['cpu_usage_percent'] < 0) | 
                                    (usage_metrics['cpu_usage_percent'] > 100)]
        if len(invalid_cpu) > 0:
            results.append((False, f"❌ {len(invalid_cpu)} metrics avec CPU usage invalide"))
        else:
            results.append((True, "✓ CPU usage dans la plage [0, 100]"))
        
        # Vérifier que Memory usage est entre 0 et 100
        invalid_mem = usage_metrics[(usage_metrics['memory_usage_percent'] < 0) | 
                                    (usage_metrics['memory_usage_percent'] > 100)]
        if len(invalid_mem) > 0:
            results.append((False, f"❌ {len(invalid_mem)} metrics avec Memory usage invalide"))
        else:
            results.append((True, "✓ Memory usage dans la plage [0, 100]"))
        
        # Vérifier que les coûts sont >= 0
        invalid_costs = cloud_costs[cloud_costs['total_cost_usd'] < 0]
        if len(invalid_costs) > 0:
            results.append((False, f"❌ {len(invalid_costs)} coûts négatifs"))
        else:
            results.append((True, "✓ Tous les coûts sont >= 0"))
        
        # Vérifier que storage_used <= storage_provisioned
        invalid_storage = usage_metrics[usage_metrics['storage_used_gb'] > usage_metrics['storage_provisioned_gb']]
        if len(invalid_storage) > 0:
            results.append((False, f"❌ {len(invalid_storage)} metrics avec storage_used > storage_provisioned"))
        else:
            results.append((True, "✓ Storage used <= provisioned"))
        
    except Exception as e:
        results.append((False, f"❌ Erreur lors de la validation qualité: {e}"))
    
    return results


def main():
    """Point d'entrée principal."""
    print("=" * 60)
    print("🔍 VALIDATION DES SCHÉMAS - IT OPS & FINOPS")
    print("=" * 60)
    
    # Vérifier que le dossier data existe
    if not DATA_PATH.exists():
        print(f"\n❌ Dossier introuvable: {DATA_PATH}")
        print("   Exécutez d'abord: python generate_data.py")
        sys.exit(1)
    
    all_valid = True
    
    # 1. Validation des schémas
    print("\n📋 Validation des schémas:")
    for filename, schema in EXPECTED_SCHEMAS.items():
        valid, message = validate_file(filename, schema)
        print(f"  {message}")
        if not valid:
            all_valid = False
    
    # 2. Validation des relations
    print("\n🔗 Validation des relations:")
    relation_results = validate_relationships(DATA_PATH)
    for valid, message in relation_results:
        print(f"  {message}")
        if not valid:
            all_valid = False
    
    # 3. Validation de la qualité
    print("\n✨ Validation de la qualité:")
    quality_results = validate_data_quality(DATA_PATH)
    for valid, message in quality_results:
        print(f"  {message}")
        if not valid:
            all_valid = False
    
    # Résultat final
    print("\n" + "=" * 60)
    if all_valid:
        print("✅ VALIDATION RÉUSSIE - Toutes les données sont conformes")
        print("=" * 60)
        print("\n🎯 Prochaines étapes:")
        print("  1. Uploader les CSV vers OneLake")
        print("  2. Créer les tables Delta dans le Lakehouse")
        print("  3. Configurer le modèle sémantique")
        print("  4. Tester le Data Agent")
        sys.exit(0)
    else:
        print("❌ VALIDATION ÉCHOUÉE - Corriger les erreurs ci-dessus")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
