from bruno import create_app, create_socketio

app = create_app()
socketio = create_socketio(app)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
