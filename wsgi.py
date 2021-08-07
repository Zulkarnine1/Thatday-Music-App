from main import app
from env import IS_PROD

if __name__ == "__main__":
    app.run(debug=IS_PROD)