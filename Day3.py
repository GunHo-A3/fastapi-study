from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello":"World"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return{"message":f"Hello, {name}"}

@app.get("/calc")
def calculate(a: int, b: int):
    return {"sum": a + b, "product": a * b}