from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="DevOps To-Do WebApp")

# HTML und CSS Ordner in FastAPI registrieren
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class TodoItem(BaseModel):
    id: Optional[int] = None
    titel: str
    erledigt: bool = False

todo_db: List[TodoItem] = []
id_counter = 1

# 1. Hauptseite liefert jetzt das HTML Template aus
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "todos": todo_db})

# 2. Neues To-Do über das HTML-Formular hinzufügen
@app.post("/add")
def add_todo(titel: str = Form(...)):
    global id_counter
    item = TodoItem(id=id_counter, titel=titel)
    todo_db.append(item)
    id_counter += 1
    return RedirectResponse(url="/", status_code=303)

# 3. To-Do über die Weboberfläche löschen
@app.post("/delete/{todo_id}")
def delete_todo(todo_id: int):
    global todo_db
    todo_db = [item for item in todo_db if item.id != todo_id]
    return RedirectResponse(url="/", status_code=303)
