from app import app

@app.route('/')
def index():
    return f'<h1>Hello world</h1>'