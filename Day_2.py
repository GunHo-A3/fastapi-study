from fastapi import FastAPI

app = FastAPI()

@app.get("/")

def root():
    return {"message": "super gunho"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message":f"Hello, {name}!"}

@app.get("/square/{number}")
def square_number(number: int):
    return {"result": number**2}