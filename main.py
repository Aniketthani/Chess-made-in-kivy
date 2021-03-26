from kivy.config import Config
Config.set('graphics', 'resizable', False)

from kivy.core.window import Window
Window.size=(700,700)



from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color,Rectangle

from kivy.uix.image import Image 
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.label import Label



class pawn(Button):
    def __init__(self,color="white",**kwargs):
        super(pawn,self).__init__(**kwargs)
        if color=="white":
            self.img="images/wpawn.png"
            
        else:
            self.img="images/bpawn.png"
            
        self.tex=Image(source=self.img).texture
        self.color=(1,1,1,1)


        self.background_color=(0,0,0,0)
        
        
        with self.canvas.after:
            Color(*self.color)
            Rectangle(size=(self.size[0]/3,self.size[1]),pos=(self.pos[0]+self.size[0]/3,self.pos[1]),texture=self.tex)
    
    def update_texture(self):
        self.canvas.after.clear()
        


        self.background_color=(0,0,0,0)
        with self.canvas.after:
            Color(*self.color)
            Rectangle(size=(self.size[0]/3,self.size[1]),pos=(self.pos[0]+self.size[0]/3,self.pos[1]),texture=self.tex)
        
        

    def calculate_next_move(self,color):
        if color=="w":
            self.next_moves=[(self.pos[0],(self.pos[1] - self.parent.height/8) ),(self.pos[0] + self.parent.width/8,self.pos[1]-self.parent.height/8),(self.pos[0] - self.parent.width/8,self.pos[1]-self.parent.height/8) ]
        else:
            self.next_moves=[(self.pos[0],(self.pos[1] + self.parent.height/8) ),(self.pos[0] + self.parent.width/8,self.pos[1]+self.parent.height/8),(self.pos[0] - self.parent.width/8,self.pos[1]+self.parent.height/8) ]
        
        for i in range(len(self.next_moves)):
            if self.next_moves[i][0]<self.parent.pos[0] or self.next_moves[i][0]>(self.parent.width - self.size[0]):
                self.next_moves[i]=(None,None)
            
            elif self.next_moves[i][1]<self.parent.pos[1] or self.next_moves[i][1]>(self.parent.height-self.size[1]):
                self.next_moves[i]=(None,None)
        
        #checking for availability of attack moves
        rel_coords=self.parent.abs_to_rel_pos(self.next_moves[1])

        if rel_coords!=(None,None):

            if self.parent.grid[rel_coords[0]][rel_coords[1]]==0 or (( color=="w" and self.parent.grid[rel_coords[0]][rel_coords[1]]>0) or ( color=="b" and  self.parent.grid[rel_coords[0]][rel_coords[1]]<0)):
                self.next_moves[1]=(None,None)
        
        rel_coords=self.parent.abs_to_rel_pos(self.next_moves[2])

        if rel_coords!=(None,None): 
            if self.parent.grid[rel_coords[0]][rel_coords[1]]==0 or (( color=="w" and self.parent.grid[rel_coords[0]][rel_coords[1]]>0) or ( color=="b" and  self.parent.grid[rel_coords[0]][rel_coords[1]]<0)):
                self.next_moves[2]=(None,None)
        
        #checking for availability of normal move
        rel_coords=self.parent.abs_to_rel_pos(self.next_moves[0])

        if rel_coords!=(None,None):
            if self.parent.grid[rel_coords[0]][rel_coords[1]] !=0:
                self.next_moves[0]=(None,None)

        

        return self.next_moves

