from view import get_wsgi_app

app = get_wsgi_app()

if __name__ == '__main__':
    app.run()
