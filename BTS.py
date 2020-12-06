import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import html
import wget


# Fonction permettant de trouver l'URL de la page suivante
def next_absolute_url():
    scrape_next = scraping_bookcategory.find("li", {"class": "next"})
    if scrape_next:
        next_url = scrape_next.a.get('href')
        absolute_url = absolute_url_bookcategory[:-10] + next_url
        repertoire_url_bookcategory.append(absolute_url)
    else:
        pass

# Requête pour le site booksToScrap
requeteBooksToScrape = requests.get("https://books.toscrape.com/index.html")
scrapingBooksToScrape = BeautifulSoup(requeteBooksToScrape.text, "html.parser")

# Récupérer l'URL de la catégorie book qui répertorie tout les livres
all_book_category_url = scrapingBooksToScrape.find("ul", {"class": "nav nav-list"}).find_all("a")[0]
category_link = all_book_category_url["href"]

# Requête et le scrape de la première page
absolute_url_bookcategory = "https://books.toscrape.com/" + category_link
repertoire_url_bookcategory = [absolute_url_bookcategory]

# Liste pour stocker l'ensemble des url de la catégorie book
repertoire_url_books = []

# Liste pour stocker les requêtes de chaque URL de livre
texte_requete_book = []

# Boucle permettant de récupérer les requêtes pour les livres
for url in repertoire_url_bookcategory:
    # Requête et scrape de la page
    requete_bookcategory = requests.get(repertoire_url_bookcategory[-1])
    scraping_bookcategory = BeautifulSoup(requete_bookcategory.text, "html.parser")

    for book in scraping_bookcategory.find_all(attrs={'class': 'product_pod'}):
        # Récupérer l'URL de chaque livre
        book_link = book.a.get("href")
        absolute_url_book = "https://books.toscrape.com/catalogue/" + book_link[6:]
        # Créer une requête pour chaque livre
        requete_book = requests.get(absolute_url_book)
        # Ajouter la requête à texte_requete_book
        texte_requete_book.append(requete_book)

    next_absolute_url()

# Dataframe = ensemble des données de chaque livre
df_books = pd.DataFrame()

# Boucle permettant de récupérer l'ensemble des données sous forme d'un dataframe
for requete_book in texte_requete_book:
    scraping_book = BeautifulSoup(requete_book.text, "html.parser")
    html_string_book = html.fromstring(requete_book.content)
    # Dataframe = ensemble des données des livres de la page scrapée
    df_book = pd.DataFrame({'URL': [requete_book.url],
                            'Title': [scraping_book.h1.text],
                            'UPC': [scraping_book.find_all("td")[0].text],
                            'Price_Including_Tax': [scraping_book.find_all("td")[3].text[2:]],
                            'Price_Excluding_Tax': [scraping_book.find_all("td")[2].text[2:]],
                            'Number_Available': [scraping_book.find_all("td")[5].text[10:12]],
                            'Product_Description': [
                                html_string_book.xpath("/html/body/div/div/div[2]/div[2]/article/p/text()")],
                            'Category': [html_string_book.xpath("/html/body/div/div/ul/li[3]/a/text()")],
                            'Rating': [scraping_book.find("p", {"class": "star-rating"}).get("class")[1]],
                            'Image_URL': ["https://books.toscrape.com/" + scraping_book.img.get("src")[6:]]})
    # Ajout des données récupérées au dataframe global
    df_books = pd.concat([df_books, df_book])

# Création d'un fichier csv répertoriant les 1000 livres
df_books.to_csv('books.csv')

# Boucle permettant de diviser ce fichier par catégorie
df = pd.read_csv("books.csv", index_col='Unnamed: 0')
for categoryName in df.Category.value_counts().index:
    df[df.Category == categoryName].to_csv("book" + categoryName[2:-2] + ".csv")

# Boucle permettant de télécharger la couverture des livres
compteur = 0
for URL in df.Image_URL:
    wget.download(URL, df.UPC.values[compteur] + ".jpeg")
    compteur = compteur + 1

