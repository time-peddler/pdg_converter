# pdg2pdf 步骤整合

import os
from PIL import Image
from PyPDF2 import PdfFileMerger, PdfFileWriter
import tkinter as tk
from tkinter import filedialog
from extract_zip import CompressionHandler


def walk_os_file(path):
    # 遍历文件目录下所有文件
    result = []
    for root, dirs, files in os.walk(path):
        for file in files:
            perpath = os.path.join(root, file)
            result.append(perpath.replace("\\", "/"))
    return result


def pdg2pdf(pdg_path):
    # 单页pdg转化为pdf
    new_path = pdg_path.replace(os.path.splitext(pdg_path)[1], '.pdf')
    try:
        img = Image.open(pdg_path)
        # 使用RGB模式，减少原有格式占用的空间
        img = img.convert('RGB')
        img.save(new_path, "PDF", quality=75, subsampling=0, resolution=100.0, save_all=True)
    except Exception as e:
        print(f"An error occurred: {e}")


def mergePDF(extracted_path, book_name='temp.pdf'):
    print('开始合并文件...')
    paths = [i for i in os.listdir(extracted_path) if i.endswith('pdf')]
    # 对图书页码进行排序
    pdfs = sorted(sorted(paths),
                  key=lambda x: (x[0].isdigit(), x[0] == '!', x[0] == 'f', x[0] == 'l', x[0] == 'b', x[0] == 'c'))
    merger = PdfFileMerger()
    for pdf in pdfs:
        try:
            file = os.path.join(extracted_path, pdf)
            merger.append(open(file, 'rb'))
        except Exception as e:
            print(f"An error occurred for {pdf}: {e}")
    merger.write(os.path.join(extracted_path, book_name))
    merger.close()
    print('合并完成！')


def convert(ziped_file):
    print('解压结束，开始转化格式....')
    # 解压缩的文件所在路径
    extracted_path = os.path.splitext(ziped_file)[0]
    # 保存路径，只是将压缩文件路径改为pdf
    save_path = ziped_file.replace(os.path.splitext(ziped_file)[1], '.pdf')
    # 判断是否有下级文件夹
    if len(os.listdir(extracted_path)) <= 3:
        extracted_path = os.path.join(extracted_path, os.listdir(extracted_path)[0])
    # 读取解压目录下所有文件
    pdg_paths = walk_os_file(extracted_path)
    # 将每个pdg文件转化为pdf，并删除原来的文件。
    for pdg_path in pdg_paths:
        pdg2pdf(pdg_path)
    # 合并所有页面至一个pdf文档
    mergePDF(extracted_path, save_path)
    # 删除加压的文件夹
    # shutil.rmtree(extracted_path)


if __name__ == '__main__':
    # 文件选择器选择文件
    root = tk.Tk()
    root.withdraw()

    # Folderpath = filedialog.askdirectory() #获得选择好的文件夹
    ziped_file = filedialog.askopenfilename()  # 获取图书压缩包
    # 解压解密文档
    CompressionHandler(ziped_file).extract()
    # 转化为pdf
    convert(ziped_file)
