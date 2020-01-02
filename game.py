# ---------------------------- imports
import sys, pygame
import pygame.gfxdraw
from pygame.locals import*
import random
import numpy as np

# ---------------------------- shapes
#  numpy arrays of different shapes and their rotations

S = np.array([[1,0,0,0],  #0:4 (no rotation)
             [1,0,0,0],
             [1,0,0,0],
             [1,0,0,0],

             [1,1,1,1], #4:8 (after 1 rotation)
             [0,0,0,0],
             [0,0,0,0],
             [0,0,0,0],

             [0,0,1,0], #8:12 (after 2 rotations)
             [0,0,1,0],
             [0,0,1,0],
             [0,0,1,0],

             [0,0,0,0], #12:16 (after 3 rotations)
             [0,0,0,0],
             [1,1,1,1],
             [0,0,0,0]


             ])
Box = np.array([[0,0,0,0],
               [0,1,1,0],
               [0,1,1,0],
               [0,0,0,0],

               [0,0,0,0],
               [0,1,1,0],
               [0,1,1,0],
               [0,0,0,0],

               [0,0,0,0],
               [0,1,1,0],
               [0,1,1,0],
               [0,0,0,0],

               [0,0,0,0],
               [0,1,1,0],
               [0,1,1,0],
               [0,0,0,0]])
L = np.array([[1,1,0,0],
             [0,1,0,0],
             [0,1,0,0],
             [0,0,0,0],

             [0,0,1,0],
             [1,1,1,0],
             [0,0,0,0],
             [0,0,0,0],

             [0,1,0,0],
             [0,1,0,0],
             [0,1,1,0],
             [0,0,0,0],

             [0,0,0,0],
             [1,1,1,0],
             [1,0,0,0],
             [0,0,0,0]
             ])
EgyptS = np.array([[1,0,0,0],
                  [1,1,0,0],
                  [0,1,0,0],
                  [0,0,0,0],

                  [0,1,1,0],
                  [1,1,0,0],
                  [0,0,0,0],
                  [0,0,0,0],

                  [0,1,0,0],
                  [0,1,1,0],
                  [0,0,1,0],
                  [0,0,0,0],

                  [0,0,0,0],
                  [0,1,1,0],
                  [1,1,0,0],
                  [0,0,0,0]])
T = np.array([[0,1,0,0],
             [1,1,1,0],
             [0,0,0,0],
             [0,0,0,0],

             [0,1,0,0],  #(0,1)   x = c
             [0,1,1,0],   #(1,1)
             [0,1,0,0],  #(1,2)
             [0,0,0,0],   #(2,1)

             [0,0,0,0],
             [1,1,1,0],
             [0,1,0,0],
             [0,0,0,0],

             [0,1,0,0],
             [1,1,0,0],
             [0,1,0,0],
             [0,0,0,0]])
J = np.array([[0,1,1,0],
             [0,1,0,0],
             [0,1,0,0],
             [0,0,0,0],

             [0,0,0,0],
             [1,1,1,0],
             [0,0,1,0],
             [0,0,0,0],

             [0,1,0,0],
             [0,1,0,0],
             [1,1,0,0],
             [0,0,0,0],

             [1,0,0,0],
             [1,1,1,0],
             [0,0,0,0],
             [0,0,0,0]])
Z = np.array([[0,1,0,0],
             [1,1,0,0],
             [1,0,0,0],
             [0,0,0,0],

             [1,1,0,0],
             [0,1,1,0],
             [0,0,0,0],
             [0,0,0,0],

             [0,0,1,0],
             [0,1,1,0],
             [0,1,0,0],
             [0,0,0,0],

             [0,0,0,0],
             [1,1,0,0],
             [0,1,1,0],
             [0,0,0,0]]
            )

# ... a) dictionary of the shapes
pieces = {'S': S,
         'B': Box,
         'L': L,
         'ES': EgyptS,
         'T': T,
         'J': J,
         'Z': Z}
