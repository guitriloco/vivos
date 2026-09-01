# Exemplos de Uso - Hiperpersonalizador

## API Endpoints

### 1. Gerar Conteúdo Personalizado

#### Endpoint
```
POST /api/v1/content/generate
```

#### Headers
```
Content-Type: application/json
Authorization: Bearer <seu-token>
```

#### Body
```json
{
  "user_id": 123,
  "product_info": {
    "id": "prod_001",
    "name": "Fone de Ouvido Wireless Premium",
    "category": "Eletrônicos",
    "features": ["cancelamento de ruído", "bateria 30h", "som surround"],
    "price": 599.90,
    "brand": "TechSound"
  },
  "content_type": "descricao",
  "personalization_params": {
    "purchase_history": [
      {
        "product_category": "eletronicos",
        "frequency": 4,
        "avg_rating": 4.5
      }
    ],
    "audience_profile": {
      "demographics": {
        "age": 28,
        "gender": "masculino",
        "location": "São Paulo",
        "income_level": "alto",
        "tech_savvy": true
      },
      "psychographics": {
        "personality": "inovador",
        "values": ["qualidade", "tecnologia", "status"],
        "interests": ["tecnologia", "música", "produtividade"]
      }
    },
    "behavioral_data": {
      "browsing_time": 120,
      "click_through_rate": 0.35,
      "social_shares": 2,
      "return_visits": 5
    },
    "contextual_factors": {
      "time_of_day": "noite",
      "device_type": "mobile",
      "season": "natal",
      "promotional_period": true
    }
  }
}
```

#### Response
```json
{
  "content_id": 456,
  "content": "[Conteúdo hiper-personalizado gerado]",
  "cached": false,
  "timestamp": "2026-04-12T03:00:00.000Z",
  "personalization_factors": {
    "user_context": "...",
    "product_info": "...",
    "content_type": "descricao"
  }
}
```

### 2. Recuperar Histórico de Conteúdo

#### Endpoint
```
GET /api/v1/content/history?user_id=123&limit=10
```

#### Response
```json
{
  "history": [
    {
      "id": 456,
      "user_id": 123,
      "product_id": "prod_001",
      "content_type": "descricao",
      "generated_content": "[Conteúdo gerado anteriormente]",
      "personalization_data": "{...}",
      "created_at": "2026-04-12T02:30:00.000Z"
    }
  ],
  "count": 1,
  "user_id": 123
}
```

## Integração com Frontend

### Exemplo de Integração com JavaScript

```javascript
// Função para gerar conteúdo hiper-personalizado
async function generateHiperPersonalizedContent(userData, productInfo) {
  try {
    const response = await fetch('http://localhost:5000/api/v1/content/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userData.id,
        product_info: productInfo,
        content_type: 'descricao',
        personalization_params: {
          purchase_history: userData.purchaseHistory,
          audience_profile: userData.profile,
          behavioral_data: userData.behavior,
          contextual_factors: {
            time_of_day: new Date().getHours(),
            device_type: detectDeviceType(),
            season: getCurrentSeason()
          }
        }
      })
    });

    const data = await response.json();
    
    if (data.error) {
      throw new Error(data.error);
    }

    return data.content;
  } catch (error) {
    console.error('Erro ao gerar conteúdo:', error);
    return null;
  }
}

// Função para integrar com e-commerce
function integrateWithEcommerce() {
  // Detecta produtos na página
  const products = document.querySelectorAll('.product-card');
  
  products.forEach(async (productElement) => {
    const productId = productElement.dataset.productId;
    const userId = getCurrentUserId(); // Função para obter ID do usuário
    
    // Gera conteúdo personalizado para o produto
    const personalizedContent = await generateHiperPersonalizedContent(
      getUserData(userId),
      getProductInfo(productId)
    );
    
    // Insere o conteúdo personalizado na página
    const contentDiv = productElement.querySelector('.personalized-content');
    if (contentDiv && personalizedContent) {
      contentDiv.innerHTML = `<p>${personalizedContent}</p>`;
    }
  });
}

// Inicia a integração quando a página carregar
document.addEventListener('DOMContentLoaded', integrateWithEcommerce);
```

