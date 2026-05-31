# coding: utf-8
import re
import string
import jieba
from uniseg.sentencebreak import sentence_boundaries
from __invalid.__invalid_sentence_tokenizer.sentence_tokenizer_reg \
    import RE_NOT_SPLIT_PATTERN_ZH, RE_NOT_SPLIT_PATTERN_EN, RE_SPLIT_PATTERN_ZH, RE_SPLIT_PATTERN_EN


NOT_SPLIT = 'NOT_SPLIT_PATTERN'


def replace_pattern(line, reg, replace_str):
    start = 0
    frags = []
    en_frags = []

    for match in reg.finditer(line):
        frags.append(line[start: match.span()[0]])
        matched_str = line[match.span()[0]: match.span()[1]]
        frags.append(replace_str)
        en_frags.append(matched_str)
        start = match.span()[1]

    last_frag_text = line[start:]
    if last_frag_text:
        frags.append(last_frag_text)

    return ''.join(frags), en_frags


def replace_pattern_break(line, regs):

    for reg in regs:
        line = re.sub(reg, lambda m: m.groups()[0].replace(
            '\uE105', '') + '\n' + m.groups()[-1].replace('\uE105', ''), line)

    return line


def restorefrags(splited, frags, replaced_str):
    en_idx = 0
    restored = []
    for sentence in splited:
        rp_idx = sentence.find(replaced_str)
        while rp_idx >= 0:
            sentence = sentence[:rp_idx] + frags[en_idx] + \
                sentence[rp_idx + len(replaced_str):]
            rp_idx = sentence.find(replaced_str, rp_idx + len(frags[en_idx]))
            en_idx += 1
        restored.append(sentence)
    return restored


def add_icu_hints(text):
    text = text.strip()
    boun = []
    boundaries = sentence_boundaries(text)
    for i in boundaries:
        boun.append(i)
    boundaries = boun
    boundaries = list(boundaries)
    bound_len = len(boundaries)
    bound_sentences = []
    for i in range(bound_len - 1):
        bound_sentences.append(text[boundaries[i]:boundaries[i + 1]])

    sent_idx = 0
    for sent_idx in range(bound_len - 1):
        sub_sent = bound_sentences[sent_idx]
        sent_len = len(sub_sent)
        i = sent_len
        while i > 0 and sub_sent[i - 1] in ['\f', '\r', '\t', '\v', ' ']:
            i -= 1
        bound_sentences[sent_idx] = sub_sent[:i] + '\uE105' + sub_sent[i:]

    return ''.join(bound_sentences)


def remove_icu_hints(text):
    return text.replace('\uE105', '')


def tokenizing(text, lang):
    text = add_icu_hints(text)
    if lang in ['en', 'fr', 'de', 'it', 'es', 'pt', 'ru', 'tr', 'pt', 'hu']:
        split_reg = RE_SPLIT_PATTERN_EN
        not_split_reg = RE_NOT_SPLIT_PATTERN_EN
    else:
        split_reg = RE_SPLIT_PATTERN_ZH
        not_split_reg = RE_NOT_SPLIT_PATTERN_ZH

    replaced, frags = replace_pattern(
        text.strip(), not_split_reg, NOT_SPLIT)

    replaced = replace_pattern_break(replaced, split_reg)

    splited = replaced.split('\n')
    splited = [each_split for each_split in splited if each_split.strip()
               != '']
    res1 = restorefrags(splited, frags, NOT_SPLIT)
    res1 = [remove_icu_hints(res) for res in res1]
    res1 = [each for each in res1 if each.strip() != '']
    return res1


def long_sentence_break_zh(sentence, limit):
    counter = 0
    temp_counter = 0
    start_idx = 0
    curr_punct_idx = 0
    SENTENCE_BREAK_PUNCT = [';', '，']
    temp_break_list = []
    for idx, each_word in enumerate(sentence):
        counter += 1
        if each_word in SENTENCE_BREAK_PUNCT:
            temp_counter = counter
            curr_punct_idx = idx + 1
        if counter >= limit:
            if curr_punct_idx <= idx + 1 and curr_punct_idx != 0:
                temp_break_list.append(
                    ''.join(sentence[start_idx:curr_punct_idx]))
                start_idx = curr_punct_idx
                curr_punct_idx = 0
                counter = counter - temp_counter
                temp_counter = 0
            else:
                temp_break_list.append(''.join(sentence[start_idx:idx]))
                start_idx = idx
                counter = 0
    if start_idx < len(sentence):
        temp_break_list.append(''.join(sentence[start_idx:]))
    return temp_break_list


