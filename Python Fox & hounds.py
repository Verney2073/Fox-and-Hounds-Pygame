# NEXT STEPS 
# Why do funcs like collide_check_new not work? 
# Carefully check that all coords are updating as it seems they aren't e.g. fox_fl wasn't when not in the while loop
# once a while loop is running, funcs outside of that loop will not update unless told to by functions within the while loop, they won't update automatically

#use a collide_check variable to return a set of two or four results depending on fox or hound:
#return True if square is taken, False if square is open. Build in if it's over the edge of the board
#use a for loop and cycle through a list of tuples. The list of tuples sohould contain the locations of all of the hounds coords, plus the edges (?)
#it should be ok to include the coord of the piece that's moving, since fox_fl or similar should never be equal to fox_coord 


import pygame
width = 1400
height = 800
black = (0,0,0) #rgb values for the colours
white = (255,255,240) #changed to ivory RGB; orig white is 255,255,255
gray = (128, 128, 128)
dark_gray = (50,50,50)
green =(0,255,0)
gold = (212,175,55)
blue = (0,255,255)
orange = (255,127,80) #changed to 'chocolate' RGB values, orig orange is 255,165,0

fox_clicked = False
h1_clicked = False
h2_clicked = False
h3_clicked = False
h4_clicked = False

active_foxfl = False

start_game = False
fox_turn = False
hound_turn = False

fox_wins = False
hounds_win = False

test_color = white
collide_color = white
open_squares = []


pygame.init() #initialise BEFORE using pygame specific functions liike .font below
screen=pygame.display.set_mode([width,height])

label_font = pygame.font.Font('freesansbold.ttf',22)
medium_font = pygame.font.Font('freesansbold.ttf',28)

start_btn_color = dark_gray

#to credit the image designers: 
#<a href="https://www.flaticon.com/free-icons/fox" title="fox icons">Fox icons created by Triberion - Flaticon</a>
#<a href="https://www.flaticon.com/free-icons/dog" title="dog icons">Dog icons created by Icongeek26 - Flaticon</a>
background_orig = pygame.image.load("Tapestry.jpg")
background = pygame.transform.scale(background_orig,(width,height))

hound_orig = pygame.image.load("pharaoh-hound.png")
hound = pygame.transform.scale(hound_orig,(37,37))

#no longer needed
h1 = label_font.render("H1",True,dark_gray)
h1_coord = (300,400)
h2 = label_font.render("H2",True,dark_gray)
h2_coord = (400,400)
h3 = label_font.render("H3",True,dark_gray)
h3_coord = (500,400)
h4 = label_font.render("H4",True,dark_gray)
h4_coord = (600,400)
#as this is pygame, you can't simply use string values here

fox_orig = pygame.image.load("fox_icon.png")    #label_font.render("F",True,dark_gray)
fox = pygame.transform.scale(fox_orig,(38,38))

# no longer needed ... fox_rect = pygame.draw.rect(screen,green,[600,50,100,100],3,5) # this colour doesn't change b/c later we set fox_rect colour to 'piece_color' variable

fox_coord = (450,50)
fox_open = [True,True,False,False]

# fox_fl = ((fox_coord[0] - 50),(fox_coord[1] + 50)) it seems that this runs once but does not update when the other coords are updating
#

fox_piece_color = gray
hound_piece_color = gray
edge = (300,50,400,400) # the coord troubles are happening because edge[2] and edge [3] are NOT the endpoints of a line, but rather width and height of a rect


#always create a clock - use the clock to prevent python  from running the game as many times as it can in a second
fps=60
timer=pygame.time.Clock() 

