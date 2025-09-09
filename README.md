<h1 align="center" style="font-weight: bold;">Kairos WebApp 💻</h1>
<p align="center">
 <a href="#tech">Tecnologias usadas</a> • 
 <a href="#feature-list">Funcionalidades</a> •
 <a href="#demonstration">Demonstrações</a> •
 <a href="#instalation-guide">Guia de instalação</a> • 
 <a href="#api-endpoints">API Endpoints</a> •
 <a href="#projec-actors">Autores</a> • 
 <a href="#licenca">Licença</a> • 
 <a href="#credit">Créditos</a> • 
 <a href="#contact">Contato</a>
</p>
<p align="center">
  <img src="https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D">
  <img src="https://img.shields.io/badge/Quasar-16B7FB?style=for-the-badge&logo=quasar&logoColor=black">
  <img src="https://img.shields.io/badge/Sass-CC6699?style=flat-square&logo=Sass&logoColor=white">
  <img src="https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray"></img>
  <img src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white"></img>
</p>

<h2>Gerenciamento Seguro de Eventos Pessoais</h2>

O Kairos é uma aplicação full-stack robusta para gerenciamento de eventos pessoais, construída com foco em segurança e integridade de dados. Ele possuí um sistema que minimiza a possibilidade de alterações indevidas em eventos. Vamos entender melhor isto?

Enquanto um evento não começou(ou seja, a data atual é anterior a data de início dele), todos os dados dele podem ser alterados. Quando o evento começa, a data de início não pode ser mais alterada e todos os outros dados podem ser alterados. Quando o evento termina, nenhum dado dele pode ser mais alterado. Além disto, eventos já finalizados não podem ser removidos. No caso, estas alterações e remoção não podem ocorrer pelo aplicativo web, mas, pela tela de administração continuam podendo ser alterados e removidos.

Por um lado, não existir estas limitações pode ser útil em contextos, por exemplo, que a data de início de eventos mudam de última hora frequentemente. Por outro lado, a falta destas limitações torna o histórico de eventos facilmente manipuláveis, o que será uma brecha grave de seguranças em cenários com a necessidade de histórico preciso de eventos. Portanto, este projeto foi desenvolvido justamente para usuários que que valorizam a segurança e a rastreabilidade de seus eventos.

Para finalizar, quero destacar que este projeto foi desenvolvido para demonstrar minha proeficiência em desenvolvimento full-stack, desde a arquitetura de banco de dados, lógica de backend, design de API, até a implementação do frontend responsivo e interativo.

Agora, você sabe o básico sobre este app. Quer conhecer mais sobre ele? Só ler o restante abaixo.

<img src="https://github.com/user-attachments/assets/9815f7a5-83a6-47f1-b7c6-2bb2599a2152" />

<h2 id="tech">📦 Tecnologias usadas:</h2>

<h3>Frontend:</h3>