## Exemplo de Uso com Python

```python
import requests
import json

class HiperPersonalizadorClient:
    def __init__(self, base_url, api_key=None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
    
    def generate_content(self, user_id, product_info, content_type='descricao', **kwargs):
        """Gera conteúdo hiper-personalizado"""
        url = f"{self.base_url}/api/v1/content/generate"
        
        payload = {
            'user_id': user_id,
            'product_info': product_info,
            'content_type': content_type,
            'personalization_params': kwargs.get('personalization_params', {})
        }
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def get_content_history(self, user_id, limit=10):
        """Recupera histórico de conteúdo gerado"""
        url = f"{self.base_url}/api/v1/content/history"
        params = {'user_id': user_id, 'limit': limit}
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        
        return response.json()

# Exemplo de uso
client = HiperPersonalizadorClient('http://localhost:5000')

# Dados do usuário e produto
user_data = {
    'id': 123,
    'preferences': {'categorias_preferidas': ['eletronicos', 'tecnologia']},
    'historico_compras': [{'categoria': 'eletronicos', 'frequencia': 4}]
}

product_data = {
    'id': 'fone_001',
    'name': 'Fone de Ouvido Wireless Premium',
    'category': 'Eletrônicos',
    'features': ['cancelamento de ruído', 'bateria 30h'],
    'price': 599.90
}

# Gera conteúdo personalizado
result = client.generate_content(
    user_id=user_data['id'],
    product_info=product_data,
    content_type='descricao',
    personalization_params={
        'audience_profile': {
            'demographics': {'idade': 28, 'localizacao': 'SP'},
            'interests': ['tecnologia', 'música']
        }
    }
)

print("Conteúdo gerado:", result['content'])
```

## Integração com Plataformas de E-commerce

### Magento
```php
// Plugin para Magento
class HiperPersonalizadorPlugin
{
    private $apiClient;
    
    public function __construct($apiUrl, $apiKey)
    {
        $this->apiClient = new HiperPersonalizadorClient($apiUrl, $apiKey);
    }
    
    public function personalizeProductDescription($productId, $customerId)
    {
        $productInfo = $this->getProductInfo($productId);
        $customerInfo = $this->getCustomerInfo($customerId);
        
        $personalizedContent = $this->apiClient->generate_content(
            $customerId,
            $productInfo,
            'descricao',
            ['audience_profile' => $customerInfo]
        );
        
        return $personalizedContent['content'];
    }
}
```

### Shopify
```javascript
// App para Shopify
ShopifyApp.init({
  apiKey: 'sua-api-key',
  shopOrigin: window.location.origin
});

ShopifyApp.ready(function(){
  // Personaliza descrições de produtos
  fetch('/admin/products.json')
    .then(response => response.json())
    .then(products => {
      products.forEach(product => {
        personalizeProduct(product.id);
      });
    });
});

function personalizeProduct(productId) {
  fetch(`/api/personalize/${productId}`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(getCurrentCustomerData())
  })
  .then(response => response.json())
  .then(data => {
    updateProductDescription(productId, data.content);
  });
}
```

## Considerações de Desempenho

- O sistema implementa cache para evitar regeneração desnecessária de conteúdo
- A personalização é otimizada para tempos de resposta inferiores a 2 segundos
- O histórico de conteúdo é paginado para melhor performance
- Recomenda-se monitoramento contínuo de latência e taxa de erro

## Segurança

- Todas as requisições devem ser autenticadas com API key
- Dados sensíveis são mascarados nos logs
- Validação de entrada é realizada em todos os endpoints
- Rate limiting está implementado para prevenir abuso