#create functions to do things outside of the main game loop
def draw_chessboard(edge):
	#drawing an 8/8 grid and making it chequered
	for i in range(8): 
		for j in range(8):
			if (i+j) %2 ==0: 
				chessboard = pygame.draw.rect(screen,white,[j*50 + 300,i*50 + 50, 50,50],0,5)
			else:
				chessboard = pygame.draw.rect(screen,orange,[j*50 + 300,i*50 + 50, 50,50],0,5)
	outside = pygame.draw.rect(screen,dark_gray,(edge),4,5)
		#drawing the outside parameters for showing the notation 
	for i in range(9): 
		if i != 0:
			note = label_font.render(f"{i}",True,dark_gray)
			screen.blit(note,(282,i*50 + 15))
		if i == 8:
			break
		if (i) %2 ==0: 
			chessboard = pygame.draw.rect(screen,white,[275,i*50 + 50, 25,50],0,5)
		else:
			chessboard = pygame.draw.rect(screen,orange,[275,i*50 + 50, 25,50],0,5)
	for i in range(9):
		if i != 0:
			note = label_font.render(f"{i}",True,dark_gray)
			screen.blit(note,(706,i*50 + 15))
		if i == 8:
			break
		if (i) %2 ==0: 
			chessboard = pygame.draw.rect(screen,white,[700,i*50 + 50, 25,50],0,5)
		else:
			chessboard = pygame.draw.rect(screen,orange,[700,i*50 + 50, 25,50],0,5)
	for i in range(8): 
		if i == 8:
			break
		if (i) %2 ==0: 
			chessboard = pygame.draw.rect(screen,white,[i*50 +300,25, 50,25],0,5)
		else:
			chessboard = pygame.draw.rect(screen,orange,[i*50 +300,25, 50,25],0,5)
		letters = ["A","B","C","D","E","F","G","H"] 
		letter = label_font.render(str(letters[i]),True,dark_gray)
		screen.blit(letter,(i*50 + 317,26))
	for i in range(8): 
		if i == 8:
			break
		if (i) %2 ==0: 
			chessboard = pygame.draw.rect(screen,white,[i*50 +300,450, 50,25],0,5)
		else:
			chessboard = pygame.draw.rect(screen,orange,[i*50 +300,450, 50,25],0,5)
		letters = ["A","B","C","D","E","F","G","H",] 
		letter = label_font.render(letters[i],True,dark_gray)
		screen.blit(letter,(i*50 + 317,452))

	fl_corner = pygame.draw.rect(screen,orange,[275,25,25,25],0,5)
	fr_corner = pygame.draw.rect(screen,white,[700,25,25,25],0,5)
	bl_corner = pygame.draw.rect(screen,orange,[275,450,25,25],0,5)
	br_corner = pygame.draw.rect(screen,white,[700,450,25,25],0,5)


def draw_startbtn(start_btn_color):
	start_btn = pygame.draw.rect(screen,start_btn_color,[300,500,200,75],0,5)
	start_text = medium_font.render('Start Game!',True,white)
	screen.blit(start_text,(320,520))
	return start_btn

def collide_check(f_or_h,fhopen,fox_coord):
	global test_color
	if fox_coord[0] -50 >= edge[0]  and fox_coord[1] + 50 <= edge[3] and ((fox_coord[1] + 50 < h1_coord[1]) or (fox_coord[0] -50 > h1_coord[0])): #added brackets within this or statement which seemed to help
		fhopen[0] = True
	else: 
		fhopen[0] = False
		test_color = gold


#use this function to assign true/false values to whether squares around the fox / hounds are open or taken. This can run all the time. Then refer to this for e.g. collidepoints and so on
 

