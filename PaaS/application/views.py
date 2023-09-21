import os
import time
import yaml
import psutil

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from kubernetes import client, config

config.load_kube_config(config_file='./application/config/kubeconfig.yaml')

TEMP_URL = '/media/temp/'


@csrf_exempt
def list_nodes(request):
    """获取node列表"""
    node_list = client.CoreV1Api().list_node()
    data = []
    for node in node_list.items:
        data.append({
            'name': node.metadata.name,
            'kind': node.kind,
            'create_time': node.metadata.creation_timestamp,
            'hostname': None,
            'internal_ip': None,
            'allocatable': node.status.allocatable
        })
        for address in node.status.addresses:
            if address.type == 'Hostname':
                data[-1]['hostname'] = address.address
            elif address.type == 'InternalIP':
                data[-1]['internal_ip'] = address.address
    return JsonResponse({'errno': 0, 'data': data})


@csrf_exempt
def list_pods(request):
    """获取pod列表"""
    pod_list = client.CoreV1Api().list_namespaced_pod(namespace='default', watch=False)
    data = [
        {
            'name': pod.metadata.name,
            'create_time': pod.metadata.creation_timestamp,
            'node_name': pod.spec.node_name,
            'pod_ip': pod.status.pod_ip,
            'labels': pod.metadata.labels,
            'containers': [
                {
                    'container_id': container.container_id,
                    'container_name': container.name,
                    'image_id': container.image_id,
                    'image_name': container.image
                } for container in pod.status.container_statuses
            ]
        } for pod in pod_list.items
    ]
    return JsonResponse({'errno': 0, 'data': data})


@csrf_exempt
def list_deployments(request):
    """获取deployment列表"""
    deployment_list = client.AppsV1Api().list_namespaced_deployment(namespace='default', watch=False)
    data = [
        {
            'name': deployment.metadata.name,
            'create_time': deployment.metadata.creation_timestamp,
            'replicas': deployment.status.replicas,
            'available_replicas': deployment.status.available_replicas,
            'labels': deployment.metadata.labels,
            'template': {
                'labels': deployment.spec.template.metadata.labels,
                'containers': [
                    {
                        'container_name': container.name,
                        'image_name': container.image
                    } for container in deployment.spec.template.spec.containers
                ]
            }
        } for deployment in deployment_list.items
    ]
    return JsonResponse({'errno': 0, 'data': data})


@csrf_exempt
def create_deployment(request):
    """创建deployment"""
    try:
        config = request.FILES.get('config')
        name = time.strftime('%Y%m%d%H%M%S', time.localtime())
        with open('.' + TEMP_URL + name, 'wb+') as f:
            for chunk in config.chunks():
                f.write(chunk)
        with open('.' + TEMP_URL + name, 'r') as f:
            deployment = yaml.safe_load(f)
        client.AppsV1Api().create_namespaced_deployment(namespace='default', body=deployment)
        os.remove('.' + TEMP_URL + name)
        return JsonResponse({'errno': 0, 'msg': '创建deployment成功'})
    except:
        return JsonResponse({'errno': 3001, 'msg': '创建deployment失败'})


@csrf_exempt
def update_deployment(request):
    """更新deployment"""
    try:
        config = request.FILES.get('config')
        name = time.strftime('%Y%m%d%H%M%S', time.localtime())
        with open('.' + TEMP_URL + name, 'wb+') as f:
            for chunk in config.chunks():
                f.write(chunk)
        with open('.' + TEMP_URL + name, 'r') as f:
            deployment = yaml.safe_load(f)
        client.AppsV1Api().replace_namespaced_deployment(namespace='default', name=request.POST.get('name'),
                                                         body=deployment)
        os.remove('.' + TEMP_URL + name)
        return JsonResponse({'errno': 0, 'msg': '更新deployment成功'})
    except:
        return JsonResponse({'errno': 3002, 'msg': '更新deployment失败'})


@csrf_exempt
def delete_deployment(request):
    """删除deployment"""
    try:
        client.AppsV1Api().delete_namespaced_deployment(namespace='default', name=request.POST.get('name'))
        return JsonResponse({'errno': 0, 'msg': '删除deployment成功'})
    except:
        return JsonResponse({'errno': 3003, 'msg': '删除deployment失败'})


@csrf_exempt
def list_services(request):
    """获取service列表"""
    service_list = client.CoreV1Api().list_namespaced_service(namespace='default', watch=False)
    data = [
        {
            'name': service.metadata.name,
            'create_time': service.metadata.creation_timestamp,
            'cluster_ip': service.spec.cluster_ip,
            'type': service.spec.type,
            'ports': [
                {
                    'node_port': port.node_port,
                    'port': port.port,
                    'protocol': port.protocol
                } for port in service.spec.ports
            ]
        } for service in service_list.items
    ]
    return JsonResponse({'errno': 0, 'data': data})


@csrf_exempt
def create_service(request):
    """创建service"""
    try:
        config = request.FILES.get('config')
        name = time.strftime('%Y%m%d%H%M%S', time.localtime())
        with open('.' + TEMP_URL + name, 'wb+') as f:
            for chunk in config.chunks():
                f.write(chunk)
        with open('.' + TEMP_URL + name, 'r') as f:
            service = yaml.safe_load(f)
        client.CoreV1Api().create_namespaced_service(namespace='default', body=service)
        os.remove('.' + TEMP_URL + name)
        return JsonResponse({'errno': 0, 'msg': '创建service成功'})
    except:
        return JsonResponse({'errno': 3004, 'msg': '创建service失败'})


@csrf_exempt
def update_service(request):
    """更新service"""
    try:
        config = request.FILES.get('config')
        name = time.strftime('%Y%m%d%H%M%S', time.localtime())
        with open('.' + TEMP_URL + name, 'wb+') as f:
            for chunk in config.chunks():
                f.write(chunk)
        with open('.' + TEMP_URL + name, 'r') as f:
            service = yaml.safe_load(f)
        client.CoreV1Api().replace_namespaced_service(namespace='default', name=request.POST.get('name'), body=service)
        os.remove('.' + TEMP_URL + name)
        return JsonResponse({'errno': 0, 'msg': '更新service成功'})
    except:
        return JsonResponse({'errno': 3005, 'msg': '更新service失败'})


@csrf_exempt
def delete_service(request):
    """删除service"""
    try:
        client.CoreV1Api().delete_namespaced_service(namespace='default', name=request.POST.get('name'))
        return JsonResponse({'errno': 0, 'msg': '删除service成功'})
    except:
        return JsonResponse({'errno': 3006, 'msg': '删除service失败'})


@csrf_exempt
def get_host_params(request):
    mem_percent = psutil.virtual_memory().percent
    if mem_percent >= 97:
        return JsonResponse({
            'errno': 3007,
            'msg': 'CPU内存使用率达到阈值，请小心使用'
        })
    return JsonResponse({
        'cpu_count': psutil.cpu_count(),  # cpu 逻辑数量
        'virtual_memory': psutil.virtual_memory().percent  # cpu 内存使用率
    })
