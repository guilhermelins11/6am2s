"use client";

import { useState } from 'react';

export default function HomePage() {
  const [palpite, setPalpite] = useState('');
  const [mensagem, setMensagem] = useState('Digite seu palpite!');

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    try {
      const response = await fetch('http://127.0.0.1:8000/guess', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', 
        },
        body: JSON.stringify({ palpite: palpite }),
      });
      
      const data = await response.json();

      setMensagem(data.mensagem);
      
    } catch (error) {
      setMensagem('Erro: Não foi possível conectar ao servidor.');
    }

    setPalpite('');
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <div className="bg-white p-8 rounded-lg shadow-lg max-w-sm w-full">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-6">Jogo da Adivinhação</h1>
        <p className="text-center text-gray-600 mb-4">{mensagem}</p>
        <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
          <input
            type="number"
            value={palpite}
            onChange={(e) => setPalpite(e.target.value)}
            className="p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Seu palpite"
            required
          />
          <button
            type="submit"
            className="bg-blue-500 text-white font-bold py-3 rounded-lg hover:bg-blue-600 transition-colors"
          >
            Adivinhar
          </button>
        </form>
      </div>
    </div>
  );
}