# ... b) generates a random piece (used in drawing-> used to draw what piece comes next)
pieceTypes = ['S','B','L','ES','T','J','Z']
randomPiece = pieceTypes[random.randint(0,len(pieceTypes)-1)]
piece, arr = random.choice(list(pieces.items()))

# ---------------------------- game stuff
# ... a) lists
current = [] #this is a list of the current rectangles needed to be drawn


# ... b) movement: true if arrow key associated with button is pressed
right_key = False
left_key = False
down_key = False
rotate = False
firstPiece = True
moving = True
xVal = [0,0,0,0]
yVal = [0,0,0,0]

# ... c) colors
background = (99,187,196) #background color

# ... d) display
size = width, height = 650,800 #sets width & height
screen = pygame.display.set_mode(size)

# ... e) board
board = {}
for row in range (0,10): #initially sets every spot on board as empty
   for col in range(0,20):
       board[(row,col)] = 0
#board[(3,0)] = 1

def createPiece(shape,start,end):
   """
   :param shape: gets what shape it is.(ex: shape S) Then, get the numpy array of what
           corresponds to the dictionary.
   :param start: starting location of numpy array
   :param end: ending location of numpy array
          > use start & end to acquire the correct rotation of each shape.
          > ex: start,end (0,4) = initial rotation
   :return: (function)
           1. creation gets dictionary value = gets appropriate shape & rotation
           2. 2 for loops = goes through numpy array and looks for values of 1
           3. If value == 1, then that means that it's 1 rectangle out of the total
           shape
           4. Adds each rectangle into the current list. Current list = current
           rectangles needed to draw
           5. Complete: current list is updated with necessary shape & rotation
           for drawing
   """
   # globals
   global current
   global firstPiece
   global x,y

   subX = 0
   subY = 0
   # start
   creation = pieces[shape][start:end]

   if firstPiece is True:
       for r in range(0,4):
           for c in range(0,4):
               if(creation[c][r]==1):
                   current.append(pygame.Rect(r*40,c*40,40,40))
                   firstPiece = False
   else:
       print("XV",xVal)
       print("YV",yVal)
       del current[:]
       for r in range(0,4):
           for c in range(0,4):
               if(creation[c][r]==1):
                   #if(r<xVal[r]):
                       #x = xVal[r]-r
                   #print(r,"-",xVal[r],'=',xVal[r]-r,"c",c,)
                   print("r",xVal[r],"c",xVal[c])
                   if(xVal[c]>c):
                       subX = xVal[c]-c
                   else:
                       subX = c-xVal[c]
                   if(yVal[r]>r):
                       subY = yVal[r]-r
                   else:
                       subY = r-yVal[r]

                   current.append(pygame.Rect((subX*40)+r*40,subY*40+c*40,40,40))
               #current.append(pygame.Rect(((xVal[c]-c)*40)+r*40,+c*40,40,40))
                   #current.append(pygame.Rect(r*40+(xVal[r]*40),c*40+(yVal[c]),40,40))
                   #current.append(pygame.Rect((r*40)+(xVal[c]*40),(c*40)+(yVal[c]*40),40,40))
       print("NEW", current)
""""
   for r in range(0,4):
       for c in range(0,4):
           if(creation[c][r]==1):
               if firstPiece is True:
                   current.append(pygame.Rect(r*40,c*40,40,40))
                   firstPiece = False
               else:
                   #rotate
                   del current[:]
                   current.append(pygame.Rect((r*40)+1,c*40,40,40))
"""


   #print("x: ",x)
   #print("nop")


def drawPiece(rectList):
   """
   :param rectList: gets the current list of rectangles
   :return: 1. goes through rectList
            2. draws every rectangle in the list
   """
   for x in rectList:
       pygame.draw.rect(screen,(0,0,0),x,0) #filled rectangle
       pygame.draw.rect(screen,(255,255,255),x,1) #outline of rectangle

   pygame.display.update()
   pygame.display.flip()

