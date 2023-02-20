import cv2
import os
import shutil
from PIL import Image
import time
import numpy as np

#得到照片的拍摄时间
import exifread 

from datetime import datetime
currentDataAndTime = datetime.now()

# 注意：1. 目前测试情况是默认照片文件内没有子文件夹
#       2. 如果有需要，程序会创建新的文件夹存放默认文件夹内删除的文件
#       

#######################################################
####################### Main ##########################
#######################################################

# 主函数：负责调用输入的功能
# 输入：输入功能的序号
# 输出：成功/失败
def main():
    # 照片文件路径
    dir_img = "./imgs/"

    functions=['1.read','2.find repeat','3.renumber','4.add logo','5.resize','6.watermark','7.font processing']
    
    # 进入执行指令循环
    flag = True
    while(flag):
        # 打印功能列表
        print(*functions,sep="\n")

        # 获取用户的操作
        op = input("Please input the operation number: ")

        # 执行
        if op == "1":
            read(dir_img)
        elif op == "2":
            find_repeat(dir_img)
        elif op == "3":
            renumber(dir_img)
        elif op == "4":
            add_logo(dir_img)
        elif op == "5":
            resize(dir_img)
        elif op == "6":
            watermark(dir_img)
        elif op == "7":
            font_processing(dir_img)
        # 输入格式不对
        else:
            print("Error! Please input correctly.\n")
        
        # 询问用户是否继续
        continue_processing = input("Do you want to continue? Y/N ")
        if continue_processing == "N":
            print("Process end.")
            flag = False
        else:
            continue

#######################################################
##################### intermediate Functions ##########
#######################################################


# 创建文件并写入内容
def create_file(file_path, file_name, msg):

    # 如果目标文件夹不存在，创建新的文件夹
    if not os.path.isdir(file_path):
        os.mkdir(file_path)

    # encoding解决中文写入txt乱码问题
    f = open(file_path+"\\"+file_name,"a",encoding="utf-8")
    f.write(msg)
    f.write("\n")
    f.close


# 读取图像，解决imread不能读取中文路径的问题
def cv_imread(file_path):
    cv_img=cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
    return cv_img

# 获取拍摄时间
def get_time(file_name):
    img = exifread.process_file(open(file_name,'rb'))
    time = img['Image DateTime']
    return time

# 获取文件夹及其子文件夹中文件路径列表
def getFileList(dir, Filelist, ext=None):
    """
    获取文件夹及其子文件夹中文件列表
    输入 dir: 文件夹根目录
    输入 ext: 扩展名
    返回： 文件路径列表
    """
    newDir = dir
    if os.path.isfile(dir):
        if ext is None:     # 如果没有提供后缀名，直接append
            Filelist.append(dir)
        else:   # 提供后缀名，append不包括后三位
            if ext in dir[-3:]:
                Filelist.append(dir)
    
    elif os.path.isdir(dir):    # 子文件夹存在
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            getFileList(newDir, Filelist, ext)
    return Filelist

def compare_length(dir_image1, dir_image2):
    with open(dir_image1, "rb") as f1:
        size1 = len(f1.read())
    with open(dir_image2, "rb") as f2:
        size2 = len(f2.read())
    if(size1 == size2):
        result = "大小相同"
    else:
        result = "大小不同"
    return result

def compare_size(dir_image1, dir_image2):
    image1 = Image.open(dir_image1)
    image2 = Image.open(dir_image2)
    if(image1.size == image2.size):
        result = "尺寸相同"
    else:
        result = "尺寸不同"
    return result

def compare_content(dir_image1, dir_image2):
    image1 = np.array(Image.open(dir_image1))
    image2 = np.array(Image.open(dir_image2))
    if(np.array_equal(image1, image2)):
        result = "内容相同"
    else:
        result = "内容不同"
    return result

def compare_same(dir_image1, dir_image2):
    # 比较两张图片是否相同
    # 第一步：比较大小是否相同
    # 第二步：比较长和宽是否相同
    # 第三步：比较每个像素是否相同
    # 如果前一步不相同，则两张图片必不相同
    result = "两张图不同"
    大小 = compare_length(dir_image1, dir_image2)
    if(大小 == "大小相同"):
        尺寸 = compare_size(dir_image1, dir_image2)
        if(尺寸 == "尺寸相同"):
            内容 = compare_content(dir_image1, dir_image2)
            if(内容 == "内容相同"):
                result = "2picture_same"
    return result

#######################################################



#######################################################
####################### Main Fuctions #################
#######################################################

