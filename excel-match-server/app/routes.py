import os
import json
import shutil
import logging
import threading
import pandas as pd

from flask import Blueprint, request, jsonify, send_file
from flask import current_app as app
from .utils import generate_random_string, concat_files, merge_match_candidate, save_result
from .exceptions import ConcatError, FileTypeError, ColumnKeyError, FileError

bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

def remove_files(file_path):
    shutil.rmtree(file_path)
    logger.warning(f'remove dir {file_path}')

# exception handler
@bp.errorhandler(ColumnKeyError)
def column_key_error_handler(e: ColumnKeyError):
    logger.error(e)
    return jsonify({
        'code': 400,
        'message': e.msg
    }), 400
    
@bp.errorhandler(FileTypeError)
def file_type_error_handler(e: FileTypeError):
    logger.error(e)
    timer = threading.Timer(30 * 60, remove_files, kwargs={'file_path': e.file_path})
    timer.start()
    return jsonify({
        'code': 400,
        'message': e.msg
    }), 400

@bp.errorhandler(ConcatError)
def concat_error_handler(e: ConcatError):
    logger.error(e)
    timer = threading.Timer(1 * 60, remove_files)
    timer.start()
    return jsonify({
        'code': 400,
        'message': e.msg
    }), 400

@bp.errorhandler(FileError)
def concat_error_handler(e: FileError):
    logger.error(e)
    return jsonify({
        'code': 400,
        'message': e.msg
    }), 400

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


    merge_condition = json.loads(merge_condition)

    # resolve excel files
    merge_match_files = concat_files(os.path.join(base_path, 'match'), mode='match')
    merge_candidate_files = concat_files(os.path.join(base_path, 'candidate'), mode='candidate')


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