def draw_fox_choices(fox_squares_open):
	#drawing squares where the fox can move
	# if statements block moves from showing on the edge; work this out offline!
	
	#using logic to check if there's collision with the hounds; but there should be a much easier way to find
	# the problem with this logic is that the fox_rect must overlap on BOTH coords, not just the x axis or y axis

	if fox_squares_open[0] == True:
		pygame.draw.rect(screen,fox_piece_color,[fox_fl[0],fox_fl[1],50,50],0,5)
	if fox_squares_open[1] == True:
		pygame.draw.rect(screen,fox_piece_color,[fox_fr[0],fox_fr[1],50,50],0,5)
	if fox_squares_open[2] == True:
		pygame.draw.rect(screen,fox_piece_color,[fox_bl[0],fox_bl[1],50,50],0,5)
	if fox_squares_open[3] == True:
		pygame.draw.rect(screen,fox_piece_color,[fox_br[0],fox_br[1],50,50],0,5)

	#if fox_coord[0] -50 >= edge[0]  and fox_coord[1] + 50 <= edge[3] and ((fox_coord[1] + 50 < h1_coord[1]) or (fox_coord[0] -50 > h1_coord[0])): #added brackets within this or statement which seemed to help
	#	front_left = pygame.draw.rect(screen,fox_piece_color,[(fox_coord[0]) -50,(fox_coord[1]) + 50,50,50],2,5)
	#	global active_foxfl 
	#	active_foxfl = True #note there's currently no place where this is turned back to False
	#	global test_color   
	#	test_color = green
	#if fox_coord[0] +50 < (edge[2] + edge[0]) and fox_coord[1] + 50 < (edge[1]+ edge[3]): 
	#	front_right = pygame.draw.rect(screen,fox_piece_color,[fox_coord[0] +50,fox_coord[1] + 50,50,50],3,5)
	#if fox_coord[0] -50 >=  edge[0]  and  fox_coord[1] - 50 >= edge[1]:
	#	 #global test_color  
	#	 test_color = gold  
	#	 back_left = pygame.draw.rect(screen,fox_piece_color,[fox_coord[0] - 50,fox_coord[1] - 50,50,50],3,5)
	#if fox_coord[0] +50 < (edge[2] + edge[0])  and fox_coord[1] - 50 >= edge[1]:  
	#	back_right = pygame.draw.rect(screen,fox_piece_color,[fox_coord[0] +50,fox_coord[1] - 50,50,50],3,5)

	

def draw_hound_choices(hound_choice,hbl,hbr):
#drawing squares where the hounds can move. Note hounds cannot move backwards
#notw although hounds move 'forwards', by the standard of the board they are moving only backward!
	if hound_choice[0] == True:
		pygame.draw.rect(screen,hound_piece_color,[hbl[0],hbl[1],50,50],0,5)
	if hound_choice[1] == True:
		pygame.draw.rect(screen,hound_piece_color,[hbr[0],hbr[1],50,50],0,5)




	#if hound_coord[0] -50 >=  edge[0]  and  hound_coord[1] - 50 >= edge[1]:
	#	back_left = pygame.draw.rect(screen,hound_piece_color,[hound_coord[0] - 50,hound_coord[1] - 50,50,50],3,5)
	#if hound_coord[0] +50 < (edge[2] + edge[0])  and hound_coord[1] - 50 > edge[1]:  
	#	back_right = pygame.draw.rect(screen,hound_piece_color,[hound_coord[0] +50,hound_coord[1] - 50,50,50],3,5)
	#return back_left, back_right

def hound_move(hound_coord,edge, hound_rect,hound_clicked,hound_piece_color):
	if hound_coord[0] -50 >=  edge[0]  and  hound_coord[1] - 50 >= edge[1]:
		back_left = pygame.draw.rect(screen,hound_piece_color,[hound_coord[0] - 50,hound_coord[1] - 50,50,50],3,5)
		return back_left
		if back_left.collidepoint(event.pos):
			hound_coord = ((hound_coord[0]) -50,(hound_coord[1]) - 50)
			hound_rect = back_left
			hound_clicked = False
			hound_piece_color = gray
		#return hound_coord,hound_rect,hound_clicked
	if hound_coord[0] +50 <= (edge[2] + edge[0])  and hound_coord[1] - 50 >= edge[1]:  
		back_right = pygame.draw.rect(screen,hound_piece_color,[hound_coord[0] +50,hound_coord[1] - 50,50,50],3,5)
		return back_right
		if back_right.collidepoint(event.pos):
			hound_coord = ((hound_coord[0]) +50,(hound_coord[1]) - 50)
			hound_rect = back_right
			hound_clicked = False
			hound_piece_color = gray
	return hound_coord,hound_rect,hound_clicked

