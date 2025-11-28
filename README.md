# CiConfeitaria

Aplicação web simples para cadastrar, listar e apagar receitas de confeitaria. Usa Flask com SQLite e oferece uma interface amigável em português.

## Pré-requisitos
- Python 3.10+
- pip

## Como executar
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Inicie o servidor Flask:
   ```bash
   flask --app app run
   ```
   O banco `recipes.db` será criado automaticamente na raiz do projeto.
3. Acesse o site em [http://localhost:5000](http://localhost:5000).

## Endpoints principais
- Interface web: `GET /`
- Criar receita via formulário: `POST /recipes`
- Apagar receita via formulário: `POST /recipes/<id>/delete`
- API listar receitas: `GET /api/recipes`
- API criar receita: `POST /api/recipes`
- API apagar receita: `DELETE /api/recipes/<id>`

## Notas
- Campos obrigatórios: título, descrição, ingredientes e modo de preparo.
- O campo de imagem é opcional e aceita apenas uma URL.
- Ingredientes e passos podem ser informados linha a linha no formulário.
