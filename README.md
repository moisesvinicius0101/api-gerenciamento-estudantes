
# API de Gerenciamento de Estudantes e Cursos
 
API REST para gerenciar **estudantes** e **cursos**, com relacionamento entre as duas entidades e **autenticação via JWT**. Construída com FastAPI, SQLAlchemy e Alembic.
 
## Funcionalidades
 
- CRUD completo de **estudantes** e **cursos**
- Busca de estudantes (`/students/search`)
- Relacionamento **1:N**: um curso tem vários estudantes, e cada estudante pode estar vinculado a um curso
- Cadastro e login de usuários com **JWT**
- Senhas armazenadas com hash **Argon2** (nunca em texto puro)
- Rotas de estudantes e cursos **protegidas**: exigem token válido
- Validação de dados com **Pydantic** (e-mail, tamanho de campos, idade mínima)
- Versionamento do banco com **migrations (Alembic)**
- Documentação interativa automática (Swagger UI)
## Tecnologias
 
| Camada | Tecnologia |
|---|---|
| Framework web | FastAPI |
| ORM | SQLAlchemy 2.x |
| Migrations | Alembic |
| Banco de dados | SQLite |
| Validação | Pydantic v2 |
| Autenticação | PyJWT + OAuth2 (password flow) |
| Hash de senha | pwdlib (Argon2) |
| Configuração | pydantic-settings |
| Servidor | Uvicorn |
 
## Estrutura do projeto
 
```
api-gerenciamento-aluno/
└── app/
    ├── alembic/            # migrations do banco
    │   └── versions/
    ├── crud/               # acesso ao banco (apenas lógica de dados)
    │   ├── courses.py
    │   ├── student.py
    │   └── users.py
    ├── models/             # tabelas (SQLAlchemy)
    │   ├── courses.py
    │   ├── students.py
    │   └── users.py
    ├── routers/            # rotas HTTP (decidem os códigos de erro)
    │   ├── auth.py
    │   ├── courses.py
    │   └── student.py
    ├── schemas/            # contratos de entrada e saída (Pydantic)
    │   ├── courses_schemas.py
    │   ├── student_schemas.py
    │   └── user_schemas.py
    ├── utill/
    │   └── security.py     # hash de senha e criação/validação de JWT
    ├── config.py           # configurações lidas do .env
    ├── database.py         # engine, sessão e Base
    ├── dependencies.py     # get_current_user (proteção das rotas)
    ├── main.py             # criação do app e registro dos routers
    ├── .env.example        # modelo das variáveis de ambiente
    └── requirements.txt
```
 
### Arquitetura em camadas
 
```
Rota (routers)  →  CRUD (crud)  →  Model (models)  →  Banco
     ↑                                   
  Schema (entrada/saída)
```
 
- **Routers** recebem a requisição e decidem a resposta HTTP (404, 409, 401...).
- **CRUD** contém só a lógica de banco, sem conhecer o FastAPI.
- **Schemas** definem o que entra e o que sai da API (por exemplo, a senha nunca é devolvida).
- **Models** representam as tabelas.
## Modelo de dados
 
```
┌────────────┐          ┌──────────────┐
│  courses   │ 1      N │   students   │
├────────────┤◄─────────├──────────────┤
│ id         │          │ id           │
│ title      │          │ nome         │
│ description│          │ idade        │
└────────────┘          │ email (uniq) │
                        │ course_id FK │
                        └──────────────┘
 
┌────────────┐
│   users    │   (credenciais de acesso à API, separadas dos alunos)
├────────────┤
│ id         │
│ email (uniq)│
│ hashed_password │
└────────────┘
```
 
> `users` é separada de `students` de propósito: aluno é dado do negócio, usuário é quem acessa a API.
 
## Como rodar
 
### Pré-requisitos
 
- Python 3.10 ou superior
- Git
### 1. Clonar o repositório
 
```bash
git clone https://github.com/moisesvinicius0101/api-gerenciamento-aluno.git
cd api-gerenciamento-aluno/app
```
 
### 2. Criar e ativar o ambiente virtual
 
**Windows (PowerShell):**
 
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
 
**Linux / macOS:**
 
```bash
python -m venv venv
source venv/bin/activate
```
 
> No PowerShell, se aparecer erro de execução de scripts:
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`
 
### 3. Instalar as dependências
 
```bash
pip install -r requirements.txt
```
 
### 4. Configurar as variáveis de ambiente
 
Copie o modelo e preencha a chave secreta:
 
```bash
# Windows
copy .env.example .env
 
# Linux / macOS
cp .env.example .env
```
 
Gere uma chave segura:
 
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
 
Cole o resultado em `SECRET_KEY` dentro do arquivo `.env`:
 
```env
SECRET_KEY=sua_chave_gerada_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
 
| Variável | Descrição | Padrão |
|---|---|---|
| `SECRET_KEY` | Chave usada para assinar os tokens. **Obrigatória.** | — |
| `ALGORITHM` | Algoritmo de assinatura do JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tempo de validade do token | `30` |
 
> ⚠️ Nunca faça commit do `.env`. Ele já está no `.gitignore`.
 
### 5. Criar as tabelas (migrations)
 
```bash
alembic upgrade head
```
 
### 6. Iniciar a API
 
