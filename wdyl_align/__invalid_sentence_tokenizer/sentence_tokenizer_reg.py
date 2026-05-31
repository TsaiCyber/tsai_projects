# coding: utf-8
import re
import json
from __invalid_sentence_tokenizer.config import get_specific_config

import logging
logger = logging.getLogger('ACT')

cfg = get_specific_config()


def preprocess_regex_pattern(pattern):
    """
    预处理正则表达式模式，移除内联标志并返回纯净的模式
    """
    # 匹配形如 (?i), (?m), (?s), (?x), (?im) 等内联标志
    inline_flag_pattern = r'^\\(\\?[a-zA-Z]+\\)(.*)$'
    match = re.match(inline_flag_pattern, pattern)
    if match:
        return match.group(1)   
    
    # 如果没有内联标志，直接返回原模式
    return pattern


def list_to_re(re_list):
    # 预处理正则表达式的两部分，移除内联标志
    processed_part1 = preprocess_regex_pattern(re_list[0])
    processed_part2 = preprocess_regex_pattern(re_list[1])
    pt = re.compile('(%s)(%s)' % (processed_part1, processed_part2), re.IGNORECASE)
    return pt


split_common_last = [r'\uE105\s*', r'']

split_common_last = list_to_re(split_common_last)


def get_config_not_split(key):
    rules_return = []
    if key in cfg:
        rules = dict(cfg[key]).values()
    else:
        return []
    for rule in rules:
        rule_before_after = json.loads(rule)
        # 分别处理 before 和 after 部分
        processed_before = preprocess_regex_pattern(rule_before_after[0])
        processed_after = preprocess_regex_pattern(rule_before_after[1])
        pattern = processed_before + processed_after
        
        split_re = '(' + pattern + ')'
        rules_return.append(split_re)
    return rules_return


def get_config_split(key):
    rules_return = []
    if key in cfg:
        rules = dict(cfg[key]).values()
    else:
        return []
    for rule in rules:
        rule_before_after = json.loads(rule)
        split_re = list_to_re(rule_before_after)
        rules_return.append(split_re)
    return rules_return


not_split_common = get_config_not_split('common_not_split')


not_split_zh = get_config_not_split('zh_not_split')
not_split_zh = not_split_common + not_split_zh

# not_split_en = [not_split_common]


not_split_en = get_config_not_split('en_not_split')
not_split_en = not_split_common + not_split_en

not_split_zh = '|'.join(not_split_zh)
not_split_en = '|'.join(not_split_en)


split_common = get_config_split('common_split')
split_en = get_config_split('en_split')
split_zh = get_config_split('zh_split')

split_zh = split_zh + split_common
split_en = split_en + split_common
split_zh.append(split_common_last)
split_en.append(split_common_last)


# 编译正则表达式时使用 IGNORECASE 标志，以处理那些原本包含 (?i) 的模式
RE_NOT_SPLIT_PATTERN_ZH = re.compile(not_split_zh)
RE_NOT_SPLIT_PATTERN_EN = re.compile(not_split_en)
RE_SPLIT_PATTERN_ZH = split_zh
RE_SPLIT_PATTERN_EN = split_en

# logger.info('zh not split pattern:')
# logger.info(RE_NOT_SPLIT_PATTERN_ZH)
# logger.info('en not split pattern:')
# logger.info(RE_NOT_SPLIT_PATTERN_EN)
# logger.info('zh split pattern:')
# logger.info(RE_SPLIT_PATTERN_ZH)
# logger.info('en split pattern:')
# logger.info(RE_SPLIT_PATTERN_EN)