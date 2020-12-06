# BTS 

## Descritption
BTS est un programme permettant d'extraire les données du site https://books.toscrape.com/   
et de les stocker au sein de fichiers csv.  
Les données extraites du site sont :   
 * URL,
 * Title,
 * UPC,
 * Price_Including_Tax,
 * Price_Excluding_Tax,
 * Number_Available,
 * Product_Description,
 * Category,
 * Rating,
 * Image_URL  

Les données extraites sont répertoriées dans le fichier books.csv.   
Par ailleurs, ces données sont également répertoriées dans des fichiers csv portant le nom de la catégorie auxquelles elles appartiennent.  

## Installation

Afin d'installer le programme : 
* Lancer l'invite de commande
* Cloner le repository
$ git clone https://github.com/MargueriteT/P2_Extraction_de_donnees.git  
* Se rendre dans le dossier contenant le fichier BTS.py  
$ cd path/to/the/file
* Créer un environnement virtuel grâce au fichier requirements.txt  
$ virtualenv venv  
$ pip install -r requirements.txt
* Activer l'environnement virtuel  
$ activate
* Retourner dans le dossier contenant le fichier BTS.py  
$ cd ..\..
* Exécuter le fichier BTS.py  
$ BTS.py  

## Langage utilisé  
Python  

## Amélioration
Améliorer la vitesse d'exécution

## Auteur  
Marguerite Teulon  
Programme réalisé dans le cadre du projet 2 du parcours Développeur d'application - Python Openclassrooms
