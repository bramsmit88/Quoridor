import pygame
import numpy as np
import matplotlib.path as mplPath


pygame.init()
Display_width = 800
Display_height = 600
gameDisplay = pygame.display.set_mode((Display_width,Display_height))
pygame.display.set_caption('Ninja stok')
clock = pygame.time.Clock()

class Goal1:
    def __init__(self,w,h):
        self.w = w
        self.h = h
        self.y_uplim = Display_height/2+self.h/2
        self.y_downlim = Display_height/2-self.h/2        
        
    def drawme(self):
        pygame.draw.rect(gameDisplay,[100,100,100],(0,Display_height/2-self.h/2,self.w,self.h))

class Goal2:
    def __init__(self,w,h):
        self.w = w
        self.h = h
        self.y_uplim = Display_height/2+self.h/2
        self.y_downlim = Display_height/2-self.h/2
        
    def drawme(self):
        pygame.draw.rect(gameDisplay,[100,100,100],(Display_width-self.w,Display_height/2-self.h/2,self.w,self.h))  
        
class Ball:
    def __init__(self,x,y,vx,vy,r,colour,rho,speeddamper,wallspeeddamper):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.colour = colour #[250,250,250] for white
        self.rho = rho
        A = np.pi*np.square(r)
        self.m = rho * A
        self.speeddamper = speeddamper   #0.99  
        self.wallspeeddamper = wallspeeddamper #0.8
        
    def drawme(self):
        pygame.draw.circle(gameDisplay,self.colour,(np.int(self.x),np.int(self.y)),self.r)
        
    def move(self):
        self.x = self.x+self.vx
        self.y = self.y+self.vy
        self.vx = self.vx*self.speeddamper
        self.vy = self.vy*self.speeddamper
        
    def checkme(self,destructflag):      
        # goal
#        destructflag = False
        if self.x -self.r < 0 and self.y > goal1.y_downlim and self.y< goal1.y_uplim:
            car2.points +=1          
            destructflag = True
        if self.x +self.r > Display_width and self.y > goal2.y_downlim and self.y< goal2.y_uplim:
            car1.points +=1          
            destructflag = True
            
        # collision with cars
        cars = [car1,car2]
        for j in range (0,2):
            car = cars[j]
            contactflag = False
            verts =  [(car.C[0].item(0),car.C[0].item(1)),(car.C[1].item(0),car.C[1].item(1)),(car.C[2].item(0),car.C[2].item(1)),(car.C[3].item(0),car.C[3].item(1)),(0,0)]
            codes= [1, 2, 2, 2, 79 ]
            path = mplPath.Path(verts,codes)
            angle_array = np.linspace(0,2*np.pi,5)  
            contactangle_list = [];
            for i in range (0,len(angle_array)):
                angle = angle_array[i]
                if path.contains_point((self.x+self.r*np.cos(angle),self.y+self.r*np.sin(angle))):             
                    contactangle_list.append(angle)
                    contactflag = True
                    break
            if contactflag:
                angle = np.arctan2(np.sum(np.sin(contactangle_list)),np.sum(np.cos(contactangle_list)))  
                L = np.array([car.x-self.x, car.y-self.y]).reshape(2,1)
                L_loc = R_t(car.th)*L
                L_abs = np.sqrt(np.square(car.x - self.x)+np.square(car.y - self.y)) 
                
                vx_car_atimpact = car.vx + L_abs*car.vth
                vy_car_atimpact = car.vy + L_abs*car.vth
                Dvx_self = vx_car_atimpact * car.m / self.m     
                Dvy_self = vy_car_atimpact * car.m / self.m 
                Dv = np.sqrt(np.square(Dvx_self)+np.square(Dvy_self))
                
                self.vx = 0.1*self.vx + Dvx_self + Dv*-np.cos(-angle)
                self.vy = 0.1*self.vy + Dvy_self + Dv*np.sin(-angle)
                car.vx = car.vx -0.5*self.m/car.m*(self.vx)
                car.vy = car.vy -0.5*self.m/car.m*(self.vy)
                if L_loc.item(1)  !=  0:
                    car.vth = 0.01 * L_loc.item(0)/L_loc.item(1) * Dv
        
        # collision with boundaries
        if self.x-self.r < 0:
            self.x = self.x+10
            self.vx = -self.vx*self.wallspeeddamper #0.8
        if self.x+self.r > Display_width:
            self.x = self.x -10
            self.vx = -self.vx*self.wallspeeddamper
        if self.y-self.r < 0:
            self.y = self.y + 10
            self.vy = -self.vy*self.wallspeeddamper
        if self.y+self.r > Display_height:
            self.y = self.y -10
            self.vy = -self.vy*self.wallspeeddamper
        
        return destructflag
