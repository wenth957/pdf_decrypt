import PySimpleGUI as sg
from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
import sys


def decrypt_pdf(src, to, pwd):
    src_dir = Path(src)
    for pdf in list(src_dir.glob("*.pdf")):
        reader = PdfReader(pdf)
        # 文件如果解密需要先解密再写入
        if not reader.is_encrypted:
            sg.cprint("没有密码...无需解密...")
            break
        try:
            reader.decrypt(pwd)
            sg.cprint("解密完成...")
        except Exception as e:
            sg.cprint("解密失败...请重试...")
        try:
            writer = PdfWriter()
            sg.cprint("写入新文件...")
            for page in range(len(reader.pages)):
                sg.cprint(f"写入第{page+1}页文件")
                writer.add_page(reader.pages[page])
        except Exception as e:
            sg.cprint("写入异常...请重试")
        desc_file = f"{to}/{pdf.stem}_无密.pdf"
        # 生成处理后的文件
        with open(desc_file, 'wb') as out_file:
            writer.write(out_file)
        sg.cprint("写入完成...")
        sg.cprint("输出路径为:")
        sg.cprint(desc_file)


if __name__ == "__main__":
    layout = [
        [
            sg.T("选择加密PDF文件夹", size=(18, 1)),
            sg.In(key="-src-"),
            sg.FolderBrowse(button_text="浏览")
        ],
        [
            sg.T("选择解密后的文件夹", size=(18, 1)),
            sg.In(key="-to-"),
            sg.FolderBrowse(button_text="浏览"),

        ],
        [
            sg.T("输入PDF密码",size=(18, 1)),
            sg.In(key="-pwd-"),
            sg.B("开始解密")
        ],
        [
            sg.ML(size=(80, 15), reroute_cprint=True)]
    ]

    window = sg.Window("PDF解密工具", layout)
    while True:
        event, values = window.read()
        if not event:
            break
        src = values["-src-"]
        pwd = values["-pwd-"]
        to = values["-to-"]
        if event == "开始解密":
            decrypt_pdf(src, to, pwd)
    window.close()

