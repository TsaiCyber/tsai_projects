# coding: utf-8

import jieba
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.tokenize import word_tokenize

from wdyl_logger.wdyl_logger import logger


def download_nltk_data():
    """下载必要的NLTK数据"""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')


def tokenize_text(text, language='english'):
    """
    根据语言类型进行分词

    参数:
    text (str): 待分词的文本
    language (str): 语言类型，'chinese'或'english'

    返回:
    list: 分词结果列表
    """
    if language.lower() == 'chinese':
        return list(jieba.cut(text))
    else:  # english
        download_nltk_data()
        return word_tokenize(text.lower())


def calculate_bleu(reference_texts, candidate_text, language='english', n_grams=4):
    """
    计算BLEU分数（支持中文和英文）

    参数:
    reference_texts (list): 参考译文列表，每个元素是一个字符串
    candidate_text (str): 待评估的译文
    language (str): 语言类型，'chinese'或'english'，默认为'english'
    n_grams (int): 考虑的最大n-gram级别，默认为4

    返回:
    float: BLEU分数
    """
    # 分词
    references = [tokenize_text(ref, language) for ref in reference_texts]
    candidate = tokenize_text(candidate_text, language)

    # 计算不同n-gram的权重
    weights = tuple([1.0 / n_grams] * n_grams)

    # 使用平滑函数处理短句子
    smoothing_function = SmoothingFunction().method4

    # 计算BLEU分数
    bleu_score = sentence_bleu(
        references,
        candidate,
        weights=weights,
        smoothing_function=smoothing_function
    )

    return bleu_score


def calculate_bleu_by_level(reference_texts, candidate_text, language='english'):
    """
    计算不同n-gram级别的BLEU分数（支持中文和英文）

    参数:
    reference_texts (list): 参考译文列表
    candidate_text (str): 待评估的译文
    language (str): 语言类型，'chinese'或'english'

    返回:
    dict: 包含BLEU-1到BLEU-4分数的字典
    """
    results = {}

    for n in range(1, 5):
        weights = [0.0] * 4
        weights[n - 1] = 1.0

        references = [tokenize_text(ref, language) for ref in reference_texts]
        candidate = tokenize_text(candidate_text, language)

        smoothing_function = SmoothingFunction().method4

        score = sentence_bleu(
            references,
            candidate,
            weights=tuple(weights),
            smoothing_function=smoothing_function
        )
        results[f"BLEU-{n}"] = score

    return results


def batch_calculate_bleu(reference_list, candidate_list, language='english'):
    """
    批量计算BLEU分数

    参数:
    reference_list (list): 参考译文列表的列表
    candidate_list (list): 待评估译文列表
    language (str): 语言类型

    返回:
    list: BLEU分数列表
    """
    scores = []
    for references, candidate in zip(reference_list, candidate_list):
        score = calculate_bleu(references, candidate, language)
        scores.append(score)
    return scores


if __name__ == "__main__":
    logger.info("=== 英文BLEU测试 ===")
    # 英文示例
    en_reference1 = "The cat is on the mat."
    en_reference2 = "There is a cat on the mat."
    en_candidate = "The cat is on the mat."

    en_references = [en_reference1, en_reference2]

    logger.info("参考译文:")
    for i, ref in enumerate(en_references, 1):
        logger.info(f"  {i}. {ref}")
    logger.info(f"待评估译文: {en_candidate}")

    # 计算综合BLEU分数
    en_bleu_score = calculate_bleu(en_references, en_candidate, language='english')
    logger.info(f"综合BLEU分数: {en_bleu_score:.4f}")

    # 计算各n-gram级别的BLEU分数
    en_bleu_by_level = calculate_bleu_by_level(en_references, en_candidate, language='english')
    for level, score in en_bleu_by_level.items():
        logger.info(f"{level}: {score:.4f}")

    logger.info("\n=== 中文BLEU测试 ===")
    # 中文示例
    zh_reference1 = "这只猫在垫子上。"
    zh_reference2 = "有一只猫在垫子上。"
    zh_candidate = "这只猫在垫子上。"

    zh_references = [zh_reference1, zh_reference2]

    logger.info("参考译文:")
    for i, ref in enumerate(zh_references, 1):
        logger.info(f"  {i}. {ref}")
    logger.info(f"待评估译文: {zh_candidate}")

    # 计算综合BLEU分数
    zh_bleu_score = calculate_bleu(zh_references, zh_candidate, language='chinese')
    logger.info(f"综合BLEU分数: {zh_bleu_score:.4f}")

    # 计算各n-gram级别的BLEU分数
    zh_bleu_by_level = calculate_bleu_by_level(zh_references, zh_candidate, language='chinese')
    for level, score in zh_bleu_by_level.items():
        logger.info(f"{level}: {score:.4f}")

    logger.info("\n=== 中文对比测试 ===")
    zh_candidate2 = "猫在垫子上。"
    logger.info(f"待评估译文: {zh_candidate2}")
    zh_bleu_score2 = calculate_bleu(zh_references, zh_candidate2, language='chinese')
    logger.info(f"综合BLEU分数: {zh_bleu_score2:.4f}")