class Car:
    def __init__(self,points, x, y,th, vx ,vy, vth, w, h, colour, C, rho, speeddampertrans, speeddamperrot, wallspeeddamper,v_increase_trans, v_increase_rot):
        self.points = points        
        self.x =x
        self.y =y
        self.th = th
        self.vx = vx
        self.vy = vy
        self.vth = vth
        self.w = w
        self.h = h 
        self.colour = colour #[0,250,50] for green
        self.C = C
        self.rho = rho
        A = w*h
        self.m = rho * A
        self.speeddampertrans = speeddampertrans #0.98
        self.speeddamperrot = speeddamperrot    # 0.95
        self.wallspeeddamper = wallspeeddamper # 0.4
        self.v_increase_trans = v_increase_trans #0.5
        self.v_increase_rot = v_increase_rot #0.01
        
    def checkme(self):
        destructflag = False
        x = self.x
        y = self.y
        th = self.th
        vx = self.vx
        vy = self.vy
        vth = self.vth
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_r]:
            vth = vth-self.v_increase_rot
        if pressed[pygame.K_t]:
            vth = vth + self.v_increase_rot
        if pressed[pygame.K_w]:
            vy = vy-self.v_increase_trans
        if pressed[pygame.K_s]:
           vy = vy+self.v_increase_trans
        if pressed[pygame.K_a]:
            vx = vx-self.v_increase_trans
        if pressed[pygame.K_d]:
            vx = vx+self.v_increase_trans
        
        if pressed[pygame.K_ESCAPE]:
            destructflag = True
            
        C1 = np.array([x+vx,y+vy]).reshape(2,1)+ R(th+vth)*np.array([-self.w/2,-self.h/2]).reshape(2,1)
        C2 = np.array([x+vx,y+vy]).reshape(2,1)+ R(th+vth)*np.array([-self.w/2,self.h/2]).reshape(2,1)
        C3 = np.array([x+vx,y+vy]).reshape(2,1)+ R(th+vth)*np.array([self.w/2,self.h/2]).reshape(2,1)
        C4 = np.array([x+vx,y+vy]).reshape(2,1)+ R(th+vth)*np.array([self.w/2,-self.h/2]).reshape(2,1)
        
        # in case of collision with wall
        if C1[0]<0 or C2[0]<0 or C3[0]<0 or C4[0]<0:
            vth = -self.vth*0.4
            vx = -self.vx *0.4
        if C1[0]>Display_width or C2[0]>Display_width or C3[0]>Display_width or C4[0]>Display_width:
            vth = -self.vth*0.4
            vx = -self.vx *0.4
        if C1[1]<0 or C2[1]<0 or C3[1]<0 or C4[1]<0:
            vth = -self.vth*0.4
            vy = -self.vy *0.4
        if C1[1]>Display_height or C2[1]>Display_height or C3[1]>Display_height or C4[1]>Display_height:
            vth = -self.vth*0.4
            vy = -self.vy *0.4
            
        self.vx = vx
        self.vy = vy
        self.vth = vth
        self.C = (C1,C2,C3,C4)
        return destructflag    
    
    def move(self):
        self.x = self.x+self.vx
        self.y = self.y+self.vy
        self.th = self.th+self.vth
        self.vx = self.vx*self.speeddampertrans
        self.vy = self.vy*self.speeddampertrans
        self.vth = self.vth*self.speeddamperrot
        
    def drawme(self):        
        pygame.draw.polygon(gameDisplay,self.colour,self.C)
        
