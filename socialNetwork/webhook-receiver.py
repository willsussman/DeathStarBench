from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/home-timeline-redis-query-file', methods=['GET'])
def home_timeline_redis_query_file():
    try:
        with open('home_timeline_redis_webhook_data.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found", 404

@app.route('/media-memcached-query-file', methods=['GET'])
def media_memcached_query_file():
    try:
        with open('media_memcached_webhook_data.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found", 404

@app.route('/media-mongodb-query-file', methods=['GET'])
def media_mongodb_query_file():
    try:
        with open('media_mongodb_webhook_data.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found", 404

@app.route('/post-storage-memcached-query-file', methods=['GET'])
def post_storage_memcached_query_file():
    try:
        with open('post_storage_memcached_webhook_data.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found", 404

@app.route('/post-storage-mongodb-query-file', methods=['GET'])
def post_storage_mongodb_query_file():
    try:
        with open('post_storage_mongodb_webhook_data.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found", 404

@app.route('/social-graph-mongodb-query-file', methods=['GET'])
def social_graph_mongodb_query_file():
    try:
        with open('social_graph_mongodb_webhook_data.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found", 404

@app.route('/social-graph-redis-query-file', methods=['GET'])
def social_graph_redis_query_file():
    try:
        with open('social_graph_redis_webhook_data.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found", 404

@app.route('/url-shorten-memcached-query-file', methods=['GET'])
def url_shorten_memcached_query_file():
    try:
        with open('url_shorten_memcached_webhook_data.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found", 404

@app.route('/url-shorten-mongodb-query-file', methods=['GET'])
def url_shorten_mongodb_query_file():
    try:
        with open('url_shorten_mongodb_webhook_data.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found", 404

@app.route('/user-memcached-query-file', methods=['GET'])
def user_memcached_query_file():
    try:
        with open('user_memcached_webhook_data.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found", 404

@app.route('/user-mongodb-query-file', methods=['GET'])
def user_mongodb_query_file():
    try:
        with open('user_mongodb_webhook_data.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found", 404

@app.route('/user-timeline-mongodb-query-file', methods=['GET'])
def user_timeline_mongodb_query_file():
    try:
        with open('user_timeline_mongodb-webhook_data.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found", 404

@app.route('/user-timeline-redis-query-file', methods=['GET'])
def user_timeline_redis_query_file():
    try:
        with open('user_timeline_redis_webhook_data.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found", 404


# @app.route('/webhook', methods=['POST'])
# def webhook():
#     # data = json.loads(request.data)
#     # # print("Received alert:", data)
    
#     # # Custom code execution based on alert
#     # # For example, sending a notification, logging, etc.
#     # with open('webhook_data.txt', 'a') as f:
#     #     f.write(data)
#     #     f.write('\n')
#     # return "Alert received", 200

#     data = request.json  # Assuming the incoming data is in JSON format
#     with open('webhook_data.txt', 'a') as file:  # 'a' for append mode
#         # file.write(str(data) + '\n')
#         file.write(json.dumps(data) + '\n')
#     return "Data received", 200

@app.route('/home-timeline-redis-webhook', methods=['POST'])
def home_timeline_redis_webhook():
    data = request.json  # Assuming the incoming data is in JSON format
    with open('home_timeline_redis_webhook_data.txt', 'a') as file:  # 'a' for append mode
        file.write(json.dumps(data) + '\n')
    return "Data received", 200

@app.route('/media-memcached-webhook', methods=['POST'])
def media_memcached_webhook():
    data = request.json  # Assuming the incoming data is in JSON format
    with open('media_memcached_webhook_data.txt', 'a') as file:  # 'a' for append mode
        file.write(json.dumps(data) + '\n')
    return "Data received", 200

@app.route('/media-mongodb-webhook', methods=['POST'])
def media_mongodb_webhook():
    data = request.json  # Assuming the incoming data is in JSON format
    with open('media_mongodb_webhook_data.txt', 'a') as file:  # 'a' for append mode
        file.write(json.dumps(data) + '\n')
    return "Data received", 200

@app.route('/post-storage-memcached-webhook', methods=['POST'])
def post_storage_memcached_webhook():
    data = request.json  # Assuming the incoming data is in JSON format
    with open('post_storage_memcached_webhook_data.txt', 'a') as file:  # 'a' for append mode
        file.write(json.dumps(data) + '\n')
    return "Data received", 200

@app.route('/post-storage-mongodb-webhook', methods=['POST'])
def post_storage_mongodb_webhook():
    data = request.json  # Assuming the incoming data is in JSON format
    with open('post_storage_mongodb_webhook_data.txt', 'a') as file:  # 'a' for append mode
        file.write(json.dumps(data) + '\n')
    return "Data received", 200

@app.route('/social-graph-mongodb-webhook', methods=['POST'])
def social_graph_mongodb_webhook():
    data = request.json  # Assuming the incoming data is in JSON format
    with open('social_graph_mongodb_webhook_data.txt', 'a') as file:  # 'a' for append mode
        file.write(json.dumps(data) + '\n')
    return "Data received", 200

@app.route('/social-graph-redis-webhook', methods=['POST'])
def social_graph_redis_webhook():
    data = request.json  # Assuming the incoming data is in JSON format
    with open('social_graph_redis_webhook_data.txt', 'a') as file:  # 'a' for append mode
        file.write(json.dumps(data) + '\n')
    return "Data received", 200

@app.route('/url-shorten-memcached-webhook', methods=['POST'])
def url_shorten_memcached_webhook():
    data = request.json  # Assuming the incoming data is in JSON format
    with open('url_shorten_memcached_webhook_data.txt', 'a') as file:  # 'a' for append mode
        file.write(json.dumps(data) + '\n')
    return "Data received", 200

@app.route('/url-shorten-mongodb-webhook', methods=['POST'])
def url_shorten_mongodb_webhook():
    data = request.json  # Assuming the incoming data is in JSON format
    with open('url_shorten_mongodb_webhook_data.txt', 'a') as file:  # 'a' for append mode
        file.write(json.dumps(data) + '\n')
    return "Data received", 200

@app.route('/user-memcached-webhook', methods=['POST'])
def user_memcached_webhook():
    data = request.json  # Assuming the incoming data is in JSON format
    with open('user_memcached_webhook_data.txt', 'a') as file:  # 'a' for append mode
        file.write(json.dumps(data) + '\n')
    return "Data received", 200

@app.route('/user-mongodb-webhook', methods=['POST'])
def user_mongodb_webhook():
    data = request.json  # Assuming the incoming data is in JSON format
    with open('user_mongodb_webhook_data.txt', 'a') as file:  # 'a' for append mode
        file.write(json.dumps(data) + '\n')
    return "Data received", 200

@app.route('/user-timeline-mongodb-webhook', methods=['POST'])
def user_timeline_mongodb_webhook():
    data = request.json  # Assuming the incoming data is in JSON format
    with open('user_timeline_mongodb_webhook_data.txt', 'a') as file:  # 'a' for append mode
        file.write(json.dumps(data) + '\n')
    return "Data received", 200

@app.route('/user-timeline-redis-webhook', methods=['POST'])
def user_timeline_redis_webhook():
    data = request.json  # Assuming the incoming data is in JSON format
    with open('user_timeline_redis_webhook_data.txt', 'a') as file:  # 'a' for append mode
        file.write(json.dumps(data) + '\n')
    return "Data received", 200

if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=5000)