import pygame,time,os
from settings import *
from sprites import *
from boton import Boton

class Game():
    def __init__(self):
        #initialise pygame(window,mixer,clock,etc)
        self.running = True

        pygame.init()
        pygame.display.set_caption(TITLE)
        self.window = pygame.display.set_mode((window_width, window_height))
        self.display = pygame.Surface(DISPLAY_SIZE)
        self.clock = pygame.time.Clock()
        self.debug_on = True
        self.ASSETS = {}
        self.load_assets()
    
    def new_game(self,level:int):
        #Start a new game
        self.all_sprites = pygame.sprite.Group()
        #self.player = Player(map.spawn(level))
        self.run()

    def run(self):
        #Game Loop
        self.playing = True
        self.prev_time = self.get_time()
        while self.playing:
            self.dt = self.get_deltaTime()
            self.prev_time = self.get_time()

            self.events()
            self.update()
            self.draw()
            self.clock.tick(fps)

    def events(self):
        #Game Loop: - Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def update(self):
        #Game Loop: - Update
        self.all_sprites.update()
    
    def draw(self):
        #Game Loop: - Draw
        
        #Things drawn in the display
        self.display.fill(DARKGREY)
        self.all_sprites.draw(self.display)
        
        #Things drawn in the window
        self.window.blit(pygame.transform.scale(self.display, window_size), (0, 0))
        
        if self.debug_on:
            self.debug()
        
        pygame.display.update()
    
    #Gets current time
    def get_time(self):
        return time.time()
    
    #Gets time since last frame (dt)
    def get_deltaTime(self):
        return self.get_time() - self.prev_time 
    
    #Menu Loop
    def menu_screen(self):
        game_menu:bool = True
        anim_index:int = 0
        BACKGROUND_ANIM:list[pygame.Surface] = self.ASSETS["MENU_FRAMES"]
        BOTONES_IMGS:list[pygame.Surface] = self.ASSETS["BOTONES_IMGS"]
        MAIN_MENU_ANIM_COOLDOWN:float =0.09
        update_time_m = self.get_time()

        #Intances de botones
        level_1_b:Boton = Boton(10,10,BOTONES_IMGS[0],0.5)


        # Menu_Loop
        while game_menu:
            #Events: Pygame input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            #All Updates
            if level_1_b.check_click() :
                return 0



            # All Draws
            self.display.blit(pygame.transform.scale(BACKGROUND_ANIM[anim_index], DISPLAY_SIZE), (0, 0))
            
            self.window.blit(pygame.transform.scale(self.display, window_size), (0, 0))
            
            level_1_b.draw(self.window)
            
            if self.debug_on:
                self.debug()
            pygame.display.update()
            self.clock.tick(75)
            
            if (self.get_time() - update_time_m > MAIN_MENU_ANIM_COOLDOWN):
                update_time_m = self.get_time()
                if anim_index >= len(BACKGROUND_ANIM)-1:  # 24 frames in the animation
                    anim_index = 0
                else:
                    anim_index += 1    
            


    def pause_screen(self):
        pass

    def death_screen(self):
        pass

    def debug(self):
        self.window.blit(self.update_fps(),(10,10))

    def update_fps(self):
        font = pygame.font.SysFont("Arial", 18)
        fps = str(int(self.clock.get_fps()))
        fps_text = font.render(fps, 1, pygame.Color("coral"))
        return fps_text
    
    #loads menu background assets and game background assets
    def load_assets(self):
        menu_images = []
        bg_frames = []
        botones_images = []

        nb_bg_frames = len(os.listdir(f"images/background_imgs"))
        nb_menu_frames = len(os.listdir(f"images/menu_imgs"))
        nb_botones = len(os.listdir(f"images/botones"))

        #loads menu_frames
        for i in range(nb_bg_frames):
            bg_frames.append(pygame.image.load(f"images/background_imgs/background_{i}.png").convert())
        
        #loads bg_frames
        for n in range(nb_menu_frames):
            menu_images.append(pygame.image.load(f"images/menu_imgs/{n}.png").convert())
        
        #load imagenes de botones
        for j in range(nb_botones):
            botones_images.append(pygame.image.load(f"images/botones/{j}.png"))


        self.ASSETS["BOTONES_IMGS"] = botones_images
        self.ASSETS["MENU_FRAMES"] = menu_images
        self.ASSETS["BG_FRAMES"] = bg_frames
        


    def draw_grid(self,color:str):
        for x in range(0, window_width, TILE_SIZE):
            pygame.draw.line(self.window , color, (x,0) ,(x,window_height) )
        for y in range(0,window_height, TILE_SIZE):
            pygame.draw.line(self.window, color, (0,y), (window_width,y) )


G = Game()

while G.running:
    G.new_game(G.menu_screen())

pygame.quit()

