from Settings import *
from GraphicModels import *
from MouseEvents import *

class PlayMode:
    def __init__(self):
        pass

    def _reset_canvas(self):
        screen.fill( Color.white, GAME_PORTION )
        screen.fill( Color.black, MENU_PORTION )
        pygame.display.update()

    def _initialize_buttons(self):
        b_go = Button("Go")
        b_build = Button("Build mode")

        self.b_group = RenderButtonGroup()
        self.b_group.bulk_add( [b_go, b_build] )


    
    def execute(self, resources):
        '''
        @param resources, Graphic resources inherited from the Build mode
        '''
        self._reset_canvas(); self._initialize_buttons(); pygame.display.update()
        self.src = resources[0]
        self.dest = resources[1]
        self.obstacles = resources[2]

        #if Either src or dest is absent No action can be performed so we stall in actionLess_loop
        if not self.src or not self.dest:
            self._actionLess_run()
        else:
            self._action_run()
        

    def _actionLess_run( self ):
        ''' 
        Nothing happens except for when button "Build mode" is pressed it returns
        '''
        print("actionLess run")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #click occured inside menu Screen
                    if event.pos[1] < MENU_HEIGHT:
                        button = self.b_group.check_if_triggered()
                        if button:
                            if button.name == "Build mode":
                                return
            
            list( map(blit, [self.src, self.dest ]))
            list( map( blit, self.obstacles ))
            pygame.display.update( GAME_PORTION )
            pygame.time.delay( 30 )

    def _action_run(self):
        ''' 
        Source is animated from initial point to destination
        On reaching destination the animation is paused
        If Button "Go" is pressed animation restarts
        If Button "Build mode" is pressed, returns
        '''
        print( "action run")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #click occured inside menu Screen
                    if event.pos[1] < MENU_HEIGHT:
                        button = self.b_group.check_if_triggered()
                        if button:
                            if button.name == "Build mode":
                                return
                            if button.name == "Go":
                                print( "go go go")
            list( map(blit, [self.src, self.dest ]))
            list( map( blit, self.obstacles ))
            pygame.display.update( GAME_PORTION )
            pygame.time.delay( 30 )

