# -*- coding: utf-8 -*-
import os
import requests
import json


def get_issues_from_gitbucket(url, token):
    requestHeader = {'Authorization': 'token ' + token}
    return requests.get(url, headers=requestHeader)


def get_issues_comment_from_gitbucket(url, token):
    requestHeader = {'Authorization': 'token ' + token}
    return requests.get(url, headers=requestHeader)


def create_issues_to_github(url, token, data):
    requestHeader = {'Authorization': 'token ' + token}
    data = json.dumps(data)
    return requests.post(url, headers=requestHeader, data=data)


def create_issues_comment_to_github(url, token, data):
    requestHeader = {'Authorization': 'token ' + token}
    data = json.dumps(data)
    return requests.post(url, headers=requestHeader, data=data)


if __name__ == "__main__":

    ######### NEED TO SET ENV ##########
    GITBUCKET_HOST = os.getenv("GITBUCKET_HOST")
    GITBUCKET_OWNER = os.getenv("GITBUCKET_OWNER")
    GITBUCKET_REPO = os.getenv("GITBUCKET_REPO")
    GITBUCKET_TOKEN = os.getenv("GITBUCKET_TOKEN")
    GITHUB_OWNER = os.getenv("GITHUB_OWNER")
    GITHUB_REPO = os.getenv("GITHUB_REPO")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    ######### NEED TO SET ENV ##########

    GITBUCKET_ISSUE_URL = "{gbHost}/api/v3/repos/{gbOwner}/{gbRepo}/issues?state=open".format(
        gbHost=GITBUCKET_HOST, gbOwner=GITBUCKET_OWNER, gbRepo=GITBUCKET_REPO)

    GITHUB_ISSUE_URL = "https://api.github.com/repos/{ghOwner}/{ghRepo}/issues".format(
        ghOwner=GITHUB_OWNER, ghRepo=GITHUB_REPO)

    # Get all issues from GitBucket
    issues = json.loads(get_issues_from_gitbucket(
        GITBUCKET_ISSUE_URL, GITBUCKET_TOKEN).content)

    print("Get {issueLength} issues from Gitbucket".format(
        issueLength=len(issues)))

    for issue in issues[::-1]:
        GITBUCKET_COMMENT_URL = "{gbHost}/api/v3/repos/{gbOwner}/{gbRepo}/issues/{number}/comments".format(
            gbHost=GITBUCKET_HOST, gbOwner=GITBUCKET_OWNER, gbRepo=GITBUCKET_REPO, number=issue["number"])
        # Get all issues comment each issue from GitBucket
        isuueComments = json.loads(get_issues_comment_from_gitbucket(
            GITBUCKET_COMMENT_URL, GITBUCKET_TOKEN).content)
        print("Get {commentLength} comments from Gitbucket".format(
            commentLength=len(isuueComments)))
        # Create new issue to Github
        createdIssue = json.loads(create_issues_to_github(
            GITHUB_ISSUE_URL, GITHUB_TOKEN, issue).content)
        for comment in isuueComments[::-1]:
            # Create new issue comment to Github
            create_issues_comment_to_github(
                createdIssue["url"] + "/comments", GITHUB_TOKEN, comment)
        print("Create {commentLength} comments to Github".format(
            commentLength=len(isuueComments)))
    print("Create {issueLength} issues to Github".format(
        issueLength=len(issues)))
