<h1 align="center" style="font-weight: bold;">Kairos WebApp 💻</h1>
<p align="center">
  <img src="https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D">
  <img src="https://img.shields.io/badge/Quasar-16B7FB?style=for-the-badge&logo=quasar&logoColor=black">
  <img src="https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white">
  <img src="https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray"></img>
  <img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white"></img>
</p>

Web app para agendamento de eventos pessoais.


<img src="https://github.com/user-attachments/assets/9815f7a5-83a6-47f1-b7c6-2bb2599a2152" />

<h2 id="tech">📦 Tecnologias usadas:</h2>

- [Django(Backend)](https://www.djangoproject.com/)
- [Django REST Framework(API)](https://www.django-rest-framework.org/)
- [Vue 3(Composition API com script setup)](https://vuejs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Quasar 2(Framework para construção de aplicações Vue.js)](https://quasar.dev/)
- [Pinia(Gerenciamento de estado)](https://pinia.vuejs.org/)
- [Vue-Router(Gerenciamento de rotas)](https://router.vuejs.org/)
- [Axios(Integração de APIs)](https://axios-http.com/docs/intro)
- [Bootstrap Icons](https://icons.getbootstrap.com/)

<h2 id="intro">🔥 Introdução:</h2>

<h3>⚙️ Pré-requisitos:</h3>

Você precisa ter instalado na sua máquina as seguintes tecnologias:
- Node
- Python

*Obs.: Desenvolvi este projeto com Node 20.x e Python 3.12.x. Não testei o projeto em versões anteriores destas tecnologias.

<h3>🔨 Guia de instalação:</h1>

<h4>Passo 1: Clone esse repositório</h4>

```bash
git clone git@github.com:EmanuelLacerda/kairos-webapp.git
```

<h4>Passo 2: Acesse a pasta do respositório</h4>

```bash
cd kairos-webapp
```

<h4>Passo 3: Instale as dependências</h4>

Neste repositório, há 2 diretórios, sendo um deles a api(server/) e o outro o frontend(web/). Cada repositório possuí dependências próprias. Então, você precisa instalar as dependências individualmente. Abaixo segue como fazer para cada um dos dois.

**1° Acesse o diretório "server":**

```bash
cd server
```

**2° Execute o "pip3 install -r requirements.txt":**

```bash
pip3 install -r requirements.txt
```

**3° Volte para a raiz do projeto:**

```bash
cd ..
```

**4° Acesse o diretório "web":**
```bash
cd web
```

**5° Execute o comando "npm install":**
```bash
npm install
```

**6° Volte para a raiz do projeto:**
```bash
cd ..
```

<h4>Passo 04: Adicione as variáveis de ambiente no diretório server</h4>
Ao acessar server/.env.examples você verá o seguinte conteúdo:

```
SECRET_KEY=
DEBUG=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_PORT=
```

Explicação sobre as varíaveis:
- **SECRET_KEY:** Coloque nesta a SECRET_KEY que você tiver gerado para a aplicação Django.
- **DEBUG:** Coloque nesta um boolean indicando se o projeto está ou não no debug mode.
- **DB_NAME até DB_PORT:** Coloque nestas as informações do banco relacional em você salvará os dados. De preferência, utilize um banco PostgreSQL, pois o projeto foi desenvolvido pensando neste banco.
- **EMAIL_HOST até EMAIL_PORT**: Coloque nestas as informações do host de e-mail que será utilizado para enviar as mensagens via e-mail.

<h4>Passo 05: Execute o projeto</h4>

**1° Acesse o diretório server:**
```bash
cd server
```

**2° Execute as migrations:**
```bash
python3 manage.py migrate
```

**3° Execute a api:**
```bash
python3 manage.py 
```

**4° Acesse o diretório web:**
```bash
cd web
```

**5° Execute o frontend:**
```bash
npx quasar dev #ou
quasar dev #este segundo comando só funcionará se tiver o Quasar instalado globalmente
```

*Obs.: Para o projeto funcionar corretamente, api e frontend devem estar em execução ao mesmo tempo.

<h2 id="feature-list">⚙️ Funcionalidades</h2>

**Funcionalidades de autenticação:**
- Cadastro de usuário.
- Verificação de e-mail de usuário.
- Login.
- Logout.

**Funcionalidades de gerenciamento de eventos:**
- Adição de eventos com duração de 1 dia ou mais e ligados ao usuário que os criou.
- Listagem de eventos em calendário.
- Edição de eventos.
- Remoção de eventos.

<h2 id="api-endpoints">⚙️ API Endpoints</h2>

A API provém os seguintes endpoints:

| rota               | descrição                                          
|----------------------|-----------------------------------------------------
| <kbd>POST /auth/register</kbd>     | Registra um novo usuário [Ver detalhes](#post-user)
| <kbd>POST /auth/verify-email</kbd>     | Verifica o e-mail de um usuário [Ver detalhes](#verify-email-user)
| <kbd>POST /auth/login</kbd>     | Retorna o access e o refresh token de um usuário [Ver detalhes](#login-user)
| <kbd>POST /auth/logout</kbd>     | Adiciona o refresh token de um usuário na blacklist [Ver detalhes](#logout-user)
| <kbd>GET /auth/profile</kbd>     | Verifica a validade do access token de um usuário [Ver detalhes](#check-the-validity-access-token)
| <kbd>POST /auth/token/refresh</kbd>     | Gera um novo access token para um usuário [Ver detalhes](#refresh-token)
| <kbd>GET /events</kbd>     | Pega a lista de todos os eventos. [Ver detalhes](#get-all-events)
| <kbd>GET /events/{eventUUID}/</kbd>     | Pega um evento específico por UUID. [Ver detalhes](#get-specific-event)
| <kbd>POST /events</kbd>     | Registra um novo evento [Ver detalhes](#post-event)
| <kbd>PUT /events/{eventUUID}/</kbd>     | Edita os dados de um evento específico por UUID
| <kbd>PATCH /events/{eventUUID}/</kbd>     | Edita os dados de um evento específico por UUID
| <kbd>DELETE /events/{eventUUID}/</kbd>     | Remove um evento específico por UUID
| <kbd>GET /users/{userId}/eventUUID/</kbd>     | Pega todos os eventos de um usuário específico por UUID. [Ver detalhes](#get-user-all-events)


<h3 id="post-user">POST /auth/register</h3>

<h4>REQUEST:</h4>

```
{
  name: 'Emanuel de Souza Lacerda',
  email: 'emanuellacerda@gmail.com',
  password: 'te@12klLA',
  confirm_password: 'te@12klLA'
}
```

<h4>RESPONSE:</h4>

```
{
  name: 'Emanuel de Souza Lacerda',
  email: 'emanuellacerda@gmail.com'
}
```

<h3 id="verify-email-user">POST /auth/verify-email</h3>

<h4>REQUEST:</h4>

```
{
  code: '238657'
}
```

<h4>RESPONSE:</h4>

```
{
 message: "O e-mail foi verificado com sucesso"
}
```

<h3 id="login-user">POST /auth/login</h3>

<h4>REQUEST:</h4>

```
{
  email: 'emanuellacerda@gmail.com',
  password: 'te@12klLA'
}
```

<h4>RESPONSE:</h4>

```
{
  name: 'Emanuel de Souza Lacerda',
  email: 'emanuellacerda@gmail.com',
  access_token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxNTQ5NjUxLCJpYXQiOjE3NDE1NDkwNTEsImp0aSI6IjViYTg3MzZkMDQ4ZTQ5YTk4ZGI3ZWJhNmFmYjA0YjlkIiwidXNlcl9pZCI6OH0.T69yVAqEFlAEcj8ODabqjheaYn7jEBMQZagat6EU0aI',
refresh_token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTYzNTQ1MSwiaWF0IjoxNzQxNTQ5MDUxLCJqdGkiOiJmNWE3ZTJiMzcyNTQ0ZmViYjIwZTE4OTdiYjVkZDcxMyIsInVzZXJfaWQiOjh9.FX2a-g85tgb4iL9A-ISRe10RxG34za0QxmJslcnVgjk'
}
```

<h3 id="logout-user">POST /auth/logout</h3>

<h4>REQUEST:</h4>

```
{
  refresh_token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwicm9sZSI6InVzZXIiLCJleHAiOjE2ODg4ODg4ODh9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
}
```

<h3 id="check-the-validity-access-token">POST /auth/profile</h3>

<h4>REQUEST:</h4>

```
headers: {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxNTQ5NjUxLCJpYXQiOjE3NDE1NDkwNTEsImp0aSI6IjViYTg3MzZkMDQ4ZTQ5YTk4ZGI3ZWJhNmFmYjA0YjlkIiwidXNlcl9pZCI6OH0.T69yVAqEFlAEcj8ODabqjheaYn7jEBMQZagat6EU0aI'
}
```

<h4>RESPONSE:</h4>

```
{
    message: 'Access token válido'
}
```

<h3 id="refresh-token">POST /auth/token/refresh</h3>

<h4>REQUEST:</h4>

```
{
  refresh: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwicm9sZSI6InVzZXIiLCJleHAiOjE2ODg4ODg4ODh9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
}
```

<h4>RESPONSE:</h4>

```
{
    access: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxNTU1Nzk1LCJpYXQiOjE3NDE1NTQyMDEsImp0aSI6IjQxZjlhMDgzZDc3NTQ1Nzc5MzVlYjU1ZDdkMmIxYWUzIiwidXNlcl9pZCI6MX0.LVBBXKoWAc2zj8mB68lMK1-X9fc4BULajVg1AL29Cyw'
}
```


<h3 id="get-all-events">GET /events</h3>

<h4>RESPONSE:</h4>

```
[
    {
        id: 'f75b6d05-439c-4af1-a2d9-8f7eb6efe19b',
        created_at: '2025-02-17T13:44:37.436230Z',
        updated_at: '2025-02-23T20:19:03.735480Z',
        active: true,
        description: 'Reunião de planejamento do projeto X',
        start: '2025-03-01T10:00:00Z',
        end: '2025-03-01T12:00:00Z',
        creator: 1,
        participants: []
    },
    {
        id: 'a1b2c3d4-e5f6-7890-1234-567890abcdef',
        created_at: '2025-02-20T09:00:00.000000Z',
        updated_at: '2025-02-22T15:30:00.000000Z',
        active: true,
        description: 'Aniversário da equipe',
        start: '2025-03-15T14:00:00Z',
        end: '2025-03-15T17:00:00Z',
        creator: 4,
        participants: []
    }
]
```

<h3 id="get-specific-event">GET /events/a1b2c3d4-e5f6-7890-1234-567890abcdef/</h3>

<h4>RESPONSE:</h4>

```
{
    id: 'a1b2c3d4-e5f6-7890-1234-567890abcdef',
    created_at: '2025-02-20T09:00:00.000000Z',
    updated_at: '2025-02-22T15:30:00.000000Z',
    active: true,
    description: 'Aniversário da equipe',
    start: '2025-03-15T14:00:00Z',
    end: '2025-03-15T17:00:00Z',
    creator: 4,
    participants: []
}
```

<h3 id="post-event">POST /events</h3>

<h4>REQUEST:</h4>

```
{
  description: 'Consulta médica de rotina',
  start: '2025-03-20T11:00:00Z',
  end: '2025-03-20T12:00:00Z',
  creator: 6
}
```

<h4>RESPONSE:</h4>

```
{
  id: '123e4567-e89b-12d3-a456-426614174000',
  created_at: '2025-02-23T20:30:00.000000Z',
  updated_at: '2025-02-23T20:30:00.000000Z',
  active: true,
  description: 'Consulta médica de rotina',
  start: '2025-03-20T11:00:00Z',
  end: '2025-03-20T12:00:00Z',
  creator: 6,
  participants: []
}
```

<h3 id="get-user-all-events">GET /users/6/events/</h3>

<h4>RESPONSE:</h4>

```
[
  {
    id: '123e4567-e89b-12d3-a456-426614174000',
    created_at: '2025-03-05T08:30:00.000000Z',
    updated_at: '2025-03-05T09:15:00.000000Z',
    active: true,
    description: 'Consulta médica de rotina',
    start: '2025-03-20T11:00:00Z',
    end: '2025-03-20T12:00:00Z',
    creator: 6,
    participants: []
  }
]
```

<h2 id="projec-actors">👷 Autores</h2>

* Emanuel Lacerda - Desenvolvedor - [@EmanuelLacerda](https://github.com/EmanuelLacerda/)

<h2 id="licenca">📄 Licença</h2>
Esse projeto está sob a licença MIT - acesse os detalhes <a href="https://github.com/EmanuelLacerda/kairos-webapp/blob/main/LICENSE">LICENSE.md</a>.

<h2>Créditos:</h2>
O layout das telas de login, criar conta e similares foram baseadas <a href="https://www.figma.com/community/file/872144934711314532">neste design de tela de login</a> publicado no FIGMA pelo usuário <a href="https://www.figma.com/@gorechajay">Ajay Gorecha(@gorechajay)</a>

<h2 id="contact">✉️ Contato</h2>
Se tiver alguma dúvida, quiser fazer sugestões, elogios, etc., se sinta livre para entrar em contato comigo por meio de um dos contatos abaixo:

- [in/emanuel-de-souza-lacerda](https://www.linkedin.com/in/emanuel-de-souza-lacerda/)
- emanuelsouzalacerda@gmail.com

