from fastapi import FastAPI, HTTPException
from typing import List
from uuid import UUID, uuid4
from pydantic import BaseModel

# Cria a instância principal da aplicação FastAPI
app = FastAPI()

# --- Modelos de Dados (usando Pydantic) ---

# A classe `User` define a estrutura dos dados para cada usuário
class User(BaseModel):
    id: UUID
    name: str
    email: str

# A classe `Post` define a estrutura dos dados para cada post
class Post(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    content: str

# --- Banco de Dados em Memória (simulação) ---

# Listas que simulam um banco de dados
db_users: List[User] = []
db_posts: List[Post] = []

# Adiciona alguns dados de exemplo para começar
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

# --- Rotas da API ---

@app.get("/")
def read_root():
    """
    Rota raiz para verificar se a API está funcionando.
    """
    return {"message": "Bem-vindo à plataforma de blog simples!"}

# --- Operações de Usuário ---

@app.get("/users", response_model=List[User])
def get_all_users():
    """
    Retorna a lista de todos os usuários.
    """
    return db_users

@app.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: UUID):
    """
    Retorna um usuário específico pelo seu ID.
    Se o usuário não for encontrado, retorna um erro 404.
    """
    for user in db_users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

@app.post("/users", response_model=User)
def create_user(user: User):
    """
    Cria um novo usuário.
    """
    db_users.append(user)
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: UUID):
    """
    Deleta um usuário pelo seu ID.
    """
    user_to_delete = None
    for user in db_users:
        if user.id == user_id:
            user_to_delete = user
            break
    if user_to_delete:
        db_users.remove(user_to_delete)
        return {"message": "Usuário deletado com sucesso."}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

# --- Operações de Post ---

@app.get("/posts", response_model=List[Post])
def get_all_posts():
    """
    Retorna a lista de todos os posts.
    """
    return db_posts

@app.get("/posts/{post_id}", response_model=Post)
def get_post_by_id(post_id: UUID):
    """
    Retorna um post específico pelo seu ID.
    """
    for post in db_posts:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post não encontrado")

@app.post("/posts", response_model=Post)
def create_post(post: Post):
    """
    Cria um novo post.
    """
    # Verifica se o user_id do post existe
    user_exists = any(user.id == post.user_id for user in db_users)
    if not user_exists:
        raise HTTPException(status_code=400, detail="O user_id fornecido não existe.")

    db_posts.append(post)
    return post

@app.put("/posts/{post_id}", response_model=Post)
def update_post(post_id: UUID, post_update: Post):
    """
    Atualiza um post existente.
    """
    for index, post in enumerate(db_posts):
        if post.id == post_id:
            # Atualiza os dados do post
            db_posts[index] = post_update
            return post_update
    raise HTTPException(status_code=404, detail="Post não encontrado")

@app.delete("/posts/{post_id}")
def delete_post(post_id: UUID):
    """
    Deleta um post pelo seu ID.
    """
    post_to_delete = None
    for post in db_posts:
        if post.id == post_id:
            post_to_delete = post
            break
    if post_to_delete:
        db_posts.remove(post_to_delete)
        return {"message": "Post deletado com sucesso."}
    raise HTTPException(status_code=404, detail="Post não encontrado")

