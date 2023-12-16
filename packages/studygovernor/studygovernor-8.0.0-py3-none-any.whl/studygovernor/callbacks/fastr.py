# Copyright 2017 Biomedical Imaging Group Rotterdam, Departments of
# Medical Informatics and Radiology, Erasmus MC, Rotterdam, The Netherlands
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Run a fastr network as the callback, the definition of the callback should
be like the following example:

callback:
  function: fastr
  fastr_home: ~/.fastr_testing
  network_id: cvon_prep
  source_mapping:
    t1: /scans/s T1W_3D_TFE*/resources/DICOM
    flair: /scans/3D_Brain*FLAIR*/resources/DICOM
    m0: /scans/M0 meting SENSE/resources/DICOM
    asl: /scans/ASL SENSE/resources/DICOM
    swi: /scans/SWI EPI 2min*/resources/DICOM
  sink_mapping:
    t1_nii: /scans/s T1W_3D_TFE*/resources/NIFTI/files/image{ext}
    flair_nii: /scans/3D_Brain*FLAIR*/resources/NIFTI/files/image{ext}
    flair_coregistered: /scans/s T1W_3D_TFE*/resources/NIFTI/files/flair_coreg_to_t1{ext}
    asl_header_json: /scans/ASL SENSE/resources/JSON/files/dicom_header{ext}
    asl_nii: /scans/ASL SENSE/resources/NIFTI/files/image{ext}
    m0_header_json: /scans/M0 meting SENSE/resources/JSON/files/dicom_header{ext}
    m0_nii: /scans/M0 meting SENSE/resources/NIFTI/files/image{ext}
    swi_nii: /scans/SWI EPI 2min*/resources/NIFTI/files/image{ext}
    swi_coregistered: /scans/s T1W_3D_TFE*/resources/NIFTI/files/swi_coreg_to_t1{ext}

