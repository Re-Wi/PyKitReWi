# # -*- coding: utf-8 -*-
# import ast
# import astor  # astor 库用于将 AST 转换回 Python 代码
#
# class ParentVisitor(ast.NodeVisitor):
#     def __init__(self):
#         self.parent_stack = []
#
#     def visit(self, node):
#         self.parent_stack.append(node)
#         super(ParentVisitor, self).visit(node)
#         self.parent_stack.pop()
#
#     def get_parent(self):
#         if len(self.parent_stack) > 1:
#             return self.parent_stack[-2]
#         else:
#             return None
#
# # 读取 Python 源代码文件
# with open('filePathHelper.py', 'r', encoding='utf-8') as file:
#     source_code = file.read()
#
# # 解析 Python 代码为 AST
# parsed_code = ast.parse(source_code)
#
# # 初始化 Visitor
# parent_visitor = ParentVisitor()
#
# # 用于存储模块级别函数和类内部函数的列表
# # 初始化存储函数、类、类中的函数、属性、注释和导入的包的列表和字典
# imports = []
# # comments = {}
# module_level_functions = []
# classes = []
# class_level_functions = []
# attributes = []
#
# # 遍历 AST 树，查找函数、类、类中的函数、属性、注释和导入的包
# for node in ast.walk(parsed_code):
#     parent_visitor.visit(node)
#     parent_node = parent_visitor.get_parent()
#     if isinstance(node, ast.FunctionDef):
#         # 这里可以访问函数定义的父节点 parent_node
#         print("Function Name:", node.name)
#         # 检查函数是否位于类内部
#         if parent_node and isinstance(node.parent, ast.ClassDef):
#             print("Parent Node:", type(parent_node).__name__)
#             class_level_functions.append(node)
#         else:
#             module_level_functions.append(node)
#         # comments[node.name] = ast.get_docstring(node)
#     elif isinstance(node, ast.ClassDef):
#         classes.append(node)
#     elif isinstance(node, ast.Attribute):
#         attributes.append(node)
#     elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
#         imports.append(node)
#
# # 提取所需的代码
# selected_code = ['# -*- coding: utf-8 -*-\n']
#
# # 添加导入的包
# selected_code.extend(astor.to_source(import_node) for import_node in imports)
#
# # 添加类和类中的函数
# for class_node in classes:
#     class_code = astor.to_source(class_node)
#     selected_code.append(class_code)
#
# # 添加模块级函数
# for function_node in module_level_functions:
#     function_code = astor.to_source(function_node)
#     # if function_node.name in comments:
#     #     selected_code.append(f'    """{comments[function_node.name]}"""')
#     selected_code.append(function_code)
#
# # # 添加属性
# # for attribute_node in attributes:
# #     attribute_code = astor.to_source(attribute_node)
# #     selected_code.append(attribute_code)
#
# # 生成新的 Python 代码
# new_code = '\n'.join(selected_code)
#
# # 将新代码保存到新文件
# with open('new_code.py', 'w',encoding='utf-8') as new_file:
#     new_file.write(new_code)

# import py_compile
# py_compile.compile('filePathHelper.py')