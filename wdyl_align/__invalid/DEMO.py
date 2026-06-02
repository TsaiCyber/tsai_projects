import re
import xml.etree.ElementTree as ET

def extract_source_content_without_tags(file_path, file_language='en'):
    """
    提取XLF文件中所有以<source xml:lang="en|zh">开头，以</source>结尾的内容，并去除标签
    """
    chinese_contents = []

    try:
        # 方法1: 使用正则表达式提取
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 正则表达式匹配<source xml:lang="zh">...内容...</source>
        pattern = f'<source xml:lang="{file_language}">(.*?)</source>'
        matches = re.findall(pattern, content, re.DOTALL)

        for match in matches:
            # 去除XLIFF中的占位符标签，如 <x id="1"/> 和 <g id="3">内容</g>
            cleaned_match = remove_xliff_tags(match)
            if cleaned_match.strip():  # 只添加非空内容
                chinese_contents.append(cleaned_match.strip())

    except Exception as e:
        print(f"使用正则表达式读取失败: {e}")

        # 方法2: 使用XML解析器作为备选方案
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            # 查找所有带有xml:lang="zh"属性的source元素
            for elem in root.iter():
                if elem.tag.endswith('source') and elem.get('{http://www.w3.org/XML/1998/namespace}lang') == f'{file_language}':
                    text = elem.text
                    if text and text.strip():
                        cleaned_text = remove_xliff_tags(text)
                        chinese_contents.append(cleaned_text.strip())

        except Exception as xml_error:
            print(f"XML解析也失败了: {xml_error}")

    return chinese_contents


def remove_xliff_tags(text):
    """
    去除XLIFF文件中的占位符标签
    """
    # 去除自闭合标签 <x id="数字"/>
    text = re.sub(r'<x\s+id="\d+"/>', '', text)
    # 去除自闭合标签 <g id="数字"/>
    text = re.sub(r'<g\s+id="\d+"/>', '', text)
    # 去除 <g id="数字">内容</g> 格式的标签
    text = re.sub(r'<g\s+id="\d+">(.*?)</g>', r'\1', text)
    # 去除其他可能的XML标签
    text = re.sub(r'<[^>]+>', '', text)
    # 清理多余的空白字符
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def main():
    files_path = [
        (r'c:\Users\Tsai\Desktop\参考语料文件\1\en_extract\_q0lra3Yi2Bk-JQ3DnREA.docx.xlf', 'en'),
        (r'c:\Users\Tsai\Desktop\参考语料文件\1\cn_extract\sea5mk0fhEEqxJ1StuJOL.docx.xlf', 'zh')
    ]

    for file_path, file_language in files_path:
        print(f"\n处理文件: {file_path}")
        # 提取内容并去除标签
        results = extract_source_content_without_tags(file_path, file_language)

        # for i, content in enumerate(results, 1):
        #     print(f"{i}. {content[:100]}{'...' if len(content) > 100 else ''}")  # 截断长内容便于显示
        #     if i <= 10:  # 只显示前10个示例
        #         continue
        #     elif i == 11:
        #         print("...")
        #         break

        # 保存到新的文件
        output_filename = f'cleaned_{file_language}_content.txt'
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            for content in results:
                output_file.write(content + '\n')

        print(f"\n已将所有提取并清理后的内容保存到 '{output_filename}' 文件中")

        # # 显示一些具体的清理效果
        # print("\n清理效果示例:")
        # sample_texts = results[:5] if len(results) >= 5 else results
        # for i, content in enumerate(sample_texts, 1):
        #     print(f"示例{i}: {content}")


if __name__ == "__main__":
    main()
