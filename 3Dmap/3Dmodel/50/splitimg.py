from PIL import Image
import matplotlib.pyplot as plt
import sys

def fill_image(image):
    width,height=image.size
    #print(width,height)
    # 选取长和宽中较大值作为新图片的
    new_image_length=width if width>height else height

    #print(new_image_length)
    # 生成新图片[白底]
    new_image=Image.new(image.mode,(new_image_length,new_image_length),color='white')
    # 将之前的图粘贴在新图上，居中
    if width>height:# 原图宽大于高，则填充图片的竖直维度  #(x,y)二元组表示粘贴上图相对下图的起始位置,是个坐标点。
        new_image.paste(image,(0, int((new_image_length - height) / 2)))
    else:
        new_image.paste(image, (int((new_image_length - width) / 2), 0))

    return new_image




def cut_image(image):
    width,height=image.size
    print(width,height)
    item_width=float(width/50)
    box_list=[]
    count=0
    for j in range(0,50):
        for i in range(0, 50):
            count+=1
            box=(i*item_width,j*item_width,(i+1)*item_width,(j+1)*item_width)
            box_list.append(box)
    print(count)
    image_list=[image.crop(box) for box in box_list]
    return image_list

def save_images(image_list):
    index=1
    for image in image_list:
        image.save('result/'+str(index)+'.png')
        index+=1
def display_blocks():
    plt.figure()
    for i in range(1, 2501):
        plt.subplot(50, 50, i)
        im=plt.imread('result/'+str(i)+'.png')
        plt.imshow(im)
        plt.xticks([])
        plt.yticks([])

    plt.show()


if __name__== '__main__':
    image=Image.open("mapresult.png")
    #image = Image.open("test2.jpg")
    fill_image(image)
    image=fill_image(image)
    #测试
    print(image.size)
    image.show()
    image_list=cut_image(image)
    save_images(image_list)
    #image_list[2432].show()

    display_blocks()