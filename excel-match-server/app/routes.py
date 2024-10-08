import os
import json
import shutil
import logging
import threading
import pandas as pd

from flask import Blueprint, request, jsonify, send_file
from flask import current_app as app
from .utils import generate_random_string, concat_files, merge_match_candidate, save_result, dynamic_filter, filter_conditions
from .exceptions import ConcatError, FileTypeError, ColumnKeyError, FileError

bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

def remove_files(file_path):
    shutil.rmtree(file_path)
    logger.warning(f'remove dir {file_path}')

# exception handler
@bp.errorhandler(FileError)
def concat_error_handler(e: FileError):
    logger.error(e)
    return jsonify({
        'code': 400,
        'message': e.msg
    }), 400

@bp.errorhandler(Exception)
def global_error_handler(e: Exception):
    logger.error(e)
    return jsonify({
        'code': 500,
        'message': 'Internal Server Error'
    }), 500

# router

@bp.route('/match', methods=["POST"])
def match():
    match_files = request.files.getlist('match_files')
    candidate_files = request.files.getlist('candidate_files')

    if not match_files or not candidate_files:
        raise FileError("Files are empty, please check and reupload.")

    # save match and candidate files
    folder_name = generate_random_string(len=16)
    base_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)

    # remove uploaded files in server after 30 mins
    timer = threading.Timer(30 * 60, remove_files, kwargs={'file_path': base_path})
    timer.start()

    if not os.path.exists(base_path):
        os.makedirs(os.path.join(base_path, 'match'))
        os.makedirs(os.path.join(base_path, 'candidate'))

    for match_file in match_files:
        if not match_file.filename.endswith(app.config['SUPPORT_TYPES']):
            suffix = match_file.filename.split('.')[-1]
            raise FileTypeError(f'Not supproted file type {suffix}.', base_path)
        
        match_file.save(os.path.join(base_path, os.path.join('match', match_file.filename)))

    for candidate_file in candidate_files:
        if not candidate_file.filename.endswith(app.config['SUPPORT_TYPES']):
            suffix = candidate_file.filename.split('.')[-1]
            raise FileTypeError(f'Not supproted file type {suffix}.', base_path)
        
        candidate_file.save(os.path.join(base_path, os.path.join('candidate', candidate_file.filename)))

    merge_condition = request.form.get('merge_condition')
    mode = request.form.get('mode')
    file_name = request.form.get('file_name')
    additional_conditions = request.form.get('additional_conditions')

    additional_conditions  = json.loads(additional_conditions)
    merge_condition = json.loads(merge_condition)

    # resolve excel files
    merge_match_files = concat_files(os.path.join(base_path, 'match'), mode='match')
    merge_candidate_files = concat_files(os.path.join(base_path, 'candidate'), mode='candidate')

    match_conditions, candidate_conditions, joint_conditions = filter_conditions(additional_conditions)

    if len(additional_conditions) > 0:
        merge_match_files = dynamic_filter(merge_match_files, match_conditions)
        merge_candidate_files = dynamic_filter(merge_candidate_files, candidate_conditions)

    result_df = merge_match_candidate(match_df=merge_match_files, 
                                      candidate_df=merge_candidate_files, 
                                      merge_condition=merge_condition, 
                                      mode=mode)
    
    save_result(result_df, os.path.join(base_path, file_name))

    return jsonify({
        'code': 200,
        'message': os.path.join(base_path, file_name)[2:].replace("\\\\", "/")
    })

@bp.route('/download', methods=["GET"])
def download():
    location = request.values.get('location')
    return send_file(os.path.join(os.pardir, location))