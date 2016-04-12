import os
import Schoning
from flask import *

UPLOAD_FOLDER = '/static/'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            linestring = file.stream.read()
            (values, count) = Schoning.schoning_algo(linestring)
            if not values:
                return render_template('error.html',error=count)
            return render_template('reading.html',values=values,count=count,string=linestring)
    return render_template('index.html')
if __name__ == "__main__":
    app.run(host=os.getenv("IP", "0.0.0.0"),port=int(os.getenv("PORT", 8081)),debug=True)
