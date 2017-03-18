mport sys
from flask import Flask
from github import RateLimitExceededException
from github import Github
from github import UnknownObjectException


app = Flask(__name__)
repo_url = sys.argv[1].split("/")


for x in range(len(repo_url)):
    if "github" in repo_url[x]:
        Git_usr = repo_url[x+1]
        Git_repo = repo_url[x+2]
        break

try:
    git_username_repo = Github().get_user(Git_usr).get_repo(Git_repo)
except UnknownObjectException:
    git_username_repo = "Invalid repository"
except RateLimitExceededException:
    git_username_repo = "Rate limit Has reached"



"""This function will get the latest version of the required config_file from the connected repository"""
def Response_error_check(config_file):
    try:
        return git_username_repo.get_file_contents(config_file).content.decode(git_username_repo.get_contents(config_file).encoding)
    except UnknownObjectException as e:
        return "File Not Found"
    except RateLimitExceededException:
        return "Rate Limit Exception"




@app.route("/v1/<config_file>")
def controller(config_file):
        if isinstance(git_username_repo, basestring):
            return git_username_repo
        else:
            return Response_error_check(config_file)

if __name__ == "__main__":
    app.config["url"] = sys.argv[1]
    app.run(debug=True,host='0.0.0.0')

