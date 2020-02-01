import matplotlib
matplotlib.use('Agg')

#import Tkinter as Tk
try:
    # for Python2
    import Tkinter as tk ## notice capitalized T in tkinter 
except ImportError:
    # for Python3
    import tkinter as tk ## notice lowercase 't' in tkinter here

import sys, pygame, time, os
from pygame.locals import *
from datetime import datetime
import numpy as np
import cv2 as cv
from shutil import copyfile
from verificaArq import verificaArq
from random import shuffle
import threading
import math


xScreen = 1920
yScreen = 1080
kernelBlur = 49
tempoPorLetra = 10.0
#numero de vezes que ira se repetir o treinamento com as mesmas palavras#
numBloco = 9

nTentativas = 9

nSess = 1


resultados = ''
arqcontrole = ''

nome = ''

def mse(imageA, imageB):
    # O erro medio quadratico entre duas imagens eh
    # a soma do quadradado da diferenca entre as duas imagens;
    # NOTE: imagens devem ter as mesmas dimensoes
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err = err/float(imageA.shape[0] * imageA.shape[1])
    
    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

def somaDif(imageA, imageB):
    #The sum
    #of the differences between the two images was used as scoring
    #method
    err = np.sum(np.absolute(imageA.astype("float") - imageB.astype("float")))
    err = err/float(imageA.shape[0] * imageA.shape[1])
    
    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

def iniciar():
    i=5
    while i>0:
        screen.blit(bckg2,(0,0))
        pygame.display.update()
        label = myfont.render(str(i), 1, (255,0,0))	
        screen.blit(label, ((xScreen/2)-(xScreen/15), (yScreen/2)-(yScreen/12)))
        pygame.font.init()
        pygame.display.update()
        time.sleep(3)
        screen.blit(bckg2,(0,0))
        pygame.display.update()
        i=i-1

def transicaoBloco():
    i=10
    while i:
        screen.blit(bckg2,(0,0))
        label = myfont2.render("Aguarde o proximo bloco", 1, (50,255,150))	
        screen.blit(label, ((xScreen/20), (yScreen/12)))
        label = myfont.render(str(i), 1, (255,0,0))	
        screen.blit(label, ((xScreen/2)-(xScreen/15), (yScreen/2)-(yScreen/12)))
        pygame.font.init()
        time.sleep(1)
        pygame.display.update()
        i=i-1

def telaFinaliza():
    screen.blit(bckg2,(0,0))
    label = myfont2.render("Treinamento finalizado", 1, (0,255,0))	
    screen.blit(label, ((xScreen/15), (yScreen/2)-(yScreen/12)))
    pygame.font.init()
    time.sleep(5)
    pygame.display.update()

def telaProxBloco():
    screen.blit(bckg2,(0,0))
    label = myfont2.render("Aguarde o proximo bloco", 1, (0,255,0))	
    screen.blit(label, ((xScreen/15), (yScreen/2)-(yScreen/12)))
    pygame.font.init()
    time.sleep(5)
    pygame.display.update()


def countTry(resultados):
    i=0
    with open(resultados) as a:
        for line in a:
            if(line.find("$$$ tentativa")!=-1):
                i = i + 1
    return i%(nTentativas+1)

def countBloco(resultados):
    i=0
    with open(resultados) as a:
        for line in a:
            if(line.find("@@@ Bloco")!=-1):
                i = i + 1
    return i%(numBloco+1)

def countSess(arqcontrole):
    with open(arqcontrole) as a:
        for line in a:
            b=line.find("!")
            if(b!=-1):
                i = int(line[b+1:])
    return i
def writeSess(arqcontrole):
    i=1
    with open(arqcontrole) as a:
        for line in a:
            b=line.find("!")
            if(b!=-1):
                i = int(line[b+1:])
                if i<=3:
                    i=i+1
                elif i>3:
                    i=1
    kow = open(arqcontrole,'w')				
    kow.write("Sessao !"+str(i))
    kow.close()

def getData():
    now = datetime.now()
    ano = now.year
    mes = now.month
    dia = now.day
    data = str(dia)+'_'+str(mes)+'_'+str(ano)
    return data

