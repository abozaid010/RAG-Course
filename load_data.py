import json
from vector_store import add_projects

with open("projects.json") as f:
    data = json.load(f)

projects = data["data"]["projects"]

add_projects(projects)

print("Data inserted into Chroma")