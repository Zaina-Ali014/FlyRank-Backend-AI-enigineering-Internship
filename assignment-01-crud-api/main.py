#comments incase i need to refresh my memory of what i did 

from fastapi import FastAPI # Import the FastAPI class from the library to define routes and handle HTTP requests.

from fastapi.responses import JSONResponse

from fastapi import status # For status codes
from pydantic import BaseModel # Import BaseModel from pydantic to define input data schemas/validation.

# Creating the main server application. All endpoints will attach to 'app'.
app = FastAPI()

# In-memory "database" storing initial task dictionaries.
# Note: Since this is stored in memory, modifications reset whenever the server restarts.
tasks_db = [
    {
        "id": 1,
        "title": "Make dinner",
        "description": "Prepare dinner for the evening",
        "completed": True,
    },
    {
        "id": 2,
        "title": "Complete FlyRank assignment 1",
        "description": "Finish and submit CRUD API assignment",
        "completed": False,
    },
    {
        "id": 3,
        "title": "Complete assignment 2",
        "description": "Finish and submit assignment 2",
        "completed": False,
    },
]

#-----------------------------------
# Stage 1: root and health endpoints
#-----------------------------------

# Returns metadata about our API (name, version, available endpoints)
@app.get("/")
def read_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }

# Used by monitoring systems and cloud platforms to verify the server is running
@app.get("/health")
def health_check():
    return {"status": "ok"}

#-----------------------------------
# Stage 2: read endpoints with 404
#-----------------------------------

# Returns the list of all tasks stored in tasks_db.
@app.get("/tasks")
def get_tasks():
    return tasks_db

# Searches tasks_db for a task matching task id
# FastAPI maps {id} in the route decorator directly to the function parameter 'id: int'.
@app.get("/tasks/{id}")
def get_task(id: int):
    # Loop through each dictionary inside tasks_db
    for task in tasks_db:
        if task["id"] == id: # if id found returns
            return task 

    # If not found, return custom 404 JSON response matching assignment requirements:
    # {"error": "Task <id> not found"}
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {id} not found"}
    )

#-----------------------------------
# Stage 3: create with validation
#-----------------------------------

class TaskCreate(BaseModel):
    title: str = ""
    description: str = ""
    completed: bool = False # becz when creating a task it is False

# status_code=status.HTTP_201_CREATED tells FastAPI to return HTTP 201 when creation succeeds
@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_input: TaskCreate):
    if not task_input.title or task_input.title.strip() == "":
        return JSONResponse(
            status_code=400, # else stays 201
            content={"error": "Title is required and cannot be empty"}
        )
    
    # Create a new unique ID (max existing ID + 1, or 1 if database is empty)
    new_id = max([task["id"] for task in tasks_db], default=0) + 1

    # Convert Pydantic model to a standard Python dictionary and add the generated ID
    # TaskCreate(title="Study", description="...", completed=False) to dictionary form
    new_task = task_input.model_dump()
    new_task["id"] = new_id

    # Add the new task to our in-memory database list
    tasks_db.append(new_task)

    # Return the created task dictionary
    return new_task