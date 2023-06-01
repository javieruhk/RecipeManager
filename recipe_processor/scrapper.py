import requests
from bs4 import BeautifulSoup

#RG --> Recetas Gratis
#AR --> AllRecipes

def get_RG_recipes_links():
    word_list = ["cómo","jugos", "postres", "mejores", "bebidas", "tipos", "licuados", "guisados", "recetas", "botanas", "batidos", "guarniciones", "panes"]
    
    page = requests.get(
        "https://www.recetasgratis.net/")
    soup = BeautifulSoup(page.content, 'html.parser')
    
    link_list = []
    
    bloquegroups = soup.body.find_all("div", class_="bloquegroup clear padding-left-1")
    for bloquegroup in bloquegroups:
        a = bloquegroup.select("div.bloque > a")
        etiquetas = bloquegroup.select("div.bloque > div.position-imagen > div.categoria > div.wrap > div.etiqueta")
    
        for href_n in range(len(a)):
            etiqueta = etiquetas[href_n].text
            if etiqueta != "Consejos de cocina":
                forbidden_word = False
                title = a[href_n].text.lower()
                for word in word_list:
                    if word in title:
                       forbidden_word = True
                       break
                if not forbidden_word:
                    link_list.append(a[href_n]["href"])
    return link_list

def get_RG_recipe_name(soup):
    title = soup.body.find_all("h1", class_="titulo titulo--articulo")[0].text.strip()
    title_formatted = title.replace(" ", "_")
    return title_formatted

def get_RG_ingredient_list(soup):
    ingredient_list = []
    ingredients = soup.body.find_all("li", class_="ingrediente")
    for ingredient in ingredients:
        if len(ingredient["class"]) == 1:
            ingredient_name = ingredient.select("label")[0].text.strip()
            ingredient_list.append(ingredient_name)
    return ingredient_list

def get_RG_step_list(soup):
    step_list = []
    step_section = soup.body.find_all("div", class_="apartado")
    for section in step_section:
        if section.select("div.orden") != []:
            paragraph = section.select("p")[0].text
            step_list.append(paragraph)
    return step_list


def get_AR_recipes_links():
    page = requests.get(
        "https://www.allrecipes.com/recipes-a-z-6735880")
    soup = BeautifulSoup(page.content, 'html.parser')
    
    
    alphabetical_groups = soup.body.find_all("div", class_="alphabetical-list__group")
    
    link_list = []
    
    for alphabetical_letter in alphabetical_groups:
        links = alphabetical_letter.select("ul.loc > li.comp > a.link-list__link")
        
        for link in links:
            link_list.append(link["href"])
    
    #--------------------------------------------------------------
    page = requests.get(link_list[0])
    soup = BeautifulSoup(page.content, 'html.parser')
    
    section = soup.body.find_all("section", class_="comp mntl-document-spotlight three-post mntl-block")[0]
    
    a_list = section.find_all("a", class_="comp card--image-top mntl-card-list-items mntl-document-card mntl-card card card--no-image")
    
    link_list = []
    for a in a_list:
        category = a.select("div.card__content")[0]["data-tag"]
        if category != "In the Kitchen" and category != "Product Reviews and Buying Guides":
            link_list.append(a["href"])
    
    a_list = soup.body.find_all("a", class_="comp mntl-card-list-items mntl-document-card mntl-card card card--no-image")
    
    for a in a_list:
        category = a.select("div.card__content")[0]["data-tag"]
        if category != "In the Kitchen" and category != "Product Reviews and Buying Guides":
            link_list.append(a["href"])
    
    return link_list

def get_AR_recipe_name(soup):
    title = soup.body.find_all("h1", class_="comp type--lion article-heading mntl-text-block")[0].text.strip()
    return title

def get_AR_ingredient_list(soup):
    ingredients_list = soup.body.find_all("li", class_="mntl-structured-ingredients__list-item")
    
    ingredients_names_list = []
    for ingredient in ingredients_list:
        ingredient_name = ingredient.select("p")[0].text.strip()
        ingredients_names_list.append(ingredient_name)
    return ingredients_names_list

def get_AR_step_list(soup):
    steps = soup.body.find_all("p", class_="comp mntl-sc-block mntl-sc-block-html")
    
    step_list = []
    
    for step in steps:
        step_text = step.text.strip()
        step_list.append(step_text)
    return step_list