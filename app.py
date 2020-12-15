from flask import jsonify,Flask,render_template,request
from flask_cors import CORS
# from flask_restful import Resource, Api;

app = Flask(__name__)

CORS(app)

@app.route("/", methods=['GET'])
def index():
 return "Welcome to CodezUp"

#@app.route("/ask/", methods=["POST"])
#def asked():
#    if request.method == "POST":
#        req = request.form
#        print("Key is"+req)

 #   return render_template("views/activity.hbs")

def getList():
    return ["new-lucille.hogan-2","isabel.richardson","marsha.cook","joshua.maples","jerome.johnson"]

@app.route("/suggested/", methods = ['GET'])

def suggested():
    #global weather
    #global assignees
    #convert=conversion()
    #projectpath = request.form['projectFilepath']
    key=request.args.get('keyname')
    print(key)
    a=getList()
    return jsonify([a])
    #global assignees
    #convert=conversion()
    #return convert


if __name__ == '__main__':
    app.run(debug=True)