```bash
uvicorn main:app --reload
```
 
Execute sempre de dentro da pasta `app`, para que o `.env` seja encontrado.
 
A API ficará disponível em:
 
- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
## Autenticação
 
O fluxo usa **OAuth2 com senha + token JWT (Bearer)**:
 
```
register → salva e-mail + hash da senha
login    → confere a senha e devolve um JWT
request  → header "Authorization: Bearer <token>" → rota executa
```
 
### Passo a passo no Swagger (`/docs`)
 
1. `POST /auth/register` para criar um usuário.
2. Clique em **Authorize** (cadeado no topo).
3. Preencha `username` com o **e-mail** e `password` com a senha. Deixe `client_id` e `client_secret` em branco.
4. Teste `GET /auth/me` e as demais rotas protegidas.
### Exemplo com curl
 
```bash
# 1. Registrar
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@email.com", "password": "senha12345"}'
 
# 2. Login (form-data, não JSON)
curl -X POST http://127.0.0.1:8000/auth/login \
  -d "username=usuario@email.com&password=senha12345"
 
# 3. Usar o token
curl http://127.0.0.1:8000/students/ \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```
 
## Endpoints
 
### Auth (públicas, exceto `/auth/me`)
 
| Método | Rota | Descrição |
|---|---|---|
| POST | `/auth/register` | Cria um usuário |
| POST | `/auth/login` | Autentica e devolve o token |
| GET | `/auth/me` 🔒 | Retorna o usuário logado |
 
### Students 🔒
 
| Método | Rota | Descrição |
|---|---|---|
| GET | `/students/` | Lista os estudantes |
| GET | `/students/search` | Busca estudantes |
| POST | `/students/` | Cria um estudante |
| GET | `/students/{id_student}` | Busca por id |
| PUT | `/students/{id_student}` | Atualiza um estudante |
| DELETE | `/students/{id_student}` | Remove um estudante |
 
### Courses 🔒
 
| Método | Rota | Descrição |
|---|---|---|
| GET | `/courses/` | Lista os cursos |
| POST | `/courses/` | Cria um curso |
| GET | `/courses/{id_course}` | Busca por id |
| PUT | `/courses/{id_course}` | Atualiza um curso |
| DELETE | `/courses/{id_course}` | Remove um curso |
 
🔒 = exige token JWT.
 
### Exemplo de resposta de estudante (com curso aninhado)
 
```json
{
  "id": 1,
  "nome": "Maria",
  "idade": 20,
  "email": "maria@email.com",
  "course_id": 1,
  "course": {
    "id": 1,
    "title": "Introdução ao Python",
    "description": "Curso introdutório ao Python."
  }
}
```
 
### Códigos de resposta
 
| Código | Quando acontece |
|---|---|
| 200 / 201 | Sucesso / recurso criado |
| 401 | Token ausente, inválido ou expirado; login incorreto |
| 404 | Estudante ou curso não encontrado |
| 409 | E-mail já cadastrado |
| 422 | Dados inválidos (e-mail mal formatado, senha curta, etc.) |
 
## Migrations (Alembic)
 
```bash
# Aplicar todas as migrations
alembic upgrade head
 
# Ver a versão atual do banco
alembic current
 
# Criar uma nova migration após alterar um model
alembic revision --autogenerate -m "descricao da mudanca"
 
# Desfazer a última migration
alembic downgrade -1
```
 
**Importante:**
 
- Todo model novo precisa ser **importado no `alembic/env.py`**. Senão o autogenerate gera uma migration vazia.
- No SQLite, adicionar uma foreign key exige que a constraint tenha **nome** (o Alembic usa o modo batch).
- Sempre confira o arquivo gerado antes de rodar o `upgrade`.
## Segurança
 
- Senhas com **Argon2**, nunca salvas em texto puro.
- Respostas de usuário **não incluem** senha nem hash.
- Mensagem de login idêntica para "e-mail inexistente" e "senha errada", para não revelar quais e-mails existem.
- Verificação de senha com tempo equalizado, evitando descobrir e-mails cadastrados pelo tempo de resposta.
- E-mails normalizados em minúsculas.
- `SECRET_KEY` obrigatória: a aplicação não inicia sem ela.
- O token usa o **id** do usuário (`sub`) e tem data de expiração.
## Fluxo de desenvolvimento (Git)
 
O projeto foi desenvolvido com branches por funcionalidade e Pull Requests:
 
```
feature/...  →  Pull Request  →  main
```
 
Padrão de commits usado: `feat:`, `fix:`, `refactor:`, `chore:`, `docs:`.
 
## Próximos passos
 
- [ ] Rota `GET /courses/{id}/students` (listar alunos de um curso)
- [ ] Relacionamento **N:N** (aluno em vários cursos) com tabela associativa
- [ ] Papéis de usuário (admin / comum) e restrição do `/auth/register`
- [ ] Limite de tentativas de login (rate limiting)
- [ ] Testes automatizados com `pytest` e `TestClient`
- [ ] Paginação nas listagens
- [ ] Migração para PostgreSQL
- [ ] Dockerfile e `docker-compose`
## Autor
 
**Moisés Vinícius**
GitHub: [@moisesvinicius0101](https://github.com/moisesvinicius0101)
 
