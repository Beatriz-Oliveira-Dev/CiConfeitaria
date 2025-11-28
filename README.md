# CiConfeitaria

Aplicação web simples para cadastrar, atualizar, listar e apagar receitas de confeitaria. Usa Flask com SQLite e oferece uma interface em português com layout inspirado em vitrines de confeitaria.

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
   - Home com grade estilo Pinterest: `GET /`
   - Formulário de cadastro/edição: `GET /cadastrar`

## Endpoints principais
- Interface web: `GET /`
- Formulário de cadastro/edição: `GET /cadastrar`
- Criar receita via formulário: `POST /recipes`
- Atualizar receita via formulário: `POST /recipes/<id>/update`
- Apagar receita via formulário: `POST /recipes/<id>/delete`
- API listar receitas: `GET /api/recipes`
- API criar receita: `POST /api/recipes`
- API atualizar receita: `PUT|PATCH /api/recipes/<id>`
- API apagar receita: `DELETE /api/recipes/<id>`

## Notas
- Campos obrigatórios: título, descrição, ingredientes e modo de preparo.
- O campo de imagem é opcional e aceita apenas uma URL.
- Ingredientes e passos podem ser informados linha a linha no formulário.
- O arquivo do banco SQLite (`recipes.db`) fica fora do versionamento para evitar conflitos; ele é recriado automaticamente ao subir a aplicação.
