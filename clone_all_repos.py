'''
Copyright (c) 2021-2022 Magesh K and others

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

'''
Python Script to clone all public repositories under a user

This script assumes that shell commands such as "cd" and "git" can be run from os's default shell.
windows, unix, mac supports change dir commmand and git location is added to PATH variable.

Exception is unhandled and will be raised as soon as they appear, 
please follow stacktrace for details on the error
'''

from requests import *
import subprocess as sp
import os, json

# custom configuration keys for cloning 
userconfig = 'userconfig.json'
'''
template for userconfig json file:

{
  "user"    : "mahee96",
  "results" : 100,
  "rootdir" : "cloned_users",
  "repofile": "public_repos.txt"
}

'''

# read user defined values from config file
config = {}
with open(userconfig) as userconfig:
    lines = userconfig.readlines()
    serialized = "".join(lines)
    config = json.loads(serialized)
    assert config       # config must not be False

# user defined constants
target_user     = config['user']
results_count   = config['results']

root_dir        = config['rootdir']
target_file     = config['repofile']

# formatted values
target_url  = "https://api.github.com/users/{}/repos?per_page={}"
target_path = "./{}/{}/"
target_url  = target_url.format(target_user, results_count)
target_path = target_path.format(root_dir, target_user)

# global constants
headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Content-Type': 'application/json',
    'User-Agent': 'github.com'
}

def clone_repo(url: str, path: str):
    url = url.strip()
    assert url
    # subprocess's stdout/stderr is redirected to parent's stdout/stderr
    sp.run(["cd", path, "&&", "git", "clone", url], shell=True)

def update_repo(path: str):
    sp.run(["cd", path, "&&", "git", "pull"], shell=True)

def create_reqd_dirs():
    if not os.path.exists(target_path):
        os.makedirs(target_path)

repo_name_list = []

def fetch_repo_list():
    with open(target_path + target_file, 'w') as repo_list_file:
        while(True):
            # REST - HTTP get request
            global target_url
            resp: Response = get(target_url, headers)
            next = resp.links.get('next')   # next page link
            body = resp.json()              # page results as json
            if(resp.status_code != 200):    # stop processing if returning not OK(200)
                print("\nRESPONSE ERROR CODE", resp.status_code, ":", body)
                return False
            # for each repo in current user's profile, write its url to file
            for repo in body:
                repo_name = repo['name']
                repo_name_list.append(repo_name)
                repo_url = repo['html_url']
                repo_list_file.writelines(repo_url + '\r')
            if(not next):
                return True
            target_url = next['url']        # set to next page get() request

def read_list_and_clone():
    with open(target_path + target_file, 'r') as repo_list_file:
        for repo_url in repo_list_file.readlines():
            targ_dir = target_path + repo_name_list.pop(0)
            if os.path.exists(targ_dir + "/.git/"):     # is this a git repo?
                update_repo(target_path)
            else:
                clone_repo(repo_url, target_path)

if __name__ == "__main__":
    print("Starting clone of github repositories under user:", target_user, "\n")
    create_reqd_dirs()
    if(fetch_repo_list()):
        read_list_and_clone()
    print("End of processing")
    