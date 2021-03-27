# use case for beacking up and deleting for certain ns or certain dep
import argparse

from kubernetes import client, config
from flask import Flask, request
from flask import json
# from pdb import debugpy


from k8sscheduler.backupdelete import BackupDelete
from k8sscheduler.recreate import RecreateFiles
from k8sreader.k8sreader import Readk8s
from k8sscheduler.statuscheck import StatusCheck

# debugpy.listen(("localhost", 5678))
app = Flask(__name__)



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


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(
#         description=__doc__,
#         formatter_class=argparse.RawDescriptionHelpFormatter
#     )
#     parser.add_argument('--namespace-with-deployment', required=False)
#     parser.add_argument('--for-all-ns', required=False)
#     parser.add_argument('--is-backup', required=False)
#     parser.add_argument('--is-recreate', required=False)
#     args = parser.parse_args()
#     args.is_backup= True
#     args.is_recreate= True
#     args.namespace_with_deployment= {'orc': {'orc':''}}
#     config.load_kube_config()
#     if args.is_backup:
#         BackupDelete.backup_and_delete(args.namespace_with_deployment, False)
#     if args.is_recreate:
#         RecreateFiles.recreate_from_backup()
#         RecreateFiles.clear_backedup_files()

def backup_delete(backup_json):
    config.load_kube_config()
    if backup_json is None:
        return BackupDelete.backup_and_delete(backup_json, True)
    return BackupDelete.backup_and_delete(backup_json, False)


def recreate_from_backup():
    backup_recreation_status = RecreateFiles.recreate_from_backup()
    RecreateFiles.clear_backedup_files()
    return backup_recreation_status