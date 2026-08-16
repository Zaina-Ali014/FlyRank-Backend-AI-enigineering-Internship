#comments incase i need to refresh my memory of what i did 

# Import the FastAPI class from the library to define routes and handle HTTP requests.
from fastapi import FastAPI

# Creating the main server application. All endpoints will attach to 'app'.
app = FastAPI()

#-----------------------------------
# Stage 1: root and health endpoint
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