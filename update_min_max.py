#!/usr/bin/env python3
import odoorpc
from config import *

def connect_odoo():
    """Établit la connexion avec Odoo"""
    try:
        odoo = odoorpc.ODOO(ODOO_HOST, port=ODOO_PORT, protocol='jsonrpc+ssl')
        odoo.login(ODOO_DB, ODOO_USER, ODOO_PASSWORD)
        print(f"✅ Connecté à Odoo {odoo.version}")
        return odoo
    except Exception as e:
        print(f"❌ Erreur de connexion: {str(e)}")
        return None

def update_orderpoint(odoo, company_id, warehouse, product_id, product_min, product_max):
    """Met à jour ou crée une règle de réapprovisionnement"""
    try:
        # Recherche d'une règle existante
        OrderPoint = odoo.env['stock.warehouse.orderpoint']
        existing_rule = OrderPoint.search([
            ('company_id', '=', company_id),
            ('warehouse_id', '=', warehouse['id']),
            ('product_id', '=', product_id)
        ])

        values = {
            'company_id': company_id,
            'warehouse_id': warehouse['id'],
            'product_id': product_id,
            'product_min_qty': product_min,
            'product_max_qty': product_max,
            'location_id': warehouse['location_id']
        }

        if existing_rule:
            # Mise à jour de la règle existante
            OrderPoint.write(existing_rule[0], values)
            print(f"✅ Règle mise à jour pour le produit {product_id}")
        else:
            # Création d'une nouvelle règle
            OrderPoint.create(values)
            print(f"✅ Nouvelle règle créée pour le produit {product_id}")

    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {str(e)}")

def get_products(odoo, company_id):
    """Récupère la liste des produits stockables pour une société donnée"""
    Product = odoo.env['product.product']
    domain = [
        ('type', '=', 'product'),
        ('company_id', 'in', [company_id, False])
    ]
    
    # Si des produits spécifiques sont configurés
    if PRODUCT_IDS is not None:
        domain.append(('id', 'in', PRODUCT_IDS))
    
    products = Product.search(domain)
    
    # Afficher les noms des produits traités
    if products:
        product_names = Product.browse(products).mapped('name')
        print("Produits à traiter :")
        for name in product_names:
            print(f"- {name}")
    
    return products

def main():
    odoo = connect_odoo()
    if not odoo:
        return

    # Pour chaque société
    for company in COMPANIES:
        print(f"\n📦 Traitement de la société: {company['name']}")
        
        # Récupération des produits de la société
        products = get_products(odoo, company['id'])
        print(f"📝 {len(products)} produits trouvés")
        
        # Pour chaque entrepôt
        for warehouse in WAREHOUSES:
            print(f"\n🏭 Traitement de l'entrepôt: {warehouse['name']}")

            # Pour chaque produit
            for product_id in products:
                try:
                    # Vous pouvez personnaliser la logique de calcul des min/max ici
                    # Par exemple, basé sur l'historique des ventes, les délais fournisseurs, etc.
                    min_qty = 10  # À adapter selon vos besoins
                    max_qty = 100  # À adapter selon vos besoins

                    update_orderpoint(
                        odoo,
                        company['id'],
                        warehouse,
                        product_id,
                        min_qty,
                        max_qty
                    )

                except Exception as e:
                    print(f"❌ Erreur pour le produit {product_id}: {str(e)}")

if __name__ == '__main__':
    main()
