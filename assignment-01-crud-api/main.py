#comments incase i need to refresh my memory of what i did 

# Import the FastAPI class from the library to define routes and handle HTTP requests.
from fastapi import FastAPI

# Creating the main server application. All endpoints will attach to 'app'.
app = FastAPI()


# Setting up a listener for GET requests sent to the home path ("/").
# When a user visits "http://localhost:8000/", FastAPI runs the function below.
@app.get("/")
def read_root():
    # Returns a Python dictionary. FastAPI automatically turns this into JSON text.
    return {"message": "Hello World"}