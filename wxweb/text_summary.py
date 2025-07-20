# 安装依赖：pip install transformers torch sentencepiece

from transformers import pipeline

def summarize_chinese_text(text):
    """
    使用预训练模型生成中文摘要
    :param text: 输入的中文文本
    :return: 归纳总结后的文本
    """
    # 使用IDEA-CCNL/Randeng-Pegasus-523M-Summary-Chinese模型
    summarizer = pipeline("summarization", model="IDEA-CCNL/Randeng-Pegasus-523M-Summary-Chinese")
    
    # 生成摘要（调整参数控制输出长度）
    summary = summarizer(
        text,
        max_length=150,    # 最大输出长度
        min_length=50,     # 最小输出长度
        do_sample=False,   # 不使用采样（更确定性输出）
        truncation=True    # 截断超长文本
    )
    
    return summary[0]['summary_text']

# 示例使用
original_text = """
北京时间2023年7月20日，中国航天局宣布嫦娥六号任务取得圆满成功。
探测器在月球背面南极-艾特肯盆地完成了样本采集工作，共带回1731克月壤样本。
这是人类首次从月球背面获取样品，对研究月球形成和演化历史具有重要意义。
科学家表示，这些样本中包含不同地质年代的月壤，将帮助人类更好地理解月球的地质演化过程。
"""

summary = summarize_chinese_text(original_text)
print("归纳总结结果：")
print(summary)
