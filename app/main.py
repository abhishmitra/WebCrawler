# docker run -h 0.0.0.0 --name redis-server -d redis
# rq worker --url redis://0.0.0.0:6379
from worker import *
from flask import Flask, request, jsonify
from database_file import *
import time

time.sleep(15)

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is missing."}), 400
    insert_urls_with_content(
        [(url, None)]
    )
    return jsonify("Scraping started"), 200


@app.route('/search', methods=['GET'])
def search():
    search_text = request.args.get('text')
    if not search_text:
        return jsonify({"error": "Search text parameter is missing."}), 400
    res = search_text_in_data(search_text)
    return jsonify({"results": res}), 200



if __name__ == '__main__':

    if verify_database_connection():
        create_tables_if_not_exist()
        app.run(host = "0.0.0.0", debug=True)
    else:
        print("Exiting due to database connection failure.")