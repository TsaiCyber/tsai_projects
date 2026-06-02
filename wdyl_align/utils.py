# coding: utf-8
import os
from constants import INTERMEDIATE_FILES_BASE_DIR, ALLOWED_FILE_EXTENSIONS

def return_data(errcode=0, msg='success', data=''):
    return {'errcode': errcode,
            'msg': msg,
            'data': data}


def define_save_files_base_name_and_path(uuid, english_filename, chinese_filename):
    """
    定义保存文件名和路径
    """
    english_filename_base = os.path.splitext(english_filename)[0]
    chinese_filename_base = os.path.splitext(chinese_filename)[0]

    english_file_path = os.path.abspath(os.path.join(INTERMEDIATE_FILES_BASE_DIR, f"{uuid}_en_{english_filename}"))
    chinese_file_path = os.path.abspath(os.path.join(INTERMEDIATE_FILES_BASE_DIR, f"{uuid}_zh_{chinese_filename}"))
    english_txt_file_path = os.path.abspath(os.path.join(INTERMEDIATE_FILES_BASE_DIR, f"{uuid}_en_{english_filename_base}.txt"))
    english_translated_txt_file_path = os.path.abspath(os.path.join(INTERMEDIATE_FILES_BASE_DIR, f"{uuid}_en_translated_{english_filename_base}.txt"))
    chinese_txt_file_path = os.path.abspath(os.path.join(INTERMEDIATE_FILES_BASE_DIR, f"{uuid}_zh_{chinese_filename_base}.txt"))
    chinese_translated_txt_file_path = os.path.abspath(os.path.join(INTERMEDIATE_FILES_BASE_DIR, f"{uuid}_zh_translated_{chinese_filename_base}.txt"))
    final_aligned_excel_file_path = os.path.abspath(os.path.join(INTERMEDIATE_FILES_BASE_DIR, f"aligned_en_{english_filename_base}_zh_{chinese_filename_base}_{uuid}.xlsx"))

    return english_file_path, chinese_file_path, \
        english_txt_file_path, chinese_txt_file_path, \
        english_translated_txt_file_path, chinese_translated_txt_file_path, \
        final_aligned_excel_file_path


def save_content_to_file(content:list = [], file_path:str = ''):
    if not content or not file_path:
        raise ValueError("content or file_path is empty")
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in content:
            f.write(item + '\n')
    return True