class camel(Button):
    def __init__(self,color="white",**kwargs):
        super(camel,self).__init__(**kwargs)
        if color=="white":
            self.img="images/wcamel.png"
            
        else:
            self.img="images/bcamel.png"
            
        self.tex=Image(source=self.img).texture
        self.color=(1,1,1,1)

        self.background_color=(0,0,0,0)

        with self.canvas.after:
            Color(*self.color)
            Rectangle(size=(self.size[0]/3,self.size[1]),pos=(self.pos[0]+self.size[0]/3,self.pos[1]),texture=self.tex)

    def update_texture(self):
        self.canvas.after.clear()
        


        self.background_color=(0,0,0,0)
        with self.canvas.after:
            Color(*self.color)
            Rectangle(size=(self.size[0]/3,self.size[1]),pos=(self.pos[0]+self.size[0]/3,self.pos[1]),texture=self.tex)
    
    def calculate_next_move(self,color):
        x=self.pos[0]
        y=self.pos[1]

        w=self.width
        h=self.height

        self.next_moves=[]
        i=0
        sub_counter=0
        #moving in NE
        while(x<=self.parent.width-2*w and y<=self.parent.height-2*h):
            i+=1
            x+=w
            y+=h
            self.next_moves.append((x,y))
        
        self.check_availability_of_moves(0,i,color)
        sub_counter=i

        x=self.pos[0]
        y=self.pos[1]

        #moving in NW
        while(x>=w and y<=self.parent.height-2*h):
            i+=1
            x=x-w
            y=y+h
            self.next_moves.append((x,y))
        
        self.check_availability_of_moves(sub_counter,i,color)
        sub_counter=i

        x=self.pos[0]
        y=self.pos[1]

        #moving in SW
        while(x>=w and y>=h):
            i+=1
            x=x-w
            y=y-h
            self.next_moves.append((x,y))

        self.check_availability_of_moves(sub_counter,i,color)
        sub_counter=i

        x=self.pos[0]
        y=self.pos[1]

        #moving in SE
        while(x<=self.parent.width-2*w and y>=h):
            i+=1
            x=x+w
            y=y-h
            self.next_moves.append((x,y))
        
        self.check_availability_of_moves(sub_counter,i,color)

        return self.next_moves

    def check_availability_of_moves(self,start,end,color):
        
        if color=="b":
            for k in range(start,end):
                if self.next_moves[k]!=(None,None):
                    coords=self.parent.abs_to_rel_pos(self.next_moves[k])
                    if self.parent.grid[coords[0]][coords[1]]<0:
                        self.next_moves[k]=(None,None)
                        for j in range(k+1,end):
                            self.next_moves[j]=(None,None)
                        break
                    if self.parent.grid[coords[0]][coords[1]]>0:
                         for j in range(k+1,end):
                             self.next_moves[j]=(None,None)
        elif color=="w":
            for k in range(start,end):
                if self.next_moves[k]!=(None,None):
                    coords=self.parent.abs_to_rel_pos(self.next_moves[k])

                    if self.parent.grid[coords[0]][coords[1]]>0:
                        self.next_moves[k]=(None,None)
                        for j in range(k+1,end):
                            self.next_moves[j]=(None,None)
                        break
                    if self.parent.grid[coords[0]][coords[1]]<0:
                         for j in range(k+1,end):
                             self.next_moves[j]=(None,None)
        
class horse(Button):
    def __init__(self,color="white",**kwargs):
        super(horse,self).__init__(**kwargs)
        if color=="white":
            self.img="images/whorse.png"
            
        else:
            self.img="images/bhorse.png"
            
        self.tex=Image(source=self.img).texture
        self.color=(1,1,1,1)

        self.background_color=(0,0,0,0)

        with self.canvas.after:
            Color(*self.color)
            Rectangle(size=(self.size[0]/3,self.size[1]),pos=(self.pos[0]+self.size[0]/3,self.pos[1]),texture=self.tex)

    def update_texture(self):
        self.canvas.after.clear()
        


        self.background_color=(0,0,0,0)
        with self.canvas.after:
            Color(*self.color)
            Rectangle(size=(self.size[0]/3,self.size[1]),pos=(self.pos[0]+self.size[0]/3,self.pos[1]),texture=self.tex)

    def calculate_next_move(self,color):
        x=self.pos[0]
        y=self.pos[1]
        w=self.width
        h=self.height
        #[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        self.next_moves=[(x+2*w,y+h),(x+2*w,y-h),(x-2*w,y+h),(x-2*w,y-h),(x+w,y+2*h),(x+w,y-2*h),(x-w,y+2*h),(x-w,y-2*w)] 

        for i in range(len(self.next_moves)):
            if self.next_moves[i][0]<self.parent.pos[0] or self.next_moves[i][0]>(self.parent.width - self.size[0]):
                self.next_moves[i]=(None,None)
            
            elif self.next_moves[i][1]<self.parent.pos[1] or self.next_moves[i][1]>(self.parent.height-self.size[1]):
                self.next_moves[i]=(None,None)

        #check availability of moves
        if color=="b":
            for i in range(len(self.next_moves)):
                if self.next_moves[i]!=(None,None):
                    coords=self.parent.abs_to_rel_pos(self.next_moves[i])

                    if self.parent.grid[coords[0]][coords[1]] <0:
                        self.next_moves[i]=(None,None)
        elif color=="w":
            
            for i in range(len(self.next_moves)):
                if self.next_moves[i]!=(None,None):
                    coords=self.parent.abs_to_rel_pos(self.next_moves[i])

                    if self.parent.grid[coords[0]][coords[1]] >0:
                        self.next_moves[i]=(None,None)
                    
        
        return self.next_moves

    

