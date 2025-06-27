from flask import Flask, request, jsonify

app = Flask(__name__)

users = {}
next_user_id = 1

@app.route('/')
def home():
    """
    Home route to confirm the API is running.
    """
    return "<h1>User Management API</h1><p>Use /users endpoint to manage users.</p>"

@app.route('/users', methods=['GET'])
def get_users():
    """
    GET /users
    Retrieves all users.
    """
    return jsonify(list(users.values()))

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    GET /users/<user_id>
    Retrieves a single user by ID.
    """
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    """
    POST /users
    Creates a new user.
    Expects JSON data with 'name' and 'email'.
    """
    global next_user_id
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    new_user = {
        "id": next_user_id,
        "name": name,
        "email": email
    }
    users[next_user_id] = new_user
    next_user_id += 1
    return jsonify(new_user), 201 # 201 Created

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    PUT /users/<user_id>
    Updates an existing user.
    Expects JSON data with 'name' and/or 'email'.
    """
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    if 'name' in data:
        user['name'] = data['name']
    if 'email' in data:
        user['email'] = data['email']

    return jsonify(user)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    DELETE /users/<user_id>
    Deletes a user by ID.
    """
    if user_id in users:
        deleted_user = users.pop(user_id)
        return jsonify({"message": f"User {deleted_user['name']} with ID {user_id} deleted successfully"})
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
