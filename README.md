# Odoo 17 - Gestionnaire de règles de réapprovisionnement

Ce POC (Proof of Concept) permet de gérer les règles de réapprovisionnement (quantités min/max) pour plusieurs sociétés et entrepôts dans Odoo 17 via l'API.

## Fonctionnalités

- Connexion sécurisée à Odoo via HTTPS
- Support multi-société
- Support multi-entrepôt
- Gestion flexible des produits :
  - Traitement de tous les produits stockables
  - Traitement d'un produit spécifique
  - Traitement d'une liste de produits
- Création ou mise à jour des règles de réapprovisionnement
- Gestion des emplacements de stock (location_id)

## Prérequis

- Python 3.x
- Accès à une instance Odoo 17
- Droits d'accès suffisants pour gérer les règles de réapprovisionnement

## Installation

1. Cloner le dépôt :
```bash
git clone [url-du-repo]
cd [nom-du-repo]
```

2. Créer un environnement virtuel Python :
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Installer les dépendances :
```bash
pip install odoorpc
```

4. Configurer l'application :
```bash
cp config.py.example config.py
```
Puis modifiez config.py avec vos paramètres :
- Informations de connexion Odoo
- Liste des sociétés
- Liste des entrepôts
- IDs des produits (optionnel)

## Configuration

### Configuration de la connexion (config.py)

```python
ODOO_HOST = 'your-database.odoo.com'
ODOO_PORT = 443
ODOO_DB = 'your-database'
ODOO_USER = 'user@example.com'
ODOO_PASSWORD = 'your-password'
```

### Configuration des produits

Trois modes possibles :

1. Tous les produits stockables :
```python
PRODUCT_IDS = None
```

2. Un seul produit :
```python
PRODUCT_IDS = [123]  # Remplacer 123 par l'ID du produit
```

3. Liste de produits spécifiques :
```python
PRODUCT_IDS = [123, 456, 789]  # Remplacer par vos IDs
```

### Configuration des sociétés et entrepôts

```python
COMPANIES = [
    {'id': 1, 'name': 'Société principale'},
    {'id': 2, 'name': 'Société secondaire'},
]

WAREHOUSES = [
    {
        'id': 1,
        'name': 'Entrepôt principal',
        'location_id': 1,
    },
    {
        'id': 2,
        'name': 'Entrepôt secondaire',
        'location_id': 2,
    },
]
```

## Utilisation

1. Activer l'environnement virtuel :
```bash
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

2. Exécuter le script :
```bash
python update_min_max.py
```

Le script affichera :
- ✅ Les opérations réussies
- ❌ Les erreurs éventuelles
- 📦 Le traitement par société
- 🏭 Le traitement par entrepôt
- 📝 La liste des produits traités

## Personnalisation

Dans update_min_max.py, vous pouvez personnaliser la logique de calcul des quantités min/max :

```python
min_qty = 10  # Personnalisez selon vos besoins
max_qty = 100  # Personnalisez selon vos besoins
```

Par exemple, vous pourriez baser ces valeurs sur :
- L'historique des ventes
- Les délais fournisseurs
- La saisonnalité
- Le type de produit
- etc.

## Sécurité

- Les informations de connexion sont stockées dans config.py (non versionné)
- Utilisation de HTTPS pour la connexion à Odoo
- Gestion des exceptions pour éviter les erreurs silencieuses

## Support

Pour toute question ou problème, merci d'ouvrir une issue sur GitHub.
