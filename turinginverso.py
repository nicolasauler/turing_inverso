import pygame as pg
import math
import protMqtt as mqtt
import sys
import time
from pygame import display, event, font 
from pygame.image import load
from playsound import playsound

#Botão circular
class Button:
    def __init__(self, xpos, ypos, sizex,sizey, color_light, color_dark,text,circle):
        self.xpos = xpos
        self.ypos = ypos
        self.sizex = sizex
        self.sizey = sizey
        self.color_light = color_light
        self.color_dark = color_dark
        self.text = text
        self.circle = circle

    def putText(self,tela):
        if self.circle:
            tela.blit(self.text,(self.xpos-12,self.ypos-15))
        else:
            tela.blit(self.text,(self.xpos+8,self.ypos+15))
    #Para botões circulares sizex=sizey=raio
    def isOver(self,mouse):
        if self.circle:
            if math.sqrt((self.xpos-mouse[0])**2+(self.ypos-mouse[1])**2)<self.sizex:
                return True
            else:
                return False
        else:
            if (self.xpos<mouse[0]<self.xpos+self.sizex and self.ypos<mouse[1]<self.ypos+self.sizey):
                return True
            else:
                return False
    def drawLight(self,tela):
        if self.circle:
            pg.draw.circle(tela,self.color_light,(self.xpos,self.ypos),self.sizex)
        else:
            pg.draw.rect(tela,self.color_light,[self.xpos,self.ypos,self.sizex,self.sizey])
    def drawDark(self,tela):
        if self.circle:
            pg.draw.circle(tela,self.color_dark,(self.xpos,self.ypos),self.sizex)
        else:
            pg.draw.rect(tela,self.color_dark,[self.xpos,self.ypos,self.sizex,self.sizey])



pg.init()

#Cria tela
width = 640
height =480
tela = display.set_mode(size=(width, height))
display.set_caption("Turing Inverso")

#Imagem de fundo
fundoInicio = load('imagens/1.png').convert()
fundoInst = load('imagens/2.png').convert()
fundoJogo = load('imagens/fundo.png').convert()
fundoFinal = load('imagens/fim.png').convert()

telaInicial=True
telaInst=False
telaJogo=False
telaWin=False
telaLos=False

font = pg.font.SysFont('Changa-VariableFont_wght',50)
JFont = pg.font.SysFont('Changa-VariableFont_wght',30)
RFont = pg.font.SysFont('Changa-VariableFont_wght',22)

#Botões
textJog = JFont.render('Iniciar',True,(0,0,0))
ButtonJ = Button(width/2-40,6*height/7,80,50,(210,90,90),(210,57,57),textJog,False)

textRein = RFont.render('Reiniciar',True,(0,0,0))
ButtonR = Button(width/2-40,4*height/5+10,80,50,(210,90,90),(210,57,57),textRein,False)

textA = font.render('A',True,(0,0,0))
ButtonA = Button(width/5,6*height/7,30,30,(210,90,90),(210,57,57),textA,True)

textB = font.render('B',True,(0,0,0))
ButtonB = Button(2*width/5,6*height/7,30,30,(210,90,90),(210,57,57),textB,True)

textC = font.render('C',True,(0,0,0))
ButtonC = Button(3*width/5,6*height/7,30,30,(210,90,90),(210,57,57),textC,True)

textD = font.render('D',True,(0,0,0))
ButtonD = Button(4*width/5,6*height/7,30,30,(210,90,90),(210,57,57),textD,True)



mqtt.client.connect(mqtt.Broker,mqtt.Port,mqtt.KeepAlive)

