from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Todo(BaseModel):
    title : str
    desc : str 
    status : str

class UpdateTodo(BaseModel):
    title : Optional[str]= None
    desc : Optional[str]= None
    status : Optional[str]= None

todos = {
    1: Todo(title = "Go Shopping", desc = "Get some milk, apple, and some cherries", status= "completed"),
    2: Todo(title = "Wash the car", desc = "Make sure it's spotless when you finish", status= "pending"),
    3: Todo(title = "Go walk the dog", desc = "Take him to a park and get him new friends", status= "completed")
}

#GET method (for display) --> To notify that the program is running
@app.get("/")
def index():
    return { "Hello!" : "This is an API for a to-do list creator."}

#GET method (By ID) --> Finding a specific task by ID
@app.get("/get-todo/{id}")
def get_todo(id : int = Path(description = "Search the ID of the reminder you want to search")):
    return todos[id]

#GET method (By title) --> Finding a specific task by the full title.
@app.get("/get-todo-by-title/{title}")
def get_todo_by_title(title: str):
    for todo_id in todos:
        if todos[todo_id].title == title:
            return todos[todo_id]
    return {"error" : "Planner doesn't exist."}

#GET method (By status) (Couldn't return multiple tasks, cancelled.)
# @app.get("/get-todo-by-status/{status}")
# def get_todo_by_status(status: str):
#    for todo_id in todos:
#        if todos[todo_id].status == status:
#            return todos[todo_id]
#    return {"error" : "Planner doesn't exist."}

#POST method --> Creating a new To-Do 
@app.post("/create-todo/{todo_id}")
def add_todo(todo_id: int, todo : Todo):
    if todo_id in todos:
        return {"error" : "You've got this on your planner"}
    todos[todo_id] = todo
    return todos[todo_id]

#PUT method --> Updating a To-Do
@app.put("/update-todo/{todo_id}")
def update_todo(todo_id: int, todo: UpdateTodo):
    if todo_id not in todos:
        return {"error" : "Planner hasn't been added"}

    if todo.title != None:
        todos[todo_id].title = todo.title
    if todo.desc != None:
        todos[todo_id].desc = todo.desc
    if todo.status != None:
        todos[todo_id].status = todo.status
        
    return todos[todo_id]

#DELETE method --> Deleting a To-Do
@app.delete("/delete-todo/{todo_id}")
def delete_todo(todo_id:int = Path(description = "Search the planner you want to delete")):
    if todo_id not in todos:
        return {"error" : "Planner doesn't exist."}
    del todos[todo_id]
    return {"data" : "Planner deleted successfully."}