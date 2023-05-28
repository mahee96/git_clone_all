## Python Script to clone all public repositories under a user

This script fetches all public repositories under a github user, 
saves it locally to a text file and uses this list to clone all the repos locally

### To Run the script:
1. install required dependencies using command "python -m pip install -r requirements.py".
2. run script using command "python clone_all_repos.py"

**NOTE:** This script expects git binary to be installed and available on system loader path.

**NOTE:** All Exceptions are unhandled currently and will be raised as soon as they appear, 
please follow stacktrace for details on the error