class elephant(Button):
    def __init__(self,color="white",**kwargs):
        super(elephant,self).__init__(**kwargs)
        if color=="white":
            self.img="images/welephant.png"
            
        else:
            self.img="images/belephant.png"
            
        self.tex=Image(source=self.img).texture
        self.color=(1,1,1,1)
        self.background_color=(0,0,0,0)
        with self.canvas.after:
            Color(*self.color)
            Rectangle(size=(self.size[0]/3,self.size[1]),pos=(self.pos[0]+self.size[0]/3,self.pos[1]),texture=self.tex)
    def update_texture(self):
        self.canvas.after.clear()
        


        self.background_color=(0,0,0,0)
        with self.canvas.after:
            Color(*self.color)
            Rectangle(size=(self.size[0]/3,self.size[1]),pos=(self.pos[0]+self.size[0]/3,self.pos[1]),texture=self.tex)
    def calculate_next_move(self,color):
        x=self.pos[0]
        y=self.pos[1]

        w=self.size[0]
        h=self.size[1]

        self.next_moves=[]

        i=0
        sub_counter=0
        #moving vertically up
        while(y<=self.parent.height-2*h):
            i+=1
            y+=h
            self.next_moves.append((self.pos[0],y))
        
        self.check_availability_of_moves(0,i,color)
        sub_counter=i
        
        #moving vertically down
        y=self.pos[1]

        while(y>=h):
            i+=1
            y=y-h
            self.next_moves.append((self.pos[0],y))
        
        self.check_availability_of_moves(sub_counter,i,color)
        sub_counter=i
        
        
        #moving horizontally right

        while(x<=self.parent.width-2*w):
            i+=1
            x+=w
            self.next_moves.append((x,self.pos[1]))
        self.check_availability_of_moves(sub_counter,i,color)
        sub_counter=i

        #moving horizontally left
        x=self.pos[0]
        while(x>=w):
            i+=1
            x=x-w
            self.next_moves.append((x,self.pos[1]))    
        self.check_availability_of_moves(sub_counter,i,color)

        return self.next_moves

    
    def check_availability_of_moves(self,start,end,color):
        
        if color=="b":
            for k in range(start,end):
                if self.next_moves[k]!=(None,None):
                    coords=self.parent.abs_to_rel_pos(self.next_moves[k])
                    if self.parent.grid[coords[0]][coords[1]]<0:
                        self.next_moves[k]=(None,None)
                        for j in range(k+1,end):
                            self.next_moves[j]=(None,None)
                        break
                    if self.parent.grid[coords[0]][coords[1]]>0:
                         for j in range(k+1,end):
                             self.next_moves[j]=(None,None)
        elif color=="w":
            for k in range(start,end):
                if self.next_moves[k]!=(None,None):
                    coords=self.parent.abs_to_rel_pos(self.next_moves[k])

                    if self.parent.grid[coords[0]][coords[1]]>0:
                        self.next_moves[k]=(None,None)
                        for j in range(k+1,end):
                            self.next_moves[j]=(None,None)
                        break
                    if self.parent.grid[coords[0]][coords[1]]<0:
                         for j in range(k+1,end):
                             self.next_moves[j]=(None,None)

