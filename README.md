# Count Objects

Conta o número de objetos encontrados na imagem.
Neste problema há 3 implementações diferentes:
* [1] countObject1.py
* [2] countObject2.py
* [3] countObject3.py

cada um destes resolve o problema utilizando uma abordagem diferente.
O [1] utiliza uma função da biblioteca skimage que conta a contidade
de rótulos presentes na imagem (cada região branca é contada como um
rótulo). Já o método [2] utiliza uma abordagem que percorre toda a imagem
pixel a pixel e verifica seus vizinhos de forma a contabilizar os componentes
conectados e por fim o [3] utiliza a abordagem da técnica de watershed.

A técnica que obteve resultados mais próximos a realidade foi a [2],
já as demais possui um erro relevante na contagem. O watershed era
para ter obtido os melhores resultados, sua metodologia é muito utilizada
principalmente quando se tem componentes muito próximos ou conectados.
Contudo, há uma certa dificuldade em inicializar de maneira ideal ele,
 ou seja, de criar os minimos locais para iniciar o processo de inuldação,
 muitos muitos minimos locais podem gerar hiper segmentação e poucos
 minimos podem gerar baixa segmentação, portanto este é um dos motivos
 da não acertividade deste método para este caso.


### Pré requisitos

Este programa é escrito em Python e você precisará das seguintes bibliotecas
para executar este código:

```
opencv versão 4.0
```

```
scipy
```

```
skimage
```

e 

```
numpy
```


### Instalando bibliotecas necessárias

Abaixo segue um ótimo tutorial ensinando a instalar o opencv versão 4

```
https://www.pyimagesearch.com/2018/08/15/how-to-install-opencv-4-on-ubuntu/
```

para instalar o scipy basta executar:
```
pip install scipy
```

para instalar o skimage basta executar:
```
pip install skimage
```

e para instalar o numpy basta executar:

```
pip install numpy
```

### Informações adicionais

* Sitema operacional utilizado foi o ubuntu 16.04
* As execuções foram feitas utilizando a CPU
* IDE de desenvolvimento utilizada pycharm