class Car2:
    def __init__(self,points, x, y,th, vx ,vy, vth, w, h, colour, C, rho, speeddampertrans, speeddamperrot, wallspeeddamper,v_increase_trans, v_increase_rot):
        self.points = points        
        self.x =x
        self.y =y
        self.th = th
        self.vx = vx
        self.vy = vy
        self.vth = vth
        self.w = w
        self.h = h 
        self.colour = colour #[0,250,50] for green
        self.C = C
        self.rho = rho
        A = w*h
        self.m = rho * A
        self.speeddampertrans = speeddampertrans #0.98
        self.speeddamperrot = speeddamperrot    # 0.95
        self.wallspeeddamper = wallspeeddamper # 0.4
        self.v_increase_trans = v_increase_trans #0.5
        self.v_increase_rot = v_increase_rot #0.01
   
    def processReward(self,ball1,goal1,state,best_action,Qmax):
        Qtable = []
        Rew = []
        return Qtable,Rew
    def checkme(self,car,ball,Qtable, goal):
        x = self.x
        y = self.y
        th = self.th
        vx = self.vx
        vy = self.vy
        vth = self.vth
        
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_COMMA]:
            vth = vth-self.v_increase_rot
        if pressed[pygame.K_PERIOD]:
            vth = vth + self.v_increase_rot
        if pressed[pygame.K_UP]:
            vy = vy-self.v_increase_trans
        if pressed[pygame.K_DOWN]:
           vy = vy+self.v_increase_trans
        if pressed[pygame.K_LEFT]:
            vx = vx-self.v_increase_trans
        if pressed[pygame.K_RIGHT]:
            vx = vx+self.v_increase_trans
            
        C1 = np.array([x+vx,y+vy]).reshape(2,1)+ R(th+vth)*np.array([-self.w/2,-self.h/2]).reshape(2,1)
        C2 = np.array([x+vx,y+vy]).reshape(2,1)+ R(th+vth)*np.array([-self.w/2,self.h/2]).reshape(2,1)
        C3 = np.array([x+vx,y+vy]).reshape(2,1)+ R(th+vth)*np.array([self.w/2,self.h/2]).reshape(2,1)
        C4 = np.array([x+vx,y+vy]).reshape(2,1)+ R(th+vth)*np.array([self.w/2,-self.h/2]).reshape(2,1)
        
        # in case of collision with wall
        if C1[0]<0 or C2[0]<0 or C3[0]<0 or C4[0]<0:
            vth = -self.vth*0.4
            vx = -self.vx *0.4
        if C1[0]>Display_width or C2[0]>Display_width or C3[0]>Display_width or C4[0]>Display_width:
            vth = -self.vth*0.4
            vx = -self.vx *0.4
        if C1[1]<0 or C2[1]<0 or C3[1]<0 or C4[1]<0:
            vth = -self.vth*0.4
            vy = -self.vy *0.4
        if C1[1]>Display_height or C2[1]>Display_height or C3[1]>Display_height or C4[1]>Display_height:
            vth = -self.vth*0.4
            vy = -self.vy *0.4
            
        self.vx = vx
        self.vy = vy
        self.vth = vth
        self.C = (C1,C2,C3,C4)
        
        Qtable2=[]
        state=[]
        best_action=[]
        Qmax=[]
        return Qtable2,state,best_action,Qmax
    
    def move(self,action):
        self.x = self.x+self.vx
        self.y = self.y+self.vy
        self.th = self.th+self.vth
        self.vx = self.vx*self.speeddampertrans
        self.vy = self.vy*self.speeddampertrans
        self.vth = self.vth*self.speeddamperrot
        
    def drawme(self):        
        pygame.draw.polygon(gameDisplay,self.colour,self.C)

