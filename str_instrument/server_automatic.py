from flask import Flask, request

app = Flask(__name__)

@app.route("/server_request")
def server_request():
    print(request.args.get("param"))
    return "served"

if __name__ == "__main__":
    app.run(host="0.0.0.0" , port=5000 , debug=True)

