# Educa

![Screenshot from 2022-06-28 15-29-51](https://user-images.githubusercontent.com/59217330/176256435-61e44864-b525-4015-a9d4-fa4ef127687a.png)


O educa é uma plataforma de cursos online inspirada na udemy.


## Tecnologias usadas

Abaixo está a lista de todas as tecnologias usadas para a construção desse projeto.

* [Django](https://docs.djangoproject.com/en/4.0/)
* [Django Rest Framework](https://www.django-rest-framework.org/)
* [PostgreSQL](https://www.jetbrains.com/datagrip/features/?source=google&medium=cpc&campaign=15034928143&term=postgresql&gclid=CjwKCAjwzeqVBhAoEiwAOrEmzXvmumNvZqv3cvPSzs16PuethLHO7dukXPMc3g6XyhQkcsiHkCnHKRoCNt4QAvD_BwE)
* [Tailwind](https://tailwindcss.com/)
* [Redis](https://redis.io/)
* [Selenium](https://www.selenium.dev/)

## Iniciando projecto

Siga os passos abaixo para iniciar o projeto localmente em sua máquina.

### Instalação

Primeiro passo é clonar o projeto dentro do seu editor de código dessa maneira.

```
git clone https://github.com/gabrielustosa/educa.git
```

Agora, dentro da pasta que você baixou inicie um ambiente virtual.

```
python3 -m venv venv
source venv/bin/activate
```

Instale todos os pacotes necessários

```
pip install youtube-dl && pip install -r requirements.txt
```

Ajuste o .env

```
cp .env-example .env
nano .env
```

Faça as migrações 

```
python manage.py migrate
``` 

### Observação

Certfique-se de que você tenha o Redis instalado e com um banco de dados local iniciado para o funcionamento correto do servidor.

## Contato

Gabriel Lustosa Queiroz - [@gabrielustosa](https://www.linkedin.com/in/gabrielustosa) -  me@gabrielustosa.com.br

Link para o projeto: https://educa.gabrielustosa.com.br

