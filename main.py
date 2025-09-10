from app import app

app.secret_key = '6c376c5241534222528e1154395d5383e50cad503ff20c39'

if __name__ == '__main__':
    app.run(debug=True)
