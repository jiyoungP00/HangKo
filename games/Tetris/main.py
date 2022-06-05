import sys
import os
import pygame as pg
import random

# Color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)      # 사각
GREEN = (0, 255, 0)     # z자
PINK = (255,192,203)    # ㄱ자
ORANGE = (255,165,0)    # 1자

WINSIZE = (720, 720)

def gameStart():

    pg.init()

    state = 0

    colors = [GRAY, BLACK, BLUE, GREEN, PINK, ORANGE]

    BGPath = os.path.dirname(__file__)
    BGPath = os.path.join(BGPath, 'background.jpg')

    global block
    global newBlock
    global creatable
    global score

    # 기본 틀
    pg.display.set_caption("Tetris")
    ttDis = pg.display.set_mode(WINSIZE)
    ttDis.fill(WHITE)

    clock = pg.time.Clock()
    clock.tick(60)

    backGround = pg.image.load(BGPath)
    backGround = pg.transform.scale(backGround, WINSIZE)
    ttDis.blit(backGround, (0, 0))

    blockSize = 30
    block_X = 12
    block_Y = 22
    
    gameBoardMargin = 25
    gameBoardWidth = blockSize * block_X + 10
    gameBoardHeight = blockSize * block_Y + 10
    gameBoard = pg.draw.rect(ttDis, WHITE, (gameBoardMargin, gameBoardMargin, gameBoardWidth, gameBoardHeight))

    firstBlock_X = gameBoardMargin + 5
    firstBlock_Y = gameBoardMargin + 5

    infMargin = 35
    infWidth = 200
    infHeight = 400
    infBack = pg.draw.rect(ttDis, BLACK, (gameBoardWidth + gameBoardMargin * 2 + infMargin, infMargin * 2, infWidth, infHeight))
    Inf = pg.draw.rect(ttDis, WHITE, (gameBoardWidth + gameBoardMargin * 2 + infMargin, infMargin * 2, infWidth, infHeight), 10)

    text_X = infMargin + gameBoardMargin * 2 + gameBoardWidth + infWidth / 2
    text_Y = infMargin * 2

    def makeInf():
        infFont = pg.font.SysFont("malgungothic", 28)
        blockInfText = infFont.render("다음 블록", True, WHITE)
        blockInfRect = blockInfText.get_rect()
        blockInfRect.center = (text_X, text_Y + 50)
        ttDis.blit(blockInfText, blockInfRect)

        scoreFont = pg.font.SysFont("malgungothic", 24)
        scoreText = scoreFont.render(str(score), True, WHITE)
        scoreRect = scoreText.get_rect()
        scoreRect.center = (text_X, text_Y + 300)
        ttDis.blit(scoreText, scoreRect)

        scoreInfText = infFont.render("점수", True, WHITE)
        scoreInfRect = scoreInfText.get_rect()
        scoreInfRect.center = (text_X, text_Y + 230)
        ttDis.blit(scoreInfText, scoreInfRect)

        pg.display.update()

    isEnd = True
    running = True
    creatable = True
    while running:
        for i in range(block_Y):
            for j in range(block_X):
                pg.draw.rect(ttDis, GRAY, (firstBlock_X + j * blockSize, firstBlock_Y + i * blockSize, blockSize, blockSize))
                pg.draw.rect(ttDis, BLACK, (firstBlock_X + j * blockSize, firstBlock_Y + i * blockSize, blockSize, blockSize), 1)

        btnWidth = 180
        btnHeight = 70

        myFont = pg.font.SysFont("malgungothic", 28)

        playBtn = pg.draw.rect(ttDis, GRAY, (text_X - btnWidth / 2, text_Y + infHeight + infMargin, btnWidth, btnHeight)) # 게임시작
        playBtnText = myFont.render("시작", True, BLACK)
        playTextRect = playBtnText.get_rect()
        playTextRect.center = (text_X, text_Y + infHeight + infMargin + btnHeight / 2)
        ttDis.blit(playBtnText, playTextRect)

        exitBtn = pg.draw.rect(ttDis, GRAY, (text_X - btnWidth / 2, text_Y + infHeight + infMargin + 90, btnWidth, btnHeight)) # 종료
        exitBtnText = myFont.render("종료", True, BLACK)
        exitTextRect = exitBtnText.get_rect()
        exitTextRect.center = (text_X, text_Y + infHeight + infMargin + btnHeight / 2 + 90)
        ttDis.blit(exitBtnText, exitTextRect)

        score = 0
        makeInf()

        while not isEnd:
            if creatable == True:
                clearCount = 0 
                for line in range(1, block_Y - 1):      # 점수 획득
                    fullChk = True
                    for i in range(1, block_X - 1):
                        if block[i][line] == 1:
                            fullChk = False
                            break
                    if fullChk == True:
                        for i in range(1, block_X - 1):
                            for j in range(line, 1, -1):
                                block[i][j] = block[i][j - 1]
                            block[i][1] = 1
                        clearCount += 1

                score += int(clearCount * (clearCount + 1) / 2) * 100
                makeInf()

                for i in range(1, block_X - 1): # 게임 오버
                    if block[i][1] != 1:
                        isEnd = True
                        break
                if isEnd == True:
                    break

                global newBlockColor
                newBlockColor = random.randrange(2, 6)
                X = int(block_X / 2)
                if newBlockColor == 2:
                    newBlock = [(X - 1, 1), (X, 1), (X - 1, 2), (X, 2)]
                elif newBlockColor == 3:
                    newBlock = [(X - 1, 1), (X, 1), (X, 2), (X + 1, 2)]
                elif newBlockColor == 4:
                    newBlock = [(X - 1, 1), (X, 1), (X + 1, 1), (X + 1, 2)]
                elif newBlockColor == 5:
                    newBlock = [(X - 1, 1), (X, 1), (X + 1, 1), (X + 2, 1)]



                for (x, y) in newBlock:
                    block[x][y] = newBlockColor
                creatable = False


            elif creatable == False:
                moveDown(0, 1)
                pg.time.delay(400)

            for i in range(block_Y):
                for j in range(block_X):
                    color = block[j][i]
                    pg.draw.rect(ttDis, colors[color], (firstBlock_X + j * blockSize, firstBlock_Y + i * blockSize, blockSize, blockSize))
                    pg.draw.rect(ttDis, BLACK, (firstBlock_X + j * blockSize, firstBlock_Y + i * blockSize, blockSize, blockSize), 1)
        
            pg.display.update()   # 화면 갱신

            for event in pg.event.get():
                # 프로그램 종료
                if event.type == pg.QUIT:
                    running = False
                    isEnd = True
                    state = 1
                # 키보드 이벤트
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        move(-1, 0)
                    elif event.key == pg.K_RIGHT:
                        move(1, 0)
                    elif event.key == pg.K_DOWN:    # 아래 방향키, 소프트 드랍
                        moveDown(0, 1)
                    elif event.key == pg.K_SPACE:   # 스페이스, 하드 드랍
                        while creatable == False:
                            moveDown(0, 1)
                    elif event.key == pg.K_z:   # z키, 반 시계 회전
                        turn(0)
                    elif event.key == pg.K_x:   # x키, 시계 회전
                        turn(1)
                    elif event.key == pg.K_c:   # c키, 뒤집기
                        rvs()
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if exitBtn.collidepoint(event.pos):
                        isEnd = True
                        running = False

        for event in pg.event.get():
            # 프로그램 종료
            if event.type == pg.QUIT:
                running = False
                state = 1
            # 클릭 이벤트
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if playBtn.collidepoint(event.pos):
                    isEnd = False
                    block = [[1 for _ in range(block_Y)] for _ in range(block_X)]   # 0 GRAY, 1 BLACK, 2 BLUE, 3 GREEN, 4 PINK, 5 ORAGNE
                    for i in range(block_X):
                        block[i][0] = 0
                        block[i][block_Y - 1] = 0
                    for i in range(block_Y):
                        block[0][i] = 0
                        block[block_X - 1][i] = 0
                elif exitBtn.collidepoint(event.pos):
                    running = False
                    isEnd = True
    return state

def moveDown(tx, ty):
    global creatable
    for (x, y) in newBlock:
        blockColor = block[x][y]
        if block[x][y + 1] != 1 and (x + tx, y + ty) not in newBlock:
            creatable = True
            break

    if creatable == False:
        for (x, y) in newBlock:
            block[x][y] = 1
        for i, (x, y) in enumerate(newBlock):
            block[x + tx][y + ty] = newBlockColor
            newBlock[i] = (x + tx, y + ty)

def move(tx, ty):
    moveable = True
    for (x, y) in newBlock:
        blockColor = block[x][y]
        if block[x + tx][y + ty] != 1 and (x + tx, y + ty) not in newBlock:
            moveable = False
            break

    if moveable == True:
        for (x, y) in newBlock:
            block[x][y] = 1
        for i, (x, y) in enumerate(newBlock):
            block[x + tx][y + ty] = newBlockColor
            newBlock[i] = (x + tx, y + ty)

    pg.display.update()

def turn():
    pass

def rvs():
    if newBlockColor == 3:
        pass
    if newBlockColor == 4:
        pass