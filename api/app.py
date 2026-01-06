from flask import Flask

def create_app():
    app = Flask(__name__)
    
    from api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000, threaded=True, use_reloader=False)