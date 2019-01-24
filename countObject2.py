
import numpy as np
import cv2

# Abre a imagem
# converte para tons de cinza
img = cv2.imread("images/objetos.png")
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Aumenta em um pixel as bordas da imagem para facilitar as operações nas bordas e
# por fim aplica um filtro Gaussiano para a redução do ruído
bordersize=1
imgGray=cv2.copyMakeBorder(imgGray, bordersize, bordersize, bordersize, bordersize, borderType= cv2.BORDER_CONSTANT,value=[0,0,0] )
imgGray = cv2.GaussianBlur(imgGray, (5, 5), 0)

# Faz a segmentação da imagem utilizando o método de otsu
imgBin = cv2.threshold(imgGray,0,255, cv2.THRESH_OTSU)[1]

# Aplica o operador morfológico de Abertura (Erosão seguida de Dilatação).
# Com isso remove-se o ruído contido na imagem
imgBin = cv2.morphologyEx(imgBin,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(12,12)))


# informações de altura e largura da imagem
height, width = imgBin.shape

#Cria um array com as mesmas dimensões da imagem e iniciadas com zeros.
# Este array servirá para a contagem de componentes presentes na imagem
mask = np.zeros((height,width),int)

#
# Percorre a imagem pixel a pixel e etiqueta os componentes presentes nela
#
elementCount = 1 # contador de elementos presentes na imagem
for x in range(1,height -2):
    for y in range(1,width -2):
        if imgBin[x, y] == 255:
            if mask[x-1,y-1] != 0:
                mask[x,y] = mask[x-1,y-1]

            elif mask[x-1,y] != 0:
                mask[x, y] = mask[x-1,y]

            elif mask[x-1,y+1] != 0:
                mask[x, y] = mask[x-1,y+1]

            elif mask[x,y-1] != 0:
                mask[x, y] = mask[x,y-1]

            else:
                #  Se toda vizinhaça é zero, logo é uma nova região
                # e a quantidade de elementos é incrementada
                mask[x, y] = elementCount
                elementCount += 1


print("Total de elementos na imagem é ",elementCount)
cv2.waitKey()