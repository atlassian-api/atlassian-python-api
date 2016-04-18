from atlassian import Stash

stash = Stash(
    url='http://localhost:7990',
    username='admin',
    password='admin')

changelog = stash.get_changelog(
    project='DEMO',
    repository='example-repository',
    ref_from='develop',
    ref_to='master')

print(changelog)
