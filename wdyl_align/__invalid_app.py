# coding: utf-8

from bottle import request, route, static_file, run, BaseRequest

from wdyl_logger.wdyl_logger import logger
from constants import \
    INTERMEDIATE_FILES_BASE_DIR
from sentence_tokenizer.sentence_tokenizer import \
    split_english_spacy, split_chinese_jieba

# 设置 Bottle 最大内存限制为 100MB（根据需要调整）
BaseRequest.MEMFILE_MAX = 100 * 1024 * 1024


def sentence_tokenizer(sentence: str, lang: str):
    if lang == 'en':
        sentence = split_english_spacy(sentence)
    elif lang == 'zh':
        sentence = split_chinese_jieba(sentence)
    return sentence





@route('/corpus_align')
def corpus_align():
    return static_file("corpus_align.html", ".\\")


def main():
    logger.info("Service Start to Run ...")
    run(host="0.0.0.0", server="paste", port=12345)


if __name__ == '__main__':
    main()
