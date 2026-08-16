#comments incase i need to refresh my memory of what i did 

# Import the FastAPI class from the library to define routes and handle HTTP requests.
from fastapi import FastAPI
from fastapi.responses import JSONResponse

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