**工具**：pdg2pdf --> 主要用于转换ssllibrary超星图书pdg文件

**作用**：将多个pdg文件合成为一个pdf文件,并进行压缩（原作的工具转换后文件太大，所以略作修改）

**食用方式**:

```shell
python3 pdg2pdf.py your_book_filepath.zip # 转换单个pdf文件
```

**需要的工具**:
- pip3 install PIL argparse PyPDF2 -i https://pypi.douban.com/simple

**注意事项**：

1. 主要策略是使用pillow将pdg文件转换为pdf，有部分文件可能无法转换为pdf。

2. **如果文件过大，获得正确密码的线程在解压时，脚本仍然会尝试其他密码，此时只需要等待片刻即可。**
