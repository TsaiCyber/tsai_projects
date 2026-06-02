# coding: utf-8

import pandas as pd
import numpy as np
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from itertools import product

from wdyl_logger.wdyl_logger import logger


def read_lines(file_path):
    """
    读取文件中的所有行

    Args:
        file_path (str): 文件路径

    Returns:
        list: 包含所有非空行的列表
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


def compute_bleu(reference, hypothesis):
    """
    计算两个句子之间的BLEU分数

    Args:
        reference (str): 参考句（英文）
        hypothesis (str): 候选句（翻译）

    Returns:
        float: BLEU分数
    """
    ref_tokens = reference.split()
    hyp_tokens = hypothesis.split()
    # BLEU-4，权重均匀
    weights = (0.25, 0.25, 0.25, 0.25)
    smoothing = SmoothingFunction().method1
    score = sentence_bleu([ref_tokens], hyp_tokens, weights=weights, smoothing_function=smoothing)
    return score


def align_texts_by_bleu(en_sentences, trans_sentences):
    """
    使用BLEU分数对两个句子列表进行对齐，为每个英文句子找到最高分的翻译

    Args:
        en_sentences (list): 英文句子列表
        trans_sentences (list): 翻译句子列表

    Returns:
        list: 包含(英文索引, 翻译索引, BLEU分数)的匹配结果列表
    """
    # 构建分数矩阵：rows=英文索引，cols=译文索引
    score_matrix = np.zeros((len(en_sentences), len(trans_sentences)))
    for i, en in enumerate(en_sentences):
        for j, tr in enumerate(trans_sentences):
            score_matrix[i, j] = compute_bleu(en, tr)

    matches = []  # 存储 (en_idx, trans_idx, score)

    # 为每个英文句子找到得分最高的翻译
    for i in range(len(en_sentences)):
        best_score = -1
        best_j = -1
        for j in range(len(trans_sentences)):
            s = score_matrix[i, j]
            if s > best_score:
                best_score = s
                best_j = j
        if best_j != -1:
            matches.append((i, best_j, best_score))

    return matches


def save_alignment_to_excel(matches, en_sentences, trans_sentences, zh_sentences=None,
                            output_file='aligned_sentences.xlsx'):
    """
    将对齐结果保存到Excel文件

    Args:
        matches (list): 匹配结果列表
        en_sentences (list): 英文句子列表
        trans_sentences (list): 翻译句子列表
        zh_sentences (list, optional): 中文句子列表，用于提供与translated_text.txt索引对应的原文
        output_file (str): 输出文件名

    Returns:
        DataFrame: 包含对齐结果的DataFrame
    """
    result = []
    for i, j, score in matches:
        row_data = {
            'English': en_sentences[i],
            'Translated': trans_sentences[j],
            'BLEU_Score': round(score * 100, 2)  # 转为百分制更直观
        }

        # 如果提供了中文句子列表，且索引j在范围内，则添加中文原文
        if zh_sentences is not None and j < len(zh_sentences):
            row_data['Chinese'] = zh_sentences[j]

        result.append(row_data)

    df = pd.DataFrame(result)
    df.to_excel(output_file, index=False, engine='openpyxl')
    return df


def align_files_by_bleu(en_file_path, trans_file_path, zh_file_path=None, output_file='aligned_sentences.xlsx'):
    """
    对两个文本文件进行BLEU对齐并保存到Excel

    Args:
        en_file_path (str): 英文文件路径
        trans_file_path (str): 翻译文件路径
        zh_file_path (str, optional): 中文文件路径，用于提供与translated_text.txt索引对应的原文
        output_file (str): 输出文件名

    Returns:
        tuple: (DataFrame, matches_list) 包含结果的数据框和匹配列表
    """
    en_sentences = read_lines(en_file_path)
    trans_sentences = read_lines(trans_file_path)

    # 读取中文句子列表（如果提供了路径）
    zh_sentences = None
    if zh_file_path:
        zh_sentences = read_lines(zh_file_path)

    matches = align_texts_by_bleu(en_sentences, trans_sentences)
    logger.info(f"匹配成功 {len(matches)} 对")

    df = save_alignment_to_excel(matches, en_sentences, trans_sentences, zh_sentences, output_file)
    logger.info(f"已保存到 {output_file}")

    return df, matches


# 如果直接运行此脚本，则执行默认操作
if __name__ == '__main__':
    en_sentences = read_lines('en_text.txt')
    trans_sentences = read_lines('translated_text.txt')
    # 如果有对应的中文文件，也可以加载
    # zh_sentences = read_lines('zh_text.txt')

    matches = align_texts_by_bleu(en_sentences, trans_sentences)
    logger.info(f"匹配成功 {len(matches)} 对")

    df = save_alignment_to_excel(matches, en_sentences, trans_sentences, None, 'aligned_sentences.xlsx')
    logger.info("已保存到 aligned_sentences.xlsx")
