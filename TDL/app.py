from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    deadline = db.Column(db.Date, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        """Converts the Todo object to a dictionary."""
        return {
            'id': self.id,
            'task': self.task,
            'category': self.category,
            'deadline': self.deadline.strftime('%Y-%m-%d') if self.deadline else None,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }

@app.before_request
def create_tables():
    db.create_all()

@app.route('/todos', methods=['GET'])
def get_todos():
    """Retrieve all todo items."""
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    return jsonify([todo.to_dict() for todo in todos])

@app.route('/todos', methods=['POST'])
def add_todo():
    """Add a new todo item."""
    data = request.get_json()
    new_task = data.get('task')
    if not new_task:
        return jsonify({'error': 'Task is required'}), 400

    deadline = None
    if data.get('deadline'):
        try:
            deadline = datetime.strptime(data.get('deadline'), '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    todo = Todo(
        task=new_task,
        category=data.get('category'),
        deadline=deadline
    )
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201

@app.route('/todos/<int:todo_id>/complete', methods=['PUT'])
def complete_todo(todo_id):
    """Mark a todo item as complete or incomplete."""
    todo = db.session.get(Todo, todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    data = request.get_json()
    completed_status = data.get('completed', False)

    todo.completed = bool(completed_status)
    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo item."""
    todo = db.session.get(Todo, todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully'}), 200

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo item's task, category, and deadline."""
    todo = db.session.get(Todo, todo_id)
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    data = request.get_json()

    if 'task' in data:
        todo.task = data['task']
    if 'category' in data:
        todo.category = data['category']
    if 'deadline' in data:
        if data['deadline']:
            try:
                todo.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400
        else:
            todo.deadline = None

    db.session.commit()
    return jsonify(todo.to_dict())

@app.route('/')
def index():
    """Render the main HTML page."""
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    return render_template('index.html', todos=todos)

if __name__ == '__main__':
    app.run(debug=True)
