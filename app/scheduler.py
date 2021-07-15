
"""
The use case of the application is backing up and deleting certain namespace or deployment
"""

from coreservices.deployment_service import get_all_deployments, get_deployments_from
from coreservices.namespace_service import get_all_namespaces, get_namespace_by_name
from dataobject.k8smanifest import KubernetesResourceObject
from flask import Flask, request
from flask import json
from k8sscheduler.backupdelete import BackupDelete
from k8sscheduler.recreate import RecreateFiles
from k8sreader.k8sreader import Readk8s
from kubernetes import client, config


app = Flask(__name__)


@app.route('/get/namespaces', methods=['GET'])
def get_namespaces():
    """
    This API fetches the list of all namespaces in the cluster along with its age
    :return:
    """
    ns_list = get_all_namespaces()
    return app.response_class(response=json.dumps(ns_list), status=200, mimetype='application/json')


@app.route('/get/deployments', methods=['GET'])
def get_deployments_from_all_ns():
    """
    This API fetches list of deployments from all-namespaces in the cluster
    :return:
    """
    dep_list = get_all_deployments()
    return app.response_class(response=json.dumps(dep_list), status=200, mimetype='application/json')


@app.route('/get/deployments/<namespace>', methods=['GET'])
def get_deployments_from_ns(namespace):
    """
    This API fetches list of deployments from all-namespaces in the cluster
    :return:
    """
    dep_list = get_deployments_from(namespace)
    return app.response_class(response=json.dumps(dep_list), status=200, mimetype='application/json')


@app.route('/get/namespace/<name>', methods=['GET'])
def get_namespace(name):
    """
    This API fetches the namespace with given name along with its age. If the namespace does not exist, response with
    message: 'namespace not found' and status: '404' is returned
    :param name:
    :return:
    """
    ns_object = get_namespace_by_name(name)
    if isinstance(ns_object, KubernetesResourceObject):
        status_code = 200
    else:
        status_code = 404
    return app.response_class(response=json.dumps(ns_object), status=status_code, mimetype='application/json')


@app.route('/scheduler/backupdelete', methods=['GET', 'POST'])
def backup_k8s_resources():
    config.load_kube_config()
    backup_json = request.get_json(silent=True)
    print(backup_json)
    return BackupDelete.backup_and_delete(backup_json, False)


@app.route('/scheduler/recreate', methods=['GET', 'POST'])
def recreate_k8s_resources():
    RecreateFiles.recreate_from_backup()
    RecreateFiles.clear_backedup_files()


@app.route('/reader/logs', methods=['GET'])
def read_logs():
    config.load_kube_config()
    return Readk8s.read_log_file('orc-int')


if __name__ == '__main__':
    app.run(debug=True)


def backup_delete(backup_json):
    config.load_kube_config()
    if backup_json is None:
        return BackupDelete.backup_and_delete(backup_json, True)
    return BackupDelete.backup_and_delete(backup_json, False)


def recreate_from_backup():
    backup_recreation_status = RecreateFiles.recreate_from_backup()
    RecreateFiles.clear_backedup_files()
    return backup_recreation_status
