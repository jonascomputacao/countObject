from imutils import contours
from skimage import measure
import numpy as np
import imutils
import cv2

# Carrega a imagem, converte de BGR para tons de cinza
# por fim aplica um filtro Gaussiano para a redução do ruído
image = cv2.imread("images/objetos.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (11, 11), 0)

# Executa a segmentação da imagem utilizando o método de Otsu
# ao qual possui a capacidade de escolher um valor de limiarização de forma automática
thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_OTSU)[1]

# Executa o operador morfológico de abertura (Erosão seguida de Dilatação),
# com isso os elementos de ruído que não foram removidos, serão agora
thresh = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(12,12)))

# Encontra os objetos conectados da imagem.
# Em seguida cria uma máscara para armazenar os componentes considerados grande
labels = measure.label(thresh, neighbors=8, background=0)
mask = np.zeros(thresh.shape, dtype="uint8")

print("Total de componentes = ",len(np.unique(labels)) - 1)

# Verificação de cada componente
for label in np.unique(labels):
    # o fundo da imagem é ignorado
    if label == 0:
        continue

    # Cria uma máscara de label para a contagem
    # do número de pixels presente neste componente específico
    labelMask = np.zeros(thresh.shape, dtype="uint8")
    labelMask[labels == label] = 255
    numPixels = cv2.countNonZero(labelMask)

    # se a quantidade de pixels for suficiente para considerar este objeto,
    # ele é adicionado a máscara real, que possuirá as informações de todas as labels
    #if numPixels > :

    mask = cv2.add(mask, labelMask)

    # Encontra os contornos de mask e os ordena
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = contours.sort_contours(cnts)[0]

    # para cada contorno do objeto, será desenhado um circulo
    for (i, c) in enumerate(cnts):
        # draw the bright spot on the image
        (x, y, w, h) = cv2.boundingRect(c)
        ((cX, cY), radius) = cv2.minEnclosingCircle(c)
        cv2.circle(image, (int(cX), int(cY)), int(10 ),
                   (0, 0, 255), 3)
        cv2.putText(image, ".{}".format(label), (x-10, y - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)


        # show the output image
        cv2.imshow("Image", image)
        cv2.waitKey(0)
