## Python Script to clone all public repositories under a user

This script fetches all public repositories under a github user, 
saves it locally to a text file and uses this list to clone all the repos locally

### To Run the script:
1. install required dependencies using command "python -m pip install xxxx".
2. run script using command "python clone_all_repos.py"

**NOTE:** This script assumes that shell commands such as "cd" and "git" can be run from os's default shell.
windows, unix, mac supports change dir commmand and git location is added to PATH variable.

**NOTE:** Exception is unhandled and will be raised as soon as they appear, 
please follow stacktrace for details on the error