class Car_cpu:
    def __init__(self,points, x, y,th, vx ,vy, vth, w, h, colour, C, rho, speeddampertrans, speeddamperrot, wallspeeddamper,v_increase_trans, v_increase_rot,Qtable):
        self.points = points        
        self.x =x
        self.y =y
        self.th = th
        self.vx = vx
        self.vy = vy
        self.vth = vth
        self.w = w
        self.h = h 
        self.colour = colour #[0,250,50] for green
        self.C = C
        self.rho = rho
        A = w*h
        self.m = rho * A
        self.speeddampertrans = speeddampertrans #0.98
        self.speeddamperrot = speeddamperrot    # 0.95
        self.wallspeeddamper = wallspeeddamper # 0.4
        self.v_increase_trans = v_increase_trans #0.5
        self.v_increase_rot = v_increase_rot #0.01
        self.Qtable = Qtable
        self.a = 0.9 #learning rate
        self.g = 0.9 #discount factor
        
    def checkme(self,car, ball,Qtable, goal):
        x = self.x
        y = self.y
        th = self.th
        vx = self.vx
        vy = self.vy
        vth = self.vth
        
        # NOG FOUT: moet ook x,y,th uitkomen:
        state,best_action,Qmax  = self.select_bestaction(ball)      
        
        C1 = np.array([x+vx,y+vy]).reshape(2,1)+ R(th+vth)*np.array([-self.w/2,-self.h/2]).reshape(2,1)
        C2 = np.array([x+vx,y+vy]).reshape(2,1)+ R(th+vth)*np.array([-self.w/2,self.h/2]).reshape(2,1)
        C3 = np.array([x+vx,y+vy]).reshape(2,1)+ R(th+vth)*np.array([self.w/2,self.h/2]).reshape(2,1)
        C4 = np.array([x+vx,y+vy]).reshape(2,1)+ R(th+vth)*np.array([self.w/2,-self.h/2]).reshape(2,1)
        
        # in case of collision with wall
        if C1[0]<0 or C2[0]<0 or C3[0]<0 or C4[0]<0:
            vth = -self.vth*0.4
            vx = -self.vx *0.4
        if C1[0]>Display_width or C2[0]>Display_width or C3[0]>Display_width or C4[0]>Display_width:
            vth = -self.vth*0.4
            vx = -self.vx *0.4
        if C1[1]<0 or C2[1]<0 or C3[1]<0 or C4[1]<0:
            vth = -self.vth*0.4
            vy = -self.vy *0.4
        if C1[1]>Display_height or C2[1]>Display_height or C3[1]>Display_height or C4[1]>Display_height:
            vth = -self.vth*0.4
            vy = -self.vy *0.4
            
        self.vx = vx
        self.vy = vy
        self.vth = vth
        self.C = (C1,C2,C3,C4)
        
        return Qtable,state,best_action,Qmax
    
    def select_bestaction(self,ball):
        state = self.getState(ball,7) 
#        print state[0]
#        Q_array         = np.zeros(7)
        Q_array         = np.zeros(2)

#        xBall           = np.zeros(7)
#        yBall           = np.zeros(7)
#        vxBall          = np.zeros(7)
#        vxSelf           = np.zeros(7)
#        vySelf           = np.zeros(7)
#        vthSelf          = np.zeros(7)        
#        reward_array    = np.zeros(7)
#        for action in range(0,7):
        for action in range(0,2):
            nextstate = self.getState(ball,action)
            Q_array[action]     = Qtable[nextstate][action]    

        Qmax = max(Q_array)
        Qmax_ind = np.argwhere(Q_array==np.amax(Q_array))
        Qmax_ind = Qmax_ind.flatten()
        randomint = np.random.randint(len(Qmax_ind))        
        best_action = Qmax_ind[randomint]
        
#        if Q_array[0]==Q_array[1]==Q_array[2]==Q_array[3]==Q_array[4]==Q_array[5]:
#            best_action =  np.random.randint(0,7)
#        else:
#            best_action = np.argmax(Q_array)
      
#        vth = self.vth
#        vx = self.vx
#        vy = self.vy
#        vth = vthSelf[best_action]
#        vx = vxSelf[best_action]
#        vy = vySelf[best_action]
        
