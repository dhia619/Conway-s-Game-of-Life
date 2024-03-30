import pygame
from numpy import array,zeros,count_nonzero
from button import*

pygame.init()

sw,ash = 500,650
sh = 500
tile_size = 50
clock = pygame.time.Clock()
screen = pygame.display.set_mode((sw,ash))
pygame.display.set_caption("Game of life")

grid_array = array([zeros(sw//tile_size)]*(sh//tile_size))
def draw_grid():
    x_pos,y_pos = 0,0
    for i in range(sh//tile_size+1):
        pygame.draw.line(screen,(191, 207, 231),(0,y_pos),(sw,y_pos),2)
        y_pos += tile_size
    for i in range(sw//tile_size+1):
        pygame.draw.line(screen,(191, 207, 231),(x_pos,0),(x_pos,sh),2)
        x_pos += tile_size

spot_to_spawn_cords = []
font1 = pygame.font.Font("assets/KumbhSans-VariableFont_YOPQ,wght.ttf",21)

def numberOfalive(arr):
    occ = 0
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i,j] == 1:
                occ += 1
    return occ

def create_neighbourhood(row,col):
    neighbourhood = array([zeros(3)]*3)
    try:
        neighbourhood[0,0] = grid_array[row-1,col-1]
    except:
        pass
    try:
        neighbourhood[0,1] = grid_array[row-1,col]
    except:
        pass
    try:
        neighbourhood[0,2] = grid_array[row-1,col+1]
    except:
        pass
    try:
        neighbourhood[1,0] = grid_array[row,col-1]
    except:
        pass
    try:
        neighbourhood[1,2] = grid_array[row,col+1]
    except:
        pass
    try:
        neighbourhood[2,0] = grid_array[row+1,col-1]
    except:
        pass
    try:
        neighbourhood[2,1] = grid_array[row+1,col]
    except:
        pass
    try:
        neighbourhood[2,2] = grid_array[row+1,col+1]
    except:
        pass
    return neighbourhood

def underpopulation(row,col):
    neighb = create_neighbourhood(row,col)
    if numberOfalive(neighb) < 2:
        return True
    else:
        return False

def overpopulation(row,col):
    neighb = create_neighbourhood(row,col)
    if numberOfalive(neighb) > 3:
        return True
    else:
        return False

def reproduce(row,col):
    neighb = create_neighbourhood(row,col)
    if numberOfalive(neighb) == 3:
        return True
    else:
        return False

def next_gen():
    new_arr = grid_array.copy()
    for k in range(len(grid_array)):
        for l in range(len(grid_array[k])):
            if grid_array[k,l] == 1:
                if underpopulation(k,l) or overpopulation(k,l):
                   new_arr[k,l] = 0
            if grid_array[k,l] == 0:
                if reproduce(k,l):
                    new_arr[k,l] = 1
    return new_arr

on = True
simulation = False
next_gen_cooldown = 10
speeds = [0.05,0.1,0.2,0.5,0.7,1,1.5,2,5,7,10]
speed_index = len(speeds)//2
simulation_speed = speeds[speed_index]
gen_index = 1
stats = [count_nonzero(grid_array),len(grid_array)**2-count_nonzero(grid_array)]

buttons = [
    Button("back","assets/backward.png",(sw//2-90,sh+100),5),
    Button("pause","assets/unpause.png",(sw//2-25,sh+100),5),
    Button("forw","assets/forward.png",(sw//2+40,sh+100),5),
    Button("reset","assets/reset.png",(sw//2+105,sh+100),5)
]
panel_img = pygame.image.load("assets/bg_wood.png")

cellstatesSurface = pygame.Surface((120,70),pygame.SRCALPHA)
cellstatesSurface.fill((240,248,250,90))

while on :

    #render all text
    fps_surface = font1.render("FPS :"+f'{round(clock.get_fps())}',True,(0,0,0))
    simulation_state_surface = font1.render("simulation : on" if simulation else "simulation : off",True,(0,0,0))
    sim_spd_surface = font1.render(f'{simulation_speed}',True,(205,45,85))
    generation_surface = font1.render("Generation "+f'{gen_index}',True,(255,255,255))
    Bcell_sruface = font1.render("Alive "+f'{stats[0]}',True,(25,125,45))
    Wcell_sruface = font1.render("Dead "+f'{stats[1]}',True,(200,30,10))

    #transparent surfaces
    gen_transp_surf = pygame.Surface((generation_surface.get_width()+10,generation_surface.get_height()+10),pygame.SRCALPHA)
    gen_transp_surf.fill((27,27,27,128))    
   
    #show texts,images on the screen
    screen.fill((255,255,255))
    screen.blit(panel_img,(0,sh))
    screen.blit(gen_transp_surf,(5,sh+generation_surface.get_height()))
    screen.blit(cellstatesSurface,(5,sh+Bcell_sruface.get_height()*2.5))
    screen.blit(fps_surface,(sw-fps_surface.get_width()-10,sh+fps_surface.get_height()+10))
    screen.blit(simulation_state_surface,(sw-simulation_state_surface.get_width()-10,sh+simulation_state_surface.get_height()*2+10))
    screen.blit(sim_spd_surface,(sw//2-sim_spd_surface.get_width()//2,sh+70))
    screen.blit(generation_surface,(10,sh+generation_surface.get_height()+5))
    screen.blit(Bcell_sruface,(10,sh+Bcell_sruface.get_height()*2.7))
    screen.blit(Wcell_sruface,(10,sh+Wcell_sruface.get_height()*3.5+10))
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    #draw cell states
    for row in range(len(grid_array)):
        for col in range(len(grid_array[row])):
            if grid_array[row][col] == 1:
                pygame.draw.rect(screen,(0,0,0),(row*tile_size,col*tile_size,tile_size,tile_size))
            if grid_array[row][col] == 0:
                pygame.draw.rect(screen,(255, 255, 255),(row*tile_size,col*tile_size,tile_size,tile_size))

    draw_grid()

    #handle mouse clicks
    if mouse_pressed[0] or mouse_pressed[2]:
        #check mouse cursor is not outside of the window
        if mouse_pos[0]>=0 and mouse_pos[0]<=sw:
            stats = [count_nonzero(grid_array),len(grid_array)**2-count_nonzero(grid_array)]
            spot_to_spawn_cords = [mouse_pos[0]//tile_size,mouse_pos[1]//tile_size]
            #left click
            if mouse_pressed[0]:
                try:
                    if grid_array[spot_to_spawn_cords[0]][spot_to_spawn_cords[1]] == 0:
                        grid_array[spot_to_spawn_cords[0]][spot_to_spawn_cords[1]] = 1
                except:
                    pass
            #right click
            if mouse_pressed[2]:
                try:
                    if grid_array[spot_to_spawn_cords[0]][spot_to_spawn_cords[1]] == 1:
                        grid_array[spot_to_spawn_cords[0]][spot_to_spawn_cords[1]] = 0
                except:
                    pass

    #cell state variation
    if simulation:
        next_gen_cooldown -= simulation_speed
        if next_gen_cooldown <= 0:
            grid_array = next_gen()
            next_gen_cooldown = 10
            simulation_speed = speeds[speed_index]
            gen_index += 1
            stats = [count_nonzero(grid_array),len(grid_array)**2-count_nonzero(grid_array)]

    #draw and check if buttons were clicked
    for btn in buttons:
        btn.draw(screen)
        btn.update()
        if btn.pressed:
            if btn.text == "pause":
                simulation = not(simulation)
                if simulation:
                    btn.image = pygame.image.load("assets/pause.png")
                else:
                    btn.image = pygame.image.load("assets/unpause.png")
            elif btn.text == "back":
                if speed_index > 0:
                    speed_index -= 1
                    simulation_speed = speeds[speed_index]
            elif btn.text == "forw":
                if speed_index < len(speeds)-1:
                    speed_index += 1
                    simulation_speed = speeds[speed_index]
            elif btn.text == "reset":
                gen_index = 1
                next_gen_cooldown = 10
                speed_index = len(speeds)//2
                grid_array = array([zeros(sw//tile_size)]*(sh//tile_size))
                stats = [count_nonzero(grid_array),2500-count_nonzero(grid_array)]
                simulation = False
                buttons[1].image = pygame.image.load("assets/unpause.png")

    #update screen
    pygame.display.flip()
    clock.tick(90)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                simulation = not(simulation)

pygame.quit()