def collide_check_new(piece_squares,coord_list, active_sq):
	#to find if the fox has lost, you could save all four sides of a collision check to a list and say hounds_win if all checks are false
	# can you create a list of tuples and loop through them to check for a collision?
		#global collide_color
		#if moving_square == h1_coord:
		#	collide_color = blue
		#else: collide_color = white
	active_sq = []
	collide_color =  white
	for s in piece_squares:
		inner_check = []	
		for c in coord_list: 
			if s == c:
				collide_color = blue
				inner_check.append(True)
			elif s[0] < 300:
				collide_color = blue
				inner_check.append(True)
			elif s[0] >= 700:
				collide_color = blue
				inner_check.append(True)
			elif s[1] < 50:
				collide_color = blue
				inner_check.append(True)
			elif s[1] >= 450:
				collide_color = blue
				inner_check.append(True)
			else: 
				inner_check.append(False)
		if any(inner_check) == True:
				active_sq.append(False)
		else: active_sq.append(True)



	return  collide_color, active_sq


run = True
while run: 
	timer.tick(fps)

	# screen.fill(black)
	screen.blit(background,(0,0))
	pygame.display.set_caption("Fox & Hounds")

	# test_box = pygame.draw.rect(screen, test_color,[1100,500,200,200],0,5) was used for tsting

	# collide_box = pygame.draw.rect(screen,collide_color,[1000,50,150,150],0,5) was used for testing

	coord_list = [fox_coord,h1_coord,h2_coord,h3_coord,h4_coord]

	fox_fl = ((fox_coord[0] - 50),(fox_coord[1] + 50))
	fox_fr = ((fox_coord[0] + 50),(fox_coord[1] + 50))
	fox_bl = ((fox_coord[0] - 50),(fox_coord[1] - 50))
	fox_br = ((fox_coord[0] + 50),(fox_coord[1] - 50))
	fox_squares = [fox_fl,fox_fr,fox_bl,fox_br]
	fox_squares_open = [True,True,True,True] 


	#to get the variables out of the function I had to actually call the open_squares and collide_color vars here, no idea why
	collide_color, fox_squares_open = collide_check_new(fox_squares,coord_list,fox_squares_open) #for some reason it works when NOT in the 'if' fox_clicked statement  


	#fox_F1_type = medium_font.render(f"fox_sq_open is {fox_squares_open}",True,white) was used for testingblackscreen.blit(fox_F1_type,(20,600))

	h1_bl = ((h1_coord[0] - 50),(h1_coord[1] - 50))
	h1_br = ((h1_coord[0] + 50),(h1_coord[1] - 50))
	h1_squares = [h1_bl,h1_br]
	h1_squares_open = [True,True]

	collide_color, h1_squares_open = collide_check_new(h1_squares,coord_list,h1_squares_open)

	h2_bl = ((h2_coord[0] - 50),(h2_coord[1] - 50))
	h2_br = ((h2_coord[0] + 50),(h2_coord[1] - 50))
	h2_squares = [h2_bl,h2_br]
	h2_squares_open = [True,True]

	collide_color, h2_squares_open = collide_check_new(h2_squares,coord_list,h2_squares_open) #for some reason it works when NOT in the 'if' fox_clicked statement  

	h3_bl = ((h3_coord[0] - 50),(h3_coord[1] - 50))
	h3_br = ((h3_coord[0] + 50),(h3_coord[1] - 50))
	h3_squares = [h3_bl,h3_br]
	h3_squares_open = [True,True]
	collide_color, h3_squares_open = collide_check_new(h3_squares,coord_list,h3_squares_open)

	h4_bl = ((h4_coord[0] - 50),(h4_coord[1] - 50))
	h4_br = ((h4_coord[0] + 50),(h4_coord[1] - 50))
	h4_squares = [h4_bl,h4_br]
	h4_squares_open = [True,True]

	collide_color, h4_squares_open = collide_check_new(h4_squares,coord_list,h4_squares_open)


	#if fox_fl == h1_coord: #this works when out of a function like this, but collide_check_new func not returning blue for some reason
	#	collide_color = blue


	draw_chessboard(edge)
	start_btn = draw_startbtn(start_btn_color)
	if start_game: 
		start_btn_color = green
	else: 
		start_btn_color = dark_gray

	collide_check(fox,fox_open,fox_coord)

	if fox_turn:
		screen.blit(pygame.transform.scale(fox_orig,(80,80)),(120,20))
	elif hound_turn:
		screen.blit(pygame.transform.scale(hound_orig,(80,80)),(120,20))

	#game winning logic
	if fox_coord[1] >= 400: 
		fox_wins = True
		fox_win_message = medium_font.render("Fox Wins!",True,white)
		screen.blit(fox_win_message,(120,200))
		start_game = False
		hound_turn = False

	if fox_squares_open == [False,False,False,False]:
		hounds_wins = True
		hound_win_message = medium_font.render("Hounds Win!",True,white)
		screen.blit(hound_win_message,(800,200))
		start_game = False

	fox_rect = pygame.draw.rect(screen,fox_piece_color,[fox_coord[0],fox_coord[1],50,50],2,5)
	fox_pos = ((fox_coord[0] + 6),(fox_coord[1] + 6)) #for some reason moving this within the while loop caused the 'F' fox var to move properly
	screen.blit(fox,fox_pos) 
	# remember to enter blit coords as a tuple

	#hound rectangles to follow
	h1_rect = pygame.draw.rect(screen,hound_piece_color,[h1_coord[0],h1_coord[1],50,50],2,5)
	h1_pos = ((h1_coord[0] + 6),(h1_coord[1] + 6))
	screen.blit(hound,h1_pos)

	h2_rect = pygame.draw.rect(screen,hound_piece_color,[h2_coord[0],h2_coord[1],50,50],2,5)
	h2_pos = ((h2_coord[0] + 6),(h2_coord[1] + 6))
	screen.blit(hound,h2_pos)

	h3_rect = pygame.draw.rect(screen,hound_piece_color,[h3_coord[0],h3_coord[1],50,50],2,5)
	h3_pos = ((h3_coord[0] + 6),(h3_coord[1] + 6))
	screen.blit(hound,h3_pos)

	h4_rect = pygame.draw.rect(screen,hound_piece_color,[h4_coord[0],h4_coord[1],50,50],2,5)
	h4_pos = ((h4_coord[0] + 6),(h4_coord[1] + 6))
	screen.blit(hound,h4_pos)

	if fox_clicked:
		draw_fox_choices(fox_squares_open)
		fox_piece_color = gold

	if h1_clicked:
		draw_hound_choices(h1_squares_open,h1_bl,h1_br)
		#hound_piece_color = green
		h2_clicked = False
		h3_clicked = False
		h4_clicked = False
		#can't make this function move right now
		#hound_move(h1_coord,edge,h1_rect,h1_clicked,hound_piece_color)
		

	if h2_clicked:
		draw_hound_choices(h2_squares_open,h2_bl,h2_br)
		#hound_piece_color = green
		h1_clicked = False
		h3_clicked = False
		h4_clicked = False

	if h3_clicked:
		draw_hound_choices(h3_squares_open,h3_bl,h3_br)
		#hound_piece_color = green
		h2_clicked = False
		h1_clicked = False
		h4_clicked = False

	if h4_clicked:
		draw_hound_choices(h4_squares_open,h4_bl,h4_br)
		#hound_piece_color = green
		h2_clicked = False
		h3_clicked = False
		h1_clicked = False

	#this forloop is what allows mouseclicks and other events to happen in-game
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		


			
		#setting actions to be taken when the mousebutton is up - always take this step of mousebutton up vs. down:
		if event.type == pygame.MOUSEBUTTONUP: 

			#starting and stopping the game
			if start_btn.collidepoint(event.pos):
				if start_game:
					start_game = False
					fox_turn = False
					fox_clicked = False
					hound_turn = False
					fox_coord = (450,50)
					h1_coord = (300,400)
					h2_coord = (400,400)
					h3_coord = (500,400)
					h4_coord = (600,400)
				elif not start_game: 
					start_game = True
					fox_clicked = True
					fox_turn = True



			# remember to add logic on what to do if it's already been clicked

			if fox_rect.collidepoint(event.pos) and fox_turn: 
				if fox_clicked:
					fox_clicked = False
					fox_piece_color = gray #any variable you change, must change back!
				elif not fox_clicked: 
					fox_clicked = True

			if fox_clicked:
				#front_right = pygame.draw.rect(screen,black,[fox_coord[0] +50,fox_coord[1] + 50,50,50],1,5) No longer needed
				#back_left = pygame.draw.rect(screen,black,[fox_coord[0] - 50,fox_coord[1] - 50,50,50],1,5)
				#back_right = pygame.draw.rect(screen,black,[fox_coord[0] +50,fox_coord[1] - 50,50,50],1,5)
				if fox_squares_open[0]:
					if pygame.draw.rect(screen,gray,[fox_fl[0],fox_fl[1],50,50],1,5).collidepoint(event.pos):
						fox_coord = ((fox_coord[0]) -50,(fox_coord[1]) + 50)
						fox_clicked = False
						fox_piece_color = gray
						fox_turn = False
						hound_turn = True
						active_foxfl = False
				if fox_squares_open[1]:
					if pygame.draw.rect(screen,gray,[fox_fr[0],fox_fr[1],50,50],1,5).collidepoint(event.pos):
						fox_coord = ((fox_coord[0]) +50,(fox_coord[1]) + 50)
						fox_clicked = False
						fox_piece_color = gray
						fox_turn = False
						hound_turn = True	
						active_foxfl = False
				if fox_squares_open[2]:
					if pygame.draw.rect(screen,gray,[fox_bl[0],fox_bl[1],50,50],1,5).collidepoint(event.pos):
						fox_coord = ((fox_coord[0]) -50,(fox_coord[1]) - 50)
						fox_clicked = False
						fox_piece_color = gray
						fox_turn = False
						hound_turn = True
						active_foxfl = False
				if fox_squares_open[3]:
					if pygame.draw.rect(screen,gray,[fox_br[0],fox_br[1],50,50],1,5).collidepoint(event.pos):
						fox_coord = ((fox_coord[0]) +50,(fox_coord[1]) - 50)
						fox_clicked = False
						fox_piece_color = gray
						fox_turn = False
						hound_turn = True
						active_foxfl = False

			
			if h1_rect.collidepoint(event.pos) and hound_turn:
				if h1_clicked:
					h1_clicked = False
					hound_piece_color = gray
				elif not h1_clicked: 
					h1_clicked = True

			if h1_clicked:
				back_left = pygame.draw.rect(screen,black,[h1_coord[0] - 50,h1_coord[1] - 50,50,50],1,5)
				back_right = pygame.draw.rect(screen,black,[h1_coord[0] +50,h1_coord[1] - 50,50,50],1,5)
				if back_left.collidepoint(event.pos) and h1_squares_open[0]:
					h1_coord = ((h1_coord[0]) -50,(h1_coord[1]) - 50)
					h1_rect = back_left
					h1_clicked = False
					hound_piece_color = gray
					fox_turn = True
					hound_turn = False
				if back_right.collidepoint(event.pos) and h1_squares_open[1]:
					h1_coord = ((h1_coord[0]) +50,(h1_coord[1]) - 50)
					h1_rect = back_right
					h1_clicked = False
					hound_piece_color = gray
					fox_turn = True
					hound_turn = False

			if h2_rect.collidepoint(event.pos) and hound_turn:
				if h2_clicked:
					h2_clicked = False
					hound_piece_color = gray
				elif not h2_clicked: 
					h2_clicked = True

			if h2_clicked:
				back_left = pygame.draw.rect(screen,black,[h2_coord[0] - 50,h2_coord[1] - 50,50,50],1,5)
				back_right = pygame.draw.rect(screen,black,[h2_coord[0] +50,h2_coord[1] - 50,50,50],1,5)
				if back_left.collidepoint(event.pos) and h2_squares_open[0]:
					h2_coord = ((h2_coord[0]) -50,(h2_coord[1]) - 50)
					h2_rect = back_left
					h2_clicked = False
					hound_piece_color = gray
					fox_turn = True
					hound_turn = False
				if back_right.collidepoint(event.pos) and h2_squares_open[1]:
					h2_coord = ((h2_coord[0]) +50,(h2_coord[1]) - 50)
					h2_rect = back_right
					h2_clicked = False
					hound_piece_color = gray
					fox_turn = True
					hound_turn = False


			if h3_rect.collidepoint(event.pos) and hound_turn:
				if h3_clicked:
					h3_clicked = False
					hound_piece_color = gray
				elif not h3_clicked: 
					h3_clicked = True

			if h3_clicked:
				back_left = pygame.draw.rect(screen,black,[h3_coord[0] - 50,h3_coord[1] - 50,50,50],1,5)
				back_right = pygame.draw.rect(screen,black,[h3_coord[0] +50,h3_coord[1] - 50,50,50],1,5)
				if back_left.collidepoint(event.pos) and h3_squares_open[0]:
					h3_coord = ((h3_coord[0]) -50,(h3_coord[1]) - 50)
					h3_rect = back_left and h1_squares_open[0]
					h3_clicked = False
					hound_piece_color = gray
					fox_turn = True
					hound_turn = False
				if back_right.collidepoint(event.pos) and h3_squares_open[1]:
					h3_coord = ((h3_coord[0]) +50,(h3_coord[1]) - 50)
					h3_rect = back_right
					h3_clicked = False
					hound_piece_color = gray
					fox_turn = True
					hound_turn = False


			if h4_rect.collidepoint(event.pos) and hound_turn:
				if h4_clicked:
					h4_clicked = False
					hound_piece_color = gray
				elif not h4_clicked: 
					h4_clicked = True

			if h4_clicked:
				back_left = pygame.draw.rect(screen,black,[h4_coord[0] - 50,h4_coord[1] - 50,50,50],1,5)
				back_right = pygame.draw.rect(screen,black,[h4_coord[0] +50,h4_coord[1] - 50,50,50],1,5)
				if back_left.collidepoint(event.pos) and h4_squares_open[0]:
					h4_coord = ((h4_coord[0]) -50,(h4_coord[1]) - 50)
					h4_rect = back_left
					h4_clicked = False
					hound_piece_color = gray
					fox_turn = True
					hound_turn = False
				if back_right.collidepoint(event.pos) and h4_squares_open[1]:
					h4_coord = ((h4_coord[0]) +50,(h4_coord[1]) - 50)
					h4_rect = back_right
					h4_clicked = False
					hound_piece_color = gray
					fox_turn = True
					hound_turn = False

	pygame.display.update() #this is ESSENTIAL or pygame functions will run and then close

pygame.quit()
sys.exit() # rather than put this within the 'if run = True' statement, drumkit tutorial creates a new variable run and uses turning that to false to exit the game loop