class BuildMode:
    def __init__(self):
        ''' 
        cached_xxx are loaded as starting resources when the user reverts back to the build mode from the play mode
        cached_xxx are saved when we toggle to play mode
        '''
        self.cached_src = None
        self.cached_dest = None
        self.cached_obs_stack = Stack()
        
    def _reset_canvas(self):
        screen.fill( Color.white, GAME_PORTION )
        screen.fill( Color.black, MENU_PORTION )
        pygame.display.update()

    def _initialize_buttons(self):
        self.b_undo = Button("undo obstacle")   
        self.b_confirm = Button("confirm obstacle")

        self.b_source = Button("Place source")
        self.b_destination = Button("Place destination")
        self.b_obstacle = Button("Place obstacle")
        self.b_clear = Button("Clear screen")
        self.b_action = Button("Action mode")

        self.b_group = RenderButtonGroup()
        self.b_group.bulk_add( [self.b_undo, self.b_confirm, self.b_source, 
                                self.b_destination, self.b_obstacle,
                                self.b_clear, self.b_action] )

    
    def _cache_resources(self, src_obj, dest_obj, obs_stack ):                            
        ''' 
        -Caches src, dest, and obstacles so that it could be reloaded when the user returns back to the build mode
        -New copies of src and dest are cached, so that when loading they 
         could be loaded at the original position when they were built
        '''
        
        #New copy of source is cached
        src_copy = None
        if src_obj:
            src_copy = Source( src_obj.pos.x, src_obj.pos.y)
        self.cached_src = src_copy

        #New copy of destination is cached
        dest_copy = None
        if dest_obj:
            dest_copy = Destination( dest_obj.pos.x, dest_obj.pos.y )
        self.cached_dest = dest_copy

        self.cached_obs_stack = obs_stack
        
    
    def _load_cache(self):
        '''
        Returns cached properties which are loaded and initialized immediately in _run
        '''
        return [self.cached_src, self.cached_dest, self.cached_obs_stack]

    
    def execute( self ):
        '''
        Initializes properties, Resets canvas and calls Main loop _run
        After Loop ends returns the Graphic Objects to Game
        '''
        self._reset_canvas(); self._initialize_buttons(); pygame.display.update()

        resources =  self._run( )
        #saves for next round of Build Mode
        self._cache_resources( resources[0], resources[1], resources[2] )

        #returns iterable to Game instead of the stack        
        return [resources[0], resources[1], resources[2].iterable()]

    
    def _run( self ):
        '''
        Main Loop for Running Build Mode
        @return Source, Destination and List of Obstacles
        '''
        caches = self._load_cache()
        src, dest, obs_stack = caches

        #Mouse Actions
        MA_obs = ObstacleMouseAction()
        MA_src = MouseAction( Source(0,0) ) 
        MA_dest = MouseAction( Destination(0,0) )
        
        #semi_perm_obs sticks in the screen once user clicks but fades if not confirmed
        semi_perm_obs = None

        #Temp figures are the ghost figures that stick to the mouse cursor and are used for positioning these objects
        temp_obs = None
        temp_src = None
        temp_dest = None
 
        flag = True
        while flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEMOTION:
                    if event.pos[1] > MENU_HEIGHT:
                        temp_obs = MA_obs.hover_event()
                        temp_src = MA_src.hover_event()
                        temp_dest = MA_dest.hover_event()

                elif event.type == pygame.MOUSEBUTTONDOWN:

                    #click occured inside game Screen
                    #click_event() returns None when the buttons are inactive
                    if event.pos[1] > MENU_HEIGHT:
                        x1 = MA_src.click_event()
                        x2 = MA_dest.click_event()
                        x3 = MA_obs.click_event()

                        if x1 is not None: src = x1
                        if x2 is not None: dest = x2
                        if x3 is not None: semi_perm_obs = x3 

                    #click occured inside menu screen
                    else:
                        button = self.b_group.check_if_triggered()
                        if button:
                            if button.name == "undo obstacle":
                            
                                #Undoes the permanently placed obstacle
                                obs_stack.pop()
                            elif button.name == "confirm obstacle":
                                
                                #Once Obstacles are placed, They need to be confirmed, to make them permanent
                                if semi_perm_obs:
                                    if semi_perm_obs.pos.width > 1 and semi_perm_obs.pos.height > 1:
                                        obs_stack.push(semi_perm_obs)
                            elif button.name == "Place source":
                                
                                src = None#The earlier placed source is vanished
                                MA_src.active_state, MA_dest.active_state, MA_obs.active_state = True, False, False                
                            elif button.name == "Place destination":

                                dest = None#The earlier placed destination is vanished
                                MA_src.active_state, MA_dest.active_state, MA_obs.active_state = False, True,False                                 
                            elif button.name == "Place obstacle":                            

                                MA_src.active_state, MA_dest.active_state, MA_obs.active_state = False, False, True
                            elif button.name == "Clear screen":

                                #GAME_PORITON is now a clean White Slate
                                src, dest = None, None
                                obs_stack = Stack()
                            elif button.name == "Action mode":

                                #Build Mode Ends and subsequently, all the graphic units are return to action Mode
                                flag = False
                                

                        #if menu is clicked, reset the temp_objects
                        temp_obs = None
                        temp_src = None
                        temp_dest = None
                        semi_perm_obs = None

            screen.fill( Color.white, GAME_PORTION )

            list(map(blit, [semi_perm_obs, src, dest, temp_obs, temp_src, temp_dest]))
            list(map(blit, obs_stack.iterable() ))

            pygame.display.update( GAME_PORTION )
            pygame.time.delay(30)

        return  [ src, dest, obs_stack ]
                
                
    


class Main:
    ''' 
    Entry point for the Application
    Toggles between BuilMode and PlayMode 
    '''
    def __init__(self):
        self.bm = BuildMode()
        self.pm = PlayMode()

    def loop(self):
        '''
        Starts off with Build Mode and passes the graphic objects to the Play mode to be displayed
        Continues Forever until user closes pygame
        '''
        objects = self.bm.execute()
        self.pm.execute( objects )
        self.loop()
    
Main().loop()

        
                
        
        




        
    








