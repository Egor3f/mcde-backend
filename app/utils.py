from docker import DockerClient


dockerClient = None
def getDockerClient():
    global dockerClient
    if dockerClient is None:
        dockerClient = DockerClient()
    return dockerClient


def serializeObjectAttrs(obj, *attr_list):
    return {attr: getattr(obj, attr, None) for attr in attr_list}

def serializeObjectListAttrs(lst, *attr_list):
    return [serializeObjectAttrs(obj, *attr_list) for obj in lst]
