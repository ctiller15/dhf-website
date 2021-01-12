DHF - A website to track fictional characters

[Figma](https://www.figma.com/file/IdY8QLekrR0EpmGWH3A2aD/DHF_Site?node-id=0%3A1)

[Database Diagram](https://lucid.app/lucidchart/76e43fbc-96b1-4c4f-8ab0-25a2b610cd84/view?page=0_0#)

set up environment variables:
`cp .env.example .env`
Edit the enviroment variables to correspond to your current environment.

Run the tests:
First ensure your postgres user can run the tests:
`ALTER USER <username> CREATEDB;`

`python manage.py test`
