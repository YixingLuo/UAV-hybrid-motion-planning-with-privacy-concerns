from PIL import Image
import numpy as np

#img = Image.open("pic.png")
L_image = Image.open("map1.png")
img =  L_image.convert("RGB")
# img = np.array(out)

height = 762
width = 1011

# 输出图片的像素值

for i in range(width):
      for j in range(height):
            # print (img.getpixel((0,0)))
            # print(i, j)
            r, g, b = img.getpixel((i, j))
            if (b > g and b > r):  # 对蓝色进行判断
                b = 0
                g = 0
                r = 0
            else:
                b = 255
                g = 255
                r = 255

            img.putpixel((i, j), (r, g, b))

print(type(img))
img.save('mapresult.png')

# for x in range(762):
#     for y in range(1011):
# # for x in range(580):
# #     for y in range(592):
#         i = x
#         j = y
#         print(img.getpixel((i, j)))
#         r, g, b = img.getpixel((i, j))
#         if (b > g and b > r):  # 对蓝色进行判断
#             b = 0
#             g = 0
#             r = 0
#         else:
#             b=255
#             g=255
#             r=255
#
#         img.putpixel((i, j), (r, g, b))
# print(type(img))
# img.save('mapresult.png')



