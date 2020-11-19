from flask import Flask, render_template, request, g
import sqlite3
import random

DATABASE = 'test.db'

app = Flask(__name__, template_folder='templates')

def get_db():
    db = getattr(g, '_database',None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database',None)
    if db is not None:
        db.close()

# # ONLY RUN ON FIRST EXECUTION!
# def create_dbtable():
#     cursor = get_db().cursor()
#     cursor.execute('CREATE TABLE articles (title TEXT, author TEXT, contents TEXT)')

@app.route('/', methods=['GET'])
def main():
    # create_new_article_page('Jack', 'Jacksz', 'Jackkk')
    # create_new_article_page('Jack','Jay','s')
    create_new_article_page('Jack Donofrio','Jack Donofrio','SJ Class of 2021. Started Coding Club')
    # access_article_by_title('Jack')
    # delete_article_by_title('Jack')
    return render_template(
        'index.html',
        ip=request.remote_addr
    )

@app.route('/about')
def aboutpage():
    return render_template(
        'about.html'
    )

# Sends user to random article
@app.route('/random')
def randompage():
    cursor = get_db().cursor()
    rows = cursor.execute(f"SELECT title, author, contents FROM articles").fetchall()
    random_row = rows[random.randint(0,len(rows)-1)]
    return render_template(
        'articlepage.html',
        title=random_row[0],
        author=random_row[1],
        contents=random_row[2]
    )

@app.route('/new/article')
def new_article_page():
    return render_template('')

class Article:
    def __init__(self, title, author, contents):
        self.title = title
        self.author = author
        self.contents = contents

# remember to replace spaces in title with dashes and to perform strip() to cut off end spaces
@app.route('/article/<string:title>')
def load_article(title):
    title = title.replace('-', ' ')
    article = access_article_by_title(title)
    return render_template(
        'articlepage.html',
        title=article.title,
        author=article.author,
        contents=article.contents
    )

def create_table(connection, create_table_sql):
    try:
        c = connection.cursor()
        c.execute(create_table_sql)
        print('success')
    except Error as e:
        print(e)

def create_new_article_page(title, author, contents):
    connection = get_db()
    cursor = connection.cursor()
    # adds row if title does not exist yet
    cursor.execute(f"""INSERT INTO articles(title,author,contents)
                    SELECT '{title}', '{author}', '{contents}'
                    WHERE NOT EXISTS (SELECT 1 FROM articles WHERE title = '{title}');
                    """)
    connection.commit()

def delete_article_by_title(title):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(f"""
        DELETE FROM articles
        WHERE title = '{title}'
    """)
    connection.commit()

def access_article_by_title(title):
    cursor = get_db().cursor()
    row = cursor.execute(f"SELECT title, author, contents FROM articles WHERE title LIKE '%{title}%'").fetchone()
    if row is None:
        return Article('Article Does Not Exist','Nobody','Congratulations, this article doesn\'t exist!')
    return Article(row[0],row[1],row[2])

def modify_article_title(old_title, new_title):
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute(f"UPDATE articles SET title = '{new_title}' WHERE title = '{old_title}'")
    connection.commit()

# TO-DO: Add validation to prevent SQL-Injection attacks
def validate_entry(text):
    return text.strip()






if __name__ == '__main__':
    app.run(debug=True)