# coding: utf-8
import os
import configparser


CUR_DIR = os.path.dirname(os.path.abspath(__file__))


def get_specific_config():
    filepath = os.path.join(CUR_DIR, 'sentence_tokenizer_default.properties')
    cfg = configparser.RawConfigParser()
    cfg.read(filepath, encoding='utf-8')
    return cfg
