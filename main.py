from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import BEDCA_foodex2_matcher

#BEDCA_dict = BEDCA_foodex2_matcher.create_BEDCA_dict(BEDCA_foodex2_matcher.BEDCA_file)
#foodex2_dict = BEDCA_foodex2_matcher.create_foodex2_dict(BEDCA_foodex2_matcher.foodex2_file)
#foodex2_dict_lemmatized = BEDCA_foodex2_matcher.lemmatize_dict(foodex2_dict)
#foodex2_facet_dict = BEDCA_foodex2_matcher.create_foodex2_facet_dict(BEDCA_foodex2_matcher.foodex2_file)

app = FastAPI()

app.mount("/static", StaticFiles(directory="./public/static"), name="static")

templates = Jinja2Templates(directory="./public/templates")

#uvicorn main:app --reload
#http://127.0.0.1:8000/

"""
@app.get("/BEDCA_food/{code}")
async def read_item(code: int, BEDCA_name: str = Query()):
    print(BEDCA_name)
    web_service_BEDCA_food = BEDCA_foodex2_matcher.create_web_service_BEDCA_food(BEDCA_name)
    print(web_service_BEDCA_food)
    return web_service_BEDCA_food


@app.get("/BEDCA_food/name_coincidences/{food_name}")
async def read_item(food_name: int, BEDCA_name: str = Query()):
    print(BEDCA_name)
    web_service_BEDCA_food = BEDCA_foodex2_matcher.create_web_service_BEDCA_food(BEDCA_name)
    print(web_service_BEDCA_food)
    return web_service_BEDCA_food

@app.get("/", response_class=HTMLResponse)
def root():
    html_adress = "./public/static/html/index.html"
    return FileResponse(html_adress, status_code=200)
"""


@app.get("/search", response_class=HTMLResponse)
def search_food_name(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})


@app.get("/coincidences", response_class=HTMLResponse)
def get_coincidences(request: Request, busqueda: str):
    search_dict = BEDCA_foodex2_matcher.create_search_coincidences_dict(busqueda)
    return templates.TemplateResponse("coincidence.html", {"request": request, "busqueda": search_dict})   


@app.get("/food_information", response_class=HTMLResponse)
def get_food_information(request: Request, food_name_code: int):
    print(food_name_code)
    web_service_BEDCA_food = BEDCA_foodex2_matcher.create_web_service_BEDCA_food(food_name_code)
    return templates.TemplateResponse("food_details.html", {"request": request, "food_information": web_service_BEDCA_food})   
