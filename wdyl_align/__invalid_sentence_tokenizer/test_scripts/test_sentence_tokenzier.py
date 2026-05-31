# coding: utf-8
from apps.core.utils import return_data
from apps.sentence_tokenizer.sentence_tokenizer import sentence_break_batch, sentence_break_limit, word_break_limit

url = 'http://localhost:18088/sentence-tokenizer/regrex-tokenizer'


def test_sentence_batch_break():
    sentence_batch_break_data = {
        'lines': ['申请书主张，原产于巴西的白羽肉鸡产品;以低于正常价值的价格向中国出口销售。[1]申请人依据合理获得的证据和信息，在申请书中以巴西申请调查产品的同类产品在本国市场销售价格作为确定巴西白羽肉鸡产品正常价值的基础，以中国海关统计的巴西申请调查产品对中国出口价格作为确定出口价格的基础，在对影响价格可比性的各种因素进行调整后，主张申请调查产品存在较大幅度的倾销。申请书同时主张，申请调查产品进入中国市场数量大幅增长，价格大幅下降，对国内产业同类产品价格造成削减和抑制，导致国内产业产能、销售数量、销售收入增长幅度下降，销售价格总体呈下降趋势，投资收益率始终为负值，国内产业遭受了实质损害，且申请调查产品的倾销与国内产业实质损害存在因果关系。经审查，商务部认为申请书中包含了《中华人民共和国反倾销条例》第十四条、第十五条规定的反倾销调查立案所要求的内容及有关证据。'],
        'lang': 'zh'
    }

    data = [
        ['申请书主张，原产于巴西的白羽肉鸡产品;以低于正常价值的价格向中国出口销售。[1]',
         '申请人依据合理获得的证据和信息，在申请书中以巴西申请调查产品的同类产品在本国市场销售价格作为确定巴西白羽肉鸡产品正常价值的基础，以中国海关统计的巴西申请调查产品对中国出口价格作为确定出口价格的基础，在对影响价格可比性的各种因素进行调整后，主张申请调查产品存在较大幅度的倾销。',
         '申请书同时主张，申请调查产品进入中国市场数量大幅增长，价格大幅下降，对国内产业同类产品价格造成削减和抑制，导致国内产业产能、销售数量、销售收入增长幅度下降，销售价格总体呈下降趋势，投资收益率始终为负值，国内产业遭受了实质损害，且申请调查产品的倾销与国内产业实质损害存在因果关系。',
         '经审查，商务部认为申请书中包含了《中华人民共和国反倾销条例》第十四条、第十五条规定的反倾销调查立案所要求的内容及有关证据。']
    ]

    expect_res = return_data(0, 'sentence batch break succeed', data)

    sentence_batch_break_res = sentence_break_batch(
        sentence_batch_break_data['lines'],
        sentence_batch_break_data['lang']
    )
    return sentence_batch_break_res, expect_res


def test_sentence_length_limit_break():
    sentence_length_limit_break_data = {
        'lines': ['申请书主张，原产于巴西的白羽肉鸡产品以低于正常价值的价格向中国出口销售。'],
        'lang': 'zh',
        'limit': 30
    }

    data = [
        ['申请书主张，',
         '原产于巴西的白羽肉鸡产品以低于正常价值的价格向中国出口销售',
         '。']
    ]
    expect_res = return_data(0, 'sentence length limit break succeed', data)

    sentence_length_limit_break_res = sentence_break_limit(
        sentence_length_limit_break_data['lines'],
        sentence_length_limit_break_data['lang'],
        sentence_length_limit_break_data['limit']
    )
    return sentence_length_limit_break_res, expect_res


def test_sentence_word_limit_break():
    sentence_word_limit_break_data = {
        'lines': ['申请书主张，原产于巴西的白羽肉鸡产品以低于正常价值的价格向中国出口销售。'],
        'lang': 'zh',
        'limit': 30
    }

    data = [
        ['申请书主张，原产于巴西的白羽肉鸡产品以低于正常价值的价格向中国出口销售。']
    ]
    expect_res = return_data(0, 'sentence word limit break succeed', data)

    sentence_word_limit_break_res = word_break_limit(
        sentence_word_limit_break_data['lines'],
        sentence_word_limit_break_data['lang'],
        sentence_word_limit_break_data['limit']
    )
    return sentence_word_limit_break_res, expect_res


batch_break_res, expect_batch_break_res = test_sentence_length_limit_break()
length_limit_break_res, expect_length_limit_break_res = test_sentence_length_limit_break()
word_limit_break_res, expect_word_limit_break_res = test_sentence_word_limit_break()


assert batch_break_res == expect_batch_break_res
assert length_limit_break_res == expect_length_limit_break_res
assert word_limit_break_res == expect_word_limit_break_res
