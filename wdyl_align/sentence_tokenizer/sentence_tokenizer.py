# coding: utf-8
from apps.core.utils import return_data
from apps.sentence_tokenizer.utils import \
    tokenizing, tokenizing_length_limit, tokenizing_word_limit
import logging
from apps.constants import LANG_MAPPING


logger = logging.getLogger('ACT')


def sentence_break_batch(lines, lang):
    try:
        logger.info('[sentence_tokenizer] start sentence_break_batch:' + lines[0])
        if lang not in LANG_MAPPING.keys():
            logger.error('[sentence_tokenizer] language is wrong')
            return return_data(400, 'language not satisfied')
        all_splited_lines = []
        for single_line in lines:
            splited_lines = tokenizing(single_line, lang)
            all_splited_lines.append(splited_lines)
        return return_data(0, 'sentence batch break succeed', all_splited_lines)
    except Exception as e:
        logger.error('[sentence_tokenizer] Exception of breaking batch sentence', exc_info=True)
        return return_data(400, e)


def sentence_break_limit(lines, lang, limit=20):
    try:
        limit = limit if limit > 20 else 20
        if lang not in LANG_MAPPING.keys():
            logger.error('[sentence_tokenizer] language is wrong')
            return return_data(400, 'language not satisfied')
        all_splited_lines = []
        for single_line in lines:
            splited_lines = tokenizing_length_limit(
                single_line, lang, limit)
            all_splited_lines.append(splited_lines)
        return return_data(0, 'sentence length limit break succeed', all_splited_lines)
    except Exception as e:
        logger.error('[sentence_tokenizer] Exception of breaking limit sentence', exc_info=True)
        return return_data(400, e)


def word_break_limit(lines, lang, limit=20):
    try:
        limit = limit if limit > 20 else 20
        if lang not in ['en', 'zh']:
            logger.error('[sentence_tokenizer] language is wrong')
            return return_data(400, 'language not satisfied')
        all_splited_lines = []
        for single_line in lines:
            splited_lines = tokenizing_word_limit(
                single_line, lang, limit)
            all_splited_lines.append(splited_lines)
        return return_data(0, 'sentence word limit break succeed', all_splited_lines)
    except Exception as e:
        logger.error('[sentence_tokenizer] Exception of breaking limit word', exc_info=True)
        return return_data(400, e)
