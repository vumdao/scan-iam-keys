#!/usr/bin/env python
import boto3
import subprocess as sub
import re
import threading


def get_commit_change_content():
    output = sub.check_output(["git", "show"])
    return output


def scan_iam_access_keys():
    iam = boto3.client('iam')
    users = iam.list_users()['Users']
    commit_change = get_commit_change_content()

    def check_key(the_key):
        if re.search(the_key['AccessKeyId'], str(commit_change)):
            print(f"Detect {the_key['AccessKeyId']}")
            exit(1)

    def check_user(the_user):
        user_name = the_user['UserName']
        access_keys = iam.list_access_keys(UserName=user_name)['AccessKeyMetadata']
        for key in access_keys:
            check_key(key)

    for user in users:
        user_thread = threading.Thread(target=check_user, args=(user,))
        user_thread.start()


if __name__ == '__main__':
    scan_iam_access_keys()
