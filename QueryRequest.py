from flask import Flask, jsonify
from flask.views import MethodView

app = Flask(__name__)


class API_Test(MethodView):
    def get(self):
        return jsonify(message='I am GET')

    def post(self):
        return jsonify(message='I am POST')

    def delete(self):
        return jsonify(message='I am DELETE')


app.add_url_rule('/test_api/', view_func=API_Test.as_view('test_api'))

if __name__ == '__main__':
    app.run(debug=True)
