import requests


def trigger_miqa_test(miqa_server, trigger_id, version_name):
    """
      Trigger an offline execution of the specified Miqa trigger ID for the specified version.

      :param miqa_server: Miqa server e.g. yourco.miqa.io
      :param trigger_id: Miqa test trigger ID e.g. ABC123
      :param version_name: Name representing the version that was being tested/generated the outputs being uploaded, e.g. a commit ID ('abc123') or version number ('v1.2.3')
      :return: The ID for the Test Chain Run created as a result of this trigger (int).
      :rtype: int
    """
    trigger_url = f"https://{miqa_server}/api/trigger_test_auto/{trigger_id}?app=mn&offline_version=True&name={version_name}"
    trigger_response_json = requests.get(trigger_url).json()
    run_id = trigger_response_json.get('run_id')
    if run_id:
        run_id = int(run_id)
    return run_id


def get_tcr_info_json(miqa_server, run_id, directory_containing_outputs=None, ds_id=None, wfv_id=None):
    """
      Retrieve a JSON describing the test chain run.

      :param str miqa_server: Miqa server e.g. yourco.miqa.io
      :param int run_id: Miqa Test Chain Run ID
      :param str directory_containing_outputs: Source location - local directory containing outputs to upload - only used if attempting to retrieve the upload command to use. (Optional)
      :param int ds_id: Datasource ID - enables getting specific information for the particular datasource
      :param int wfv_id: Workflow Variant ID - enables getting specific information for the particular workflow variant (i.e. if running a test on multiple workflow variants)
      :return: JSON representation of Test Chain Run information
      :rtype: dict
    """
    get_info_url = f"https://{miqa_server}/api/get_tcr_exec_info/{run_id}"
    query_pars = []
    if directory_containing_outputs:
        query_pars.append(f"source_location={directory_containing_outputs}")
    if ds_id:
        query_pars.append(f"ds_id={ds_id}")
    if wfv_id:
        query_pars.append(f"&wfv_id={wfv_id}")

    if len(query_pars)>0:
        get_info_url = f"{get_info_url}?{'&'.join(query_pars)}"

    get_info_response_json = requests.get(get_info_url).json()
    return get_info_response_json


def get_trigger_info(miqa_server, trigger_id):
    trigger_url = f"https://{miqa_server}/api/test_trigger/{trigger_id}/get_ds_id_mapping"
    trigger_response_json = requests.get(trigger_url).json()
    # return {"ds_id_mapping":{"results":trigger_response_json, "url":trigger_url}}
    return {"ds_id_mapping":{"results":trigger_response_json}}