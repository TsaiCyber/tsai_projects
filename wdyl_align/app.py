# coding: utf-8

from flask import Flask, request, jsonify, send_file, render_template_string
import os
import tempfile
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
import re

# 导入初始化模块并在应用启动时预加载资源
from initializer import initialize_resources

from extraction.extract_from_docx import extract_docx_content
from sentence_tokenizer.sentence_tokenizer import split_sentences_batch
from translate_batch.translate_batch import get_translated_content_list

from utils import return_data, define_save_files_base_name_and_path, save_content_to_file
from wdyl_logger.wdyl_logger import logger
from constants import INTERMEDIATE_FILES_BASE_DIR, ALLOWED_FILE_EXTENSIONS

# 导入BLEU对齐模块
from bleu_align.bleu_align import align_files_by_bleu, align_texts_by_bleu, save_alignment_to_excel

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS

@app.route('/')
def index():
    # Return the HTML content from the corpus_align.html file
    with open('corpus_align.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    return html_content


@app.route('/align_documents', methods=['POST'])
def align_documents():
    """
    Endpoint to handle document alignment.
    """
    logger.info("Received POST request to align_documents endpoint")

    try:
        # Check if the post request has the file parts
        if 'english_file' not in request.files or 'chinese_file' not in request.files:
            return return_data(
                errcode=500,
                msg="upload files error",
                data="ERROR: Both English and Chinese files are required")

        english_file = request.files['english_file']
        chinese_file = request.files['chinese_file']

        if english_file.filename == '' or chinese_file.filename == '':
            return return_data(
                errcode=500,
                msg="upload files error",
                data="ERROR: Both files must be selected")

        if not (allowed_file(english_file.filename) and allowed_file(chinese_file.filename)):
            return return_data(
                errcode=500,
                msg="upload files error",
                data="ERROR: Invalid file types. Allowed: .docx")

        english_filename = secure_filename(english_file.filename)
        chinese_filename = secure_filename(chinese_file.filename)

        # 获取任务 UUID
        align_work_session_uuid = uuid.uuid4()

        # 获取各阶段保存文件路径
        english_file_path, chinese_file_path, \
            english_txt_file_path, chinese_txt_file_path, \
            english_translated_txt_file_path, chinese_translated_txt_file_path, \
            final_aligned_excel_file_path= \
            define_save_files_base_name_and_path(
                align_work_session_uuid, english_filename, chinese_filename)

        # 保存文件到本地中间文件目录
        english_file.save(english_file_path)
        chinese_file.save(chinese_file_path)

        # 抽取文件内容
        english_text_list = extract_docx_content(english_file_path, file_language='en')
        chinese_text_list = extract_docx_content(chinese_file_path, file_language='zh')

        # 对文档内容进行分句
        english_tokenized_sentences_list = split_sentences_batch(english_text_list, lang='en')
        chinese_tokenized_sentences_list = split_sentences_batch(chinese_text_list, lang='zh')

        if save_content_to_file(english_tokenized_sentences_list, english_txt_file_path) \
                and save_content_to_file(chinese_tokenized_sentences_list, chinese_txt_file_path):
            logger.info("Successfully extracted documents")
            chinese_tokenized_translated_sentences_list = get_translated_content_list(
                content_list=chinese_tokenized_sentences_list,
                language_direction=('zh', 'en'))

            if save_content_to_file(chinese_tokenized_translated_sentences_list, chinese_translated_txt_file_path):
                logger.info(f"Successfully translate document {chinese_txt_file_path} to {chinese_translated_txt_file_path}")

        # 对齐文档
        df, matches = align_files_by_bleu(
            en_file_path=english_txt_file_path,
            trans_file_path=chinese_translated_txt_file_path,
            zh_file_path=chinese_txt_file_path,
            output_file=final_aligned_excel_file_path)

        # Generate aligned files in different formats
        output_files = []

        final_aligned_excel_file_name = os.path.basename(final_aligned_excel_file_path)
        output_files.append({
            'name': final_aligned_excel_file_name,
            'size': os.path.getsize(final_aligned_excel_file_path),
            'download_url': f'/download/{final_aligned_excel_file_name}',
            'format': 'xlsx',})

        logger.info("Successfully aligned documents")

        return jsonify({
            'success': True,
            'message': 'Documents aligned successfully',
            'files': output_files})

    except Exception as e:
        print(f"Error in align_documents: {str(e)}")
        return return_data(errcode=500,
                           msg='Documents alignment error',
                           data=f'Internal server error: {str(e)}')


@app.route('/download/<filename>')
def download_file(filename):
    """
    Endpoint to download aligned files.
    """
    try:
        filepath = os.path.join(INTERMEDIATE_FILES_BASE_DIR, secure_filename(filename))
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return return_data(errcode=404, msg="Download failed", data=f"File {filepath} not found")
    except Exception as e:
        return return_data(errcode=500, msg="Download failed", data=f"Download failed: {str(e)}")


if __name__ == '__main__':
    # 应用启动时预加载所有必需的资源（NLTK数据包和spaCy模型）
    initialize_resources()

    app.run(debug=True, host='0.0.0.0', port=5000)