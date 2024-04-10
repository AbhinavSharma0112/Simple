# import yaml
from flask import Flask, request, redirect, render_template
from github import Github
import os
import subprocess
import urllib.parse
import oyaml as yaml

app = Flask(__name__)

github_token = os.environ.get("GITHUB_TOKEN")
github_username = os.environ.get("GITHUB_USERNAME")

repo_name = "Simple"  # Repository name (without username)
repo_path = r"D:\workspace\Simple"  # Specify the path in the repository where you want to save the YAML files

try:
    g = Github(login_or_token=github_token)
    gituser = g.get_user()
    repo = gituser.get_repo(repo_name)

except Exception as e:
    print("An error occurred:", e)


@app.route('/add', methods=['POST'])
def get_user_input():
    if request.method == "POST":
        company_name = request.form.get('company_name')
        repo_name = request.form.get('repo_name')  # Get the repository name from the form
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
        escaped_company_name = urllib.parse.quote(company_name, safe='')
        escaped_repo_name = urllib.parse.quote(repo_name, safe='')  # Escape repository name
        escaped_name = urllib.parse.quote(name, safe='')

        # Construct the directory path
        directory_path = os.path.join(repo_path, 'pipelines', 'SoftwareMathematics', escaped_company_name, escaped_repo_name)

        # Ensure the directory exists, creating if necessary
        os.makedirs(directory_path, exist_ok=True)

        # Construct the file path
        file_path = os.path.join(directory_path, file_name)

        # Save YAML file locally
        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

        # Upload YAML file to GitHub
        try:
            # Read the contents of the file
            with open(file_path, 'r') as file:
                content = file.read()

            # Construct the dynamic_repo_path
            dynamic_repo_path = f"pipelines/SoftwareMathematics/{escaped_company_name}/{escaped_repo_name}/{file_name}"

            repo.create_file(dynamic_repo_path, f"Create {file_name}", content, branch="yaml_file_create")

            git_cmd_add = ["git", "add", file_path]
            subprocess.run(git_cmd_add)

            git_cmd_commit = ["git", "commit", "-m", f"Add {file_name}"]
            subprocess.run(git_cmd_commit)

            git_cmd_push = ["git", "push", "origin", "yaml_file_create"]
            subprocess.run(git_cmd_push)

            return redirect('/')
        except Exception as e:
            error_message = str(e)
            print("An error occurred while uploading file to GitHub:", str(e))
            return "Error occurred while uploading file to GitHub. Please check logs for details."




@app.route('/')
def hello_world():
    return render_template("newindex.html", github_username=github_username)


if __name__ == "__main__":
    app.run(debug=True)
