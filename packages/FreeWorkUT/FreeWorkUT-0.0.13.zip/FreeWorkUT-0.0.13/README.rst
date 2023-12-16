**★ 关于FreeWork的相关介绍 (Introduction for FreeWork) ★**

*本文档为中英双语文档，其中括号内的为中文部分的英语译文，其二者内容相同。(This document is a bilingual document in Chinese and English, with the English translation of the Chinese part enclosed in parentheses, both of which have the same content.)*

**一、安装 (Installation)**

.. code:: python

    pip install FreeWork

**二、使用 (Usage)**

**1. 导包 (Import)**

.. code:: python

    from FreeWork import OfficeWork as ow

**2. 内置函数 (Integrated functions)**

**(1) 文件复制函数 (File Copy Function)**

本函数用于复制文件，在复制的同时可以根据需求修改函数名字。通常与for循环结合进行批量复制并改名的操作。(This function is used to copy files, and the function name can be modified as needed while copying. Usually combined with the for loop for batch copying and renaming operations.)

.. code:: python

    from FreeWork import OfficeWork as ow

    ow.CopyFile(FileOriginalPath, FileNewPath)
    # ow.CopyFile(文件原始路径, 文件新路径)

*注意，这里文件路径为包含文件名的路径，可以是相对路径，也可以是绝对路径。如：(1)D:\Example\EasyWork\example.png;(2)\Example\example.png。*

*(Note that the file path here is a path that includes the file name, which can be a relative path or an absolute path. For example:(1)D:\Example\EasyWork\example.png;(2)\Example\example.png)*
