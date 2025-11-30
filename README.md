# CiConfeitaria

Aplicação web simples para cadastrar, atualizar, listar e apagar receitas de confeitaria. Usa Flask com SQLite e oferece uma interface em português com layout inspirado em vitrines de confeitaria.

## Recursos
- Home em grade estilo Pinterest com cards clicáveis e modal de detalhes.
- Cabeçalho fixo com navegação para Home, cadastro e atalho de favoritos.
- Botões de favorito em cada card para salvar e filtrar apenas as receitas queridinhas.
- Formulário de criação/edição com validação server-side.
- API REST simples para integração com frontend ou scripts.

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

### Favoritos
- Clique no coração do card para marcar ou desmarcar a receita como favorita.
- Use o atalho "♥ Favoritos" no topo para ver apenas as favoritas; clique novamente para voltar a listar todas.

### Carregar receitas de exemplo
Use o script `seed_recipes.py` para popular o banco com receitas de exemplo (macarrons, cheesecake e red velvet). Se quiser incluir as fotos em data URL que você já tem, exporte as variáveis antes de rodar o script:

```bash
export CHEESECAKE_IMAGE_DATA="data:image/jpeg;base64,..."  # cole aqui a data URL completa
export REDVELVET_IMAGE_DATA="data:image/jpeg;base64,..."   # cole aqui a data URL completa
python seed_recipes.py
```

O script cria novas entradas quando o título não existe e atualiza as receitas existentes se elas já estiverem no banco.

## Endpoints principais
- Interface web: `GET /`
- Formulário de cadastro/edição: `GET /cadastrar`
- Criar receita via formulário: `POST /recipes`
- Atualizar receita via formulário: `POST /recipes/<id>/update`
- Apagar receita via formulário: `POST /recipes/<id>/delete`
- API listar receitas: `GET /api/recipes`
- API atualizar favorito: `PATCH /api/recipes/<id>/favorite`
- API criar receita: `POST /api/recipes`
- API atualizar receita: `PUT|PATCH /api/recipes/<id>`
- API apagar receita: `DELETE /api/recipes/<id>`

## Notas
- Campos obrigatórios: título, descrição, ingredientes e modo de preparo.
- O campo de imagem é opcional e aceita apenas uma URL.
- Ingredientes e passos podem ser informados linha a linha no formulário.
- O arquivo do banco SQLite (`recipes.db`) fica fora do versionamento para evitar conflitos; ele é recriado automaticamente ao subir a aplicação.

## Histórico
- Consulte o [CHANGELOG](CHANGELOG.md) para ver as decisões já integradas (incluindo o PR previamente mergeado sobre artefatos do banco).
