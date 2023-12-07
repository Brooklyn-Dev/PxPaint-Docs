import requests
import json


def get_github_repo_contents(username, repo_name, path="", branch="main"):
    url = f"https://api.github.com/repos/{username}/{repo_name}/contents/{path}?ref={branch}"
    response = requests.get(url)
    return response.json()


def create_contents_json(username, repo_name, branch="main"):
    contents = get_github_repo_contents(username, repo_name, branch=branch)
    tree = build_tree(contents)
    
    with open("content.json", "w") as json_file:
        json.dump(tree, json_file, indent=2)


def build_tree(contents):
    tree = []

    for item in contents:
        if item["type"] == "dir" and item["name"] != ".github":
            subtree = get_github_repo_contents(username, repo_name, path=item["path"])
            tree.append({
                "name": item["name"],
                "type": "dir",
                "children": build_tree(subtree)
            })
        elif item["type"] == "file" and item["name"].endswith(".md"):
            tree.append({
                "name": item["name"],
                "type": "file",
                "href": item["_links"]["html"]
            })

    return tree


username = "Brooklyn-Dev"
repo_name = "PxPaint-Docs"

create_contents_json(username, repo_name)