def bounds(rectList,dir):
   """
   (function): -checks to make sure if you can move to the right, left, or down
               -makes sure you don't go out of bounds of the board
   :param rectList: Current list of rectangles
   :param dir: Direction going (right, left, down)
   :return: 1. goes through rectList
            2. find the direction the player wants to go
            3. for every rectangle, adds or subtracts x's or y's
            > +/- in order to see if you +/- (if you were to move right for ex.)
            and go out of bounds
            > if you do go out of bounds, return false
            > return false: player is out of bounds | movement invalid
            > return true: player is not out of bounds | movement can occur
   """
   for x in range(0,len(rectList)):
       if(dir==1): #right
           if((rectList[x][0]+40)>360):
               return False
       elif(dir==2): #left
           if((rectList[x][0]-40)<0):
               return False
       elif(dir==3): #down
           if((rectList[x][1]+40)>760):
               return False
   return True

def move(rectList):
   """
   :param rectList: current list
   :param og: X
   :return: returns updated list of rectangles to draw
   """

   #globals
   global right_key
   global left_key
   global down_key
   global current
   #global xVal
   #global yVal
   global rotate

   #start
   for x in range(0,len(rectList)):
       if(right_key is True):
           rectList[x][0] = ((rectList[x][0])+40)
           current[x] = (pygame.Rect(rectList[x][0],rectList[x][1],40,40))
       elif(down_key is True):
           rectList[x][1] = ((rectList[x][1])+40)
           current[x] = (pygame.Rect(rectList[x][0],rectList[x][1],40,40))
       elif(left_key is True):
           rectList[x][0] = ((rectList[x][0])-40)
           current[x] = (pygame.Rect(rectList[x][0],rectList[x][1],40,40))
          
   if rotate is True:



       print((rectList),"lll")
       #y=[1,2,3,4]
       for test in range(0,len(rectList)):
           xVal[test] = (rectList[test][0]/40)
           yVal[test] = (rectList[test][1]/40)

       #createPiece('L',4,8)
       createPiece('S',0,4)   
       drawPiece(current)
       rotate = False




   #updates x's & y's


   right_key = False
   down_key = False

def nextPiece(shape):

   next = pieces[shape][0:4]
   for r in range(0,4):
       for c in range(0,4):
           if(next[c][r]==1):
               if(shape=='S'):
                   pygame.draw.rect(screen,(0,0,0),(r*40+510,c*40+135,40,40),0)
                   pygame.draw.rect(screen,(255,255,255),(r*40+510,c*40+135,40,40),1)
               elif(shape=='B'):
                   pygame.draw.rect(screen,(0,0,0),(r*40+452,c*40+135,40,40),0)
                   pygame.draw.rect(screen,(255,255,255),(r*40+452,c*40+135,40,40),1)
               elif(shape=='L'):
                   pygame.draw.rect(screen,(0,0,0),(r*40+490,c*40+155,40,40),0)
                   pygame.draw.rect(screen,(255,255,255),(r*40+490,c*40+155,40,40),1)
               elif(shape=='ES'):
                   pygame.draw.rect(screen,(0,0,0),(r*40+490,c*40+155,40,40),0)
                   pygame.draw.rect(screen,(255,255,255),(r*40+490,c*40+155,40,40),1)
               elif(shape=='T'):
                   pygame.draw.rect(screen,(0,0,0),(r*40+475,c*40+170,40,40),0)
                   pygame.draw.rect(screen,(255,255,255),(r*40+475,c*40+170,40,40),1)
               elif(shape=='J'):
                   pygame.draw.rect(screen,(0,0,0),(r*40+460,c*40+155,40,40),0)
                   pygame.draw.rect(screen,(255,255,255),(r*40+460,c*40+155,40,40),1)
               elif(shape=='Z'):
                   pygame.draw.rect(screen,(0,0,0),(r*40+490,c*40+155,40,40),0)
                   pygame.draw.rect(screen,(255,255,255),(r*40+490,c*40+155,40,40),1)

