import os
import sys

import urllib.request

from .sc import SCError


def Bit_Unit_Conversion(fsize: int):
    """
    字节单位转换

    (大小,单位,原大小)

    :param fsize: 大小
    :return: 大小,单位,原大小
    """
    if fsize < 1024:
        return fsize, 'Byte', fsize
    else:
        KBX = fsize / 1024
        if KBX < 1024:
            return round(KBX, 2), 'KB', fsize
        else:
            MBX = KBX / 1024
            if MBX < 1024:
                return round(MBX, 2), 'MB', fsize
            else:
                return round(MBX / 1024, 2), 'GB', fsize


def getdirsize(dirpath: str):
    """
    :param dirpath:目录或者文件
    :return: size: 目录或者文件的大小
    """
    size = 0
    print(os.path.isdir(dirpath), os.path.isfile(dirpath))
    if os.path.isdir(dirpath): # 如果是目录
        for root, dirs, files in os.walk(dirpath):
            size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        return size
    elif os.path.isfile(dirpath):  # 如果是文件
        size = os.path.getsize(dirpath)
        return size
    else:
        raise SCError("目录/文件 不存在")



def getFileSize(filepath: str):
    """
    获取目录或文件的总大小

    :param filePath: 目录或者文件
    :return: 例子：(2, 'M', 2048)
    """
    fsize = getdirsize(filepath)  # 返回的是字节大小
    return Bit_Unit_Conversion(fsize)


def getUrlFileSize(url: str):
    """
    获取url上的文件的总大小

    :param url: 网络url
    :return: 例子：(2, 'M', 2048)
    """
    response = urllib.request.urlopen(url)
    file_size = int(response.headers["Content-Length"])
    return Bit_Unit_Conversion(file_size)


def AddPwd(InputPath: str, OutputPath: str, PassWord: str, BoolEnforce=False, OldPassWord: str = ''):
    """
    pdf加密/修改密码
    :param InputPath: 待加密的pdf文件路径
    :param OutputPath: 输出的pdf文件路径
    :param PassWord: 添加的密码
    :param BoolEnforce: 是否强制加密【修改密码】
    :param OldPassWord: 若强制加密则需要原密码
    :return:
    """
    pdf_reader = PdfReader(open(InputPath, 'rb'))  # 打开pdf文件

    if pdf_reader.is_encrypted and not BoolEnforce:  # 已加密且不修改密码
        # print("该PDF文件为已加密的PDF文件")
        return None
    if pdf_reader.is_encrypted and BoolEnforce:  # 已加密且修改密码
        # print("修改密码中......")
        pdf_reader = PdfReader(open(InputPath, "rb+"), password=OldPassWord)  # 打开有密码的pdf文件
    pdf_writer = PdfWriter()  # 创建写入对象
    for page in pdf_reader.pages:
        pdf_writer.add_page(page)
    pdf_writer.encrypt(PassWord)  # 添加密码
    pdf_writer.write(open(OutputPath, 'wb'))  # 写入新文件
    return True


def TryGetPDFPwd(filename: str, tl: list[str]):
    """
    从字典中尝试解密
    :param filename: str: pdf文件路径
    :param tl: list[str]: 字典
    :return: 是否有密码-True/Flase, 是否解密成功-None/密码
    """
    pdfFile = PdfReader(open(filename, "rb+"))  # 打开pdf文件

    if pdfFile.is_encrypted:  # 如果有密码
        with tqdm(tl, total=len(tl), unit="word") as bar:  # 进度条
            for word in bar:
                try:
                    bar.set_postfix(CurrentPwd=word)
                    PdfReader(open(filename, "rb+"), password=word)
                    return True, word
                except Exception as err:
                    # print(word, err)
                    continue
        return True, None
    else:  # 如果没密码
        return False, None

