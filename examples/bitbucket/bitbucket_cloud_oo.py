# coding=utf-8

from textwrap import indent

from atlassian.bitbucket import Cloud

cloud = Cloud(url="https://api.bitbucket.org/", username="admin", password="admin")

index = 0
for w in cloud.workspaces.each():
    print(("Workspace name " + w.name))
    p = next(w.projects.each())
    print(("   First project name " + p.name))
    index += 1
    if index == 5:
        print("   ...")
        break

print()
w = cloud.workspaces.get(w.slug)
p = w.projects.get(p.key)
print(("Project key " + p.key))
for r in p.repositories.each():
    print(("   Repository name " + r.name))
    for i in r.issues.each():
        print(("   Issue uuid " + str(i.id)))
        print(("      Title: " + i.title))
    index = 0
    for pl in r.pipelines.each(sort="-created_on"):
        index += 1
        if index == 5:
            print("   ...")
            break
        print(("   Pipeline uuid " + pl.uuid))
        for s in pl.steps():
            print(("      Step uuid " + s.uuid))
            size, log = s.log(start=0, end=20)
            if size is None:
                print("         No log")
            else:
                print(("         Size of log: " + size))
                print((indent(log.decode("utf-8"), "            ")))
    for dr in r.default_reviewers.each():
        print(("   Default reviewer " + dr.nickname))
    for br in r.branch_restrictions.each():
        print(("   Branch restriction ID " + str(br.id)))
        print(("      Kind " + br.kind))
