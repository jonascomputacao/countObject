from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import numpy as np
import cv2

# Carrega a imagem, converte de BGR para tons de cinza e
# por fim aplica um filtro Gaussiano para a redução do ruído
image = cv2.imread("images/objetos.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image = cv2.GaussianBlur(image, (11, 11), 0)

# Executa a segmentação da imagem utilizando o método de Otsu
# ao qual possui a capacidade de escolher um valor de limiarização de forma automática
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)[1]

# Executa o operador morfológico de abertura (Erosão seguida de Dilatação),
# com isso os elementos de ruído que não foram removidos, serão agora
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (12, 12)))


# Cria uma mapa de distãncia utilizando distancia Euclidiana,
# o cálculo de distãncia consiste da distância dos pixels do elemento
# até o pixel mais próximo de valor zero, em seguida encontra-se os picos deste mapa
D = ndimage.distance_transform_edt(thresh)
localMax = peak_local_max(D, indices=False, min_distance=10,
                          labels=thresh)

# Realiza uma analise dos componentes conectados dos picos locais (localMax),
# com isso tem-se o inicializador do algoritmo de Watershed
markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
labels = watershed(-D, markers, mask=thresh)
print("Total de Labels {}".format(len(np.unique(labels)) - 1))

#
# Para cada label retornada pelo watershed
for label in np.unique(labels):

    if label == 0:
        continue

    # Cria uma máscara para marcar as labes
    mask = np.zeros(gray.shape, dtype="uint8")
    mask[labels == label] = 255

    # detecta os contornos
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    c = max(cnts, key=cv2.contourArea)

    # desenha um círculo no objeto
    ((x, y), r) = cv2.minEnclosingCircle(c)
    cv2.circle(image, (int(x), int(y)), int(r), (0, 255, 0), 2)
    cv2.putText(image, "{}".format(label), (int(x) - 10, int(y)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

# apresenta a imagem com as marcações dos objetos
cv2.imshow("Output", image)
cv2.imwrite("result/resultado_countObject3.jpg",image)
cv2.waitKey(0)
