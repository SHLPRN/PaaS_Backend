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
            'image': {
                'id': container.image.id,
                'tags': container.image.tags
            },
            'labels': container.labels,
            'short_id': container.short_id,
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
        'image_id': container.image.id,
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
    command = '' if request.POST.get('command') is None else request.POST.get('command').split(',')
    environment = '' if request.POST.get('environment') is None else request.POST.get('environment').split(',')
    container_ports = '' if request.POST.get('container_ports') is None \
        else request.POST.get('container_ports').split(',')
    host_posts = '' if request.POST.get('host_posts') is None else request.POST.get('host_posts').split(',')
    volumes = '' if request.POST.get('volumes') is None else request.POST.get('volumes').split(',')
    ports = {}
    for container_port, host_port in zip(container_ports, host_posts):
        if container_port != '' and host_port != '':
            ports[container_port] = host_port
    try:
        container = client.containers.create(image=request.POST.get('image'), detach=True, environment=environment,
                                          name=request.POST.get('name'), ports=ports, command=command, volumes=volumes)
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
    command = None if request.POST.get('command') is None or '' else request.POST.get('command').split(',')
    environment = [] if request.POST.get('environment') is None or '' else request.POST.get('environment').split(',')
    container_ports = '' if request.POST.get('container_ports') is None or '' \
        else request.POST.get('container_ports').split(',')
    host_posts = '' if request.POST.get('host_posts') is None or '' else request.POST.get('host_posts').split(',')
    volumes = None if request.POST.get('volumes') is None or '' else request.POST.get('volumes').split(',')
    ports = {}
    for container_port, host_port in zip(container_ports, host_posts):
        if container_port != '' and host_port != '':
            ports[container_port] = host_port
    """
    try:
        container = client.containers.run(image=request.POST.get('image'), detach=True, environment=environment,
                                          name=request.POST.get('name'), ports=ports, command=command, volumes=volumes)
        return JsonResponse({'errno': 0, 'msg': '运行容器成功', 'container_id': container.id})
    except:
        return JsonResponse({'errno': 2003, 'msg': '运行容器失败'})
    """
    container = client.containers.run(image=request.POST.get('image'), detach=True, environment=environment,
                                      name=request.POST.get('name'), ports=ports, command=command, volumes=volumes)
    return JsonResponse({'errno': 0, 'msg': '运行容器成功', 'container_id': container.id})


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