#        print vth
#        Qtable = Qtable
        return state,best_action,Qmax
        
    def processReward(self,ball,goal,state,best_action,Qmax)    :
        reward = self.getReward(ball.x,ball.y,ball.vx,goal)
        Qtable[state][best_action] = Qtable[state][best_action] + self.a*(reward+self.g*Qmax-Qtable[state][best_action])
        return Qtable,reward
        
    def getState(self, ball, action)  :
        Dvx = 0
        Dvy = 0
        Dvth= 0
        taketimestep = 1
        #ACTIONS
        # left
        # right
        # up
        # down
        # CCW
        # CW
        # do nothing
        if action == 0:
            Dvx = -self.v_increase_trans
        if action == 1:
            Dvx = self.v_increase_trans
        if action == 2:
            Dvy = -self.v_increase_trans
        if action == 3:
            Dvy = self.v_increase_trans
        if action == 4:
            Dvth = -self.v_increase_rot
        if action == 5:
            Dvth = self.v_increase_rot
        if action ==7:
            taketimestep = 0
      
        x_max = Display_width
        y_max = Display_height
        vx_max = 17
        vy_max = 16
        vth_max = 0.19
        
        if self.x+(self.vx+Dvx)*taketimestep>= 4*x_max/5:
            x_self = 4
        elif self.x+(self.vx+Dvx)*taketimestep > 3*x_max/5:
            x_self = 3
        elif self.x +(self.vx+Dvx)*taketimestep>2*x_max/5:
            x_self = 2
        elif self.x+(self.vx+Dvx)*taketimestep > x_max/5:
            x_self = 1
        else:
            x_self = 0
            
        if ball.x+ball.vx*taketimestep>= 4*x_max/5:
            x_ball = 4
        elif ball.x+ball.vx*taketimestep > 3*x_max/5:
            x_ball = 3
        elif ball.x+ball.vx*taketimestep >2*x_max/5:
            x_ball = 2
        elif ball.x+ball.vx*taketimestep > x_max/5:
            x_ball = 1
        else:
            x_ball = 0
            
        if self.y+(self.vy+Dvy)*taketimestep>= 4*y_max/5:
            y_self = 4
        elif self.y+(self.vy+Dvy)*taketimestep > 3*y_max/5:
            y_self = 3
        elif self.y+(self.vy+Dvy)*taketimestep >2*y_max/5:
            y_self = 2
        elif self.y+(self.vy+Dvy)*taketimestep > y_max/5:
            y_self = 1
        else:
            y_self = 0
            
        if ball.y+ball.vx*taketimestep>= 4*y_max/5:
            y_ball = 4
        elif ball.y+ball.vx*taketimestep > 3*y_max/5:
            y_ball = 3
        elif ball.y+ball.vx*taketimestep >2*y_max/5:
            y_ball = 2
        elif ball.y+ball.vx*taketimestep > y_max/5:
            y_ball = 1
        else:
            y_ball = 0  

        if np.sin(self.th+(self.vth+Dvth)*taketimestep)>0.5:
            th_self = 4
        elif np.sin(self.th+(self.vth+Dvth)*taketimestep) > 0:
            th_self = 3
        elif np.sin(self.th+(self.vth+Dvth)*taketimestep) == 0:
            th_self = 2
        elif np.sin(self.th+(self.vth+Dvth)*taketimestep) <-0.5:
            th_self = 0
        else:
            th_self = 1 
            
        if self.vx + Dvx*taketimestep>= vx_max/2: # wrong: damping not included
            vx_self = 4
        elif self.vx  + Dvx*taketimestep> 0:
            vx_self = 3
        elif self.vx + Dvx*taketimestep == 0:
            vx_self = 2
        elif self.vx + Dvx*taketimestep <-vx_max/2:
            vx_self = 0
        else:
            vx_self = 1 

        if self.vy + Dvy*taketimestep>= vy_max/2:# wrong: damping not included
            vy_self = 4
        elif self.vy + Dvy*taketimestep> 0:
            vy_self = 3
        elif self.vy + Dvy*taketimestep== 0:
            vy_self = 2
        elif self.vy + Dvy*taketimestep<-vx_max/2:
            vy_self = 0
        else:
            vy_self = 1 

        if ball.vx >= vx_max/2: # wrong: damping not included
            vx_ball = 4
        elif ball.vx > 0:
            vx_ball = 3
        elif ball.vx == 0:
            vx_ball = 2
        elif ball.vx <-vx_max/2:
            vx_ball = 0
        else:
            vx_ball = 1 

        if ball.vy>= vy_max/2: # wrong: damping not included
            vy_ball = 4
        elif ball.vy > 0:
            vy_ball= 3
        elif ball.vy == 0:
            vy_ball = 2
        elif ball.vy <-vx_max/2:
            vy_ball= 0
        else:
            vy_ball = 1 
            
        if self.vth + Dvth*taketimestep>= vth_max/2: # wrong: damping not included
            vth_self = 4
        elif self.vth + Dvth*taketimestep> 0:
            vth_self = 3
        elif self.vth + Dvth*taketimestep == 0:
            vth_self = 2
        elif self.vth + Dvth*taketimestep <-vth_max/2:
            vth_self = 0
        else:
            vth_self = 1  
            
#        state= vth_self + th_self*5 + vy_ball*np.power(5,2) + vy_self*np.power(5,3) + y_ball*np.power(5,4) + y_self*np.power(5,5) + vx_ball*np.power(5,6) + vx_self*np.power(5,7) +  x_ball*np.power(5,8)+x_self*np.power(5,9)
        state = x_self-x_ball
        return state#, ball.x, ball.y, ball.vx, vx_self, vy_self, vth_self

    
    def getReward(self,ball_x, ball_y, ball_vx, goal):
