import pymongo
import streamlit as st


def filter_products(products, name_filter=None, min_price=None, max_price=None):
    filtered_products = []
    for product in products:
        name = product['name']
        price = float(product['price'].replace('€', '').replace(',', '.'))
        if (not name_filter or name_filter.lower() in name.lower()) and \
                (not min_price or price >= min_price) and \
                (not max_price or price <= max_price):
            filtered_products.append({'Nom': name, 'Prix': product['price']})
    return filtered_products


client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['products']
collection = db['scraper']

data = []
for product in collection.find():
    data.append(product)

st.sidebar.header('Filtrer les produits')
filtre_nom = st.sidebar.text_input('Nom')
filtre_prix_min = st.sidebar.number_input('Prix minimum', value=0)
filtre_prix_max = st.sidebar.number_input('Prix maximum', value=1000)

resultats_filtrage = filter_products(data, filtre_nom, filtre_prix_min, filtre_prix_max)

if resultats_filtrage:
    st.write('Résultats du filtrage')
    st.table(resultats_filtrage)
else:
    st.write('Aucun produit ne correspond aux critères de filtrage.')
