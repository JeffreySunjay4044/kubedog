"""
The use case of the application is backing up and deleting certain namespace or deployment
"""
from flask import Flask, request
from k8sscheduler.backupdelete import BackupDelete
from k8sscheduler.recreate import RecreateFiles
from k8sreader.k8sreader import Readk8s
from kubernetes import config

from blueprints.ingress_blueprint import ingress_bp
from blueprints.namespace_blueprint import namespace_bp
from blueprints.service_blueprint import service_bp
from blueprints.deployment_blueprint import deploy_bp
from blueprints.daemonset_blueprint import daemonset_bp

app = Flask(__name__)
app.register_blueprint(ingress_bp)
app.register_blueprint(namespace_bp)
app.register_blueprint(service_bp)
app.register_blueprint(deploy_bp)
app.register_blueprint(daemonset_bp)


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