"""

import os
import re
import json
import shutil
import subprocess
from urllib.parse import urlparse, urlunparse, urlencode

from typing import Mapping, Optional, Dict, Any

import logging
import requests


def create_uri(xnat_uri: str,
               extra_path: str,
               extra_query: Mapping[str, str] = None):
    if extra_query is None:
        query = {}
    else:
        query = dict(extra_query)

    parsed_url = urlparse(xnat_uri)

    if parsed_url.scheme not in ['http', 'https']:
        raise ValueError('XNAT uri should be http or https, found {}'.format(parsed_url.scheme))

    path = parsed_url.path
    scheme = f'xnat+{parsed_url.scheme}'

    path = '{}/{}'.format(path.rstrip('/'), extra_path.lstrip('/'))

    if '{latest_timestamp}' in path:
        resource, filename = path.split('/files/', 1)
        pattern = filename.format(latest_timestamp=r'(_?(?P<timestamp>\d\d\d\d\-\d\d\-\d\dT\d\d:\d\d:\d\d(\.\d+)?)_?)?') + '$'

        # Query all files and sort by timestamp
        files = requests.get('{}/{}/files'.format(xnat_uri.rstrip('/'), resource.lstrip('/'))).json()
        files = [x['Name'] for x in files['ResultSet']['Result']]
        print('Found file candidates {}, pattern is {}'.format(files, pattern))
        files = {re.match(pattern, x): x for x in files}
        files = {k.group('timestamp'): v for k, v in files.items() if k is not None}
        print('Found files: {}'.format(files))

        if len(files) >= 1:
            # None is the first, timestamp come after that, so last one is highest timestamp
            latest_file = sorted(files.items())[-1][1]
            print('Select {} as being the latest file'.format(latest_file))

            # Construct the correct path again
            path = '{}/files/{}'.format(resource, latest_file)

    # Convert query dict to str
    qs = urlencode(query)
    url_parts = (
        scheme,  # Scheme
        parsed_url.netloc,  # Netloc
        path,  # Path
        '',  # Params
        qs,  # Query
        ''  # Fragment
    )

    return urlunparse(url_parts)


def create_source_sink_data(xnat_uri: str,
                            project: str,
                            experiment: str,
                            source_mapping: Mapping[str, str],
                            sink_mapping: Mapping[str, str],
                            subject: Optional[str] = None,
                            label: Optional[str] = None):
    if subject is None:
        subject = '*'

    if label is None:
        label = experiment

    experiment_path = f"data/archive/projects/{project}/subjects/{subject}/experiments/{experiment}"

    # Example source mapping
    # source_mapping = {
    #    "t1": "/scans/s T1W_3D_TFE*/resources/DICOM",
    #    "flair": "/scans/3D_Brain*FLAIR*/resources/DICOM",
    #    "swi":  "/scans/SWI EPI 2min*/resources/DICOM",
    #    "asl": "/scans/ASL SENSE/resources/DICOM",
    #    "m0": "/scans/M0 meting SENSE/resources/DICOM",
    # }

    # Example sink mapping
    # sink_data = {
    #    "t1_nii": "/scans/s T1W_3D_TFE*/resources/NIFTI/files/image{ext}",
    #    "flair_nii": "/scans/3D_Brain*FLAIR*/resources/NIFTI/files/image{ext}",
    #    "swi_nii": "/scans/SWI EPI 2min*/resources/NIFTI/files/image{ext}",
    #    "asl_nii": "/scans/ASL SENSE/resources/NIFTI/files/image{ext}",
    #    "m0_nii": "/scans/M0 meting SENSE/resources/NIFTI/files/image{ext}",
    #    "flair_coregistered": "/scans/s T1W_3D_TFE*/resources/NIFTI/files/flair_coreg_to_t1{ext}",
    #    "swi_coregistered": "/scans/s T1W_3D_TFE*/resources/NIFTI/files/swi_coreg_to_t1{ext}",
    #    "asl_header_json": "/scans/ASL SENSE/resources/JSON/files/dicom_header{ext}",
    #    "m0_header_json": "/scans/M0 meting SENSE/resources/JSON/files/dicom_header{ext}",
    # }

    # Wrap the paths into a full-fledged uri
    source_mapping = {k: {label: create_uri(xnat_uri, experiment_path + v)} for k, v in source_mapping.items()}
    sink_query = {'resource_type': 'xnat:resourceCatalog',
                  'assessors_type': 'xnat:qcAssessmentData'}
    sink_mapping = {k: create_uri(xnat_uri, experiment_path + v, sink_query) for k, v in sink_mapping.items()}

    return source_mapping, sink_mapping


def run_network(network_id: str,
                source_data: Mapping,
                sink_data: Mapping[str, str],
                label: str, fastr_home: Optional[str],
                config: Dict[str, Any]):
    print('SOURCE: {}'.format(source_data))
    print('SINK: {}'.format(sink_data))
    network_files = os.listdir(config['STUDYGOV_PROJECT_NETWORKS'])

    tmpdir = os.path.join(config['STUDYGOV_PROJECT_SCRATCH'], 'fastr_{}_{}'.format(network_id, label))
    code_file_path = tmpdir + '.py'
    stdout_path = tmpdir + '_stdout.txt'
    stderr_path = tmpdir + '_stderr.txt'
    # Create a networkfile that can be run commandline in a fastr/python module environment
    with open(code_file_path, 'w') as code_file:
        code_file.write(
"""#!/bin/env python
# Autogenerated file for network execution via module

import imp
import fastr

# Log to console and reinitialize to take redirected stdout
fastr.config.logtype = 'console'
fastr.config._update_logging()

source_data = {source_data}

sink_data = {sink_data}

