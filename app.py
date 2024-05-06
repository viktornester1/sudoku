import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from models import User, Game, db
import sudoku_generator

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sudoku.db'
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('game'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/game', methods=['GET', 'POST'])
def game():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        data = request.get_json()
        difficulty_level = data.get('difficulty', 'easy')
        board_str = data.get('board', '')
        if board_str:
            submitted_board = [list(map(int, row)) for row in board_str.split(',')]
        else:
            submitted_board = []
        time_taken = int(data.get('time_taken', '0'))
        completed = data.get('completed', False)
        solution_board = data.get('solution', [])

        user_id = session['user_id']
        difficulty = 1 if difficulty_level == 'easy' else 2 if difficulty_level == 'medium' else 3

        game = Game(user_id=user_id, difficulty=difficulty, time_taken=time_taken, completed=completed, board=board_str, puzzle=json.dumps(submitted_board), solution=json.dumps(solution_board))
        db.session.add(game)
        db.session.commit()

    difficulty_level = request.args.get('difficulty', 'easy')
    board, solution = sudoku_generator.generate_sudoku(difficulty_level)

    print("Solution Board:")
    for row in solution:
        print(row)

    if request.headers.get('Accept') == 'application/json':
        return jsonify({'board': board, 'solution': solution})

    return render_template('game.html', board=board, solution=solution, difficulty=difficulty_level)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/stats')
def stats():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    if not user:
        return "User not found", 404

    games = user.games.all()

    stats = {
        'easy': {'games_played': 0, 'games_completed': 0, 'total_time': 0},
        'medium': {'games_played': 0, 'games_completed': 0, 'total_time': 0},
        'hard': {'games_played': 0, 'games_completed': 0, 'total_time': 0}
    }

    for game in games:
        difficulty_level = 'easy' if game.difficulty == 1 else 'medium' if game.difficulty == 2 else 'hard'
        stats[difficulty_level]['games_played'] += 1

        if game.completed:
            stats[difficulty_level]['games_completed'] += 1
            stats[difficulty_level]['total_time'] += game.time_taken

    return render_template('stats.html', stats=stats, user=user)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)