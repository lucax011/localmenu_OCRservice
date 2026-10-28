# LocalMenu: OCR Service

Microsserviço que transforma a **foto de um cardápio** em itens estruturados (nome, preço, descrição, categoria, confiança e posição na imagem). O app do restaurante ([B2B](https://github.com/lucax011/localmenu_frontendB2B)) usa o serviço, através do backend, para importar o cardápio sem digitar item por item.

## Ecossistema LocalMenu

| Repositório | Papel |
| --- | --- |
| [localmenu_backend](https://github.com/lucax011/localmenu_backend) | API NestJS + PostgreSQL |
| [localmenu_frontendB2C](https://github.com/lucax011/localmenu_frontendB2C) | App do cliente (Expo) |
| [localmenu_frontendB2B](https://github.com/lucax011/localmenu_frontendB2B) | App do restaurante (Expo) |
| [localmenu_OCRservice](https://github.com/lucax011/localmenu_OCRservice) | Microsserviço de OCR em Python (FastAPI) |

## Como funciona

1. **Pré-processamento** (OpenCV): escala de cinza, remoção de ruído e limiarização
2. **OCR**: Tesseract (padrão) ou PaddleOCR, com idioma configurável (`por` por padrão); as palavras são agrupadas em linhas, na ordem de leitura
3. **Interpretação** (regras em `src/core/nlp.py`):
   - linha que termina em preço (`R$ 24,90`, `24,90`, `1.234,50`) vira um item; pontilhados e traços entre o nome e o preço são removidos
   - linha curta em maiúsculas sem preço (`LANCHES`) é o título da categoria dos itens seguintes
   - outra linha sem preço logo abaixo de um item vira a descrição dele

## Stack

- Python 3.11 + FastAPI + Uvicorn
- Tesseract / PaddleOCR (opcional), OpenCV
- Pydantic 1 para configuração
- Pytest, Ruff, Black e isort (com pre-commit)
- Docker e Jenkinsfile

## Como rodar

Com Docker (já instala o Tesseract com o idioma português):

```bash
docker compose up --build    # http://localhost:8000/docs
```

Local (precisa do [Tesseract](https://github.com/tesseract-ocr/tesseract) instalado com o idioma português):

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
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
    { "name": "X-Burger", "price": 24.9, "description": "Pão, carne e queijo", "category": "Lanches", "confidence": 0.91,
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

Erros: `415` para arquivo que não é JPEG ou PNG, `413` acima de `MAX_UPLOAD_MB`, `422` para imagem corrompida.

## Testes

```bash
pytest                                                    # local; o teste com OCR real é pulado sem Tesseract
docker build -t localmenu-ocr . && docker run --rm localmenu-ocr python -m pytest   # todos, com Tesseract
```

A imagem de cardápio usada nos testes é gerada na hora (`tests/conftest.py`).
