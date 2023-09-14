import docker
from django.views.decorators.csrf import csrf_exempt
from kubernetes import client, config
import yaml
from django.http import JsonResponse, request

config.load_kube_config()

docker_client = docker.from_env()

@csrf_exempt
def list_images():
    images = docker_client.images.list()
    imageList = []
    for image in images:
        dic = {}
        dic["attrs"] = image.attrs
        dic["id"] = image.id
        dic["labels"] = image.labels
        dic["short_id"] = image.short_id
        dic["tags"] = image.tags
        imageList.append(dic)
    return JsonResponse({"errno": 0, "imageList": imageList})


@csrf_exempt
def remove_image():
    image_id = request.POST.get("image_id")
    docker_client.images.remove(image_id)
    return JsonResponse({"errno": 0, "msg": "删除成功"})


@csrf_exempt
def pull_image():
    repository = request.POST.get("repository")
    try:
        docker_client.images.pull(repository=repository)
    except Exception as e:
        return JsonResponse({"errno": 1, "msg": "没有此镜像"})
    return JsonResponse({"errno": 0, "msg": "拉取镜像成功"})


@csrf_exempt
def build_image():
    dockerfile = request.FILES["dockerfile"]
    tag = request.POST.get("tag")
    docker_client.images.build(fileobj=dockerfile, tag=tag)
    return JsonResponse({"errno": 0, "msg": "创建镜像成功"})