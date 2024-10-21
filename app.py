from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

# Sekretny klucz do kodowania i dekodowania tokenów JWT
app.config['SECRET_KEY'] = 'twoj_sekretny_klucz'

# Funkcja generująca token JWT dla zalogowanego użytkownika
def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token ważny przez 1 godzinę
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

# Dekorator sprawdzający, czy użytkownik jest zalogowany
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Sprawdzanie, czy token jest obecny w nagłówkach żądania
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message': 'Brak tokenu!'}), 401

        try:
            # Dekodowanie tokenu JWT
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except:
            return jsonify({'message': 'Token jest nieprawidłowy lub wygasł!'}), 401

        return f(current_user_id, *args, **kwargs)
    
    return decorated

# Dodaj trasę główną
@app.route('/')
def home():
    return jsonify({'message': 'Witaj w API autoryzacji użytkowników!'})

# Przykład logowania użytkownika
@app.route('/login', methods=['POST'])
def login():
    auth = request.json  # Zakładamy, że dane są przesyłane jako JSON
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Nieprawidłowe dane logowania!'}), 401
    
    # Zakładamy, że użytkownik o ID 1 ma username "admin" i password "password"
    if auth['username'] == 'admin' and auth['password'] == 'password':
        token = generate_token(user_id=1)
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Nieprawidłowa nazwa użytkownika lub hasło!'}), 401

# Przykład chronionej trasy
@app.route('/protected', methods=['GET'])
@token_required
def protected(current_user_id):
    return jsonify({'message': f'Dostęp udzielony. Jesteś zalogowany jako użytkownik o ID: {current_user_id}'})

if __name__ == '__main__':
    app.run(debug=True)
