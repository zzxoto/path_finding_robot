from Settings import *

class Block:
    '''
    THIS IS A INTERFACE
    All classes that use pygame Surface should inherit this
    '''
    def __init__(self):
        self.image = None
        self.pos = None
    def move(self, x, y):
        self.pos = self.pos.move( x, y )
        return self.pos


class Obstacles( Block ):
    """
    Obstacles that source object has to avoid to reach destination object
    """
    def __init__(self, x, y, width, height):
        self.image = pygame.Surface( (width, height) )
        self.image.fill( Color.brown )
        self.pos = pygame.Rect( x, y, width, height )
    

class Source( Block ):
    '''
    Source is the 25 X 25 object that moves and reaches the destination
    '''
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface( ( S_D_SIZE, S_D_SIZE ) )
        self.image.fill( Color.green )
        self.pos = self.image.get_rect()
        self.move( x, y )

class Destination( Block ):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface( ( S_D_SIZE, S_D_SIZE ) )
        self.image.fill( Color.red )
        self.pos = self.image.get_rect()
        self.move( x, y )

from Settings import *
class Button(Block):
    '''
    Buttons on the MENU_PORTION of the screen
    '''
    def __init__(self, name):
        """
        @param name, Text inscribed inside button
        """
        super().__init__()
        self.name = name
        self.image = Button._makeButton( name )
        self.pos = self.image.get_rect()

    @staticmethod
    def _makeButton(text):
        '''
        returns a Surface object that encapsulates the text surface with 5px padding
        All the button objects are initialized this way
        '''
        text = Font.render( text, False, Color.white )
        textArea = text.get_rect()

        #makes the surface that encapsulates text lil bit bigger than text object
        surf = pygame.Surface( (textArea.width + 10, textArea.height + 10) )

        #centering the textObject inside the surface
        textArea= textArea.move( 5, 5)
        surf.blit( text, textArea )
        return surf

class ButtonGroup:
    def __init__(self):
        self.buttons = []

    def check_if_triggered(self):
        '''
        Checks if the any of the buttons is self.buttons was clicked
        If the buttton was clicked and it had event_handler registered, returns the button
        '''
        click = pygame.mouse.get_pos()
        x, y = click[0], click[1]
        dummy_rect = pygame.Rect( x, y, 1, 1)
        for i in self.buttons:
            if (dummy_rect.colliderect( i.pos )):
                return i
                    
    def add(self, button):
        self.buttons.append( button )

    def bulk_add(self, buttons):
        for button in buttons:
            self.buttons.append( button )


class RenderButtonGroup( ButtonGroup ):
    ''' 
    -Buttons that could be aligned and rendered horizontally make use of this class
    -After adding each button they are immediately blitted with supposition that,
    buttons are placed in menu section and menu section display is not flushed everytime rendering happens
    '''
    def __init__(self, spacing = 10):
        super().__init__()
        self.spacing = spacing

    #Override
    def add(self, button):
        self.renderButton( button )
        self.buttons.append( button )

    #Override
    def bulk_add( self, buttons):
        for button in buttons:
            self.renderButton( button )
            self.buttons.append( button ) 

    def renderButton( self, button ):
        if len(self.buttons) == 0:
            button.move( self.spacing, 0)
        else:
            lastButton = self.buttons[-1]
            button.move( lastButton.pos.x + lastButton.pos.width + self.spacing, 0 )
        blit( button )
