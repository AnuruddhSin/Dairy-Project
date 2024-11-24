from app import create_app

app = create_app()

if __name__ == "__main__":
    # During Production/Deployment change debug=True to False
    app.run(debug=True)