class king(Button):
    def __init__(self,color="white",**kwargs):
        super(king,self).__init__(**kwargs)
        if color=="white":
            self.img="images/wking.png"
            
        else:
            self.img="images/bking.png"
            
        self.tex=Image(source=self.img).texture
        self.color=(1,1,1,1)
        self.background_color=(0,0,0,0)
        with self.canvas.after:
            Color(*self.color)
            Rectangle(size=(self.size[0]/3,self.size[1]),pos=(self.pos[0]+self.size[0]/3,self.pos[1]),texture=self.tex)
    def update_texture(self):
        self.canvas.after.clear()
        


        self.background_color=(0,0,0,0)
        with self.canvas.after:
            Color(*self.color)
            Rectangle(size=(self.size[0]/3,self.size[1]),pos=(self.pos[0]+self.size[0]/3,self.pos[1]),texture=self.tex)
    def calculate_next_move(self,color):
        x=self.pos[0]
        y=self.pos[1]
        h=self.height
        w=self.width

        if color=="w":
            self.next_moves=[(x,y -h ),(x + w,y-h),(x - w,y-h),(x + w,y+h),(x - w,y+h),(x,y+h),(x+w,y),(x-w,y) ]
        else:
            self.next_moves=[(x,y+h ),(x + w,y+h),(x - w,y+h),(x,y-h ),(x + w,y-h),(x - w,y-h),(x+w,y),(x-w,y)  ]
        
        for i in range(len(self.next_moves)):
            if self.next_moves[i][0]<self.parent.pos[0] or self.next_moves[i][0]>(self.parent.width - self.size[0]):
                self.next_moves[i]=(None,None)
            
            elif self.next_moves[i][1]<self.parent.pos[1] or self.next_moves[i][1]>(self.parent.height-self.size[1]):
                self.next_moves[i]=(None,None)

        #check availability of moves
        if color=="b":
            for i in range(len(self.next_moves)):
                if self.next_moves[i]!=(None,None):
                    coords=self.parent.abs_to_rel_pos(self.next_moves[i])

                    if self.parent.grid[coords[0]][coords[1]] <0:
                        self.next_moves[i]=(None,None)
        elif color=="w":
            
            for i in range(len(self.next_moves)):
                if self.next_moves[i]!=(None,None):
                    coords=self.parent.abs_to_rel_pos(self.next_moves[i])

                    if self.parent.grid[coords[0]][coords[1]] >0:
                        self.next_moves[i]=(None,None)
        
        return self.next_moves

