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
            'short_id': container.short_id,
            'name': container.name,
            'create_time': list(container.attrs.items())[1][1],
            'image': {
                'id': container.image.id,
                'tags': container.image.tags
            },
            'port': [
                {
                    'container_port': container_port,
                    'host_port': (list(container.attrs.items())[18][1]['PortBindings'])[container_port]['HostPort']
                } for container_port in list(container.attrs.items())[18][1]['PortBindings'].keys()
            ],
            'labels': container.labels,
            'status': container.status
        })
    return JsonResponse({'errno': 0, 'data': data})


@csrf_exempt
def create_container(request):
    """创建容器"""
    command = None if request.POST.get('command') == '' else request.POST.get('command')
    environment = None if request.POST.get('environment') == '' else request.POST.get('environment')
    volumes = None if request.POST.get('volumes') == '' else request.POST.get('volumes')
    container_ports = request.POST.get('container_ports').split(',')
    host_posts = request.POST.get('host_ports').split(',')
    ports = {}
    for container_port, host_port in zip(container_ports, host_posts):
        ports[container_port] = host_port
    try:
        container = client.containers.run(image=request.POST.get('image'), name=request.POST.get('name'), ports=ports,
                                          command=command, environment=environment, volumes=volumes, detach=True)
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
    command = None if request.POST.get('command') == '' else request.POST.get('command')
    environment = None if request.POST.get('environment') == '' else request.POST.get('environment')
    volumes = None if request.POST.get('volumes') == '' else request.POST.get('volumes')
    container_ports = request.POST.get('container_ports').split(',')
    host_posts = request.POST.get('host_ports').split(',')
    ports = {}
    for container_port, host_port in zip(container_ports, host_posts):
        ports[container_port] = host_port
    try:
        container = client.containers.run(image=request.POST.get('image'), name=request.POST.get('name'), ports=ports,
                                          command=command, environment=environment, volumes=volumes, detach=True)
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


@csrf_exempt
def restart_container(request):
    """重启容器"""
    try:
        container = client.containers.get(request.POST.get('container_id'))
        container.restart()
        return JsonResponse({'errno': 0, 'msg': '重启容器成功', 'container_id': container.id})
    except:
        return JsonResponse({'errno': 2006, 'msg': '重启容器失败'})


@csrf_exempt
def rename_container(request):
    """重命名容器"""
    try:
        container = client.containers.get(request.POST.get('container_id'))
        container.rename(request.POST.get('new_name'))
        return JsonResponse({'errno': 0, 'msg': '重命名容器成功', 'container_id': container.id})
    except:
        return JsonResponse({'errno': 2007, 'msg': '重命名容器失败'})
