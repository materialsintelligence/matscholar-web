from matscholar_web.callbacks import app

server = app.server

if __name__ == '__main__':
    print("starting...")
    app.run_server(debug=True)