#        if ball_x < 0 and ball_y > goal.y_downlim and ball_y< goal.y_uplim:
#            R= 100
#        elif ball_vx == 0:
#            R = 0
#        else:
#            R = -ball_vx
#        return R
#        R = Display_width-self.x
        if self.x == ball_x:
            R = 100
        else:
            R = 100/abs(self.x-ball_x)
        return R
            
    def move(self,action):
                #ACTIONS
        # left
        # right
        # up
        # down
        # CCW
        # CW
        # do nothing
        vx = self.vx
        vy = self.vy
        vth = self.vth
        
        if action == 0:
            vx = vx-self.v_increase_trans
        if action == 1:
            vx = vx+self.v_increase_trans 
        if action == 2:
            vy = vy-self.v_increase_trans
        if action == 3:
           vy = vy+self.v_increase_trans
        if action == 4:
            vth = vth-self.v_increase_rot
        if action == 5:
            vth = vth + self.v_increase_rot

       
        
        self.x = self.x+vx
        self.y = self.y+vy
        self.th = self.th+vth
        self.vx = self.vx*self.speeddampertrans
        self.vy = self.vy*self.speeddampertrans
        self.vth = self.vth*self.speeddamperrot
        
    def drawme(self):        
        pygame.draw.polygon(gameDisplay,self.colour,self.C)        
def R(th):
    rotmat = np.matrix([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    return rotmat

def R_t(th):
    rotmat = np.matrix([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    rotmat = rotmat.transpose()
    return rotmat
    
def spawnall(points1, points2, player1,player2,Qtable):
#    Qtable = np.array([])
    if player1 == 'human':
        car1 = Car(points1,100,300,0,0,0,0,15,150,[0,250,50],[],1,0.98,0.95,0.4,0.5,0.01)
    if player2 == 'human': 
        car2 = Car2(points2,Display_width-100,300,0,0,0,0,15,150,[250,250,0],[],1,0.98,0.95,0.4,0.5,0.01)
    else:

        #STATES
        # self.x
        # ball.x
        # self.vx
        # ball.vx
        # self.y
        # ball.y
        # self.vy
        # ball.vy
        # self.th
        # self.vth
        

        
        car2 = Car_cpu(points2,Display_width-100,300,0,0,0,0,15,150,[250,250,0],[],1,0.98,0.95,0.4,0.5,0.01,Qtable)
    ball1 = Ball(400,250,0,0,10,[250,250,250],5,0.99,0.8)
    goal1 = Goal1(10,100)
    goal2 = Goal2(10,100)
    return car1,car2,ball1,goal1,goal2,Qtable

def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()
###############################################################################
quitrequested = False 
player1 = 'human'   
player2 = 'human'
#Nactions = 7
Nactions = 2
#Nstates = np.power(5,10)
Nstates = np.power(5,2)
Qtable = np.zeros((Nstates,Nactions))
#Qtable = np.load('/home/bram/Desktop/savetest.npy')
car1,car2,ball1,goal1,goal2,Qtable2 = spawnall(0,0,player1,player2,Qtable)
largeText = pygame.font.Font('freesansbold.ttf',80)

while not quitrequested:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitrequested = True
   
    gameDisplay.fill( (0,0,0) ) # fill with background colour

    destructflag = car1.checkme()
    Qtable2,state,best_action,Qmax  = car2.checkme(car1,ball1,Qtable2,goal1)
    destructflag                    = ball1.checkme(destructflag)  
        
    car1.move()
    car2.move(best_action)
    
    Qtable2,Rew = car2.processReward(ball1,goal1,state,best_action,Qmax)
#    print car2.x, Rew
    ball1.move()
#    
    TextSurf1, TextRect1 = text_objects(str(car1.points), largeText,car1.colour)
    TextRect1.center = ((Display_width/4),50)
    gameDisplay.blit(TextSurf1, TextRect1)
    
    TextSurf2, TextRect2 = text_objects(str(car2.points), largeText,car2.colour)
    TextRect2.center = ((3*Display_width/4),50)
    gameDisplay.blit(TextSurf2, TextRect2)
    
    
    car1.drawme()
    car2.drawme()
    ball1.drawme()
    goal1.drawme()
    goal2.drawme()
    
#    print np.amin(Qtable2), np.amax(Qtable2)
#    print best_action
    if destructflag:
        points1 = car1.points
        points2 = car2.points
        del car1
        del ball1
        car1, car2, ball1, goal1, goal2, Qtable2 = spawnall(points1,points2, player1,player2,Qtable2)
        
    pygame.display.update()
    clock.tick(50) #in fps
np.save('/home/bram/Desktop/savetest',Qtable2)   
pygame.quit()
#quit() # to quit python to: use in stand alone script (not in Spyder)