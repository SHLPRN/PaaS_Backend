import docker
import time
from django.views.decorators.csrf import csrf_exempt
from kubernetes import client, config
import yaml
from django.http import JsonResponse, request

config.load_kube_config()

docker_client = docker.from_env()


@csrf_exempt
def list_images(request):
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
def remove_image(request):
    image_id = request.POST.get("image_id")
    docker_client.images.remove(image_id)
    return JsonResponse({"errno": 0, "msg": "删除成功"})


@csrf_exempt
def pull_image(request):
    repository = request.POST.get("repository")
    try:
        docker_client.images.pull(repository=repository)
    except Exception as e:
        return JsonResponse({"errno": 1, "msg": "没有此镜像"})
    return JsonResponse({"errno": 0, "msg": "拉取镜像成功"})


@csrf_exempt
def build_image(request):
    config = request.FILES.get("dockerfile")
    name = time.strftime('%Y%m%d%H%M%S', time.localtime())
    with open('.' + TEMP_URL + name, 'wb+') as f:
        for chunk in config.chunks():
            f.write(chunk)
    with open('.' + TEMP_URL + name, 'r') as f:
        tag = request.POST.get("tag")
        docker_client.images.build(fileobj=f, tag=tag)
    return JsonResponse({"errno": 0, "msg": "创建镜像成功"})
