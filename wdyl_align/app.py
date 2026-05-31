# coding: utf-8

from __invalid_sentence_tokenizer.sentence_tokenizer import sentence_break_batch


def sentence_tokenizer(sentence: list, lang: str):
    sentence_break_batch(sentence, lang)
    pass


if __name__ == '__main__':
    sentence_tokenizer(['您好。很高兴认识您！'], 'en')