import pygame, math, time, threading, os
FRAMERATE = 60
import psutil
pygame.init()
pygame.mixer.init()
def check_performance():
    process = psutil.Process(os.getpid())  # Get current process ID
    cpu_percent = process.cpu_percent(interval=0.1)  # CPU usage
    memory_info = process.memory_info()  # Memory usage

    # Display performance data
    print(f"CPU Usage: {cpu_percent}%")
    print(f"Memory Usage: {memory_info.rss / 1024 ** 2:.2f} MB")  # Convert bytes to MB
if __name__ == '__main__':
    pygame.display.init()
    display = pygame.display.set_mode((0,0))
    pygame.display.toggle_fullscreen()
 

from loader import phrase_simai, unpackChart




def getChart(path, diffcuilty, speed, radiusConst, summonRing):
    #return loader.phrase_simai(simaichart)
    with open(path+'/maidata.txt', 'rb') as f:
        simaichart = f.read()
    simaichart = simaichart.decode('utf-8')
    chartlist = simaichart.split('\n')
    for line in chartlist:
        if f'&inote_{diffcuilty}' in line:
            simaichart = chartlist[chartlist.index(line)+1:]
            # print(simaichart)
            for line in simaichart:
                print('"',line,'"')
                if line.replace(' ','') == 'E':
                    simaichart = simaichart[:simaichart.index(line)+1]
                    break
    # print(simaichart)
    simaichart = '\n'.join(simaichart)
    


    chart = unpackChart(phrase_simai(simaichart, diffcuilty, speed), radiusConst, summonRing, speed)
    musicpath = path+'/track.mp3'
    return chart, musicpath






