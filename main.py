import sys
import os
import pygame as pg

import common as c
import gameSelectUI

currentPath = os.getcwd()
currentPath = os.path.join(currentPath, 'HangKo')

def mainStart():

    pg.init()

    running = True
    while running:
        # 기본 틀
        pg.font.SysFont("notosanscjkkr", 10)
        pg.display.set_caption("프로그램 이름(미정)")
        mainDis = pg.display.set_mode(c.winSize)
        mainDis.fill(c.WHITE)

        # 버튼 구성
        btnWidth = 350
        btnHeight = 28

        playBtn = pg.draw.rect(mainDis, c.GRAY, ((c.winWidth - btnWidth) / 2, c.winHeight / 2, 
                                                 btnWidth, btnHeight * 1.5), 1) # 게임시작
        rankBtn = pg.draw.rect(mainDis, c.GRAY, ((c.winWidth - btnWidth) / 2, c.winHeight / 2 + btnHeight * 2, 
                                                 btnWidth, btnHeight * 1.5), 1) # 랭킹
        exitBtn = pg.draw.rect(mainDis, c.GRAY, ((c.winWidth - btnWidth) / 2, c.winHeight / 2 + btnHeight * 4, 
                                                 btnWidth, btnHeight * 1.5), 1) # 종료

        pg.display.update()   # 화면 갱신

        for event in pg.event.get():
            # 프로그램 종료
            if event.type == pg.QUIT:
                running = False
            # 클릭 이벤트
            elif event.type == pg.MOUSEBUTTONDOWN:
                if playBtn.collidepoint(event.pos):
                    if gameSelectUI.gameSelectStart() == 1:
                        running = False
                elif exitBtn.collidepoint(event.pos):
                    running = False

mainStart()
pg.quit()
