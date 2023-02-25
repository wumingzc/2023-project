import cv2
import os
import shutil
from PIL import Image
import time
import numpy as np

import re # 正则表达式

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
    
    

    functions=['1.read','2.find repeat','3.renumber','4.add logo','5.watermark','6.resize','7.font processing']
    
    # 进入执行指令循环
    flag = True
    while(flag):
        # dir_img = "./imgs/"
        dir_img = input('Please input the file directory: ') # 让用户输入要操作的文件目录
        
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
            watermark(dir_img)
        elif op == "6":
            resize(dir_img)
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
def write_file(file_path, file_name, msg):

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
    try:
        img = exifread.process_file(open(file_name,'rb'))
        time = img['EXIF DateTimeDigitized']
    except:
        time = None
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
    write_file(result_path,result_name, str(currentDataAndTime))
    file_name = os.listdir(dir_img)

    # 获取文件夹的大小：
    dir_size = os.path.getsize(dir_img)
    write_file(result_path,result_name,"File size: "+str(dir_size)+" byte")
    # print("File size:", dir_size," byte")

    # 统计文件夹中的文件个数：
    num_png = len(file_name)
    write_file(result_path,result_name, "Number of pictures: "+ str(num_png))
    # print("Number of pictures:", num_png)

    # 遍历文件夹,输出图像的属性
    # print("Properties of images:")
    # s = "{:^45}\t{:^10}\t{:^15}\t{:^20}\t{:^35}"
    s = "{:<45}\t{:<10}\t{:<15}\t{:<20}\t{:<35}"
    # s = "{:>45}\t{:>10}\t{:>15}\t{:>20}\t{:>35}"
    write_file(result_path,result_name, s.format("Name", "Format", "Size", "Shape", "Date"))
    # print(s.format("Name", "Format", "Size", "Shape", "Date"))
    
    img_list = getFileList(dir_img, [])
    for img_path in img_list:
        img_name = os.path.splitext(os.path.basename(img_path))[0]
        img_size = os.path.getsize(img_path)
        # img_date = time.ctime(os.path.getmtime(img_path))# 这里获取的是创建时间。
        img_time = get_time(img_path) # 获得拍摄时间
        img_cv = cv_imread(img_path) # 这里如果使用系统自带的cv2.imread, img_path需要是英文，因为可能会包含中文，我们使用自定义函数cv_imread
        img_shape = img_cv.shape
        img_format = os.path.splitext(img_path)[-1][1:]
        write_file(result_path,result_name, s.format(str(img_name),str(img_format),img_size,str(img_shape), str(img_time)))
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
        print("Removing repeat pictures:%s from %s to %s." %(image,dir_img,save_path))
    print("Finish remocing repeat pictures")


#######################################################


'''
功能3：照片文件重新编号
输入：照片文件路径
结果：照片文件重新编号，以原照片顺序重命名为1.jpg，2.jpg，3.jpg...或者让用户添加前缀，重命名为“前缀+数字.jpg”
'''
def renumber(dir_img):
    print("Renumbering...")
    path_name = dir_img #文件路径
    
    
    path_list = os.listdir(path_name)
    new_path_list = sorted(path_list,key = lambda i:int(re.findall(r'\d+',i)[0])) #对path_list进行排序,这里使用了正则表达式
    # print(new_path_list)

    choice = input("1. Name with numbers 1, 2, 3,...\n2.Input your prefix text.\nPlease choose the way you want to renumber: 1 OR 2?\n")
    if choice == '2':
        perfix = input("Please input your perfix: ")

    i = 1 # 表示文件的命名是从1开始的
    for item in new_path_list: # 遍历文件夹下的所有子文件，这里默认没有子文件夹
        if item.endswith('.jpg') or item.endswith('.png'): # 输入图片的格式为jpg或者png，我们在重命名时可以统一转为jpg格式
            src = os.path.join(path_name,item) #源文件路径及文件名
            format =img_format = os.path.splitext(src)[-1][1:] # 源文件的格式
            if choice == '1': #只有数字
                new_name = str(i)+'.'+format
            else: # 用户自定义前缀
                new_name = perfix + '-' +str(i) + '.'+format
            dst = os.path.join(path_name,new_name)
            # 如果已经有文件名为i.jpg,那么就跳过继续

            # rename()找不到目标文件或目录，会抛出FileNotFoundError异常
            try:
                print('Rename from %s to %s.'%(src,dst))
                os.rename(src,dst)
                i += 1
            except:
                print('Name %s exist.'%(dst))
                continue
    print("Total renamed %s files"%(i-1))
    


    print("Finish renumbering.")
 

 #######################################################

'''
功能4：批量为图片添加专属标志
输入：logo图片的路径，及位置（左上、坐下、右上、右下）
结果：目标路径下所有图片在对应位置加水印图片

现在的问题是：1.添加logo的位置不准确 2.添加logo时照片会翻转方向 3.当logo比原照片大时，没有抛出异常提醒
'''

def add_logo(dir_img):
    print("Adding logo...")
    all_path = [] #用来存储需要加logo的图片路径
    

    #创建目录保存处理后的图片
    try:
        os.mkdir('file_logo')
    except FileExistsError:
        print('dir "file_logo" Exists ')

    
    # root指当前正在遍历的文件夹的地址
    # dirs是一个list指该文件夹中所有的目录的名字（不包含子目录）
    # files是list, 内容是该文件夹中所有的文件

    #获取当前目录下所有的jpg格式文件路径
    for root, dirs, files in os.walk(dir_img):
        for file in files:
            if "jpg" in file:
                all_path.append(os.path.join(root, file))


    #打开logo图片文件
    LOGO_FILE = input('Please input the file name of logo: ')

    # 选择位置
    decide_position = input('Where do you want to put your logo?\n top-left, top-right, down-left, down-right: ')
    

    dir_logo = './logo'
    # dir_logo = input('Please input the directory of logo file: ')
    logoIm = Image.open(os.path.join(dir_logo,LOGO_FILE)).convert("RGBA") #打开logo
    logoWith, logoHeight = logoIm.size

    #r,g,b,a =logoIm.split()


    file_dir = './file_logo' # 将贴上logo的图片保存在file_logo里
    for i in range(1,len(all_path)+1): # 给贴上logo的图片重命名，从1开始
        imTmp = Image.open(all_path[i-1]).convert("RGB") #打开背景图
        imWidth,imHeight = imTmp.size
        if(decide_position == 'down-right'): #给图片的右下角添加logo
            position = (imWidth-logoWith,imHeight-logoHeight)
        elif(decide_position == 'down-left'): # 左下角
            position = (logoWith, imHeight -logoHeight)
        elif(decide_position == 'top-left'): # 左上角
            position = (logoWith, logoHeight)
        else: # 右上角
            position = (imWidth-logoWith, logoHeight)
    
        imTmp.paste(logoIm, position, logoIm)

        filename =str(i) + '.png'
        imTmp.save(os.path.join(file_dir,filename))
        print('Saved file %s.'%(filename))

'''
功能5：批量为图片添加水印
输入：
结果：
'''
def watermark(dir_img):
    print("watermarking...")

def resize(dir_img):
    print("Resizing...")


def font_processing(dir_img):
    print("processing font...")

main()