class SongPlayer():

    def __init__(self, path, display, speed, diffcuilty ):

        
        self.songId = 0 #integer for song id - determines the song to play
        self.difficultyId = 0 #0 is basic, 5 is remas (if it exists)

        self.baseTime = 60 #in ticks. 60 ticks in a second. Time taken for note to go from summon ring to judgement line with a speed of one
        self.baseTimeMs = 1000 #base time in miliseconds
        speedMultiplerFactor = (speed-1)/3 + 1
        timeTicks = int(self.baseTime/speedMultiplerFactor) #time taken for note to go from summon ring to judgement line adjusted for speed
        timeMs = int(self.baseTimeMs/speedMultiplerFactor)
        #self.metronometick1 = pygame.mixer.Sound("./assets/sounds/tick1.wav") 
        #self.metronometick2 = pygame.mixer.Sound("./assets/sounds/tick2.wav")
        
        self.display = display 
        monitorWidth, monitorHeight = pygame.display.get_window_size()
        self.radiusConst = monitorHeight * 0.45 #radius of judgement line
        self.summonRing = self.radiusConst * 1.7/6.3 #radius of summon ring
        self.center = (monitorWidth/2, monitorHeight/2) #center of judgement line
        print((self.radiusConst - self.summonRing))
        self.speed = int((self.radiusConst - self.summonRing) / timeTicks)    #this is in pixels per tick.

        self.speedMs = int((self.radiusConst - self.summonRing) / timeMs)
        
        self.fps = pygame.time.Clock()
        self.phrasedchart, self.musicpath = getChart(path, diffcuilty, self.speedMs, self.radiusConst, self.summonRing)
        
        # print(self.phrasedchart)

        # self.buffer = []
        
        self.bar = 0
        self.barfraction = 0
   
     
        # self.tickCount = 0
        # # print((self.FRAMERATE * 60) / self.bpm)
        self.chartimg = pygame.image.load("assets/images/chart.png").convert() #circle in the middle - judgement line
        self.chartimg = pygame.transform.scale(self.chartimg,(monitorHeight,monitorHeight)) 
        self.chartpos = self.chartimg.get_rect(center = self.display.get_rect().center) 
        #chartendimg is used to hide the note when it reaches outside
        self.chartendimg = pygame.image.load("assets/images/chart-end.png").convert_alpha()
        self.chartendimg = pygame.transform.scale(self.chartendimg,(monitorHeight,monitorHeight))
    def updateHolds(self):
        for note in self.activebuffer:
            if note.name ==  'HoldNote':
                note.elapsedDuration += 1 
                note.sprite[2].elapsedDuration += 1 
                if int(note.elapsedDuration) == int(note.holdDuration):

                    
                    note.sprite[1].locked = False
                

                    
        
    def phrase_notes(self, chart):
        clock = pygame.time.Clock()
        currentbarfraction = 0
        bar = 0
        self.activebuffer = []
        holdbuffer = []
        offset = 0
        # seperate loop that runs every 1/16th of a beat
        # higher accuracy may be needed later on 
        currentTime = pygame.mixer.music.get_pos()
        print(currentTime, int(self.phrasedchart[0].milisecond))
        while self.running:
            clock.tick(1000)
            self.updateHolds()
            
            
            currentTime = pygame.mixer.music.get_pos()
            
            if int(currentTime) >= int(self.phrasedchart[0].milisecond):
                self.activebuffer.append(self.phrasedchart[0])
                self.phrasedchart.pop(0)
                print(self.phrasedchart[0].milisecond)
                if int(currentTime) >= int(self.phrasedchart[0].milisecond): #check for double notes
                    self.activebuffer.append(self.phrasedchart[0])
                    self.phrasedchart.pop(0)
           
            
            # print(tpb)
            

                
                # Go through the current bar
                # for note in notes:
                    

                #     # Check if the current 16th beat is the one to display the note for
                #     if note.barFraction == currentbarfraction:
                #         # Different note types
                #         if note.name == 'TapNote':
                #             self.activebuffer.append(note)
                #         if note.name == 'HoldNote':
                #             self.activebuffer.append(note)
                            
                #             # Fix for note sprite so that they appear consistant to the offical game play
                #             note.sprite[0].update(25)
                #             note.sprite[1].locked = False
                #             note.sprite[1].update(-25)
                #             note.sprite[1].locked = True
                            
                            # Keep track of the current hold notes that are being displayed
                            

                # Look through the hold buffer to find out when to allow the tail note to move
                # for i in holdbuffer:
                    
                #     endFraction = (1/i.divider)*i.duration*currentbar['timesig']+i.barFraction
                #     endBar = int(i.barNumber)
                #     while endFraction >= currentbar['timesig']:
                #         endFraction -= currentbar['timesig']
                #         endBar += 1
                #     # print(endFraction,endBar, currentbarfraction, bar)
                #     if endFraction <= currentbarfraction and endBar == bar:
                #         # unlock the tail note so that it can move
                #         i.tailSprite.locked = False
                #         holdbuffer.remove(i)

                #         # print('removed')
                #     else:
                #         # otherwise display a hold body note
                #         # print(i.buttonNumber)
                #         sprite = i.segment(i.buttonNumber)
                #         if sprite:
                #             self.displaybuffer.append(sprite)
                    # # print(int((1/i.divider)*i.duration*currentbar['timesig']))
                # # print(currentbarfraction, len(holdbuffer))
                        
                        # if note.__name__ == 'HoldNo':
                        #     note.tailSprite.locked = True

                # if game is inconsistant, check actualms to compare the actual milisecond time plaused and compare to the tpb
                
                

                # since each loop cycle is 1/16th of the beat, incrument 1/16
                

                #update hold notes

                

                # if end of the bar, incrument bar
              

    def load_music(self):
        # load the music, calculate time offset

        #offset = 0.250

        #time.sleep((300/self.radiusConst)+offset)
        pygame.mixer.music.play()

    def play(self,):
        
        
        
        

        self.running = True
        #load bar to read
        pygame.mixer.music.load(self.musicpath)
         
        threading.Thread(target=self.load_music, daemon=True).start()
        
        
        # here need finetune offset
        # time.sleep(1)

        #main game engine
        threading.Thread(target=self.phrase_notes, args=(self.phrasedchart,), daemon = True).start()
        
        buttonpositions = [
            (-0.38268343236508984, 0.9238795325112867),
            (-0.9238795325112867, 0.38268343236508984),
            (-0.9238795325112867, -0.38268343236508984), 
            (-0.38268343236508984, -0.9238795325112867), 
            (0.38268343236508984, -0.9238795325112867),
            (0.9238795325112867, -0.38268343236508984),
            (0.9238795325112867, 0.38268343236508984),
            (0.38268343236508984, 0.9238795325112867),
            
            
        ]
        w,h =  pygame.display.Info().current_w , pygame.display.Info().current_h-50
        for x,y in buttonpositions:
            buttonpositions[buttonpositions.index((x,y))] = ((0.5-(h * 0.45 * x)/w),0.5-(0.45 * y))

    
        pressedlist = []
        judgement = pygame.font.Font("./assets/fonts/japanese.ttf",20)
        judgementtext = pygame.Surface((0,0))
        clock = pygame.time.Clock()
        while self.running:
            # Tick FRAMERATE times per second
            
            # print(FRAMERATE, end = '\r')
            clock.tick(FRAMERATE)
            
            self.display.fill((0,0,0))
            self.display.blit(self.chartimg, self.chartpos)

            for note in self.activebuffer:

                for spriteindex, sprites in enumerate(note.sprite):
                   
                    img, pos = sprites.update(self.speed/(FRAMERATE/60))
                    if note.name == "HoldNote" and spriteindex != 2:
                        if not math.sqrt((pos[0] - self.center[0] + img.get_rect().centerx)**2 + (pos[1] - self.center[1] + img.get_rect().centery)**2) > self.radiusConst * 1.2 :
                            self.display.blit(img, pos) #blit everything that hasnt crossed judgement
        
                        elif spriteindex == 1 and math.sqrt((pos[0] - self.center[0] + img.get_rect().centerx)**2 + (pos[1] - self.center[1] + img.get_rect().centery)**2) > self.radiusConst * 1.2:
                            self.activebuffer.remove(note) #if tail has passed judgement, delete hold from memoery
                    elif spriteindex == 2: #same deal here but for segments so for loop must be implemented
                        
                        for segment in img:
                            if not math.sqrt((pos[0] - self.center[0] + segment[0].get_rect().centerx)**2 + (pos[1] - self.center[1] + segment[0].get_rect().centery)**2) > self.radiusConst * 1.2:
                                self.display.blit(segment[0], segment[1])
                            else:
                                img.remove(segment)
                        
                    elif math.sqrt((pos[0] - self.center[0] + img.get_rect().centerx)**2 + (pos[1] - self.center[1] + img.get_rect().centery)**2) > self.radiusConst * 1.2 :
                        if note.name == "TapNote":
                            #judgementtext = judgement.render('Miss', False, (255,255,255))
                            self.activebuffer.remove(note)
                            # self.display.blit(judgementtext, ((0.5*w )- (judgementtext.get_rect().centerx), 0.5*h - judgementtext.get_rect().centery))
                            # print('Miss')
                            # judgementtext = judgement.render('Miss', False, (255,255,255))
                            # print('Miss')
                            
                                                    # elif note.name == "HoldNote":
                            # if note.elapsedDuration > note.holdDuration + 50:
                            #     self.activebuffer.remove(note)

                    else:
                        self.display.blit(img, pos)
                
            
            # display notes in between
            self.display.blit(self.chartendimg, self.chartpos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key== pygame.K_ESCAPE:

                        self.running = False
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()

                if event.type == pygame.FINGERDOWN:
                        
                    for x,y in buttonpositions:
                        # print(x,y)
                        if event.x >= x - 0.1 and event.x <= x + 0.1 and event.y >= y - 0.1 and event.y <= y + 0.1:
                            touch = buttonpositions.index((x,y))
                            # print(f'Button {touch} down')
                            pressedlist.append(touch)
                if event.type == pygame.FINGERUP:
                    
                    for x,y in buttonpositions:
                        if event.x >= x - 0.1 and event.x <= x + 0.1 and event.y >= y - 0.1 and event.y <= y + 0.1:
                            touch = buttonpositions.index((x,y))
                            # print(f'Button {touch} up')
                            try:
                                pressedlist.remove(touch)
                            except ValueError:
                                # somehow we missed a touch down event
                                pass
            

            for note in self.activebuffer:
                if note.buttonNumber in pressedlist:
                    sprite = note.sprite[0]
                    x, y = buttonpositions[note.buttonNumber]
                    
                    self.display.blit(judgement.render(f'{note.buttonNumber}, {pressedlist}', False, (255,255,255) ), (100, 100))
                    if note.name == 'TapNote' and sprite.pos[0]/w >= x - 0.1 and sprite.pos[0]/w <= x + 0.1 and sprite.pos[1]/h >= y - 0.1 and sprite.pos[1]/h <= y + 0.1:
                        # print(x,y, sprite.pos)
                        if sprite.pos[0]/w >= x - 0.05 and sprite.pos[0]/w <= x + 0.05 and sprite.pos[1]/h >= y - 0.05 and sprite.pos[1]/h <= y + 0.05:
                            self.activebuffer.remove(note)
                            judgementtext = judgement.render('Perfect', False, (100,255,100))
                            # print('Perfect')
                            # judgementtext = self.display.blit(judgementtext, ((0.5*w )- (judgementtext.get_rect().centerx), 0.5*h - judgementtext.get_rect().centery))

                        elif sprite.pos[0]/w >= x - 0.08 and sprite.pos[0]/w <= x + 0.08 and sprite.pos[1]/h >= y - 0.08 and sprite.pos[1]/h <= y + 0.08:
                            self.activebuffer.remove(note)
                            judgementtext = judgement.render('Great', False, (255,255,100))
                            # print('Great')
                            # judgementtext = self.display.blit(judgementtext, ((0.5*w )- (judgementtext.get_rect().centerx), 0.5*h - judgementtext.get_rect().centery))
                        else:
                            self.activebuffer.remove(note)
                            judgementtext = judgement.render('Bad', False, (255,100,100))
                            # print('Bad')
                            # self.display.blit(judgementtext, ((0.5*w )- (judgementtext.get_rect().centerx), 0.5*h - judgementtext.get_rect().centery))

                        

                        
                    
                        
            self.display.blit(judgementtext, (w/2 - judgementtext.get_rect().centerx, h/2 -judgementtext.get_rect().centery))
            self.display.blit(judgement.render(str(int(FRAMERATE)),True, (255,255,255) ), (0,0))
            pygame.display.update()
        return



        #while True:

            # output.setText(slider.getValue())
            # self.fps.tick(self.FRAMERATE)
            

            # # update screen/delete object
            # # if self.ticks == int(self.soundDelay) + 200:
                
            # self.display.fill((0,0,0))
            # # # print(int(self.ticks % ((self.FRAMERATE * 60) / self.bpm)))
            # if int(self.ticks % ((self.FRAMERATE * 60) / self.bpm)) == int(0.0):
            #     self.barfraction += 1
            #     self.tickBuffer.append(self.ticks + self.soundDelay)
            #     if self.barfraction == self.timesig:
            #         self.bar += 1
                    
            #         self.barfraction = 0
            #     if self.bar == 0:
            #         self.display.fill((20,20,20))
            # # print(self.bar, self.barf   raction)
            # # if ticks == tickBuffer[0]:
            # #     tickCount += 1
            # #     tickBuffer.remove(ticks)
            # #     if tickCount == 1:
            # #         pygame.mixer.Channel(0).play(tick1)
                    
            # #     else:
            # #         pygame.mixer.Channel(0).play(tick2)
            # #     if tickCount == timesig:
            # #         tickCount = 0
            # #self.buffer, self.chart = self.phraser.checkTime(self.chart, self.buffer, self.bar, self.barfraction)
            

            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         pygame.quit()
            #     if event.type == pygame.KEYDOWN:
            #         if event.key== pygame.K_ESCAPE:
            #             pygame.quit()
            
            
            # self.display.blit(self.chartimg, self.chartpos)
            # for note in self.buffer:
            #     image, pos = note.update()
            #     self.display.blit(image, pos)
            #     if math.sqrt((pos[0] - self.center[0] + image.get_rect().centerx)**2 + (pos[1] - self.center[1] + image.get_rect().centery)**2) > self.radiusConst * 1.05:
            #         self.buffer.remove(note)
            # self.display.blit(self.chartendimg, self.chartpos)

            # pygame.display.update()
            # self.ticks += 1

        

# class chartPhraser():
#     def __init__(self, speed, timesig):
#         self.holdbuffer = []
#         self.holdbodylock = 0
#         self.speed = speed
#         self.timesig = timesig
        
#     def phraseHold(self, buffer, duration, bar, barfraction, note):
#         tail = None
#         if note[0] == 'hold':
#             if note[1] == bar and note[2] == barfraction:
#                 tail = HoldTail(self.speed, note[3])
#                 buffer.append(tail)
#                 self.holdbuffer.append([tail, duration, bar, barfraction])
#         for hold in self.holdbuffer:
#             baroffset = 0
#             duration = hold[1]
#             if duration > 3:
#                 duration = int(duration%self.timesig)
#                 baroffset = int(duration/self.timesig)
            
#             if hold[2] + baroffset == bar and hold[3] + duration == barfraction:
#                 hold[0].locked = False
#                 self.holdbuffer.remove(hold)
#             elif hold[2] + baroffset >= bar and hold[3] + duration >= barfraction:
#                 if tail == None and hold[0].locked == True:
#                     self.buffer.append(HoldBody(self.speed, hold[0].button))

        
#         return buffer


#     def checkTime(self, chart, buffer, bar, barfraction):
#         for note in chart:
#             buffer = self.phraseHold(buffer, note[4], bar, barfraction, note)
#             if note[1] == bar and note[2] == barfraction:
#                 if note[0] == 'tap':
#                     if note[4]:
#                         tapnote = TapNote(self.speed,note[3])
#                         tapnote.double()
#                         buffer.append(tapnote)

#                         chart.remove(note)
#                     else:
#                         buffer.append(TapNote(self.speed,note[3]))
#                         chart.remove(note)
#                     break
#                 if note[0] == 'hold':
#                     buffer.append(HoldHead(self.speed, note[3]))
#                     chart.remove(note)
#                     break # for double notes just dont break
#         return buffer, chart



# chart, bpm = loader.phrase_simai(simaichart)
# chart = [['hold', 1,0,1,8,False,False]]
# # buffer = [TapNote(1,0),TapNote(1,1),TapNote(1,2),TapNote(1,3),TapNote(1,4),TapNote(1,5),TapNote(1,6),TapNote(1,7)]
# buffer = []
# ticks = 0
# bar = 0
# barfraction = 0
# soundDelay = (radiusConst/((math.log(speed) + 1)* radiusConst * 0.1/20))
# tickBuffer = []
# tickCount = 0
# # print((FRAMERATE * 60) / bpm)
# while True:
#     fps.tick(FRAMERATE)
    
#     # update screen/delete object
#     if ticks == int(soundDelay):
#         pygame.mixer.music.load('./assets/sounds/track.mp3')
#         pygame.mixer.music.play()
#     display.fill((0,0,0))
#     # print(int(ticks % ((FRAMERATE * 60) / bpm)))
#     if int(ticks % ((FRAMERATE * 60) / bpm)) == int(0.0):
#         barfraction += 1
#         tickBuffer.append(ticks + soundDelay)
#         if barfraction == timesig:
#             bar += 1
            
#             barfraction = 0
#         if bar == 0:
#             display.fill((20,20,20))
#     # print(bar, barfraction)
#     # if ticks == tickBuffer[0]:
#     #     tickCount += 1
#     #     tickBuffer.remove(ticks)
#     #     if tickCount == 1:
#     #         pygame.mixer.Channel(0).play(tick1)
            
#     #     else:
#     #         pygame.mixer.Channel(0).play(tick2)
#     #     if tickCount == timesig:
#     #         tickCount = 0
#     buffer, chart = checkTime(chart, buffer, bar, barfraction)
    

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#         if event.type == pygame.KEYDOWN:
#             if event.key== pygame.K_ESCAPE:
#                 pygame.quit()
    
    
#     display.blit(chartimg, chartpos)
#     for note in buffer:
#         image, pos = note.update()
#         display.blit(image, pos)
#         if math.sqrt((pos[0] - center[0] + image.get_rect().centerx)**2 + (pos[1] - center[1] + image.get_rect().centery)**2) > radiusConst * 1.05:
#             buffer.remove(note)
#     display.blit(chartendimg, chartpos)

#     pygame.display.update()
#     ticks += 1

if __name__ == '__main__':

    path = './tmp/ゲームバラエティ/1051_DESTR0YER_DX'
    c = SongPlayer(path,display,6,1)
    
    c.play()