'''
功能1: 照片文件分析
函数输入：照片文件路径
函数输出: txt文件,位于result文件夹内
  第一行：照片文件大小
  第二行：图像个数
  第三行（表格）：图像名称；图像格式；图像内存大小；图像形状；拍照日期；
'''
def read(dir_img):
    result_path = "./result"
    result_name = "result.txt"
    print("Reading...")
    create_file(result_path,result_name, str(currentDataAndTime))
    file_name = os.listdir(dir_img)

    # 获取文件夹的大小：
    dir_size = os.path.getsize(dir_img)
    create_file(result_path,result_name,"File size: "+str(dir_size)+" byte")
    # print("File size:", dir_size," byte")

    # 统计文件夹中的文件个数：
    num_png = len(file_name)
    create_file(result_path,result_name, "Number of pictures: "+ str(num_png))
    # print("Number of pictures:", num_png)

    # 遍历文件夹,输出图像的属性
    # print("Properties of images:")
    # s = "{:^45}\t{:^10}\t{:^15}\t{:^20}\t{:^35}"
    s = "{:<45}\t{:<10}\t{:<15}\t{:<20}\t{:<35}"
    # s = "{:>45}\t{:>10}\t{:>15}\t{:>20}\t{:>35}"
    create_file(result_path,result_name, s.format("Name", "Format", "Size", "Shape", "Date"))
    # print(s.format("Name", "Format", "Size", "Shape", "Date"))
    
    img_list = getFileList(dir_img, [])
    for img_path in img_list:
        img_name = os.path.splitext(os.path.basename(img_path))[0]
        img_size = os.path.getsize(img_path)
        img_date = time.ctime(os.path.getmtime(img_path))# 这里获取的是创建时间。
        # img_time = get_time(img_path)
        img_cv = cv_imread(img_path) # 这里如果使用系统自带的cv2.imread, img_path需要是英文，因为可能会包含中文，我们使用自定义函数cv_imread
        img_shape = img_cv.shape
        img_format = os.path.splitext(img_path)[-1][1:]
        create_file(result_path,result_name, s.format(str(img_name),str(img_format),img_size,str(img_shape),img_date))
        # print(s.format(img_name,'JPG',img_size,str(img_shape),img_date))

    print("End reading.\n")


#######################################################
'''
功能2：找出重复的照片文件
原理：先对所有图片按照byte大小排序，然后执行遍历比较。先比较大小，再比较尺寸，最后比较内容。
函数输入：照片文件路径dir_img
函数输出：不同的图片
运行结果：
  该照片路径下重复的照片剩余1张，多余的照片移至save_path指定的文件夹下。
'''

def find_repeat(dir_img):
    print("Removing repeat pictures...")
    save_path = "./imgs_move_repeat" #空文件夹，用于储存检测到的重复的照片
    os.makedirs(save_path,exist_ok=True)

    # 获取图片列表 file_map，字典{文件路径filename : 文件大小image_size}
    file_map = {}
    image_size = 0
    # 遍历filePath下的文件、文件夹（包括子目录）
    for parent, dirnames, filenames in os.walk(dir_img):
        for filename in filenames:
            # print('parent is %s, filename is %s' % (parent, filename))
            # print('the full name of the file is %s' % os.path.join(parent, filename))
            image_size = os.path.getsize(os.path.join(parent, filename))
            file_map.setdefault(os.path.join(parent, filename), image_size)

    # 获取的图片列表按 文件大小image_size 排序
    file_map = sorted(file_map.items(), key=lambda d: d[1], reverse=False)
    file_list = []
    for filename, image_size in file_map:
        file_list.append(filename)

    # 取出重复的图片
    file_repeat = []
    for currIndex, filename in enumerate(file_list):
        dir_image1 = file_list[currIndex]
        dir_image2 = file_list[currIndex + 1]
        result = compare_same(dir_image1, dir_image2)
        if(result == "2picture_same"):
            file_repeat.append(file_list[currIndex + 1])
            print("Same pictures: ", file_list[currIndex], file_list[currIndex + 1])
        else:
            print("Different pictures: ", file_list[currIndex], file_list[currIndex + 1])
        currIndex += 1
        if currIndex >= len(file_list)-1:
            break

    # 将重复的图片移动到新的文件夹，实现对原文件夹降重
    for image in file_repeat:
        shutil.move(image, save_path)
        print("Removing repeat pictures:", image)
    print("Finish remocing repeat pictures")


#######################################################


'''
功能3：照片文件重新编号
输入：照片文件路径
结果：照片文件重新编号，以原照片顺序重命名为1.jpg，2.jpg，3.jpg...
'''
def renumber(dir_img):
    print("Renumbering...")
    choice = input("Please choose the way you want to renumber:\n1. Name with numbers 1, 2, 3,...\n2.Name with shot date like 2022-02-19 means shot on Feb 19,2022")
    if choice == '1':
        path_name = dir_img
        i = 1
        for item in os.listdir(path_name):
            os.rename(os.path.join(path_name,item),os.path.join(path_name,(str(i)+'.jpg')))
            i += 1
    else :
        path_name = dir_img


    print("Finish renumbering.")
 

 #######################################################

'''
功能3：添加专属标志
1. 文字 2.图片
'''

def add_logo(dir_img):
    print("Adding logo...")


def resize(dir_img):
    print("Resizing...")


def watermark(dir_img):
    print("watermarking...")


def font_processing(dir_img):
    print("processing font...")
