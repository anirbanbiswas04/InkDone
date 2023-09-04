from inkdone import create_app

app = create_app()

if __name__ == '__main__':
    app.app(debug=True)