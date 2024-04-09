import yaml
from flask import Flask, request, redirect, render_template
from github import Github
import os
import subprocess
import urllib.parse


app = Flask(__name__)

# GitHub credentials
username = "AbhinavSharma0112"
password = "Abhinavsharma@1"
repo_name = "Simple"  # Repository name (without username)
repo_path = r"D:\workspace\Simple"  # Specify the path in the repository where you want to save the YAML files

try:
    # Initialize GitHub instance
    # Initialize GitHub instance with Personal Access Token
    g = Github(login_or_token="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")

    # g = Github(username, password)
    gituser = g.get_user()
    print(gituser)
    repo = gituser.get_repo(repo_name)
    print(repo)


except Exception as e:
    print("An error occurred:", e)


@app.route('/add', methods=['POST'])
def get_user_input():
    if request.method == "POST":
        name = request.form.get('name')
        repo_url = request.form.get('repo_url')
        enabled = request.form.get('enabled')
        job_type = request.form.get('job_type')
        run_command = request.form.get('run_command')
        src_path = request.form.get('src_path')
        application_port = request.form.get('application_port')
        deploy_port = request.form.get('deploy_port')
        ssh_port_prod = request.form.get('ssh_port_prod')
        ssh_port_dev = request.form.get('ssh_port_dev')
        build_command = request.form.get('build_command')
        pvt_deploy_servers_dev = request.form.get('pvt_deploy_servers_dev')
        deploy_servers_dev = request.form.get('deploy_servers_dev')
        pvt_deploy_servers_prod = request.form.get('pvt_deploy_servers_prod')
        deploy_servers_prod = request.form.get('deploy_servers_prod')
        deploy_env_prod = request.form.get('deploy_env_prod')
        deploy_env_dev = request.form.get('deploy_env_dev')
        deploy_env = request.form.get('deploy_env')

        data = {
            'name': name,
            'repo_url': repo_url,
            'enabled': enabled,
            'job_type': job_type,
            'run_command': run_command,
            'src_path': src_path,
            'application_port': application_port,
            'deploy_port': deploy_port,
            'ssh_port_prod': ssh_port_prod,
            'ssh_port_dev': ssh_port_dev,
            'build_command': build_command,
            'pvt_deploy_servers_dev': pvt_deploy_servers_dev,
            'deploy_servers_dev': deploy_servers_dev,
            'pvt_deploy_servers_prod': pvt_deploy_servers_prod,
            'deploy_servers_prod': deploy_servers_prod,
            'deploy_env_prod': deploy_env_prod,
            'deploy_env_dev': deploy_env_dev,
            'deploy_env': deploy_env
        }

        file_name = f"{name}.yaml"
        escaped_repo_url = urllib.parse.quote(repo_url, safe='')

        dynamic_repo_path = r"pipelines/SoftwareMathematics" + f"/{escaped_repo_url}" + r"/companyname" + f"/{escaped_repo_url}"
        # Ensure the file path is correctly constructed
        file_path = os.path.join(repo_path, file_name)

        # Save YAML file locally
        with open(file_path, 'w') as file:
            yaml.dump(data, file)

        # Upload YAML file to GitHub
        try:
            # Read the contents of the file
            with open(file_path, 'r') as file:
                content = file.read()


            repo.create_file(dynamic_repo_path, f"Create {file_name}", content, branch="yaml_file_create")

            git_cmd = ["git", "push"]
            subprocess.run(git_cmd)

            return redirect('/')
        except Exception as e:
            print("An error occurred while uploading file to GitHub:", str(e))
            return "Error occurred while uploading file to GitHub."


@app.route('/')
def hello_world():
    return render_template("newindex.html")


if __name__ == "__main__":
    app.run(debug=True)
