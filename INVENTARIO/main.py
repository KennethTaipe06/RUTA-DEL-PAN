from flask import Flask, render_template
from routes.inventarios import inventario_bp

app = Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(inventario_bp)

@app.route('/')
def home():
    # Sirve el archivo index.html desde la carpeta templates
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