def long_sentence_break_en(sentence, limit):
    counter = 0
    temp_counter = 0
    start_idx = 0
    curr_punct_idx = 0
    temp_break_list = []
    for idx, each_char in enumerate(sentence):
        counter += 1
        if each_char in [';', ',', ' ']:
            curr_punct_idx = idx + 1
            temp_counter = counter

        if counter >= limit:
            if curr_punct_idx <= idx + 1 and curr_punct_idx != 0:
                temp_break_list.append(sentence[start_idx:curr_punct_idx])
                start_idx = curr_punct_idx
                curr_punct_idx = 0
                counter = counter - temp_counter
                temp_counter = 0
            else:
                temp_break_list.append(sentence[start_idx:idx])
                start_idx = idx
                counter = 0
    if start_idx < len(sentence):
        temp_break_list.append(sentence[start_idx:])
    return temp_break_list


def tokenizing_length_limit(text, lang, limit):
    final_list = []
    long_sentence_break = long_sentence_break_zh if \
        lang in ['zh', 'ja', 'ko'] else long_sentence_break_en
    if len(text) <= limit:
        return [text]
    else:
        tokenized = tokenizing(text, lang)
        for tok_sent in tokenized:
            if len(tok_sent) <= limit:
                final_list.append(tok_sent)
            else:
                short_sents = long_sentence_break(tok_sent, limit)
                final_list.extend(short_sents)
        return final_list


def word_limit_zh(sentence, word_limit_each_sentence):
    temp_break_list = []
    counter = 0
    temp_counter = 0
    start_idx = 0
    curr_punct_idx = 0
    SENTENCE_BREAK_PUNCT = [';', '，']
    words = list(jieba.cut(sentence))
    for idx, each_word in enumerate(words):
        counter += 1
        if each_word in SENTENCE_BREAK_PUNCT:
            temp_counter = counter
            curr_punct_idx = idx + 1
        if counter >= word_limit_each_sentence:
            if curr_punct_idx <= idx + 1 and curr_punct_idx != 0:
                temp_break_list.append(
                    ''.join(words[start_idx:curr_punct_idx]))
                start_idx = curr_punct_idx
                curr_punct_idx = 0
                counter = counter - temp_counter
                temp_counter = 0
            else:
                temp_break_list.append(''.join(words[start_idx:idx + 1]))
                start_idx = idx + 1
                counter = 0
    if start_idx < len(words):
        temp_break_list.append(''.join(words[start_idx:]))
    return temp_break_list


def word_limit_en(sentence, word_limit_each_sentence):
    temp_break_list = []
    counter = 0
    temp_counter = 0
    consecutive_space_check = False
    start_idx = 0
    curr_punct_idx = 0
    SENTENCE_BREAK_PUNCT = [';', ',']
    for idx, each_char in enumerate(sentence):
        if each_char == " " and (not consecutive_space_check):
            consecutive_space_check = True
            counter += 1
        else:
            consecutive_space_check = False
            if each_char in string.punctuation:
                counter += 2
                consecutive_space_check = True
                if each_char in SENTENCE_BREAK_PUNCT:
                    curr_punct_idx = idx + 1
                    temp_counter = counter

        if counter >= word_limit_each_sentence:
            if curr_punct_idx <= idx + 1 and curr_punct_idx != 0:
                temp_break_list.append(sentence[start_idx:curr_punct_idx])
                start_idx = curr_punct_idx
                curr_punct_idx = 0
                counter = counter - temp_counter
                temp_counter = 0
            else:
                temp_break_list.append(sentence[start_idx:idx])
                start_idx = idx
                counter = 0
    if start_idx < len(sentence):
        temp_break_list.append(sentence[start_idx:])
    return temp_break_list


def tokenizing_word_limit(sentence, lang, limit):
    if lang not in ('zh', 'en'):
        raise ValueError('tokenizing_word_limit lang is not satisfied')
    return word_limit_zh(sentence, limit) if lang == 'zh' else word_limit_en(sentence, limit)
