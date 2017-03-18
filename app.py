import sys
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




def Response_error_check(configuration):
    try:
        return git_username_repo.get_file_contents(configuration).content.decode(git_username_repo.get_contents(configuration).encoding)
    except UnknownObjectException as e:
        return "File Not Found"
    except RateLimitExceededException:
        return "Rate Limit Exception"




@app.route("/v1/<configuration>")
def controller(configuration):
        if isinstance(git_username_repo, basestring):
            return git_username_repo
        else:
            return Response_error_check(configuration)

if __name__ == "__main__":
    app.config["url"] = sys.argv[1]
    app.run(debug=True,host='0.0.0.0')

