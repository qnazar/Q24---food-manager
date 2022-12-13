from application import init_app, celery


app = init_app(celery=celery)

if __name__ == '__main__':
    app.run(debug=True)
