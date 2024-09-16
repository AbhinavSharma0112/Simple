import yaml
from flask import Flask, request, redirect, render_template

app = Flask(__name__)


@app.route('/add', methods=['POST'])
def get_user_input():
    if request.method == "POST":
        name = request.form.get('username')
        email = request.form.get('email')
        job=request.form.get('job')
        location=request.form.get('location')
        data = {'username': name, 'email': email,'job':job , 'location':location}


        file_name = f"{name}.yaml"

        with open(file_name, 'w') as file:
            yaml.dump(data, file)
        
        return redirect('/')


@app.route('/')
def hello_world():
   
   return render_template("index.html")


if __name__ =="__main__":
    app.run(debug=True)