class queen(Button):
    def __init__(self,color="white",**kwargs):
        super(queen,self).__init__(**kwargs)
        if color=="white":
            self.img="images/wqueen.png"
            
        else:
            self.img="images/bqueen.png"
        
        self.tex=Image(source=self.img).texture
        self.color=(1,1,1,1)
        self.background_color=(0,0,0,0)
        with self.canvas.after:
            Color(*self.color)
            Rectangle(size=(self.size[0]/3,self.size[1]),pos=(self.pos[0]+self.size[0]/3,self.pos[1]),texture=self.tex)

    def update_texture(self):
        self.canvas.after.clear()
        


        self.background_color=(0,0,0,0)
        with self.canvas.after:
            Color(*self.color)
            Rectangle(size=(self.size[0]/3,self.size[1]),pos=(self.pos[0]+self.size[0]/3,self.pos[1]),texture=self.tex)

    def calculate_next_move(self,color):
        x=self.pos[0]
        y=self.pos[1]

        w=self.size[0]
        h=self.size[1]

        self.next_moves=[]
        i=0
        sub_counter=0
        #moving vertically up
        while(y<=self.parent.height-2*h):
            i+=1
            y+=h
            self.next_moves.append((self.pos[0],y))

        self.check_availability_of_moves(0,i,color)
        sub_counter=i

        #moving vertically down
        y=self.pos[1]

        while(y>=h):
            i+=1
            y=y-h
            self.next_moves.append((self.pos[0],y))
        
        self.check_availability_of_moves(sub_counter,i,color)
        sub_counter=i

        #moving horizontally right
        while(x<=self.parent.width-2*w):
            i+=1
            x+=w
            self.next_moves.append((x,self.pos[1]))
        
        self.check_availability_of_moves(sub_counter,i,color)
        sub_counter=i

        #moving horizontally left
        x=self.pos[0]
        while(x>=w):
            i+=1
            x=x-w
            self.next_moves.append((x,self.pos[1]))
        
        self.check_availability_of_moves(sub_counter,i,color)
        sub_counter=i
        
        x=self.pos[0]
        y=self.pos[1]
        #moving in NE
        while(x<=self.parent.width-2*w and y<=self.parent.height-2*h):
            i+=1
            x+=w
            y+=h
            self.next_moves.append((x,y))
        
        self.check_availability_of_moves(sub_counter,i,color)
        sub_counter=i

        x=self.pos[0]
        y=self.pos[1]

        #moving in NW
        while(x>=w and y<=self.parent.height-2*h):
            i+=1
            x=x-w
            y=y+h
            self.next_moves.append((x,y))

        self.check_availability_of_moves(sub_counter,i,color)
        sub_counter=i
        
        x=self.pos[0]
        y=self.pos[1]

        #moving in SW
        while(x>=w and y>=h):
            i+=1
            x=x-w
            y=y-h
            self.next_moves.append((x,y))
        
        self.check_availability_of_moves(sub_counter,i,color)
        sub_counter=i

        x=self.pos[0]
        y=self.pos[1]

        #moving in SE
        while(x<=self.parent.width-2*w and y>=h):
            i+=1
            x=x+w
            y=y-h
            self.next_moves.append((x,y))
        
        self.check_availability_of_moves(sub_counter,i,color)
        

        return self.next_moves
    
    def check_availability_of_moves(self,start,end,color):
        
        if color=="b":
            for k in range(start,end):
                if self.next_moves[k]!=(None,None):
                    coords=self.parent.abs_to_rel_pos(self.next_moves[k])
                    if self.parent.grid[coords[0]][coords[1]]<0:
                        self.next_moves[k]=(None,None)
                        for j in range(k+1,end):
                            self.next_moves[j]=(None,None)
                        break
                    if self.parent.grid[coords[0]][coords[1]]>0:
                         for j in range(k+1,end):
                             self.next_moves[j]=(None,None)
        elif color=="w":
            for k in range(start,end):
                if self.next_moves[k]!=(None,None):
                    coords=self.parent.abs_to_rel_pos(self.next_moves[k])

                    if self.parent.grid[coords[0]][coords[1]]>0:
                        self.next_moves[k]=(None,None)
                        for j in range(k+1,end):
                            self.next_moves[j]=(None,None)
                        break
                    if self.parent.grid[coords[0]][coords[1]]<0:
                         for j in range(k+1,end):
                             self.next_moves[j]=(None,None)



