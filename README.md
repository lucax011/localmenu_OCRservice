# LocalMenu: OCR Service

Microsserviço que transforma a **foto de um cardápio** em itens estruturados (nome, preço, confiança e posição na imagem). O app do restaurante ([B2B](https://github.com/lucax011/localmenu_frontendB2B)) usa o serviço para importar o cardápio sem digitar item por item.

## Ecossistema LocalMenu

| Repositório | Papel |
| --- | --- |
| [localmenu_backend](https://github.com/lucax011/localmenu_backend) | API NestJS + PostgreSQL |
| [localmenu_frontendB2C](https://github.com/lucax011/localmenu_frontendB2C) | App do cliente (Expo) |
| [localmenu_frontendB2B](https://github.com/lucax011/localmenu_frontendB2B) | App do restaurante (Expo) |
| [localmenu_OCRservice](https://github.com/lucax011/localmenu_OCRservice) | Microsserviço de OCR em Python (FastAPI) |

## Como funciona

1. **Pré-processamento** (OpenCV): escala de cinza, remoção de ruído e limiarização
2. **OCR**: Tesseract (padrão) ou PaddleOCR, com idioma configurável (`por` por padrão)
3. **Interpretação** (spaCy `pt_core_news_sm` + regex): identifica o nome do item e o preço no formato `R$ 00,00`

## Stack

- Python 3.11 + FastAPI + Uvicorn
- Tesseract / PaddleOCR (opcional), OpenCV, spaCy
- Pydantic 1 para configuração
- Pytest, Ruff, Black e isort (com pre-commit)
- Docker e Jenkinsfile

## Como rodar

Com Docker (já instala o Tesseract):

```bash
docker compose up --build    # http://localhost:8000/docs
```

Local (precisa do [Tesseract](https://github.com/tesseract-ocr/tesseract) instalado com o idioma português):

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
cp .env.example .env
uvicorn src.main:app --reload --port 8000
```

## Endpoints

| Método | Rota | Descrição |
| --- | --- | --- |
| GET | `/health` | Verificação de saúde |
| GET | `/version` | Versão do serviço |
| POST | `/ocr/extract` | Recebe `file` (JPEG ou PNG, até `MAX_UPLOAD_MB`) e devolve os itens |

Parâmetros de `/ocr/extract`: `lang` (padrão `por`), `use_paddle`, `preprocess` e `return_bboxes`.

Exemplo de resposta:

```json
{
  "source": { "filename": "cardapio.jpg", "size_bytes": 182340, "content_type": "image/jpeg" },
  "items": [
    { "name": "X-Burger", "price": 24.9, "description": null, "confidence": 0.91,
      "bbox": { "x": 40, "y": 120, "w": 300, "h": 28 } }
  ],
  "metadata": { "engine": "tesseract", "lang": "por", "processing_ms": 840,
    "preprocessing": { "applied": true, "steps": ["grayscale", "denoise", "threshold"] } }
}
```

## Configuração (`.env`)

| Variável | Padrão | Descrição |
| --- | --- | --- |
| `APP_PORT` | `8000` | Porta |
| `EXTRACTOR_ENGINE` | `tesseract` | `tesseract` ou `paddle` |
| `ENABLE_PREPROCESSING` | `true` | Liga o pré-processamento |
| `RETURN_BBOXES` | `true` | Retorna a posição de cada item |
| `MAX_UPLOAD_MB` | `10` | Tamanho máximo da imagem |

## Testes

```bash
pytest
```
