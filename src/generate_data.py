"""
Générateur de données synthétiques pour démo Microsoft Fabric
IT Ops & FinOps

Usage:
    python generate_data.py
"""

import os
import sys
import yaml
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from faker import Faker
from typing import Dict, List, Tuple

# Configuration globale
CONFIG_FILE = Path(__file__).parent / "config.yaml"


class FinOpsDataGenerator:
    """Générateur de données synthétiques pour la démo IT Ops & FinOps."""
    
    def __init__(self, config_path: Path):
        """Initialise le générateur avec la configuration."""
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # Initialiser Faker avec seed pour reproductibilité
        seed = self.config['seed']
        Faker.seed(seed)
        random.seed(seed)
        np.random.seed(seed)
        
        self.fake = Faker('en_US')
        
        # Dates
        self.start_date = datetime.fromisoformat(self.config['date_range']['start'])
        self.end_date = datetime.fromisoformat(self.config['date_range']['end'])
        
        # Chemins de sortie
        self.base_path = Path(__file__).parent.parent
        self.output_dir = self.base_path / self.config['output']['output_dir']
        
        # Créer le dossier si nécessaire
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"✓ Configuration chargée (seed={seed})")
        print(f"✓ Période: {self.start_date.date()} → {self.end_date.date()}")
    
    def random_date(self, start: datetime, end: datetime) -> datetime:
        """Génère une date aléatoire entre start et end."""
        delta = end - start
        random_days = random.randint(0, delta.days)
        return start + timedelta(days=random_days)
    
    def generate_subscriptions(self) -> pd.DataFrame:
        """Génère la table subscriptions."""
        print("\n📋 Génération des subscriptions Azure...")
        subscriptions = []
        
        for sub_type in self.config['subscriptions']['types']:
            for i in range(sub_type['count']):
                sub_id = f"SUB_{self.fake.uuid4()[:8].upper()}"
                subscription = {
                    'subscription_id': sub_id,
                    'subscription_name': f"{sub_type['name'].upper()}-{i+1:02d}",
                    'subscription_type': sub_type['name'],
                    'owner': self.fake.name(),
                    'status': 'active',
                    'created_date': self.random_date(
                        self.start_date - timedelta(days=730),
                        self.start_date
                    ).strftime(self.config['output']['date_format'])
                }
                subscriptions.append(subscription)
        
        df = pd.DataFrame(subscriptions)
        print(f"  ✓ {len(df)} subscriptions générées")
        return df
    
    def generate_environments(self, subscriptions_df: pd.DataFrame) -> pd.DataFrame:
        """Génère la table environments."""
        print("\n🌍 Génération des environments...")
        environments = []
        env_id = 1
        
        for env_type, config in self.config['environments']['by_type'].items():
            for i in range(config['count']):
                # Choisir une subscription appropriée
                if env_type == 'production':
                    sub_type = 'prod'
                elif env_type == 'preproduction':
                    sub_type = random.choice(['prod', 'test'])
                elif env_type == 'development':
                    sub_type = 'dev'
                else:  # sandbox
                    sub_type = random.choice(['dev', 'shared'])
                
                matching_subs = subscriptions_df[subscriptions_df['subscription_type'] == sub_type]
                subscription = matching_subs.sample(n=1).iloc[0] if len(matching_subs) > 0 else subscriptions_df.sample(n=1).iloc[0]
                
                environment = {
                    'environment_id': f'ENV_{env_id:03d}',
                    'environment_name': config['names'][i],
                    'environment_type': env_type,
                    'subscription_id': subscription['subscription_id'],
                    'region': random.choice(['eastus', 'westeurope', 'northeurope', 'francecentral']),
                    'tags': f"env={env_type},managed=true",
                    'created_date': self.random_date(
                        self.start_date - timedelta(days=365),
                        self.start_date
                    ).strftime(self.config['output']['date_format'])
                }
                environments.append(environment)
                env_id += 1
        
        df = pd.DataFrame(environments)
        print(f"  ✓ {len(df)} environments générés")
        return df
    
    def generate_workloads(self, environments_df: pd.DataFrame) -> pd.DataFrame:
        """Génère la table workloads."""
        print("\n⚙️ Génération des workloads...")
        workloads = []
        workload_id = 1
        total = self.config['volumes']['workloads']
        
        for wl_type, type_config in self.config['workloads']['types'].items():
            count = int(total * type_config['percentage'] / 100)
            
            for i in range(count):
                # Sélectionner un environment selon distribution
                env_type_rand = random.random()
                if env_type_rand < self.config['workloads']['distribution']['production']:
                    env_type = 'production'
                elif env_type_rand < (self.config['workloads']['distribution']['production'] + 
                                     self.config['workloads']['distribution']['preproduction']):
                    env_type = 'preproduction'
                elif env_type_rand < (self.config['workloads']['distribution']['production'] + 
                                     self.config['workloads']['distribution']['preproduction'] +
                                     self.config['workloads']['distribution']['development']):
                    env_type = 'development'
                else:
                    env_type = 'sandbox'
                
                matching_envs = environments_df[environments_df['environment_type'] == env_type]
                environment = matching_envs.sample(n=1).iloc[0] if len(matching_envs) > 0 else environments_df.sample(n=1).iloc[0]
                
                # Générer les attributs selon le type
                workload = {
                    'workload_id': f'WL_{workload_id:08d}',
                    'workload_name': f"{wl_type.replace('_', '-')}-{self.fake.word()}-{i+1:03d}",
                    'workload_type': wl_type,
                    'environment_id': environment['environment_id'],
                    'status': random.choice(['running', 'running', 'running', 'stopped', 'paused']),
                    'created_date': self.random_date(
                        self.start_date - timedelta(days=180),
                        self.end_date - timedelta(days=30)
                    ).strftime(self.config['output']['date_format']),
                    'owner': self.fake.name(),
                    'tags': f"type={wl_type},env={env_type}"
                }
                
                # Ajouter les attributs spécifiques au type
                if wl_type == 'fabric_capacity':
                    workload['capacity_units'] = random.randint(*type_config['capacity_units_range'])
                    workload['vcpu_count'] = None
                    workload['storage_gb'] = random.randint(1000, 10000)
                elif wl_type == 'azure_vm':
                    workload['capacity_units'] = None
                    workload['vcpu_count'] = random.choice([2, 4, 8, 16, 32, 64])
                    workload['storage_gb'] = random.randint(128, 2048)
                elif wl_type == 'azure_storage':
                    workload['capacity_units'] = None
                    workload['vcpu_count'] = None
                    workload['storage_gb'] = random.randint(*type_config['storage_gb_range'])
                elif wl_type == 'azure_sql':
                    workload['capacity_units'] = None
                    workload['vcpu_count'] = random.choice([2, 4, 8, 16])
                    workload['storage_gb'] = random.randint(*type_config['db_size_range'])
                elif wl_type == 'azure_functions':
                    workload['capacity_units'] = None
                    workload['vcpu_count'] = random.choice([1, 2, 4])
                    workload['storage_gb'] = random.randint(10, 100)
                
                workloads.append(workload)
                workload_id += 1
        
        df = pd.DataFrame(workloads)
        print(f"  ✓ {len(df)} workloads générés")
        return df
    
    def generate_usage_metrics(self, workloads_df: pd.DataFrame) -> pd.DataFrame:
        """Génère la table usage_metrics."""
        print("\n📊 Génération des usage metrics...")
        metrics = []
        
        # Pour chaque workload
        for workload in workloads_df.itertuples():
            # Déterminer si ce workload est over-provisioned ou zombie
            is_over_provisioned = random.random() < self.config['usage_metrics']['anomalies']['over_provisioned_percentage']
            is_zombie = random.random() < self.config['usage_metrics']['anomalies']['zombie_percentage']
            
            # Générer des métriques quotidiennes
            current_date = self.start_date
            while current_date <= self.end_date:
                # Déterminer si c'est un jour ouvré
                is_weekday = current_date.weekday() < 5
                is_business_hours = True  # Simplifié pour quotidien
                
                # Base CPU/Memory selon profil
                if is_zombie:
                    cpu_base = random.uniform(5, 15)
                    memory_base = random.uniform(10, 25)
                elif is_over_provisioned:
                    cpu_base = random.uniform(15, 35)
                    memory_base = random.uniform(20, 45)
                else:
                    if is_weekday:
                        cpu_base = random.uniform(*self.config['usage_metrics']['weekday_usage']['cpu_range'])
                        memory_base = random.uniform(*self.config['usage_metrics']['weekday_usage']['memory_range'])
                    else:
                        cpu_base = random.uniform(*self.config['usage_metrics']['weekend_usage']['cpu_range'])
                        memory_base = random.uniform(*self.config['usage_metrics']['weekend_usage']['memory_range'])
                
                # Appliquer tendance de croissance
                days_from_start = (current_date - self.start_date).days
                growth_factor = 1 + (days_from_start / 365) * self.config['usage_metrics']['growth_trend']['avg_monthly_growth'] * 12
                cpu_usage = min(100, cpu_base * growth_factor + random.gauss(0, 5))
                memory_usage = min(100, memory_base * growth_factor + random.gauss(0, 5))
                
                # Storage usage
                storage_provisioned = workload.storage_gb if workload.storage_gb else 1000
                storage_used = storage_provisioned * self.config['usage_metrics']['storage_usage_ratio'] * random.uniform(0.8, 1.2)
                storage_used = min(storage_provisioned, max(0, storage_used))
                
                # Query count (pour Fabric/SQL workloads)
                if workload.workload_type in ['fabric_capacity', 'azure_sql']:
                    query_count = int(cpu_usage * self.config['usage_metrics']['query_count_factor'] * random.uniform(0.5, 1.5))
                else:
                    query_count = 0
                
                # Data processed (pour Fabric principalement)
                if workload.workload_type == 'fabric_capacity':
                    data_processed_gb = cpu_usage / 100 * random.uniform(100, 5000)
                else:
                    data_processed_gb = 0
                
                # Spike aléatoire
                if random.random() < self.config['usage_metrics']['anomalies']['spike_probability']:
                    cpu_usage = min(100, cpu_usage * random.uniform(1.5, 2.5))
                    memory_usage = min(100, memory_usage * random.uniform(1.3, 2.0))
                
                metric = {
                    'workload_id': workload.workload_id,
                    'date': current_date.strftime(self.config['output']['date_format']),
                    'cpu_usage_percent': round(max(0, cpu_usage), 2),
                    'memory_usage_percent': round(max(0, memory_usage), 2),
                    'storage_used_gb': round(storage_used, 2),
                    'storage_provisioned_gb': storage_provisioned,
                    'query_count': query_count,
                    'data_processed_gb': round(data_processed_gb, 2),
                    'active_users': random.randint(0, 100) if workload.status == 'running' else 0
                }
                metrics.append(metric)
                
                current_date += timedelta(days=1)
        
        df = pd.DataFrame(metrics)
        print(f"  ✓ {len(df)} metrics générées")
        return df
    
    def generate_cloud_costs(self, workloads_df: pd.DataFrame, usage_metrics_df: pd.DataFrame, 
                            environments_df: pd.DataFrame) -> pd.DataFrame:
        """Génère la table cloud_costs."""
        print("\n💰 Génération des cloud costs...")
        costs = []
        
        # Identifier les workloads qui vont avoir le spike de janvier
        spike_workloads = set(random.sample(
            list(workloads_df['workload_id']), 
            k=self.config['cloud_costs']['cost_drift']['spike_workloads_count']
        ))
        
        # Pour chaque ligne de usage_metrics, calculer le coût
        for metric in usage_metrics_df.itertuples():
            workload = workloads_df[workloads_df['workload_id'] == metric.workload_id].iloc[0]
            environment = environments_df[environments_df['environment_id'] == workload['environment_id']].iloc[0]
            
            # Coût de base selon le type
            if workload['workload_type'] == 'fabric_capacity':
                daily_cost = workload['capacity_units'] * self.config['cloud_costs']['pricing']['fabric_cu_per_day']
            elif workload['workload_type'] == 'azure_vm':
                hourly_cost = workload['vcpu_count'] * self.config['cloud_costs']['pricing']['vm_vcpu_per_hour']
                daily_cost = hourly_cost * 24
            elif workload['workload_type'] == 'azure_storage':
                monthly_cost = metric.storage_provisioned_gb * self.config['cloud_costs']['pricing']['storage_gb_per_month']
                daily_cost = monthly_cost / 30
            elif workload['workload_type'] == 'azure_sql':
                daily_cost = self.config['cloud_costs']['pricing']['sql_base_per_day']
            elif workload['workload_type'] == 'azure_functions':
                daily_cost = metric.query_count / 1_000_000 * self.config['cloud_costs']['pricing']['functions_per_million']
            else:
                daily_cost = 10  # Default
            
            # Appliquer multiplicateurs d'environnement
            env_multiplier = self.config['cloud_costs']['environment_cost_multiplier'].get(
                environment['environment_type'], 1.0
            )
            daily_cost *= env_multiplier
            
            # Appliquer croissance organique
            metric_date = datetime.strptime(metric.date, self.config['output']['date_format'])
            months_from_start = (metric_date.year - self.start_date.year) * 12 + (metric_date.month - self.start_date.month)
            growth_factor = (1 + self.config['cloud_costs']['cost_drift']['baseline_growth']) ** months_from_start
            daily_cost *= growth_factor
            
            # Appliquer spike de janvier 2026 si applicable
            if metric_date.year == 2026 and metric_date.month == 1 and metric.workload_id in spike_workloads:
                daily_cost *= (1 + self.config['cloud_costs']['cost_drift']['january_2026_spike'])
            
            # Ajouter variabilité basée sur usage
            usage_factor = 0.7 + (metric.cpu_usage_percent / 100) * 0.3
            daily_cost *= usage_factor
            
            cost = {
                'workload_id': metric.workload_id,
                'date': metric.date,
                'compute_cost_usd': round(daily_cost * 0.7, 2),  # 70% compute
                'storage_cost_usd': round(daily_cost * 0.25, 2),  # 25% storage
                'network_cost_usd': round(daily_cost * 0.05, 2),  # 5% network
                'total_cost_usd': round(daily_cost, 2),
                'currency': 'USD',
                'billing_period': metric_date.strftime('%Y-%m')
            }
            costs.append(cost)
        
        df = pd.DataFrame(costs)
        print(f"  ✓ {len(df)} cost records générés")
        return df
    
    def generate_business_units(self) -> pd.DataFrame:
        """Génère la table business_units."""
        print("\n🏢 Génération des business units...")
        business_units = []
        
        for bu in self.config['business_units']['units']:
            business_unit = {
                'business_unit_id': bu['code'],
                'business_unit_name': bu['name'],
                'budget_monthly_usd': bu['budget_monthly_usd'],
                'head_of_unit': self.fake.name()
            }
            business_units.append(business_unit)
        
        df = pd.DataFrame(business_units)
        print(f"  ✓ {len(df)} business units générées")
        return df
    
    def generate_teams(self, business_units_df: pd.DataFrame) -> pd.DataFrame:
        """Génère la table teams."""
        print("\n👥 Génération des teams...")
        teams = []
        team_id = 1
        
        for bu in business_units_df.itertuples():
            bu_config = next(b for b in self.config['business_units']['units'] if b['code'] == bu.business_unit_id)
            team_count = bu_config['team_count']
            
            for i in range(team_count):
                team = {
                    'team_id': f'TEAM_{team_id:03d}',
                    'team_name': f"{bu.business_unit_name} {random.choice(['Analytics', 'Operations', 'Platform', 'Engineering', 'Data', 'Digital', 'Innovation'])} Team",
                    'business_unit_id': bu.business_unit_id,
                    'team_size': random.randint(*self.config['teams']['size_range']),
                    'budget_monthly_usd': random.randint(*self.config['teams']['budget_range'])
                }
                teams.append(team)
                team_id += 1
        
        df = pd.DataFrame(teams)
        print(f"  ✓ {len(df)} teams générées")
        return df
    
    def generate_applications(self, teams_df: pd.DataFrame, workloads_df: pd.DataFrame) -> pd.DataFrame:
        """Génère la table applications."""
        print("\n📱 Génération des applications...")
        applications = []
        app_id = 1
        
        # Créer un mapping workload -> app (certains workloads peuvent ne pas être mappés)
        available_workloads = list(workloads_df['workload_id'])
        random.shuffle(available_workloads)
        workload_idx = 0
        
        for team in teams_df.itertuples():
            apps_count = self.config['teams']['applications_per_team']
            
            for i in range(apps_count):
                # Assigner 1-3 workloads à cette app
                num_workloads = random.randint(*self.config['applications']['workloads_per_app_range'])
                app_workloads = []
                for _ in range(num_workloads):
                    if workload_idx < len(available_workloads):
                        app_workloads.append(available_workloads[workload_idx])
                        workload_idx += 1
                
                app_type = random.choice(self.config['applications']['types'])
                
                application = {
                    'application_id': f'APP_{app_id:06d}',
                    'application_name': f"{app_type} - {self.fake.company()}",
                    'team_id': team.team_id,
                    'application_type': app_type,
                    'active_users': random.randint(*self.config['applications']['active_users_range']),
                    'workload_ids': ','.join(app_workloads)  # Liste séparée par virgules
                }
                applications.append(application)
                app_id += 1
        
        df = pd.DataFrame(applications)
        print(f"  ✓ {len(df)} applications générées")
        return df
    
    def save_csv(self, df: pd.DataFrame, filename: str):
        """Sauvegarde un DataFrame en CSV."""
        filepath = self.output_dir / filename
        df.to_csv(
            filepath,
            index=False,
            encoding=self.config['output']['encoding'],
            sep=self.config['output']['separator']
        )
        print(f"  💾 {filename} sauvegardé ({len(df)} lignes)")
    
    def generate_all(self):
        """Génère toutes les données."""
        print("=" * 60)
        print("🚀 GÉNÉRATION DES DONNÉES IT OPS & FINOPS")
        print("=" * 60)
        
        # 1. Infrastructure
        subscriptions_df = self.generate_subscriptions()
        self.save_csv(subscriptions_df, 'subscriptions.csv')
        
        environments_df = self.generate_environments(subscriptions_df)
        self.save_csv(environments_df, 'environments.csv')
        
        workloads_df = self.generate_workloads(environments_df)
        self.save_csv(workloads_df, 'workloads.csv')
        
        # 2. Usage & Costs
        usage_metrics_df = self.generate_usage_metrics(workloads_df)
        self.save_csv(usage_metrics_df, 'usage_metrics.csv')
        
        cloud_costs_df = self.generate_cloud_costs(workloads_df, usage_metrics_df, environments_df)
        self.save_csv(cloud_costs_df, 'cloud_costs.csv')
        
        # 3. Business Mapping
        business_units_df = self.generate_business_units()
        self.save_csv(business_units_df, 'business_units.csv')
        
        teams_df = self.generate_teams(business_units_df)
        self.save_csv(teams_df, 'teams.csv')
        
        applications_df = self.generate_applications(teams_df, workloads_df)
        self.save_csv(applications_df, 'applications.csv')
        
        print("\n" + "=" * 60)
        print("✅ GÉNÉRATION TERMINÉE")
        print("=" * 60)
        print(f"\n📊 Résumé:")
        print(f"  • Subscriptions: {len(subscriptions_df)}")
        print(f"  • Environments: {len(environments_df)}")
        print(f"  • Workloads: {len(workloads_df)}")
        print(f"  • Usage Metrics: {len(usage_metrics_df)}")
        print(f"  • Cloud Costs: {len(cloud_costs_df)}")
        print(f"  • Business Units: {len(business_units_df)}")
        print(f"  • Teams: {len(teams_df)}")
        print(f"  • Applications: {len(applications_df)}")
        print(f"\n📁 Fichiers générés dans: {self.output_dir}")
        print("\n🎯 Prochaine étape: python validate_schema.py")


def main():
    """Point d'entrée principal."""
    try:
        generator = FinOpsDataGenerator(CONFIG_FILE)
        generator.generate_all()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
