import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [productInfo, setProductInfo] = useState({
    name: '',
    category: '',
    features: '',
    price: ''
  });
  const [userInfo, setUserInfo] = useState({
    name: '',
    preferences: '',
    interests: ''
  });

  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api/v1';

  const generateContent = async () => {
    if (!userInfo.name || !productInfo.name) {
      alert('Por favor, preencha pelo menos o nome do usuário e do produto');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/content/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: 1, // Em uma aplicação real, isso viria de um sistema de autenticação
          product_info: {
            id: Date.now().toString(),
            name: productInfo.name,
            category: productInfo.category,
            features: productInfo.features.split(',').map(f => f.trim()),
            price: parseFloat(productInfo.price) || 0,
          },
          content_type: 'descricao',
          personalization_params: {
            purchase_history: [],
            audience_profile: {
              demographics: userInfo
            },
            behavioral_data: {},
            contextual_factors: {}
          }
        })
      });

      const data = await response.json();

      if (data.error) {
        alert(`Erro: ${data.error}`);
      } else {
        setContent(data.content);
        // Atualiza o histórico (simulado)
        setHistory(prev => [...prev, {
          id: Date.now(),
          content: data.content.substring(0, 100) + '...',
          timestamp: new Date().toLocaleString(),
          type: data.personalization_factors?.content_type || 'descricao'
        }]);
      }
    } catch (error) {
      console.error('Erro ao gerar conteúdo:', error);
      alert('Erro ao gerar conteúdo. Verifique o console para detalhes.');
    } finally {
      setLoading(false);
    }
  };

  const loadHistory = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/content/history?user_id=1&limit=5`);
      const data = await response.json();

      if (data.history) {
        setHistory(data.history.map(item => ({
          id: item.id,
          content: item.generated_content.substring(0, 100) + '...',
          timestamp: new Date(item.created_at).toLocaleString(),
          type: item.content_type
        })));
      }
    } catch (error) {
      console.error('Erro ao carregar histórico:', error);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Hiperpersonalizador - Conteúdo Hiper-Personalizado</h1>
        <p>Gere conteúdo único para cada cliente com base em seu perfil individual</p>
      </header>

      <main className="main-content">
        <section className="input-section">
          <h2>Dados do Cliente</h2>
          <div className="form-group">
            <label>Nome do Cliente:</label>
            <input
              type="text"
              value={userInfo.name}
              onChange={(e) => setUserInfo({...userInfo, name: e.target.value})}
              placeholder="Ex: João Silva"
            />
          </div>

          <div className="form-group">
            <label>Preferências:</label>
            <input
              type="text"
              value={userInfo.preferences}
              onChange={(e) => setUserInfo({...userInfo, preferences: e.target.value})}
              placeholder="Ex: produtos ecológicos, tecnologia"
            />
          </div>

          <div className="form-group">
            <label>Interesses:</label>
            <input
              type="text"
              value={userInfo.interests}
              onChange={(e) => setUserInfo({...userInfo, interests: e.target.value})}
              placeholder="Ex: futebol, leitura, viagens"
            />
          </div>
        </section>

        <section className="input-section">
          <h2>Informações do Produto/Serviço</h2>
          <div className="form-group">
            <label>Nome do Produto:</label>
            <input
              type="text"
              value={productInfo.name}
              onChange={(e) => setProductInfo({...productInfo, name: e.target.value})}
              placeholder="Ex: Fone de Ouvido Wireless"
            />
          </div>

          <div className="form-group">
            <label>Categoria:</label>
            <input
              type="text"
              value={productInfo.category}
              onChange={(e) => setProductInfo({...productInfo, category: e.target.value})}
              placeholder="Ex: Eletrônicos"
            />
          </div>

          <div className="form-group">
            <label>Principais Features (separadas por vírgula):</label>
            <input
              type="text"
              value={productInfo.features}
              onChange={(e) => setProductInfo({...productInfo, features: e.target.value})}
              placeholder="Ex: cancelamento de ruído, bateria 30h, som surround"
            />
          </div>

          <div className="form-group">
            <label>Preço (R$):</label>
            <input
              type="number"
              value={productInfo.price}
              onChange={(e) => setProductInfo({...productInfo, price: e.target.value})}
              placeholder="Ex: 299.90"
            />
          </div>
        </section>

        <section className="action-section">
          <button onClick={generateContent} disabled={loading}>
            {loading ? 'Gerando...' : 'Gerar Conteúdo Hiper-Personalizado'}
          </button>
        </section>

        <section className="output-section">
          <h2>Conteúdo Gerado</h2>
          <div className="content-display">
            {content ? (
              <div className="generated-content">
                <pre>{content}</pre>
              </div>
            ) : (
              <p>Seu conteúdo personalizado aparecerá aqui...</p>
            )}
          </div>
        </section>

        <section className="history-section">
          <h2>Histórico de Gerações</h2>
          <div className="history-list">
            {history.length > 0 ? (
              history.map((item) => (
                <div key={item.id} className="history-item">
                  <div className="history-content">{item.content}</div>
                  <div className="history-meta">
                    <span className="history-type">{item.type}</span>
                    <span className="history-time">{item.timestamp}</span>
                  </div>
                </div>
              ))
            ) : (
              <p>Nenhum conteúdo gerado ainda...</p>
            )}
          </div>
        </section>
      </main>

      <footer className="App-footer">
        <p>Hiperpersonalizador © {new Date().getFullYear()} - Transformando cada interação em uma experiência única</p>
      </footer>
    </div>
  );
}

export default App;