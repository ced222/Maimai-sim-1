import pygame
import time
from zipfile import ZipFile, Path
import io
import os
import threading
from os import walk
import gc
import logging

# class GenreSelectionGUI:
#     def __init__(self,):
#         pass

def fade_image(image_path):
    display_size = pygame.display.Info().current_w , pygame.display.Info().current_h - 50
    screen = pygame.display.set_mode(display_size)
    image = pygame.image.load(image_path)
    image_size = image.get_rect().size

    centered_image = [(display_size[0] - image_size[0])/2, (display_size[1] - image_size[1])/2]
    
    time.sleep(1)

    for i in range (255):
        screen.fill((0,0,0))    
        image.set_alpha(i)    
        screen.blit(image, centered_image)    
        pygame.display.update()    
        time.sleep(0.001)

    time.sleep(1.5)

    for i in range (255, 0, -1):
        screen.fill((0,0,0))       
        image.set_alpha(i)    
        screen.blit(image, centered_image)    
        pygame.display.update()    
        time.sleep(0.001)



class MainGUI:
    def __init__(self):
        self.songlist = []
        self.path = './assets/charts/'
        pygame.font.init()
        pygame.init()
        self.display = pygame.display.set_mode((0,0))
        pygame.display.toggle_fullscreen()
        windowcaption = 'Python MaiMai Sim'
        pygame.display.set_caption(windowcaption)
        self.clock = pygame.time.Clock()

    

    def read_charts(self):
        self.songlist = []
        self.genrelist = {}
        f = []
        # background = pygame.Surface((pygame.display.Info().current_w , pygame.display.Info().current_h))
        self.loading = 0
        self.total = 0
        
        for (dirpath, dirnames, filenames) in walk(self.path):
            f.extend(filenames)
            break
        for file_name in f:
            with ZipFile(self.path+file_name, 'r') as zip: 
                self.total += len(zip.namelist())/4
        
        for file_name in f:
            
            with ZipFile(self.path+file_name, 'r') as zip: 
                for file in zip.namelist():
                    if 'maidata' in file:
                        self.clock.tick()

                        metadata = file.split('/')
                        genre = metadata[0]
                        data = zip.read(name = file).decode('utf-8')
                        data = data.split('\n')
                        name = data[0].split('=')[1]
                        
                        img = file[:-11] + 'bg.png'
                        
                        
                        
                        track = file[:-11] + 'track.mp3'
                        id = metadata[1].split('_')[0]
                        self.genrelist[genre] = file_name
                        self.songlist.append(Chart(genre, name, img, track, id, file))
                        
                        # print(f'loading {int((self.loading/self.total)*100)}%, {file_name}')
                        self.loading += 1
                        self.clock.tick()
                        self.display.fill((int((self.loading/self.total)*255),int((self.loading/self.total)*255),int((self.loading/self.total)*255)))
                        pygame.display.flip()
                        
                        # time.sleep(0.01)
    
    def play_chart(self, genre, id):
        
        import sim

        for song in self.songlist:
            if song.genre == genre and song.id == id:
                break
        with ZipFile(self.path+self.genrelist[genre], 'r') as zip: 
            if not os.path.exists(f'./tmp/'+song.path[:-11]):
                zip.extract(song.track, path=f'./tmp')
                zip.extract(song.path, path=f'./tmp')
                
                
        path=f'./tmp/'+song.path[:-11]
        # print(path)
        c = sim.SongPlayer(path,self.display,6.5 ,self.diffcuilty)
        c.play()
    def animate_in(self, img):
        display_size = pygame.display.Info().current_w , pygame.display.Info().current_h
        w, h = display_size
        for i in range (0,255,1): 
            img.set_alpha(i)         
            time.sleep(0.002)
            self.display.fill((255,255,255))
            self.display.blit(img, (0.5*w - img.get_rect().centerx,0.5*h-img.get_rect().centery))

            pygame.display.update()

    def animate_out(self, img):
        display_size = pygame.display.Info().current_w , pygame.display.Info().current_h
        w, h = display_size
        for i in range (225,0,-1): 
            img.set_alpha(i)  
            self.display.fill((255,255,255))       
            time.sleep(0.002)
            self.display.blit(img, (0.5*w - img.get_rect().centerx,0.5*h-img.get_rect().centery))

            pygame.display.update()
    def animate_in_chart(self, img):
        display_size = pygame.display.Info().current_w , pygame.display.Info().current_h
        w, h = display_size
        diffcuiltynames  = [
            '','',
            'Basic',
            'Advancced',
            'Expert',
            'Master',
        ]
        font = pygame.font.Font("./assets/fonts/japanese.ttf",15)
        diffcuilty_surface = font.render(diffcuiltynames[self.diffcuilty], False, (0,0,0))
        for i in range (0,255,8): 
            img.set_alpha(i)         
            time.sleep(0.001)
            
            background_surface = pygame.Surface(display_size)
            background_surface.fill(pygame.Color("#000000"))
            background_surface2 = pygame.Surface((img.get_rect().width, img.get_rect().height))
            background_surface2.fill(pygame.Color('#FFFFFF'))
            
            self.display.blit(background_surface, (0, 0))
            self.display.blit(self.chartimg, self.chartpos)
            self.display.blit(self.textsurface, ((0.5*w )- (self.textsurface.get_rect().centerx), 0.3*h - self.textsurface.get_rect().centery))
            
            self.display.blit(diffcuilty_surface, (w/2 - diffcuilty_surface.get_rect().centerx,100))
            self.display.blit(background_surface2, (0.5*w - img.get_rect().centerx,0.5*h-img.get_rect().centery))
            self.display.blit(img, (0.5*w - img.get_rect().centerx,0.55*h-img.get_rect().centery))

            pygame.display.update()
        self.oldselection = self.currentselection
    def animate_out_chart(self,img):
        diffcuiltynames  = [
            '','',
            'Basic',
            'Advancced',
            'Expert',
            'Master',
        ]
        font = pygame.font.Font("./assets/fonts/japanese.ttf",15)
        diffcuilty_surface = font.render(diffcuiltynames[self.diffcuilty], False, (0,0,0))
        for i in range (255, 0, -8): 
            img.set_alpha(i)         
            time.sleep(0.001)
            display_size = pygame.display.Info().current_w , pygame.display.Info().current_h
            w, h = display_size
            background_surface = pygame.Surface(display_size)
            background_surface.fill(pygame.Color("#000000"))
            background_surface2 = pygame.Surface((img.get_rect().width, img.get_rect().height))
            background_surface2.fill(pygame.Color('#FFFFFF'))
            self.display.blit(background_surface, (0, 0))
            self.display.blit(self.chartimg, self.chartpos)
            self.display.blit(self.textsurface, ((0.5*w )- (self.textsurface.get_rect().centerx), 0.3*h - self.textsurface.get_rect().centery))
            
            self.display.blit(diffcuilty_surface, (w/2 - diffcuilty_surface.get_rect().centerx,100))
            self.display.blit(background_surface2, (0.5*w - img.get_rect().centerx,0.5*h-img.get_rect().centery))
            self.display.blit(img, (0.5*w - img.get_rect().centerx,0.55*h-img.get_rect().centery))
            pygame.display.update()
    def run(self):
        self.diffcuilty = 2
        display_size = pygame.display.Info().current_w , pygame.display.Info().current_h
        

        diffcuiltynames  = [
            '','',
            'Basic',
            'Advancced',
            'Expert',
            'Master',
        ]
        

        clock = pygame.time.Clock()
        font = pygame.font.Font("./assets/fonts/japanese.ttf",15)
        logofont = pygame.font.Font("./assets/fonts/japanese.ttf",40)
        titlefont = pygame.font.Font("./assets/fonts/japanese.ttf",30)
        titletext = logofont.render('Python MaiMai Simulator', True, (0,0,0))
        self.animate_in(titletext)
        
        
        
        w,h = display_size
        
        y = 0
        genre = str(list(self.genrelist)[0])

        self.chartimg = pygame.image.load("assets/images/song_menu.png").convert() #circle in the middle - judgement line
        self.chartimg = pygame.transform.scale(self.chartimg,(h,h)) 
        self.chartpos = self.chartimg.get_rect(center = self.display.get_rect().center) 

        background_surface = pygame.Surface(display_size)
        background_surface.fill(pygame.Color("#000000"))
        
        
        self.textsurface = titlefont.render(genre, True, (0, 0, 0))
        
        self.currentselection = 0
        
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
        for x,y in buttonpositions:
            buttonpositions[buttonpositions.index((x,y))] = ((0.5-(h * 0.45 * x)/w),0.5-(0.45 * y))

        # print(genre)
        pressedlist = []

        self.buttonlock = [0,0,0,0,0,0,0,0]
        self.oldselection = 0
        # background_surface.blit(background_surface, (0, 0))
        background_surface.blit(self.chartimg, self.chartpos)
        background_surface.blit(self.textsurface, ((0.5*w )- (self.textsurface.get_rect().centerx), 0.3*h - self.textsurface.get_rect().centery))
        for song in self.songlist:
            if song.genre == genre:
                # print(self.path+self.genrelist[genre])
                self.genreoffset = self.songlist.index(song)
                for song in self.songlist[self.genreoffset+1:]:
                    if song.genre != genre:
                        self.nextgenreindex = self.songlist.index(song)
                        break
                break
                
        song = self.songlist[self.genreoffset+self.currentselection]
        with ZipFile(self.path+self.genrelist[genre], 'r') as zip: 
            songimg = pygame.image.load(io.BytesIO(zip.read(song.img)))

        
        songsurface = pygame.Surface((0.25*h, 0.30*h))
        songsurface.fill((255,255,255))
        songsurface.blit(pygame.transform.scale(songimg, (0.225*h,0.225*h)), (0.0125*h,0))
        text = font.render(song.name, True, (0,0,0))
        songsurface.blit(text, (songsurface.get_rect().centerx-text.get_rect().centerx, 0.85*songsurface.get_rect().height))
        background_surface.blit(songsurface, (0.5*w - songsurface.get_rect().centerx,0.55*h-songsurface.get_rect().centery))
        time.sleep(0.5)
        gc.collect()
        gc.enable()
        self.animate_out(titletext)
        self.animate_in(background_surface)
        clock.tick(60)

        while True:
            
            
            
            
            self.display.blit(background_surface, (0, 0))
            self.display.blit(self.chartimg, self.chartpos)
            self.display.blit(self.textsurface, ((0.5*w )- (self.textsurface.get_rect().centerx), 0.30*h - self.textsurface.get_rect().centery))
            if self.currentselection < 0:
                self.currentselection = 0
            self.nextgenreindex = 1
            if self.currentselection > self.nextgenreindex-self.genreoffset:
                self.currentselection = self.oldselection
            if self.oldselection != self.currentselection:
                self.animate_out_chart(songsurface)
                song = self.songlist[self.currentselection]
                songsurface = pygame.Surface((0.25*h, 0.30*h))
                songsurface.fill((255,255,255))
                # print(self.currentselection, self.genreoffset)

                song = self.songlist[self.genreoffset+self.currentselection]
                
                with ZipFile(self.path+self.genrelist[genre], 'r') as zip: 
                    songimg = pygame.image.load(io.BytesIO(zip.read(song.img)))
                songsurface.blit(pygame.transform.scale(songimg, (0.225*h,0.225*h)), (0.0125*h,0))
                text = font.render(song.name, True, (0,0,0))
                songsurface.blit(text, (songsurface.get_rect().centerx-text.get_rect().centerx, 0.85*songsurface.get_rect().height))
                self.animate_in_chart(songsurface)
            else:
                song = self.songlist[self.currentselection]
                songsurface = pygame.Surface((0.25*h, 0.30*h))
                songsurface.fill((255,255,255))
                song = self.songlist[self.genreoffset+self.currentselection]
                with ZipFile(self.path+self.genrelist[genre], 'r') as zip: 
                    songimg = pygame.image.load(io.BytesIO(zip.read(song.img)))
                songsurface.blit(pygame.transform.scale(songimg, (0.225*h,0.225*h)), (0.0125*h,0))
                text = font.render(song.name, True, (0,0,0))
                songsurface.blit(text, (songsurface.get_rect().centerx-text.get_rect().centerx, 0.85*songsurface.get_rect().height))
                self.display.blit(songsurface, (0.5*w - songsurface.get_rect().centerx,0.55*h-songsurface.get_rect().centery))
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not event.touch:
                        event.x,event.y = event.pos
                        event.x = event.x/w
                        event.y = event.y/h
                        for x,y in buttonpositions:
                            if event.x >= x - 0.1 and event.x <= x + 0.1 and event.y >= y - 0.1 and event.y <= y + 0.1:
                                touch = buttonpositions.index((x,y))
                                # print(f'Button {touch} down')
                                pressedlist.append(touch)
                    # print(event.x, event.y)
                if event.type == pygame.MOUSEBUTTONUP:
                    if not event.touch:
                        event.x,event.y = event.pos
                        event.x = event.x/w
                        event.y = event.y/h
                        for x,y in buttonpositions:
                            if event.x >= x - 0.1 and event.x <= x + 0.1 and event.y >= y - 0.1 and event.y <= y + 0.1:
                                touch = buttonpositions.index((x,y))
                                # print(f'Button {touch} up')
                                pressedlist.remove(touch)
                    
                if event.type == pygame.FINGERDOWN:
                    
                    for x,y in buttonpositions:
                        if event.x >= x - 0.1 and event.x <= x + 0.1 and event.y >= y - 0.1 and event.y <= y + 0.1:
                            touch = buttonpositions.index((x,y))
                            # print(f'Button {touch} down')
                            pressedlist.append(touch)
                if event.type == pygame.FINGERUP:
                    
                    for x,y in buttonpositions:
                        if event.x >= x - 0.1 and event.x <= x + 0.1 and event.y >= y - 0.1 and event.y <= y + 0.1:
                            touch = buttonpositions.index((x,y))
                            # print(f'Button {touch} up')
                            pressedlist.remove(touch)

            if 1 in pressedlist:
                if self.buttonlock[1] == 0:
                    index = list(self.genrelist).index(genre) + 1
                    if index == len(self.genrelist):
                        index = 0
                    
                    genre = list(self.genrelist)[index]
                    self.textsurface = titlefont.render(genre, True, (0, 0, 0))
                    for song in self.songlist:
                        if song.genre == genre:
                            # print(self.path+self.genrelist[genre])
                            self.genreoffset = self.songlist.index(song)
                            for song in self.songlist[self.genreoffset+1:]:
                                if song.genre != genre:
                                    self.nextgenreindex = self.songlist.index(song)
                                    break
                            break
                    self.currentselection = 0
                self.buttonlock[1] += 1
            elif self.buttonlock[1] >= 1:
                self.buttonlock[1] = 0
            if 6 in pressedlist:
                if self.buttonlock[6] == 0:
                    index = list(self.genrelist).index(genre) - 1
                    if index < 0:
                        index = len(self.genrelist)-1
                    genre = list(self.genrelist)[index]
                    
                    self.textsurface = titlefont.render(genre, True, (0, 0, 0))
                    for song in self.songlist:
                        if song.genre == genre:
                            # print(self.path+self.genrelist[genre])
                            self.genreoffset = self.songlist.index(song)
                            for song in self.songlist[self.genreoffset+1:]:
                                if song.genre != genre:
                                    self.nextgenreindex = self.songlist.index(song)
                                    break
                            break
                    self.currentselection = 0
                self.buttonlock[6] += 1
            elif self.buttonlock[6] >= 1:
                self.buttonlock[6] = 0
                
            if 2 in pressedlist:
                if self.buttonlock[2] == 0:
                    self.currentselection += 1
                    # print(self.currentselection)
                self.buttonlock[2] += 1
            elif self.buttonlock[2] >= 1:
                self.buttonlock[2] = 0

            if 5 in pressedlist:
                if self.buttonlock[5] == 0:
                    self.currentselection -= 1
                    # print(self.currentselection)
                self.buttonlock[5] += 1
            elif self.buttonlock[5] >= 1:
                self.buttonlock[5] = 0
            
            if 3 in pressedlist:
                if self.buttonlock[3] == 0:
                    clock.tick(5)
                    self.animate_out_chart(songsurface)
                    self.play_chart(song.genre, song.id)
                    print('exited song')
                    pressedlist.remove(3)
                    self.animate_in_chart(songsurface)

                self.buttonlock[3] += 1
            elif self.buttonlock[3] >= 1:
                self.buttonlock[3] = 0

            if 4 in pressedlist:
                if self.buttonlock[4] == 0:
                    pass

                self.buttonlock[4] += 1
            elif self.buttonlock[4] >= 1:
                self.buttonlock[4] = 0

            if 0 in pressedlist:
                if self.buttonlock[0] == 0:
                    self.diffcuilty += 1
                    if self.diffcuilty >= len(diffcuiltynames)-1:
                        self.diffcuilty = len(diffcuiltynames)-1
                self.buttonlock[0] += 1
            elif self.buttonlock[0] >= 1:
                self.buttonlock[0] = 0

            if 7 in pressedlist:
                if self.buttonlock[7] == 0:
                    self.diffcuilty -= 1
                    if self.diffcuilty <= 0:
                        self.diffcuilty = 0
                self.buttonlock[7] += 1
            elif self.buttonlock[7] >= 1:
                self.buttonlock[7] = 0
            diffcuilty_surface = font.render(diffcuiltynames[self.diffcuilty], True, (0,0,0))
            self.display.blit(diffcuilty_surface, (w/2 - diffcuilty_surface.get_rect().centerx,100))

            
                
            pygame.display.update()
            clock.tick(60)

        # test code
        # self.play_chart('ゲームバラエティ', '734')

class Lock(list):
    pass

                        

class Chart:
    def __init__(self, genre, name, img, track,id, path):
        self.genre = genre
        self.name = name
        self.img = img
        self.track = track
        self.path = path
        self.id = id
        self.button = None



c = MainGUI()
gc.disable()
c.read_charts()
c.run()