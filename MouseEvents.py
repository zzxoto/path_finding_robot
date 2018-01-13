from GraphicModels import *
from Settings import *


class MousePosition:
    def __init__(self):
        self.x = None
        self.y = None

    def get_mouse_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        self.x, self.y = mouse_pos[0], mouse_pos[1]

class MouseAction(MousePosition):
    def __init__(self, block):
        '''
        @param block, Objects that are inherited from type Block
        '''
        super().__init__()
        self.block = block
        self.active_state = False

    def click_event(self):
        if self.active_state:
            self.get_mouse_pos()
            self.block.pos.x = self.x
            self.block.pos.y = self.y
            self.active_state = False
            return self.block

    def hover_event(self):
        if self.active_state:
            self.get_mouse_pos()
            self.block.pos.x = self.x
            self.block.pos.y = self.y
            return self.block
            
        

        
class ObstacleMouseAction( MouseAction ):
    '''
    In build state when a mouse is clicked, selection area starts forming
    When mouse is clicked again selection area takes shape which will  be our new obstacle
    Picture selection area as in age of empires
    '''
    def __init__(self):
        '''
        --src_x, src_y the location where the initial click occured and cause
        selection area to form
        --After a click we go to "hover_state". The change in location of mouse, cause
        by hovering in the screen relative to the src_x, src_y forms the rectangle
        '''
        super().__init__( None )

        self.block = Obstacles( 0, 0, 0, 0 )
        self.src_x = None
        self.src_y = None

        self.draw_state = False
        
    #Override    
    def click_event(self):
        '''
        if not active_state, fixes the 
        '''
        if self.active_state:
            self.get_mouse_pos()
            if self.draw_state:
                self.draw_state = False
                return self.block
            else:
                self.src_x = self.x
                self.src_y = self.y
                self.draw_state = True

    #Override      
    def hover_event(self):
        if self.active_state and self.draw_state:
            self.get_mouse_pos()
            width = self.x - self.src_x
            height = self.y - self.src_y
            '''
            In pygame Rectangles are drawn from top left corner, so maintining that top left corner as the source of the rectangle
            -src_x and src_y is not necessarily top left corner of the rectangle, but it is the "pivot" point an obstacle has
            src_x and src_y point in common
            '''
            x , y = self.x, self.y
            if width > 0:
                x = self.src_x
            if height > 0:
                y = self.src_y
            self.block = Obstacles( x, y, abs(width), abs(height) )
            return self.block
            
            
