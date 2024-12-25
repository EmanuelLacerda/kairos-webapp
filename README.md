<h1 align="center" style="font-weight: bold;">Kairos WebApp 💻</h1>

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
npx quasar dev //ou
quasar dev // este segundo comando só funcionará se tiver o Quasar instalado globalmente
```

*Obs.: Para o projeto funcionar corretamente, api e frontend devem estar em execução ao mesmo tempo.
