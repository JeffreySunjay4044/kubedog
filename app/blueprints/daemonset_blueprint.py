from flask import Blueprint
from flask.wrappers import Response

from coreservices.daemonset_service import get_all_daemon_sets, get_daemon_sets_from
from utils.service_utils import get_json_list


daemonset_bp = Blueprint('daemonset_blueprint',__name__)


@daemonset_bp.route('/get/daemon-sets', methods=['GET'])
def get_daemon_sets_from_all_ns():
    """
    This API fetches list of daemonsets from all-namespaces in the cluster
    :return HTTP Response with list of daemonsets:
    """
    ds_list = get_all_daemon_sets()
    return Response(response=get_json_list(ds_list), status=200, mimetype='application/json')


@daemonset_bp.route('/get/daemon-sets/<namespace>', methods=['GET'])
def get_daemon_sets_from_ns(namespace):
    """
    This API fetches list of daemonsets from all-namespaces in the cluster
    :param namespace: Name of the namespace
    :return HTTP Response with list of daemonsets:
    """
    ds_list = get_daemon_sets_from(namespace)
    return Response(response=get_json_list(ds_list), status=200, mimetype='application/json')