- **Base:** HTML5, CSS3, JavaScript (ES6+)
- **Reatividade:** [Vue 3(Composition API com script setup)](https://vuejs.org/) e [Quasar 2](https://quasar.dev/)
- **Gerenciamento de estado:** [Pinia](https://pinia.vuejs.org/)
- **Gerenciamento de rotas:** [Vue-Router](https://router.vuejs.org/)
- **Calendário:** [FullCalendar](https://fullcalendar.io/)
- **CSS:** Sass
- **Requisição HTTP:** Axios
- **Demais tecnologias:** jwt-decode, [Bootstrap Icons](https://icons.getbootstrap.com/) e SweetAlert2

<h3>Backend:</h3>

- **Lógica do servidor:** [Django](https://www.djangoproject.com/)
- **API:** [Django REST Framework(API)](https://www.django-rest-framework.org/)
- **Gerenciamento de sessão:** Simple JWT

<h3>Controle de Versão:</h3>

- Git com Conventional Commits e seguindo Git-Flow

<h2 id="feature-list">⚙️ Funcionalidades:</h2>

**Funcionalidades de autenticação:**
- **Criação de de conta:** Processo intuitivo com verificação de e-mail no final para garantir que o novo usuário realmente tem acesso ao e-mail informado.
- **Login:** O usuário acessa o sistema por meio de e-mail e senha válidos e tem sua sessão mantida por meio de JWT.
- **Logout:** O usuário pode deslogar manualmente a qualquer momento, bem como ser deslogado automaticamente quando o refresh token não for mais válido.

**Funcionalidades de gerenciamento de eventos:**
- **Criação de Eventos:** Adição fácil de novos compromissos e atividades com duração variada (um ou múltiplos dias).
- **Visualização em Calendário:** Acompanhamento dos eventos de maneira clara e organizada utilizando a biblioteca FullCalendar.
- **Edição de Eventos:** Edição simples e rápida dos eventos, com restrições inteligentes para garantir a consistência dos dados:
    - Não é possível alterar o período de início de um evento após seu início.
    - Eventos já finalizados não podem ser editados.
- **Remoção de Eventos:** Possibilidade de excluir qualquer evento ainda não finalizado.

<h2 id="demonstration">▶️ Demonstrações:</h2>

<h3>Autenticação:</h3>

<h4>Criação de conta:</h4>

https://github.com/user-attachments/assets/ad14d643-28b1-4594-9eb5-e8a577e6f0a0

<h4>Verificação de e-mail:</h4>

O código que o usuário passa para verificar seu e-mail é um OTP enviado para o respectivo e-mail após a conta ser criada com sucesso.

No momento, não existe restrição nos endpoints de gerenciamento de eventos para usuários sem e-mail verificado. Devido a isto, os usuários sem e-mail verificado não pode fazer login. O objetivo é que em futuras versões um usuário sem o e-mail verificado consiga fazer login e ver o calendário, porém, não consiga agendar nenhum evento.

https://github.com/user-attachments/assets/549f9091-3321-40a2-8429-a2d4a71ba66c


<h4>Login:</h4>

Conforme demonstra o vídeo abaixo, o login é feito a partir do e-mail e senha do usuário. Quando o login é efetuado com sucesso, a requisição de login, dentre outras informações, retorna os tokens JWT(access token e refresh token).

O access token é utilizado para manter a sessão do usuário ativa durante um período curto. O access token de duração curta foi escolhido para evitar que, em caso de descoberta do access token por outra pessoa, consiga evitar outra pessoa possa fazer requisições com o access token roubado por muito tempo.

Esta abordagem de segurança exige o usuário fazer o login muito frenquentemente. Para evitar este efeito colateral, é utilizado o refresh token para criar um novo access token sempre que a validade do atual acabar. Como o refresh token tem um tempo grande de validade, demora muito tempo até o usuário precisar fazer o login novamente.

Em futuras versões, será aplicada a estratégia de Refresh Token Rotation para tornar o gerenciamento de sessão ainda mais seguro.

https://github.com/user-attachments/assets/c48733c4-9816-4c32-b6ca-5689bcf22284

<h4>Logout:</h4>

Conforme demonstrado no vídeo abaixo, se o usuário estiver deslogado, ele é redirecionado para tela de login sempre que tentar acessar a home.

https://github.com/user-attachments/assets/66934918-e36f-4f44-b00a-50bbde5545e7

<h3>Gerenciamento de eventos:</h3>

<h4>Criação e visualização de evento:</h4>

Conforme demonstrado no vídeo abaixo, a criação começa clicando na célula do calendário que é respectiva ao dia inicial do evento, podendo o evento durar tanto 1 dia quanto múltiplos dias(o vídeo abaixo só mostra o caso em que o evento dura múltiplos dias). Além disto, os eventos são associados ao id do usuário que os criou. Em futuras versões, será possível convidar outros usuários para participar do evento.

Também conforme mostrado no vídeo abaixo, quando o evento é criado, um "link" para o respectivo evento aparece no calendário conforme a duração dele e a abertura dele é feita clicando nesse "link".

Falando mais sobre a visualização, vale destacar como o carregamento dos eventos no calendário ocorre. Um primeiro filtro para o carregamento é os eventos serem do usuário logado, o que é indispensável para manter a privacidade da lista de eventos de cada usuário. O segundo filtro é o período de tempo da view do calendário para o qual os eventos serão carregados. Por exemplo, os eventos da view semanal só irá crregar os eventos que a duração incluí os dias da respectiva semana. Este segundo filtro tem como objetivo otimizar o tamanho das requisições, pois será muito pesado ter que carregar todos os eventos do usuário sempre que ele mudar de view. Principalmente, no caso de usuários com muito eventos.


https://github.com/user-attachments/assets/f85914e4-41ee-4dd4-8620-3654a3c281c4

<h4>Edição de evento:</h4>

https://github.com/user-attachments/assets/cd5ef441-3062-467c-85fd-6d133a97d33b

<h4>Exclusão de evento:</h4>

https://github.com/user-attachments/assets/7802e5e0-652f-494c-8a32-5b00cf538b45

<h4>Lógica de Gerenciamento de Eventos:</h4>

O objetivo do Kairos é ser um software de agendamento de eventos pessoais. Considerando isto, as seguintes regras são necessárias:
- Eventos não podem ser agendados para uma data anterior a atual.
- O período inicial não pode ser posterior ao período final.

Elas são aplicadas tanto nas requisições de criação e edição de eventos quanto no frontend referente a estas operações.

Além disto, as requisições de criação e edição de eventos quanto o respectivo frontend foram desenvolvidos para não permitir que eventos sejam definidos para períodos que entram em conflito com outros eventos. Isto incluí não permitir que eventos sejam definidos para o exato mesmo período de outros, nem permitir que eventos sejam definidos para um período que tem intersecção com o período de outros eventos. Isto foi criado para evitar conflitos na agenda dos usuários.

Existe a possibilidade de que um usuário precise/queira realizar outros eventos entre o período de algum evento. Por exemplo, ficará 4 dias em um Congresso e precisa fazer uma reunião entre este período. As regras atuais do Kairos não permitiriam haver esses dois eventos na agenda do usuário. Então, em versões futuras, será adicionada a opção do usuário informar se ele permite intersecções de período com o respectivo evento.

Finalizando, o Kairos possuí regras relacionadas a até quando eventos podem ser editados e removidos:
- Enquanto um evento não começou(ou seja, a data atual é anterior a data de início dele), todos os dados dele podem ser alterados.
- Quando o evento começa, a data de início não pode ser mais alterada e todos os outros dados podem ser alterados.
- Quando o evento termina, nenhum dado dele pode ser mais alterado.
- Eventos já finalizados não podem ser removidos.

No caso, estas alterações e remoção não podem ocorrer pelo aplicativo web, mas, pela tela de administração continuam podendo ser alterados e removidos.

Por um lado, não existir estas limitações pode ser útil em contextos, por exemplo, que a data de início de eventos mudam de última hora frequentemente. Por outro lado, a falta destas limitações torna o histórico de eventos facilmente manipuláveis, o que será uma brecha grave de seguranças em cenários com a necessidade de histórico preciso de eventos. Portanto, este projeto foi desenvolvido justamente para usuários que que valorizam a segurança e a rastreabilidade de seus eventos.

Esta é toda a lógica de gerenciamento de eventos neste app. Agora, você pode testar o Kairos para ver esta lógica na prática. Inclusive, abaixo segue o tutorial de como executar ele.

<h2 id="instalation-guide">🛠️ Guia de instalação:</h2>

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
python3 manage.py runserver
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

<h2 id="api-endpoints">🔗 API Endpoints:</h2>

A API provém os seguintes endpoints:

| rota               | descrição                                          
|----------------------|-----------------------------------------------------
| <kbd>POST /auth/register/</kbd>     | Registra um novo usuário [Ver detalhes](#post-user)
| <kbd>POST /auth/verify-email/</kbd>     | Verifica o e-mail de um usuário [Ver detalhes](#verify-email-user)
| <kbd>POST /auth/login/</kbd>     | Retorna o access e o refresh token de um usuário [Ver detalhes](#login-user)
| <kbd>POST /auth/logout/</kbd>     | Adiciona o refresh token de um usuário na blacklist [Ver detalhes](#logout-user)
| <kbd>GET /auth/profile/</kbd>     | Verifica a validade do access token de um usuário [Ver detalhes](#check-the-validity-access-token)
| <kbd>POST /auth/token/refresh/</kbd>     | Gera um novo access token para um usuário [Ver detalhes](#refresh-token)
| <kbd>POST /auth/password-reset/</kbd>     | Solicita mudança de senha [Ver detalhes](#refresh-token)
| <kbd>GET /auth/password-reset-confirm/{uidb64}/{passwordResetToken}/</kbd> | Verifica se o token de mudança de senha é válido [Ver detalhes](#password-reset-confirm)
| <kbd>PATCH /auth/set-new-password/</kbd> | Muda a senha [Ver detalhes](#set-new-password)
| <kbd>GET /events</kbd>     | Pega a lista de todos os eventos. [Ver detalhes](#get-all-events)
| <kbd>GET /events/{eventUUID}/</kbd>     | Pega um evento específico por UUID. [Ver detalhes](#get-specific-event)
| <kbd>POST /events</kbd>     | Registra um novo evento [Ver detalhes](#post-event)
| <kbd>PUT /events/{eventUUID}/</kbd>     | Edita os dados de um evento específico por UUID
| <kbd>PATCH /events/{eventUUID}/</kbd>     | Edita os dados de um evento específico por UUID
| <kbd>DELETE /events/{eventUUID}/</kbd>     | Remove um evento específico por UUID
| <kbd>GET /users/{userId}/eventUUID/</kbd>     | Pega todos os eventos de um usuário específico por UUID. [Ver detalhes](#get-user-all-events)


<h3 id="post-user">POST /auth/register/</h3>

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

<h3 id="verify-email-user">POST /auth/verify-email/</h3>

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

<h3 id="login-user">POST /auth/login/</h3>

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

<h3 id="logout-user">POST /auth/logout/</h3>

<h4>REQUEST:</h4>

```
{
  refresh_token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwicm9sZSI6InVzZXIiLCJleHAiOjE2ODg4ODg4ODh9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
}
```

<h3 id="check-the-validity-access-token">POST /auth/profile/</h3>

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

<h3 id="refresh-token">POST /auth/token/refresh/</h3>

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

<h3 id="password-reset">POST /auth/password-reset/</h3>

<h4>REQUEST:</h4>

```
{
  email: 'emanuellacerda@gmail.com'
}
```

<h4>RESPONSE:</h4>

```
{
    message: 'Um link foi enviado para seu e-mail para redefinir sua senha'
}
```

<h3 id="password-reset-confirm">GET /auth/password-reset-confirm/</h3>

<h4>RESPONSE:</h4>

```
{
    success: true,
    message: 'Credenciais são válidas',
    uidb64: 'OA',
    token: 'cmfa98-977a1ffcda77d9d43fee15f27c0e3e28'
}
```

<h3 id="set-new-password">PATCH /auth/set-new-password/</h3>

<h4>REQUEST:</h4>

```
{
  "password": "758$JFJ388lka@",
	"confirm_password": "758$JFJ388lka@",
	"uidb64": "OA",
	"token": "cmf783-35b27aa704b3d4b6e9010f6b1ab79c54"
}
```

<h4>RESPONSE:</h4>

```
{
  message: 'Sua senha foi redefinida com sucesso'
}
```

<h3 id="get-all-events">GET /events/</h3>

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

<h3 id="post-event">POST /events/</h3>

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

<h2 id="future-features">Funcionalidades futuras:</h2>

Ao longo do conteúdo acima, falo as funcionalidades/melhorias futuras. Abaixo segue a lista completa e organizada, com o link do respectivo issue em cada funcionalidade:
- [ ] Restrição de criação, edição e remoção de eventos a somente usuários com e-mail verificado - [Issue #3](https://github.com/EmanuelLacerda/kairos-webapp/issues/3);
- [ ] Estratégia de Refresh Token Rotation no gerenciamento de sessão com JWT - [Issue #8](https://github.com/EmanuelLacerda/kairos-webapp/issues/8);
- [ ] Convidar outros usuários para participar dos eventos criados pelo usuário - [Issue #9](https://github.com/EmanuelLacerda/kairos-webapp/issues/9).
- [ ] Definir que um evento pode ter intersecção de período com outros eventos - [Issue #10](https://github.com/EmanuelLacerda/kairos-webapp/issues/10).

<h2 id="projec-actors">🧑‍💻 Autores:</h2>

* Emanuel Lacerda - Desenvolvedor - [@EmanuelLacerda](https://github.com/EmanuelLacerda/)

<h2 id="licenca">📄 Licença:</h2>
Esse projeto está sob a licença MIT - acesse os detalhes <a href="https://github.com/EmanuelLacerda/kairos-webapp/blob/main/LICENSE">LICENSE.md</a>.

<h2 id="credit">🙏 Créditos:</h2>
O layout das telas de login, criar conta e similares foram baseadas <a href="https://www.figma.com/community/file/872144934711314532">neste design de tela de login</a> publicado no FIGMA pelo usuário <a href="https://www.figma.com/@gorechajay">Ajay Gorecha(@gorechajay)</a>

<h2 id="contact">✉️ Contato:</h2>
Se tiver alguma dúvida, quiser fazer sugestões, elogios, etc., se sinta livre para entrar em contato comigo por meio de um dos contatos abaixo:

- [in/emanuel-de-souza-lacerda](https://www.linkedin.com/in/emanuel-de-souza-lacerda/)
- emanuelsouzalacerda@gmail.com