end = False
mqtt.client.loop_start()
while(not end):
    pg.init()

    mouse = pg.mouse.get_pos()

    if telaInicial:
        tela.blit(fundoInicio,(0,0))
        if ButtonJ.isOver(mouse):
            ButtonJ.drawLight(tela)
        else:
            ButtonJ.drawDark(tela)

        ButtonJ.putText(tela)

        pg.display.update()

        for event in pg.event.get():
                if(event.type == pg.QUIT):
                    pg.quit() 
                if (event.type == pg.MOUSEBUTTONDOWN):  
                    if ButtonJ.isOver(mouse):
                        telaInst=True
                        telaInicial=False
    
    elif telaInst:
        tela.blit(fundoInst,(0,0))

        if ButtonJ.isOver(mouse):
            ButtonJ.drawLight(tela)
        else:
            ButtonJ.drawDark(tela)

        ButtonJ.putText(tela)

        pg.display.update()

        for event in pg.event.get():
                if(event.type == pg.QUIT):
                    pg.quit() 
                if (event.type == pg.MOUSEBUTTONDOWN):  
                    if ButtonJ.isOver(mouse):
                        mqtt.client.publish(mqtt.user+"/E2", payload="1", qos=0, retain=False)
                        time.sleep(0.6)
                        mqtt.client.publish(mqtt.user+"/E2", payload="0", qos=0, retain=False)
                        telaJogo=True
                        telaInst=False

    elif telaJogo:

        tela.blit(fundoJogo,(0,0))

        if ButtonA.isOver(mouse):
            ButtonA.drawLight(tela)
        else:
            ButtonA.drawDark(tela)

        if ButtonB.isOver(mouse):
            ButtonB.drawLight(tela)
        else:
            ButtonB.drawDark(tela)

        if ButtonC.isOver(mouse):
            ButtonC.drawLight(tela)
        else:
            ButtonC.drawDark(tela)

        if ButtonD.isOver(mouse):
            ButtonD.drawLight(tela)
        else:
            ButtonD.drawDark(tela)

        ButtonA.putText(tela)
        ButtonB.putText(tela)
        ButtonC.putText(tela)
        ButtonD.putText(tela)
        
        pg.display.update()

        if mqtt.audio==1:
            playsound('beep-01a.mp3')
            time.sleep(0.1)
            mqtt.client.publish(mqtt.user+"/S6", payload="1", qos=0, retain=False)
            time.sleep(0.6)
            mqtt.client.publish(mqtt.user+"/S6", payload="0", qos=0, retain=False)


        for event in pg.event.get():
            if(event.type == pg.QUIT):
                pg.quit() 
            if (event.type == pg.MOUSEBUTTONDOWN):  
                if ButtonA.isOver(mouse):
                    mqtt.client.publish(mqtt.user+"/E3", payload="1", qos=0, retain=False)
                    time.sleep(0.6)
                    mqtt.client.publish(mqtt.user+"/E3", payload="0", qos=0, retain=False)
                elif ButtonB.isOver(mouse):
                    mqtt.client.publish(mqtt.user+"/E4", payload="1", qos=0, retain=False)
                    time.sleep(0.6)
                    mqtt.client.publish(mqtt.user+"/E4", payload="0", qos=0, retain=False)
                elif ButtonC.isOver(mouse):
                    mqtt.client.publish(mqtt.user+"/E5", payload="1", qos=0, retain=False)
                    time.sleep(0.6)
                    mqtt.client.publish(mqtt.user+"/E5", payload="0", qos=0, retain=False)
                elif ButtonD.isOver(mouse):
                    mqtt.client.publish(mqtt.user+"/E6", payload="1", qos=0, retain=False)
                    time.sleep(0.6)
                    mqtt.client.publish(mqtt.user+"/E6", payload="0", qos=0, retain=False)

        if mqtt.ganhou == 1:
            telaWin = True
            telaJogo= False
            mqtt.ganhou = 0

        if mqtt.perdeu == 1:
            telaLos = True
            telaJogo = False
            mqtt.perdeu = 0

    elif telaWin:
        tela.blit(fundoFinal,(0,0))

        vitorias=load('imagens/graphVitorias.png').convert()
        rod=load('imagens/graphRodadas.png').convert()

        tela.blit(vitorias,(80,180))
        tela.blit(rod,(350,180))
        
        if ButtonR.isOver(mouse):
            ButtonR.drawLight(tela)
        else:
            ButtonR.drawDark(tela)

        ButtonR.putText(tela)

        pg.display.update()

        for event in pg.event.get():
                if(event.type == pg.QUIT):
                    pg.quit() 
                if (event.type == pg.MOUSEBUTTONDOWN):  
                    if ButtonR.isOver(mouse):
                        telaJogo=True
                        telaWin=False

    elif telaLos:
        tela.blit(fundoFinal,(0,0))

        vitorias=load('imagens/graphVitorias.png').convert()
        rod=load('imagens/graphRodadas.png').convert()

        tela.blit(vitorias,(80,180))
        tela.blit(rod,(350,180))

        if ButtonR.isOver(mouse):
            ButtonR.drawLight(tela)
        else:
            ButtonR.drawDark(tela)

        ButtonR.putText(tela)

        pg.display.update()

        for event in pg.event.get():
                if(event.type == pg.QUIT):
                    pg.quit() 
                if (event.type == pg.MOUSEBUTTONDOWN):  
                    if ButtonR.isOver(mouse):
                        telaJogo=True
                        telaLos=False
            
mqtt.client.loop_stop()

pg.quit()