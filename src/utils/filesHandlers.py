def ProcessFileRemoveCertainRows(input_file, output_file, line_ranges_to_remove:list):
    """
    从输入文件中删除指定的行数范围，并将剩余的内容保存到输出文件中。

    :example
    `# 定义要删除的行数区间列表
    ranges_to_remove = [(2, 4), (7, 9)]
    # 调用函数
    ProcessFileRemoveCertainRows('input.txt', 'output.txt', ranges_to_remove)
    `
    :param input_file: 输入文件的路径
    :param output_file: 输出文件的路径
    :param line_ranges_to_remove: 要删除的行数范围列表，每个元素是一个包含开始和结束行号的元组
    """
    # 读取原始文件内容
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 对行数区间进行排序
    line_ranges_to_remove.sort()

    # 根据line_ranges_to_remove中的行数区间删除相应行
    lines_to_keep = []
    for i, line in enumerate(lines, start=1):
        should_remove = False
        for start, end in line_ranges_to_remove:
            if start <= i <= end:
                should_remove = True
                break
        if not should_remove:
            lines_to_keep.append(line)

    # 将剩余内容保存到新文件
    with open(output_file, 'w',encoding='utf-8') as f:
        f.writelines(lines_to_keep)