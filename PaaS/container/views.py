import os
import json
import docker
import random

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

client = docker.from_env()


@csrf_exempt
def list_containers(request):
    """获取容器列表"""
    containers = client.containers.list(all=True)
    data = []
    for container in containers:
        data.append({
            'id': container.id,
            'name': container.name,
            'create_time': list(container.attrs.items())[1][1],
            'image': container.image.id,
            'status': container.status
        })
    return JsonResponse({'errno': 0, 'data': data})


@csrf_exempt
def get_container_info(request):
    """获取容器详细信息"""
    container = client.containers.get(request.POST.get('container_id'))
    data = {
        'id': container.id,
        'name': container.name,
        'create_time': list(container.attrs.items())[1][1],
        'image': container.image.id,
        'port': list(container.attrs.items())[18][1]['PortBindings'],
        'labels': container.labels,
        'status': container.status
    }
    try:
        for key in data['port'].keys():
            data['port'][key] = data['port'][key][0]['HostPort']
    except:
        data['port'] = {}
    return JsonResponse({'errno': 0, 'data': data})


@csrf_exempt
def create_container(request):
    """创建容器"""
    image = request.POST.get('image')
    inner_port = request.POST.get('inner_port')
    outer_port = request.POST.get('outer_port')
    ports = {inner_port + '/tcp': outer_port}
    try:
        if ports == {'22/tcp': '22'}:
            ports['22/tcp'] = str(get_port())
        container = client.containers.create(image, ports=ports)
        return JsonResponse({'errno': 0, 'msg': '创建容器成功', 'container_id': container.id})
    except:
        return JsonResponse({'errno': 2001, 'msg': '创建容器失败'})


@csrf_exempt
def start_container(request):
    """启动容器"""
    try:
        container = client.containers.get(request.POST.get('container_id'))
        container.start()
        return JsonResponse({'errno': 0, 'msg': '启动容器成功', 'container_id': container.id})
    except:
        return JsonResponse({'errno': 2002, 'msg': '启动容器失败'})


@csrf_exempt
def run_container(request):
    """运行容器"""
    image = request.POST.get('image')
    inner_port = request.POST.get('inner_port')
    outer_port = request.POST.get('outer_port')
    name = request.POST.get('name')
    environment = {} if request.POST.get('environment') is None else dict(request.POST.get('environment'))
    # command = "" if request.POST.get('command') is None else request.POST.get('command')
    ports = {inner_port + '/tcp': outer_port}
    try:
        if ports == {'22/tcp': '22'}:
            ports['22/tcp'] = str(get_port())
        container = client.containers.run(image, detach=True, environment=environment, name=name, ports=ports)
        return JsonResponse({'errno': 0, 'msg': '运行容器成功', 'container_id': container.id})
    except:
        return JsonResponse({'errno': 2003, 'msg': '运行容器失败'})


@csrf_exempt
def stop_container(request):
    """停止容器"""
    try:
        container = client.containers.get(request.POST.get('container_id'))
        container.stop()
        return JsonResponse({'errno': 0, 'msg': '停止容器成功', 'container_id': container.id})
    except:
        return JsonResponse({'errno': 2004, 'msg': '停止容器失败'})


@csrf_exempt
def remove_container(request):
    """删除容器"""
    try:
        container = client.containers.get(request.POST.get('container_id'))
        container.stop()
        container.remove()
        return JsonResponse({'errno': 0, 'msg': '删除容器成功', 'container_id': container.id})
    except:
        return JsonResponse({'errno': 2005, 'msg': '删除容器失败'})


def get_port():
    pscmd = "netstat -ntl |grep -v Active| grep -v Proto|awk '{print $4}'|awk -F: '{print $NF}'"
    procs = os.popen(pscmd).read()
    procarr = procs.split("\n")
    tt = random.randint(15000, 20000)
    if tt not in procarr:
        return tt
    else:
        get_port()
