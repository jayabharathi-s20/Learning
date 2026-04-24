# FastAPI is a Python framework used to build APIs (Application Programming Interfaces) quickly and efficiently.

# To install fast api
    # pip install fastapi
    # pip install uvicorn

#To run --
    # uvicorn main:app --reload

from fastapi import FastAPI , HTTPException
from pydantic import BaseModel

app = FastAPI()

products = []

# GET home
@app.get("/")
def sample_func():
    return {"message": "Hello, FastAPI!"}

# GET all products
@app.get("/show-products")
def show_all_products():
    return products

# POST - add product
@app.post("/post-products")
def post_products(product: str):
    products.append(product)
    return {"message": "Product added successfully", "products": products}

# PUT - update product
@app.put("/products/{index}")
def update_product(index: int, product: str):
    products[index] = product
    return {"message": "updated", "products": products}

@app.delete("/products/{index}")
def delete_product(index: int):
    products.pop(index)
    return {"message": "deleted", "products": products}

#-------------------------------------------------------------------------

students = {}

class Student(BaseModel):
    name: str
    age: int

class StudentPatch(BaseModel):
    name: str | None = None
    age: int | None = None

@app.get("/")
def home():
    return {"message": "Student CRUD API"}

@app.get("/students")
def get_students():
    return students

@app.post("/students")
def create_student(id: int, student: Student):
    if id in students:
        raise HTTPException(status_code=400, detail="Student already exists")

    students[id] = student
    return {"message": "Student created", "students": students}


@app.put("/students/{id}")
def update_student(id: int, student: Student):
    if id not in students:
        raise HTTPException(status_code=404, detail="Student not found")

    students[id] = student
    return {"message": "Student fully updated", "students": students}

@app.patch("/students/{id}")
def patch_student(id: int, student: StudentPatch):
    if id not in students:
        raise HTTPException(status_code=404, detail="Student not found")

    if student.name is not None:
        students[id].name = student.name

    if student.age is not None:
        students[id].age = student.age

    return {"message": "Student partially updated", "students": students}


@app.delete("/students/{id}")
def delete_student(id: int):
    if id not in students:
        raise HTTPException(status_code=404, detail="Student not found")

    deleted = students.pop(id)
    return {"message": "Student deleted", "deleted": deleted, "students": students}

# raise means: “stop the program and throw an error”
# HTTPException is a FastAPI error type used to send proper HTTP error responses to the client.





