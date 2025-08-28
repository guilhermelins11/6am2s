from fastapi import FastAPI, HTTPException
from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel
app = FastAPI()

class User(BaseModel):
    id: UUID
    name: str
    email: str

class Post(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    content: str

db_users: List[User] = []
db_posts: List[Post] = []

def seed_database():
    user1 = User(id=uuid4(), name="Alice", email="alice@example.com")
    user2 = User(id=uuid4(), name="Bob", email="bob@example.com")
    db_users.append(user1)
    db_users.append(user2)

    post1 = Post(id=uuid4(), user_id=user1.id, title="Meu Primeiro Post", content="Olá, mundo!")
    post2 = Post(id=uuid4(), user_id=user2.id, title="Post do Bob", content="Este é um post de teste.")
    db_posts.append(post1)
    db_posts.append(post2)

seed_database()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à plataforma de blog simples!"}

@app.get("/users", response_model=List[User])
def get_all_users():
    return db_users

@app.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: UUID):
    for user in db_users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.post("/users", response_model=User)
def create_user(user: User):
    db_users.append(user)
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: UUID):
    user_to_delete = None
    for user in db_users:
        if user.id == user_id:
            user_to_delete = user
            break
    if user_to_delete:
        db_users.remove(user_to_delete)
        return {"message": "Usuário deletado com sucesso."}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.get("/posts", response_model=List[Post])
def get_all_posts():
    return db_posts

@app.get("/posts/{post_id}", response_model=Post)
def get_post_by_id(post_id: UUID):
    for post in db_posts:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post não encontrado")

@app.post("/posts", response_model=Post)
def create_post(post: Post):
    user_exists = any(user.id == post.user_id for user in db_users)
    if not user_exists:
        raise HTTPException(status_code=400, detail="O user_id fornecido não existe.")
    db_posts.append(post)
    return post

@app.put("/posts/{post_id}", response_model=Post)
def update_post(post_id: UUID, post_update: Post):

    for index, post in enumerate(db_posts):
        if post.id == post_id:
            db_posts[index] = post_update
            return post_update
    raise HTTPException(status_code=404, detail="Post não encontrado")

@app.delete("/posts/{post_id}")
def delete_post(post_id: UUID):
    post_to_delete = None
    for post in db_posts:
        if post.id == post_id:
            post_to_delete = post
            break
    if post_to_delete:
        db_posts.remove(post_to_delete)
        return {"message": "Post deletado com sucesso."}
    raise HTTPException(status_code=404, detail="Post não encontrado")

