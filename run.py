from app import create_app, insert_sample_data

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        insert_sample_data()
    app.run()
