import docker

client = docker.from_env()

for container in client.containers.list():
    print(container.name)
    print(container.image.attrs['RepoTags'][0])

    if 'test_app:latest' in container.image.attrs['RepoTags']:
        container.stop()

client.containers.run(
    "test_app:latest",
    name='night_owl',
    detach=True,
    ports={'5000/tcp': '5000'},
    remove=True,
    auto_remove=True
)