class Root(Screen):
    def __init__(self,**kwargs):
        super(Root,self).__init__(**kwargs)
        self.name="root"
        self.size_hint=(1,1 )
        self.size=Window.size
        with self.canvas.before:
            for r in range(8):
                for c in range(8):
                    if r%2!=0:
                        if c%2==0:
                            Color(0,0,0,1)
                            
                        else:
                            Color(1,1,1,1)
                        
                    else:
                        if c%2==0:
                            Color(1,1,1,1)
                        else:
                            Color(0,0,0,1)

                    Rectangle(size=(self.width/8,self.height/8),pos=(c*(self.width/8),r*(self.height/8)))
        self.place_objects()
        self.maintain_grid()
        self.moves_available=[]
        self.obj_on_focus=None
        self.last_played_by=None
        
        
        

    def maintain_grid(self):
        self.grid=[[0,0,0,0,0,0,0,0] for i in range(8) ]
        #Initializing Black Side
        self.grid[0][0]=-1 #left elephant
        self.grid[0][1]=-2 #left horse  
        self.grid[0][2]=-3 #left camel
        self.grid[0][3]=-4 #king
        self.grid[0][4]=-5 #queen
        self.grid[0][5]=-6 #right camel 
        self.grid[0][6]=-7 #right horse 
        self.grid[0][7]=-8 #right elephant

        self.grid[1][0]=-11 #pawns  
        self.grid[1][1]=-12 #pawns   
        self.grid[1][2]=-13 #pawns 
        self.grid[1][3]=-14 #pawns 
        self.grid[1][4]=-15 #pawns 
        self.grid[1][5]=-16 #pawns 
        self.grid[1][6]=-17 #pawns
        self.grid[1][7]=-18 #pawns 

        #Initializing White Side
        self.grid[7][0]=1 #elephant
        self.grid[7][1]=2 #horse  
        self.grid[7][2]=3 #camel
        self.grid[7][3]=5 #queen
        self.grid[7][4]=4 #king
        self.grid[7][5]=6 #camel 
        self.grid[7][6]=7 #horse 
        self.grid[7][7]=8 #elephant

        self.grid[6][0]=11 #pawns  
        self.grid[6][1]=12 #pawns   
        self.grid[6][2]=13 #pawns 
        self.grid[6][3]=14 #pawns 
        self.grid[6][4]=15 #pawns 
        self.grid[6][5]=16 #pawns 
        self.grid[6][6]=17 #pawns
        self.grid[6][7]=18 #pawns
    
        self.blackmaping={"-1":"le","-2":"lh","-3":"lc","-4":"k","-5":"q","-6":"rc","-7":"rh","-8":"re","-11":"p1","-12":"p2","-13":"p3","-14":"p4","-15":"p5","-16":"p6","-17":"p7","-18":"p8"}
        self.whitemaping={"1":"le","2":"lh","3":"lc","4":"k","5":"q","6":"rc","7":"rh","8":"re","11":"p1","12":"p2","13":"p3","14":"p4","15":"p5","16":"p6","17":"p7","18":"p8"}
    def abs_to_rel_pos(self,coords):
        if coords==(None,None):
            return coords
        coords=(coords[0]/(self.width/8), coords[1]/(self.height/8))
        coords=(round(coords[0]),round(coords[1]))
        temp=coords[:]
        coords=(temp[1],temp[0])

        return coords




    def place_objects(self):
        #placing the pawns
        self.player_white={'p1':None,'p2':None,'p3':None,'p4':None,'p5':None,'p6':None,'p7':None,'p8':None,'le':None,'re':None,'lc':None,'rc':None,'lh':None,'rh':None,'k':None,'q':None}
        self.player_black={'p1':None,'p2':None,'p3':None,'p4':None,'p5':None,'p6':None,'p7':None,'p8':None,'le':None,'re':None,'lc':None,'rc':None,'lh':None,'rh':None,'k':None,'q':None}

        #Black side

        self.player_black['p1']=pawn(color="black",pos=(0,self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("p1","b"))
        self.player_black['p2']=pawn(color="black",pos=(self.width/8,self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("p2","b"))
        self.player_black['p3']=pawn(color="black",pos=(2*self.width/8,self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("p3","b"))
        self.player_black['p4']=pawn(color="black",pos=(3*self.width/8,self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("p4","b"))
        self.player_black['p5']=pawn(color="black",pos=(4*self.width/8,self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("p5","b"))
        self.player_black['p6']=pawn(color="black",pos=(5*self.width/8,self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("p6","b"))
        self.player_black['p7']=pawn(color="black",pos=(6*self.width/8,self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("p7","b"))
        self.player_black['p8']=pawn(color="black",pos=(7*self.width/8,self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("p8","b"))
        
        self.player_black['le']=elephant(color="black",pos=(0,0),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("le","b"))
        self.player_black['re']=elephant(color="black",pos=(7*self.width/8,0),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("re","b"))

        self.player_black['lh']=horse(color="black",pos=(self.width/8,0),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("lh","b"))
        self.player_black['rh']=horse(color="black",pos=(6*self.width/8,0),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("rh","b"))

        self.player_black['lc']=camel(color="black",pos=(2*self.width/8,0),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("lc","b"))
        self.player_black['rc']=camel(color="black",pos=(5*self.width/8,0),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("rc","b"))

        self.player_black['k']=king(color="black",pos=(3*self.width/8,0),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("k","b"))
        self.player_black['q']=queen(color="black",pos=(4*self.width/8,0),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("q","b"))
        
        self.add_widget(self.player_black['p1'])     
        self.add_widget(self.player_black['p2'])
        self.add_widget(self.player_black['p3'])
        self.add_widget(self.player_black['p4'])
        self.add_widget(self.player_black['p5'])
        self.add_widget(self.player_black['p6'])
        self.add_widget(self.player_black['p7'])
        self.add_widget(self.player_black['p8'])

        self.add_widget(self.player_black['le'])
        self.add_widget(self.player_black['re'])

        self.add_widget(self.player_black['lh'])
        self.add_widget(self.player_black['rh'])

        self.add_widget(self.player_black['lc'])
        self.add_widget(self.player_black['rc'])

        self.add_widget(self.player_black['k'])
        self.add_widget(self.player_black['q'])

        

        #White side

        self.player_white['p1']=pawn(pos=(0,6*self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("p1","w"))
        self.player_white['p2']=pawn(pos=(self.width/8,6*self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("p2","w"))
        self.player_white['p3']=pawn(pos=(2*self.width/8,6*self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("p3","w"))
        self.player_white['p4']=pawn(pos=(3*self.width/8,6*self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("p4","w"))
        self.player_white['p5']=pawn(pos=(4*self.width/8,6*self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("p5","w"))
        self.player_white['p6']=pawn(pos=(5*self.width/8,6*self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("p6","w"))
        self.player_white['p7']=pawn(pos=(6*self.width/8,6*self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("p7","w"))
        self.player_white['p8']=pawn(pos=(7*self.width/8,6*self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("p8","w"))
        
        self.player_white['le']=elephant(pos=(0,7*self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("le","w"))
        self.player_white['re']=elephant(pos=(7*self.width/8,7*self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("re","w"))

        self.player_white['lh']=horse(pos=(self.width/8,7*self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("lh","w"))
        self.player_white['rh']=horse(pos=(6*self.width/8,7*self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("rh","w"))

        self.player_white['lc']=camel(pos=(2*self.width/8,7*self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("lc","w"))
        self.player_white['rc']=camel(pos=(5*self.width/8,7*self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("rc","w"))

        self.player_white['k']=king(pos=(4*self.width/8,7*self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("k","w"))
        self.player_white['q']=queen(pos=(3*self.width/8,7*self.height/8),size=(self.width/8,self.height/8),size_hint=(None,None ),on_press=lambda x:self.callback("q","w"))
        
        self.add_widget(self.player_white['p1'])     
        self.add_widget(self.player_white['p2'])
        self.add_widget(self.player_white['p3'])
        self.add_widget(self.player_white['p4'])
        self.add_widget(self.player_white['p5'])
        self.add_widget(self.player_white['p6'])
        self.add_widget(self.player_white['p7'])
        self.add_widget(self.player_white['p8'])

        self.add_widget(self.player_white['le'])
        self.add_widget(self.player_white['re'])

        self.add_widget(self.player_white['lh'])
        self.add_widget(self.player_white['rh'])

        self.add_widget(self.player_white['lc'])
        self.add_widget(self.player_white['rc'])

        self.add_widget(self.player_white['k'])
        self.add_widget(self.player_white['q'])

    def callback(self,obj,color):
        if color=="w":
            next_moves=self.player_white[obj].calculate_next_move(color=color)
            self.moves_available=next_moves
            self.obj_on_focus=self.player_white[obj]
            
            self.canvas.after.clear()
            

            with self.canvas.after:
                Color(1,0.8,0,0.5)
                Rectangle(size=(self.width/8,self.height/8),pos=self.player_white[obj].pos)
            for i in next_moves:
                if i !=(None,None):
                    with self.canvas.after:
                        Color(0,1,1,0.5)
                        Rectangle(pos=i,size=(self.width/8,self.height/8))
        else:
            next_moves=self.player_black[obj].calculate_next_move(color=color)
            self.moves_available=next_moves
            self.obj_on_focus=self.player_black[obj]
            self.canvas.after.clear()
            

            with self.canvas.after:
                Color(1,0.8,0,0.5)
                Rectangle(size=(self.width/8,self.height/8),pos=self.player_black[obj].pos)
            for i in next_moves:
                if i !=(None,None):
                    with self.canvas.after:
                        Color(0,1,1,0.5)
                        Rectangle(pos=i,size=(self.width/8,self.height/8))
    

    def on_touch_down(self,touch):
        def transform(x,sidelength):
            return (x - (x%sidelength))

        coords=(transform(touch.x,self.width/8),transform(touch.y,self.height/8))
        
        rel_coords=self.abs_to_rel_pos(coords)
        
       

        
            

        

        if self.grid[rel_coords[0]][rel_coords[1]]!=0 and  (self.moves_available==[]or (coords not in self.moves_available)) :
            if self.grid[rel_coords[0]][rel_coords[1]]>0:
                if self.last_played_by=="White":
                    return
                self.callback(self.whitemaping[str(self.grid[rel_coords[0]][rel_coords[1]])],"w")

            else:
                if self.last_played_by=="Black":
                    return
                self.callback(self.blackmaping[str(self.grid[rel_coords[0]][rel_coords[1]])],"b")
            

        if coords in self.moves_available and self.obj_on_focus :

            if self.grid[rel_coords[0]][rel_coords[1]]!=0:
                if self.grid[rel_coords[0]][rel_coords[1]]>0:
                    self.player_white[self.whitemaping[str(self.grid[rel_coords[0]][rel_coords[1]])]].canvas.after.clear()
                    self.remove_widget(self.player_white[self.whitemaping[str(self.grid[rel_coords[0]][rel_coords[1]])]])
                    self.grid[rel_coords[0]][rel_coords[1]]=0
                else:
                    self.player_black[self.blackmaping[str(self.grid[rel_coords[0]][rel_coords[1]])]].canvas.after.clear()
                    self.remove_widget(self.player_black[self.blackmaping[str(self.grid[rel_coords[0]][rel_coords[1]])]])
                    self.grid[rel_coords[0]][rel_coords[1]]=0
            
            rel_coords_of_obj=self.abs_to_rel_pos(self.obj_on_focus.pos)
            #updating the last_played_by variable 

            if self.grid[rel_coords_of_obj[0]][rel_coords_of_obj[1]] <0:
                self.last_played_by="Black"
            else:
                self.last_played_by="White"
            
            self.obj_on_focus.pos=coords
            
            self.obj_on_focus.update_texture()
            
            
            self.grid[rel_coords[0]][rel_coords[1]]=self.grid[rel_coords_of_obj[0]][rel_coords_of_obj[1]]
            
            self.grid[rel_coords_of_obj[0]][rel_coords_of_obj[1]]=0

            #clear canvas.after , empty the available_moves and empty the obj_on_focus
            self.moves_available=[]
            self.obj_on_focus=None
            self.canvas.after.clear()

            objs=self.children
            if self.player_white["k"] not in objs:
                self.gameover(won_by="Black")
            elif self.player_black["k"] not in objs:
                self.gameover(won_by="White")

    def gameover(self,won_by):
        
        
        self.parent.goverscreen.ids.game_over_mess.text=f"{won_by} Won"
        self.parent.current="gameoverscreen"


            
class play_screen(Screen):
    def __init__(self, **kwargs):
        super(play_screen,self).__init__(**kwargs)
        self.name="playscreen"
               
    def play(self,*args):
        self.parent.current="root"

class game_over_screen(Screen):
    def __init__(self, **kwargs):
        super(game_over_screen,self).__init__(**kwargs)
        self.name="gameoverscreen"

    def play_again(self,*args):
        self.parent.remove_widget(self.parent.mainscreen)
        self.parent.mainscreen=Root()
        self.parent.add_widget(self.parent.mainscreen)
        self.parent.current="root"  
                   

class MyApp(App):
    def build(self):
        #screenmanager
        
        sm=ScreenManager()
        sm.mainscreen=Root()
        sm.add_widget(sm.mainscreen)
       
        sm.add_widget(play_screen())
        sm.goverscreen=game_over_screen()
        sm.add_widget(sm.goverscreen)
        sm.current="playscreen"
        return sm

if __name__=="__main__":
   
   MyApp().run()