from PIL import ImageFont, ImageDraw, Image  
import cv2
import numpy as np  
import os
   
#define as palavras
class verificaArq():

    def __init__(self):
           self.palavras = ["  que ","  nao "," voce ","  para ","  esta ","  uma "," muito "," coisa "," agora ","  isso ","  com ","  por ","  vai "," aqui "," mais "," tudo ","  pode "," tenho "," entao ","  fazer"," quer ", "  mas ","  sim ","  foi "," sabe "," nada "," onde "," estou "," certo "," minha "]
           self.branco = "common_files/branco.png"
           self.xScreen = 1366
           self.yScreen = 768
    

    def listaPalavras(self):
        aux = []
        for txt in self.palavras:
            aux.append(txt.replace(" ", ""))
        return aux
    
    def criaArq(self):
        #cmd = ["  que ","  nao "," voce ","  para ","  esta ","  uma "," muito "," estou "," agora ","  isso "]
        #Cria imagem fundo branco.
        if not os.path.exists(self.branco):
            bckg_b = np.ones((self.yScreen,self.xScreen, 3)) * 255
            cv2.imwrite(self.branco,bckg_b)
        
        for txt in self.palavras:

            if not os.path.exists("common_files/palavras/"+txt.replace(" ", "")+".png"):
             # Carrega image in OpenCV  

                image = cv2.imread(self.branco)
                W,H, chan =  image.shape

                print ("exec")
                 # Converte a imagem p RGB (OpenCV uses BGR)  
                cv2_im_rgb = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)  
                   
                 # Converte a imagem pro PIL
                pil_im = Image.fromarray(cv2_im_rgb)  
                   
                draw = ImageDraw.Draw(pil_im)  

                 # Carrega a fonte
                font = ImageFont.truetype("fonte/league-script-number-one-master/webfonts/LeagueScriptNumberOne-webfont.ttf", 300)
                   
                 # Escreve o texto

                w, h = draw.textsize(txt)
                draw.text((0,(H-h)/4), txt, font=font,fill="black")  
    
                   
                 # Devolve a imagem formato OPENCV
                cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR) 
             
                # Salva imagem	   
                cv2.imwrite("common_files/palavras/"+txt.replace(" ", "")+".png",cv2_im_processed)  