def verificar_arquivo(nome):

  
  var = "+str.lower(nome)+'/bloco_'+str(numBloco)"
  caminho = 'resultados/'+str.lower(nome)+'/'+getData()
  

  common = 'common_files'
  palavras = 'common_files/palavras'
  images = 'images'
  images_usr = 'images/'+str.lower(nome)
  blur = 'images/blur'
  blur_usr = 'images/blur/'+str.lower(nome)



  #global resultados 
  #resultados = caminho + '/'+str.lower(nome)+'_resultados.txt'
  global arqcontrole
  arqcontrole = 'resultados/'+str.lower(nome)+'/control.txt'

  resultados2 = caminho + '/'+str.lower(nome)+'_resultados2.txt'
  resultados3 = caminho + '/'+str.lower(nome)+'_resultados3.txt'
 
  if not os.path.exists(caminho):
    os.makedirs(caminho)

  if not os.path.exists(common):
    os.makedirs(common)

  if not os.path.exists(palavras):
    os.makedirs(palavras)

  if not os.path.exists(images):
    os.makedirs(images)

  if not os.path.exists(blur):
    os.makedirs(blur)
  if not os.path.exists(images_usr):
    os.makedirs(images_usr)

  if not os.path.exists(blur_usr):
    os.makedirs(blur_usr)

  if not os.path.exists(arqcontrole):
    au = open(arqcontrole, 'w')
    au.write("Sessao !1 \n")
    au.close()

  
  nSess = countSess(arqcontrole)
  
  global resultados 
  resultados = caminho + '/'+str.lower(nome)+'_resultados_'+str(nSess)+'.txt'

  if not os.path.exists(resultados):
    open(resultados, 'w')

  if not os.path.exists(resultados2):
    open(resultados, 'w')

  if not os.path.exists(resultados3):
    open(resultados, 'w')



  
  nTry = countTry(resultados)
  nbloco = countBloco(resultados)


  #arquivo = open(resultados, 'r')
  aux = 0
  #arquivo.close()
  with open(resultados, 'a') as arq:
      if nbloco==0:
          arq.write("tam_palavra,tempo,erro,bloco,secao\n")
      '''
      elif nTry>0:
          arq.write('\n')
          if (nbloco>0):
              arq.write("\n@@@ Bloco "+str(nbloco)+"\n")

      arq.write('\n$$$ tentativa '+str(nTry)+' $$$')
      arq.write('\n')
      print ('$tentativa '+str(nTry)+'$\n' )
      '''
      arq.close()
    


def button_onclick():
    print("participante" + textBox.get())
    verificar_arquivo(textBox.get())
    global nome
    nome = textBox.get()
    root.destroy()

root = tk.Tk()
root.title('Plataforma de Treino Motor')


textBox = tk.Entry(root)
textBox.place( x=20, y=100)
lb = tk.Label(root,text="Digite seu nome")
lb.place(x=50, y=70)

Button = tk.Button(root,text='Iniciar', command=button_onclick)
Button.place(x=70, y=150)
#Button.pack()

root.geometry("200x200+300+300")
root.mainloop()

pygame.init()

#arquivo = open('/home/mateus/Documentos/tcc3/result.txt', 'w')
txt = []
aux = 0

myfont = pygame.font.SysFont("monospace", 100)
myfont2 = pygame.font.SysFont("monospace", 90)

#definicao do tamanho da tela
screen = pygame.display.set_mode((xScreen,yScreen))
pygame.display.toggle_fullscreen()
screen.fill((255,255,255))

#criacao das imagens

verificaArq().criaArq()
listaPalavras = verificaArq().listaPalavras()
nSess = countSess(arqcontrole)

if nSess==1:
    listaPalavras = listaPalavras[0:10]
    for x in listaPalavras:
        print( x )
elif nSess==2:
    listaPalavras = listaPalavras[10:20]
    for x in listaPalavras:
        print( x )
elif nSess==3:
    listaPalavras = listaPalavras[20:30]
    for x in listaPalavras:
        print( x )



