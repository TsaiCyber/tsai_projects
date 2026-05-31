import subprocess
import sys
import re
import jieba
import spacy
import nltk
from nltk.tokenize import sent_tokenize


def load_spacy_model(model_name: str):
    """
    智能加载 spaCy 模型，如果模型不存在则自动下载
    """
    try:
        # 尝试直接加载模型
        nlp = spacy.load(model_name)
        print(f"✅ 成功加载模型: {model_name}")
        return nlp
    except OSError:
        # 捕获到模型不存在的错误 (OSError: [E050])
        print(f"⚠️ 未找到模型 '{model_name}'，正在尝试自动下载...")
        try:
            # 使用当前 Python 解释器执行下载命令
            subprocess.check_call([sys.executable, "-m", "spacy", "download", model_name])
            print(f"✅ 模型 '{model_name}' 下载并安装成功！")

            # 下载完成后，重新加载模型
            nlp = spacy.load(model_name)
            return nlp
        except Exception as e:
            print(f"❌ 自动下载模型失败，请检查网络连接或手动执行命令: python -m spacy download {model_name}")
            raise e


# 首次使用NLTK需要下载punkt数据包
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# # 加载spaCy英文模型
# nlp_en = spacy.load("en_core_web_sm")
# 使用封装好的函数来加载英文模型
nlp_en = load_spacy_model("en_core_web_sm")


# 1. 英文断句：使用 spaCy（工业级，准确度高，速度快）
def split_english_spacy(text):
    doc = nlp_en(text)
    return [sent.text.strip() for sent in doc.sents]


# 2. 英文断句：使用 NLTK（学术常用，简单易用）
def split_english_nltk(text):
    return sent_tokenize(text)


# 3. 中文断句：使用 正则表达式（最常用，兼容性好）
def split_chinese_regex(text):
    # 匹配中文常见的句子结束标点：。！？；以及英文的.!?
    pattern = r'([。！？；.!?]["”’]?)'
    # 在结束标点后插入特殊分隔符
    processed_text = re.sub(pattern, r'\1<SEP>', text)
    sentences = [s.strip() for s in processed_text.split('<SEP>') if s.strip()]
    return sentences


# 4. 中文断句：使用 jieba + 标点判断（结合分词，逻辑更严密）
def split_chinese_jieba(text):
    punctuations = set("。！？；.!?")
    sentences = []
    current_sentence = ""

    # jieba.cut 会将文本切分成词，我们遍历这些词
    for word in jieba.cut(text):
        current_sentence += word
        # 如果词的最后一个字符是标点符号，认为是一个句子的结束
        if word[-1] in punctuations:
            sentences.append(current_sentence.strip())
            current_sentence = ""

    if current_sentence.strip():
        sentences.append(current_sentence.strip())
    return sentences


if __name__ == "__main__":
    # 测试英文文本
    en_text = "Hello world! This is a test sentence. Is Python great for NLP tasks? Yes, it is."
    print("--- 英文断句测试 ---")
    print("spaCy结果:", split_english_spacy(en_text))
    print("NLTK结果: ", split_english_nltk(en_text))

    # 测试中文文本
    cn_text = "你好，世界！这是一个测试文本。Python在处理自然语言时非常方便，你觉得呢？"
    print("\n--- 中文断句测试 ---")
    print("正则表达式结果:", split_chinese_regex(cn_text))
    print("jieba分词结果:  ", split_chinese_jieba(cn_text))