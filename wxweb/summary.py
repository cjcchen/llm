# 安装依赖：pip install jieba textrank4zh

from textrank4zh import TextRank4Sentence

def textrank_summary(text, num_sentences=3):
    """
    使用TextRank算法提取关键句子
    :param text: 输入的中文文本
    :param num_sentences: 返回的关键句数量
    :return: 归纳总结后的文本
    """
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source='all_filters')
    
    # 获取最重要的num_sentences个句子
    key_sentences = tr4s.get_key_sentences(num=num_sentences)
    
    # 按原文顺序排序并拼接
    sorted_sentences = sorted(key_sentences, key=lambda x: x.index)
    return ''.join([s.sentence for s in sorted_sentences])

if __name__ == '__main__':
  # 示例使用
  original_text = """
  人工智能技术正在深刻改变医疗行业。最新研究显示，AI辅助诊断系统在肺癌筛查中的准确率已达到92%，
  超过人类放射科医生的平均水平。多家医院已部署AI分诊系统，有效缩短了患者等待时间。
  专家预测，到2025年，全球医疗AI市场规模将超过340亿美元。但同时需要关注数据隐私和伦理问题。
  """

  summary = textrank_summary(original_text, num_sentences=2)
  print("关键句提取结果：")
  print(summary)