def placed(rectList):
   global board
   global firstPiece
   global current
   global moving

   #for x in range(0,(len(rectList)-1)):
   for x in rectList:
       pygame.draw.rect(screen,(0,0,0),x,0) #filled rectangle
       pygame.draw.rect(screen,(255,255,255),x,1)
       #board[(rectList[x][0],rectList[x][1])] = 1

   firstPiece = True
   del current[:]
   createPiece(randomPiece,0,4)
   moving = True








def main():
   pygame.init()

   run_Game()

def run_Game():
   #globals
   global current
   global screen
   global piece

   global down_key
   global right_key
   global left_key

   global x
   global y
   global rotate
   global moving

   game = 'pause'

   #spawns piece originally
   #createPiece(randomPiece,0,4)
   #createPiece('L',0,4)
   createPiece('S',0,4)
   clock = pygame.time.Clock()
   falltime = 0
   fallspeed = .27

   movedelay = 200

   while 1:

       if(game == 'pause'):
           screen.fill((99,187,196))
           font = pygame.font.SysFont('Century Gothic',55, True, False)
           pause = font.render("Press 'S' to start",True,(0,0,0))
           screen.blit(pause,[130,350])
           for event in pygame.event.get(pygame.KEYDOWN):
               if event.key == pygame.K_s:
                   game = 'playing'
           pygame.display.update()

       else:




           #if falltime/1000 > fallspeed:
            #   falltime = 0
             #  falltime+=clock.get_rawtime()

           #"""
           if(bounds(current,3) is True):
               for x in range(0,len(current)):
                   current[x][1]+=40
                   drawPiece(current)
           else:
               moving = False
               placed(current)
               #print("end")
           #wait 0.4 seconds
           #"""

           """"
           for x in range(0,len(current)):
               if(current[x][1])
           """



           #keyboard listener
           for event in pygame.event.get():
               if event.type == pygame.QUIT: sys.exit()
               elif event.type == KEYDOWN:
                   if event.key == pygame.K_UP:
                       rotate = True


                       move(current)
                       #print("rotate")
                   elif event.key == pygame.K_DOWN:
                       if(bounds(current,3) is True and moving is True):

                           down_key = True
                           move(current)

                           drawPiece(current)
                           #print(current)
                       else:
                           moving = False
                   elif event.key == pygame.K_RIGHT:
                       if(bounds(current,1) is True and moving is True):

                           right_key = True
                           move(current)
                           drawPiece(current)
                   elif event.key == pygame.K_LEFT:
                       if(bounds(current,2) is True and moving is True):
                           left_key = True
                           move(current)
                           drawPiece(current)
                   elif event.key == pygame.K_SPACE:
                       print("TBA")
                       movedelay = 10

           pygame.time.delay(movedelay)

                       # make it drop faster





           #draws initial spawned piece
           drawPiece(current)



           # v i s u a l
           screen.fill((99,187,196)) #background fill
           #... a) draws grid on background
           for row in range(0,10):
               for col in range(0,20):
                   pygame.draw.rect(screen,(219,219,219),(row*40,col*40,40,40),1)

                   if(board[row,col]==1):
                       pygame.draw.rect(screen,(0,0,0),(row*40,col*40,40,40),0)
                       pygame.draw.rect(screen,(255,255,255),(row*40,col*40,40,40),1)

           #... b) draws next piece box
           pygame.gfxdraw.rectangle(screen,(430,120,200,200),(255,255,255))
           #nextPiece(piece)
           nextPiece('Z')
           font = pygame.font.SysFont('Calibri',25, True, False)
           Next_text = font.render("Next piece:",True,(0,0,0))
           screen.blit(Next_text,[460,90])

           #pygame.draw.rect(screen,(0,0,0),(0,0,40,40),0)
   pygame.display.update()

if __name__ == '__main__':
   main()


