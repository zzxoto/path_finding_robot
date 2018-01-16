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
        b_go = Button("Restart")
        b_build = Button("Build mode")

        self.b_group = RenderButtonGroup()
        self.b_group.bulk_add( [b_go, b_build] )


    
    def execute(self, resources):
        '''
        @param resources, Graphic resources inherited from the Build mode
        '''
        self.src = resources[0]
        self.dest = resources[1]
        self.obstacles = resources[2]
        for i in self.obstacles:
            print ( i.pos )
        #if Either src or dest is absent No action can be performed so we stall in actionLess_loop
        if not self.src or not self.dest:
            self._reset_canvas(); self._initialize_buttons(); pygame.display.update()
            self._stall()
        else:
            path = self._algorithm()
            self._reset_canvas(); self._initialize_buttons(); pygame.display.update()
            self._animate( path )        

    def _stall( self ):
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


    def _animate( self,  leafPath ):
        ''' 
        Animates the source from its starting position to destination following the path found by the algorithm
        @param leafPath is the final node and by following its pointers entire path could be traced
        '''

        #transforming a singly linked source to destination path to a doubly linked by adding a child pointer
        rootPath = leafPath
        childNode = None

        #while loop ends by having leafPath pointing at Null and childNode pointing at topMost SourcePath
        while leafPath:
            leafPath.child = childNode
            childNode = leafPath
            leafPath = leafPath.parent
        rootPath = childNode
        
        #Making class Varaiables available to private function run()
        _src = self.src
        _b_group = self.b_group
        def run():
            '''
            When Restart is pressed animation starts from begining
            '''
            robot = Source( _src.pos.x, _src.pos.y )
            robot.pos = rootPath

            #playing animation
            while robot.pos:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        #click occured inside menu Screen
                        if event.pos[1] < MENU_HEIGHT:
                            button = _b_group.check_if_triggered()
                            if button:
                                if button.name == "Build mode":
                                    return
                                if button.name == "Restart":
                                    return run()
                
                screen.fill( Color.white, GAME_PORTION )
                list( map(blit, [ robot, self.dest ]))
                list( map( blit, self.obstacles ))
                robot.pos = robot.pos.child
                pygame.display.update( GAME_PORTION )
                pygame.time.delay( 30 )
                
            #after animation completes just waits for some event on the  button         
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        #click occured inside menu Screen
                        if event.pos[1] < MENU_HEIGHT:
                            button = _b_group.check_if_triggered()
                            if button:
                                if button.name == "Build mode":
                                    return
                                if button.name == "Restart":
                                    return run()
                
                pygame.time.delay( 30 )
        run()








    def _algorithm(self):
        ''' 
        -Search algorithm implemented to find the shortest path
        -On reaching destination, the algorithm returns the final node in the  shortest path
        '''
        def nearest_neighbors( sp ):
            '''
            Given a source Path returns all the possible sourcePaths that could eminate from that sourcePath
            if x and y are the coordinates of sp then, x-25, x, x+25 are the abcissa of the nearest neighbors 
            and similar for the y coordinates
            '''
            nearest_neighbors = []
            def inBoundY( k ):
                if k > MENU_HEIGHT and k < SCREEN_SIZE:
                    return True
            def inBoundX( k ):
                if k > 0 and k < SCREEN_SIZE:
                    return True
            sp_x,  sp_y = sp.x, sp.y
            for x in [sp_x - S_D_SIZE, sp_x, sp_x + S_D_SIZE ]:
                for y in [ sp_y - S_D_SIZE, sp_y, sp_y + S_D_SIZE] :
                    if inBoundX( x ):
                        if inBoundY( y ):
                            nearest_neighbors.append( SourcePath( x, y ) )
            
            return nearest_neighbors

        def notVisitedNeighbors( neighbors , visited ):
            '''
            from the list of neighbors returns the neighbors that have not yet been visited
            @param neigbors, SourcePath object, List of SourcePath accesible from some SourcePath
            @param visited, dictionary of SourcePath objects that represents SourcePaths already visited
            '''
            notVisited = []
            for i in neighbors:
                if i not in visited:
                    notVisited.append( i )
            return notVisited

        def notObstructedNeighbors( neighbors ):
            '''
            From list of neighbors returns the neighbors that are not touching the obstacles
            '''
            notObstructed = []
            for i in neighbors:
                anyCollision = False
                for j in self.obstacles:
                    if i.colliderect( j.pos ):
                        anyCollision = True
                if not anyCollision:
                    notObstructed.append( i )
            return notObstructed

        def updateVisited( sps, visited ):
            '''
            @param sps, {List} of SourcePaths to be added to the dictionary visited
            @param visited, {dictionary}  of SourcePath objects that represents SourcePaths already visited
            '''
            for sp in sps:
                visited[ sp ] = 0
        
        def destination_reached( sp ):
            '''
            Checks if a source path has collided with the destination object
            '''
            if sp.colliderect( self.dest.pos ):
                return True
        
        #initial sourcePosition taken as a root for calculating source path
        sp = SourcePath( self.src.pos.x, self.src.pos.y )
        
        #List of SourcePaths that is to be visited in current iteration
        frontier = [ sp ] 
        
        #to be visited in the next iteration
        nextFrontier = []

        #Tracks the SorucePaths visited
        visited = { }

        flag = True
        while flag:                
            #main algorithm
            for f in frontier:
                if destination_reached( f ):
                    flag = False
                    return f
                n_obs_n = notObstructedNeighbors( notVisitedNeighbors( nearest_neighbors( f ), visited ) )
                for neighbor in n_obs_n:
                    neighbor.parent = f
                    nextFrontier.append( neighbor )

                updateVisited( n_obs_n   , visited)
            
            #algorithm could not find shortest path because of obstacles
            if len(n_obs_n) == 0:
                flag = False
                return
            frontier = nextFrontier


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
        b_undo = Button("undo obstacle")   
        b_confirm = Button("confirm obstacle")
        b_obstacle = Button("Place obstacle")

        b_source = Button("Place source")
        b_destination = Button("Place destination")
        b_clear = Button("Clear screen")
        b_start = Button("Start")

        self.b_group = RenderButtonGroup()
        self.b_group.bulk_add( [b_start, b_undo, b_confirm, b_obstacle,
                           b_source, b_destination, b_clear,])

    
    def _cache_resources(self, resources ):                            
        ''' 
        @param resources, src, dest, stack of obstacles that are to be cached for later re-run of BuildMode
        -Caches src, dest, and obstacles so that it could be reloaded when the user returns back to the build mode
        -New copies of src and dest are cached, so that when loading they 
         could be loaded at the original position when they were built
        '''
        src_obj, dest_obj, obs_stack  = resources[0], resources[1], resources[2]
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

    
    def execute( self, initial_resources = None ):
        '''
        @params initial_resources, starting graphic objects to load when application is opened for the very_first time
        Initializes properties, Resets canvas and calls Main loop _run
        After Loop ends returns the Graphic Objects to Game
        '''
        self._reset_canvas(); self._initialize_buttons(); pygame.display.update()

        if initial_resources:
            self._cache_resources( initial_resources )

        resources =  self._run()
        #saves for next round of Build Mode
        self._cache_resources( resources )

        #returns iterable to Game instead of the stack        
        return [resources[0], resources[1], resources[2].iterable()]

    
    def _run( self):
        '''
        Main Loop for Running Build Mode
        @params initial_resources, starting graphic objects to load when application is opened for the first time
        @return Source, Destination and Stack of Obstacles
        '''
        src, dest, obs_stack = self._load_cache()

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
                        temp_src = MA_src.hover_event( )
                        temp_dest = MA_dest.hover_event( )

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
                            elif button.name == "Start":

                                #Build Mode Ends and subsequently, all the graphic units are passed to Play Mode
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

    def loop(self, initial_resources = None):
        '''
        @param initial_resources, initial graphic objects to begin the game with instead of white clean canvas
        Starts off with Build Mode and passes the graphic objects to the Play mode to be displayed
        Continues Forever until user closes pygame
        '''
        objects = self.bm.execute( initial_resources )
        self.pm.execute( objects )
        self.loop()


#Some initial Resources to load on very first execution
so = Source( 100, MENU_HEIGHT + 500 )
d = Destination( 500 , MENU_HEIGHT + 300 )

st = Stack()
st.push( Obstacles( 200, MENU_HEIGHT + 50, 25, SCREEN_SIZE - 50 ) )
    
Main().loop( [so , d, st] )

        
                
        
        




        
    