control = True
ini = True
spaceBreak = True
contaBloco = 0
if control:
    while contaBloco<=numBloco:
        shuffle(listaPalavras)
        for palavra in listaPalavras:
            tempoTransicao = tempoPorLetra * len(palavra)
        

            bckg = pygame.image.load('common_files/palavras/'+palavra+'.png')
            bckg2 = pygame.image.load('common_files/branco.png')


            clock = pygame.time.Clock()
            pos = pygame.mouse.get_pos()
            rel = pygame.mouse.get_rel()
            z = 0 #botao esquerdo pressionado
            w = 0 #botao direito pressionado

            pygame.display.update()



            if ini == True:
                iniciar()
                ini = False
            w=1
            qt = True
            kt = True
            #screen.blit(img,(0,0))
            screen.blit(bckg,(0,0))
            pygame.display.update()
            #tempoini = time.clock()
            tempoini = time.time()
            

            while qt:

                screen.blit(bckg,(0,0))
                
                clock.tick(60)
                #duracao = time.clock() - tempoini
                duracao = time.time() - tempoini
                contador = myfont.render(str(int(tempoTransicao-duracao)),0,(255,0,0))
                screen.blit(contador,(200,100))
                pygame.display.update()

               
                x,y = pygame.mouse.get_pos()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        control = False
                        sys.exit()

                    elif event.type == MOUSEBUTTONDOWN:
                        if event.button==1 and w==1:
                            z=1
                    elif event.type == MOUSEBUTTONUP:
                            z=0
                    elif event.type == KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            control = False
                            sys.exit()
                        if event.key == pygame.K_RIGHT:
                            if spaceBreak==True:
                                kt = False



                if (duracao>tempoTransicao or kt==False):
                    print ('salvando '+palavra+' duracao '+str(duracao) )


            
                    qt = False	
                    screen.blit(bckg,(0,0))
                    pygame.display.update()
                    aux = str(duracao)
                    gaussian = cv.getGaussianKernel(ksize=49, sigma=12)

                    pygame.image.save(bckg, 'images/'+nome+'/'+palavra+'_bloco_'+str(numBloco)+'_image '+aux+'.png')
                    pygame.image.save(bckg2, 'images/'+nome+'/'+palavra+'_bloco_'+str(numBloco)+'_bck2_image '+aux+'.png')
                    imgR= cv.imread('images/'+nome+'/'+palavra+'_bloco_'+str(numBloco)+'_bck2_image '+aux+'.png')
                    #imgR = cv.cvtColor(imgR, cv.COLOR_BGR2GRAY)
                    blurredImage = cv.GaussianBlur(imgR,(kernelBlur,kernelBlur),12)
                    #blurredImage = cv.filter2D(imgR,-1,gaussian)
                    cv.imwrite('images/blur/'+nome+'/'+palavra+'_bloco_'+str(numBloco)+'_image '+aux+'_blur.png', blurredImage)
                    imgR2= cv.imread('common_files/palavras/'+palavra+'.png')
                    #	imgR2 = cv.cvtColor(imgR2, cv.COLOR_BGR2GRAY)
                    blurredImage2 = cv.GaussianBlur(imgR2,(kernelBlur,kernelBlur),12)
                    #blurredImage2 = cv.filter2D(imgR2,-1,gaussian)
                    cv.imwrite('common_files/'+palavra+'_blur.png', blurredImage2)


                    #pygame.image.save(bckg, "image "+aux+".png")


                    img1 = cv.imread('common_files/'+palavra+'_blur.png')
                    img2 = cv.imread('images/blur/'+nome+'/'+palavra+'_bloco_'+str(numBloco)+'_image '+aux+'_blur.png')	

                    #img_neg = cv.imread('common_files/img_neg.png')

                    h, w, depth = img2.shape


                    #imgAUX2 = cv.cvtColor(bckg2, cv.COLOR_BGR2GRAY)


                    #img teste : equalizacao + blur
                    a = cv.imread('common_files/'+palavra+'_blur.png',0)
                    a=	cv.equalizeHist(a)
                    a =	np.where(a<250,a,255)
                    a =	np.where(a>250,a,0)


                    b = cv.imread('common_files/branco.png',0)

                    #subtracao - normalizar
                    c = cv.subtract(b,a)



                    e = cv.imread('images/blur/'+nome+'/'+palavra+'_bloco_'+str(numBloco)+'_image '+aux+'_blur.png',0)
                    e = cv.equalizeHist(e)
                    e =	np.where(e<250,e,255)
                    e =	np.where(e>250,e,0)


                    cv.imwrite('images/blur/'+nome+'/'+palavra+'_bloco_'+str(numBloco)+'_image '+aux+'_blur_e.png',e)
                    f = cv.subtract(e,a)

                    img_sub = cv.subtract(e,f)

                    cv.imwrite('images/subtract/'+nome+'/'+palavra+'_bloco_'+str(numBloco)+'_image '+aux+'_subtract.png', img_sub)

                    threshold = np.sum(c.astype("float"))/float(c.shape[0]*c.shape[1])
                    d = np.sum(f.astype("float"))/float(f.shape[0]*f.shape[1])
                    res = (d/threshold)
                    erro = 1 - res
                    with open(resultados, 'a') as arquivo:	
                        arquivo.write(str(len(palavra))+',')
                        arquivo.write(str(duracao)+',')
                        arquivo.write(str(res)+',')
                        arquivo.write(str(contaBloco+1)+',')
                        arquivo.write(str(nSess)+'\n')
                        
                        #arquivo.write('\n######\n')


                if z == 1:
                    pygame.draw.line(screen, (255,0,0), pygame.mouse.get_pos(), [x,y], 1)
                    pygame.draw.line(bckg, (255,0,0), pygame.mouse.get_pos(), [x,y], 1)
                    pygame.draw.line(bckg2, (255,0,0), pygame.mouse.get_pos(), [x,y], 1)
                    pygame.display.update()
        contaBloco = contaBloco + 1
        #with open(resultados, 'a') as arquivo:	
        #	arquivo.write('\n@@@ Bloco '+str(contaBloco)+'\n')
        #telaProxBloco()
        spaceBreak = False
        transicaoBloco()  
        spaceBreak = True
        print ("bloco "+str(numBloco)+" finalizado" )
    writeSess(arqcontrole)
telaFinaliza()
