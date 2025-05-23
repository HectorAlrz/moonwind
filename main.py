import os

from flask import Flask, send_file, render_template
from src.queries.user_queries import UserQueries

app = Flask(__name__, template_folder='src/templates')

@app.route("/")
def index():
    return send_file('src/index.html')

@app.route('/users')
def user_queries():
    user_queries_instance = UserQueries()
    users = user_queries_instance.get_all_users()
    return render_template('user_queries.html', users=users)

## TODO: create route for this queries
# @app.route('/codigo-facilito')
# def user_queries():
#     user_queries_instance = UserQueries()
#     users = user_queries_instance.get_all_users()
#     return render_template('codigo_facilito.html', users=users)

def main():
    app.run(port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    main()