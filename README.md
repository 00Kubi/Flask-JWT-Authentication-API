# Flask JWT Authentication API

## Opis projektu
Ten projekt to prosty serwer API stworzony w Pythonie z wykorzystaniem frameworka Flask, który implementuje autoryzację i uwierzytelnianie użytkowników za pomocą tokenów JWT (JSON Web Token). API udostępnia podstawowe operacje logowania oraz dostęp do chronionych tras tylko dla zalogowanych użytkowników.

## Funkcje
- **Generowanie tokenu JWT** dla zalogowanych użytkowników.
- **Dekodowanie i weryfikacja tokenu JWT** przy każdej chronionej trasie.
- **Ochrona tras** z wykorzystaniem tokenów JWT.
- **Przykładowa trasa chroniona** dostępna tylko dla użytkowników z poprawnym tokenem JWT.

## Wymagania
Przed uruchomieniem projektu upewnij się, że masz zainstalowane następujące narzędzia:
- Python 3.x
- Flask
- Biblioteka JWT (`pyjwt`)
  
Aby zainstalować niezbędne zależności, uruchom polecenie:

```bash
pip install Flask pyjwt
```

## Struktura projektu
```
.
├── app.py          # Główna aplikacja Flask
├── README.md       # Dokumentacja
```

## Uruchomienie aplikacji

Aby uruchomić aplikację lokalnie, wykonaj następujące kroki:

1. Sklonuj repozytorium lub pobierz pliki projektu.
2. Uruchom aplikację:

```bash
python app.py
```

3. Serwer uruchomi się na adresie: `http://127.0.0.1:5000/`

## Endpointy API

### 1. Logowanie użytkownika - `/login`
**Metoda:** `POST`

Endpoint służy do logowania użytkownika i generowania tokenu JWT.

- **Nagłówki:**
  - `Content-Type: application/json`
  
- **Body (przykład):**
```json
{
  "username": "admin",
  "password": "password"
}
```

- **Odpowiedź (przykład):**
```json
{
  "token": "twój_token_jwt"
}
```

### 2. Chroniona trasa - `/protected`
**Metoda:** `GET`

Endpoint dostępny tylko dla zalogowanych użytkowników, którzy posiadają poprawny token JWT. Wymaga przesłania tokenu w nagłówku `x-access-token`.

- **Nagłówki (przykład):**
  - `x-access-token: <twój_token_jwt>`

- **Odpowiedź (przykład):**
```json
{
  "message": "Dostęp udzielony. Jesteś zalogowany jako użytkownik o ID: 1"
}
```

## Przykładowe użycie API

1. Wyślij żądanie `POST` na endpoint `/login`:

```bash
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{"username": "admin", "password": "password"}'
```

Przykład odpowiedzi:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2MjU4NDk1NTZ9.dhHs8jzT2mNGOEsWX3STP-ynGnNmA5DQ3dRIdaRZzKM"
}
```

2. Użyj otrzymanego tokenu, aby uzyskać dostęp do chronionej trasy `/protected`:

```bash
curl -X GET http://127.0.0.1:5000/protected \
-H "x-access-token: <twój_token_jwt>"
```

Przykład odpowiedzi:
```json
{
  "message": "Dostęp udzielony. Jesteś zalogowany jako użytkownik o ID: 1"
}
```

## Uwagi
- Token JWT wygasa po 1 godzinie od momentu zalogowania.
- W przypadku braku tokenu w nagłówku `x-access-token` lub wprowadzenia nieprawidłowego tokenu, serwer zwróci błąd 401 z odpowiednią wiadomością.