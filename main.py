from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random
from typing import Dict

class Palpite(BaseModel):
    palpite: int

app = FastAPI()

# Configuração do CORS:
origins = [
    "http://localhost",
    "http://localhost:3000",  # Permite requisições do seu front-end Next.js
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

numero_secreto = random.randint(1, 100)

@app.get("/")
def read_root():
    return {"message: " "Bem-vindo á 6AM2S sua plataforma de jogos in browser!"}

@app.post("/guess")
def process_guess(data: Palpite) -> Dict:
    if data.palpite > numero_secreto:
        return {"mensagem": f"ERROU! O número secreto é MENOR que {data.palpite}"}
    elif data.palpite < numero_secreto:
        return {"mensagem": f"ERROU! O número secreto é MAIOR que {data.palpite}"}
    else:
        return {"mensagem": f"Parabéns! Você acertou!"}