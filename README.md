<p align="center">
  <a href="https://dev.to/vumdao">
    <img alt="Scan AWS Keys For A Commit" src="https://github.com/vumdao/scan-iam-keys/blob/master/scaniamkeys.png?raw=true" width="500" />
  </a>
</p>
<h1 align="center">
  <div><b>Scan AWS Keys For A Commit</b></div>
</h1>

### - Sometimes developers add their env file to git commit which contains AWS Access key, to avoid this, we can use git HOOK to check personal key first and use merge_request pipeline job to check before merging the commit to branch

---

## What’s In This Document 
- [How to scan all AWS keys](#-How-to-scan-all-AWS-keys)
- [Test A Commit](#-Test-A-Commit)

---

### 🚀 **[How to scan all AWS keys](#-How-to-scan-all-AWS-keys)**
https://github.com/vumdao/scan-iam-keys/scan-iam-keys.py

```
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

    def check_user(the_user):
        user_name = the_user['UserName']
        print("Get keys")
        access_keys = iam.list_access_keys(UserName=user_name)['AccessKeyMetadata']
        for key in access_keys:
            check_key(key)
        print(f"Done {user_name}")

    for user in users:
        user_thread = threading.Thread(target=check_user, args=(user,))
        user_thread.start()


if __name__ == '__main__':
    scan_iam_access_keys()
```

### 🚀 **[Test A Commit](#-Test-A-Commit)**
- Create text file eg. sample.txt which contains an AWS key
- Run test
```
⚡ $ ./scan-iam-keys.py 
Detect AKIAZUFR7JW2ZBEOKUVR
```


<h3 align="center">
  <a href="https://dev.to/vumdao">:stars: Blog</a>
  <span> · </span>
  <a href="https://github.com/vumdao/">Github</a>
  <span> · </span>
  <a href="https://vumdao.hashnode.dev/">Web</a>
  <span> · </span>
  <a href="https://www.linkedin.com/in/vu-dao-9280ab43/">Linkedin</a>
  <span> · </span>
  <a href="https://www.linkedin.com/groups/12488649/">Group</a>
  <span> · </span>
  <a href="https://www.facebook.com/CloudOpz-104917804863956">Page</a>
  <span> · </span>
  <a href="https://twitter.com/VuDao81124667">Twitter :stars:</a>
</h3>