""".format(source_data=json.dumps(source_data, indent=4),
           sink_data=json.dumps(sink_data, indent=4))
        )

        if '{}.json'.format(network_id) in network_files:
            network_file = os.path.join(config['STUDYGOV_PROJECT_NETWORKS'], '{}.json'.format(network_id))
            network_file_path = tmpdir + '_network.json'
            shutil.copy2(network_file, network_file_path)
            code_file.write("network = fastr.Network.loadf('{}')\n".format(network_file_path))
        elif '{}.py'.format(network_id) in network_files:
            network_file = os.path.join(config['STUDYGOV_PROJECT_NETWORKS'], '{}.py'.format(network_id))
            network_file_path = tmpdir + '_network.py'
            shutil.copy2(network_file, network_file_path)
            code_file.write("network_module = imp.load_source('{}', '{}')\n".format(network_id, network_file_path))
            code_file.write("network = network_module.create_network()\n")
        else:
            raise ValueError('Could not find network file for {}'.format(network_id))

        print('TMPDIR: {}'.format(tmpdir))
        code_file.write("run = network.execute(source_data, sink_data, tmpdir='vfs://tmp/fastr_{}_{}')\n".format(network_id, label))
        code_file.write("exit(0 if run.result else 1)\n")

    if os.path.exists(tmpdir):
        print('Removing old tmpdir: {}'.format(tmpdir))
        if os.path.isdir(tmpdir):
            shutil.rmtree(tmpdir)
        else:
            os.remove(tmpdir)

    result_data = {
        'network_id': network_id,
        'code_file': code_file_path,
        'scratch_dir': tmpdir,
        'stdout_log': stdout_path,
        'stderr_log': stderr_path,
        'fastr_home': fastr_home,
        'source_data': source_data,
        'sink_data': sink_data,
        'cleanup_done': False,
        'return_value': None,
    }

    # Write the progress to own files
    with open(stdout_path, 'w') as stdout, open(stderr_path, 'w') as stderr:
        if fastr_home:
            os.environ['FASTRHOME'] = fastr_home
        process = subprocess.Popen(['fastr_python_launcher', code_file_path], stdout=stdout, stderr=stderr)
        return_value = process.wait()

    if return_value == 0 and os.path.exists(tmpdir):
        print('Removing tmpdir after success: {}'.format(tmpdir))
        if os.path.isdir(tmpdir):
            shutil.rmtree(tmpdir)
        result_data['cleanup_done'] = True

    result_data['return_value'] = return_value

    return result_data


def fastr(callback_execution_data,
          config: Dict[str, Any],
          network_id: str,
          source_mapping: Mapping[str, str],
          sink_mapping: Mapping[str, str],
          xnat_external_system_name: str = 'XNAT',
          fastr_home: Optional[str] = None,
          **ignore) -> Dict[str, Any]:
    """
    Execute Fastr pipeline

    :param callback_execution_data: All data needed about the callback execution
    :param config: App configuration
    :param network_id: network that gets executed
    :param source_mapping: Mapping[str, str],
    :param sink_mapping: Mapping[str, str],
    :param fastr_home: optionally, set the FASTRHOME variable passed to fastr

    Example:

    .. code-block:: YAML

        function: fastr
        callback_arguments:
          network_id: preprocessing
          source_mapping:
            t1: /scans/T1W*/resources/DICOM
            flair: /scans/*FLAIR*/resources/DICOM
          sink_mapping:
            t1_nii: /scans/T1W*/resources/NIFTI/files/image{ext}
            flair_nii: /scans/*FLAIR*/resources/NIFTI/files/image{ext}
            flair_coregistered: /scans/T1W*/resources/NIFTI/files/flair_to_t1{ext}
          xnat_external_system_name: XNAT
          fastr_home: /path/to/fastr_home

    .. note:: If setting ``fastr_home`` this needs to be available on the worker nodes, as the
              callback will be executed on workers and not the main StuyGovernor process.

    ==================== ====== ===================================================================
    Variable name        Type   Description
    ==================== ====== ===================================================================
    xnat_uri             str    URL of the XNAT server used to create the source and sink data
    project              str    The XNAT project used to create the source and sink data
    subject              str    The XNAT subject id used to create source and sink data
    experiment           str    The XNAT experiment id used to create source and sink data
    source_mapping       dict   The source_mapping used
    sink_mapping         dict   The sink_mapping used
    label                str    The experiment label use as the sample id for fastr
    ==================== ====== ===================================================================

    """
    # Get XNAT address from database
    logging.debug(f"Starting callback for callback execution: {callback_execution_data['uri']}")
    xnat_server = callback_execution_data['external_systems'][xnat_external_system_name].rstrip('/')
    logging.debug(f"Using xnat: {xnat_server}")

    # Fetch data
    print('Get all required information from study manager')
    experiment = callback_execution_data['experiment']
    subject = callback_execution_data['subject']

    experiment_label = experiment['label']
    xnat_experiment_id = experiment['external_ids'][xnat_external_system_name]
    xnat_subject_id = subject['external_ids'][xnat_external_system_name]

    # Create source and sink data
    source_data, sink_data = create_source_sink_data(xnat_uri=xnat_server,
                                                     project=config['STUDYGOV_XNAT_PROJECT'],
                                                     experiment=xnat_experiment_id,
                                                     source_mapping=source_mapping,
                                                     sink_mapping=sink_mapping,
                                                     subject=xnat_subject_id,
                                                     label=experiment_label)

    result = run_network(network_id, source_data, sink_data, experiment_label, fastr_home, config)

    return result
