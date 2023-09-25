#Importing pandas and OpenCV
import pandas as pd
import cv2


#Paths
picture_path = 'pictures/image.jpg'
colors_path = 'dataset/colors.csv'

#Data Importing
columns = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df_colors = pd.read_csv(colors_path, names=columns, header=None)
#Reading and resizing picture
picture = cv2.imread(picture_path)
picture = cv2.resize(picture, (900, 700))

#Variable initialization
clicked = False
#OpenCV is in b, g, r format
b = 0
r = 0
g = 0

#Color threshold
th_light = 600

#x, y coordinates
xpos = 0
ypos = 0

#get_color_name
def get_color_name(R, G, B):
    min = 1000
    for i in range(len(df_colors)):
        d_r = R - int( df_colors.loc[i,'R'])
        d_g = G - int( df_colors.loc[i,'G'])
        d_b = B - int( df_colors.loc[i,'B'])
        d_total = abs(d_r) + abs(d_g) + abs(d_b)
        if d_total <= min:
            min = d_total
            color_name = df_colors.loc[i,'color_name']
    return color_name


def draw(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        #Making the variables global
        global clicked, b, g, r, xpos, ypos
        clicked = True
        xpos = x
        b, g, r = picture[y, x]
        #Convert values to integer
        b = int(b)
        g = int(g)
        r = int(r)

#Program
cv2.namedWindow('picture')
cv2.setMouseCallback('picture', draw)

while True:
    cv2.imshow('picture', picture)
    if clicked:
        # Display with color information
        cv2.rectangle(picture, (20, 20), (600, 60), (b, g, r), -1)
        color_info = get_color_name(r, g, b) + ' R= ' + str(r) + ' G= ' + str(g) + ' B= ' + str(b) 
        cv2.putText(picture, color_info,(50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
        if r + g + b >= th_light:
             cv2.putText(picture, color_info,(50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    if cv2.waitKey(30) & 0xFF == 27:
        break

cv2.destroyAllWindows()


       

