class Laser:
    '''
    Simulates the behavior of a laser on the board, tracking its movement and interactions.

    
    **Parameters**
        x: *int*
            Initial x-coordinate of the laser.
        y: *int*
            Initial y-coordinate of the laser.
        vx: *int*
            Velocity in the x direction.
        vy: *int*
            Velocity in the y direction.
    '''

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self):
        '''
        Moves the laser to the next position based on its velocity.
        '''
        self.x += self.vx
        self.y += self.vy

    def get_position(self):
        '''
        Returns the current position of the laser.

        **Returns**
            tuple[int, int]: Current (x, y) coordinates of the laser.
        '''
        return self.x, self.y


class A_Block:
    '''
    Reflective block that changes the laser direction upon contact.
    '''
    def __init__(self, position):
        '''
        Initialize a ReflectBlock object with its position.

        **Parameters**
            position: *tuple*
                A tuple (x, y) representing the block's position on the grid.
        '''
        self.position = position
        self.type = 'A'  # Add type attribute

    def reflect(self, laser: 'Laser') -> 'Laser':
        '''
        Reflects the laser based on its impact on the block.

        **Parameters**
            laser: *Laser*
                An object representing the laser with position and velocity.

        **Returns**
            Laser: The laser object with updated position and velocity after reflection.
        '''
        relative_position = (laser.x - self.position[0],
                             laser.y - self.position[1])

        if (relative_position == (0, 1) or
                relative_position == (0, -1)):  # Vertical hit
            laser.vy = -laser.vy
        elif (relative_position == (1, 0) or
              relative_position == (-1, 0)):  # Horizontal hit
            laser.vx = -laser.vx

        laser.x += laser.vx
        laser.y += laser.vy

        return laser

    def __call__(self, laser):
        '''
        Allows the object to be called like a function to reflect a laser.

        **Parameters**
            laser: *Laser*
                The laser object to be reflected.

        **Returns**
            Laser: The updated laser object.
        '''
        return self.reflect(laser)


class B_Block:
    '''
    Opaque block that stops the laser completely.
    '''
    def __init__(self, position):
        '''
        Initialize an OpaqueBlock object with its position.

        **Parameters**
            position: *tuple*
                A tuple (x, y) representing the block's position on the grid.
        '''
        self.position = position
        self.type = 'B'  # Add type attribute

    def opaque(self, laser):
        '''
        Stops the laser completely upon contact.

        **Parameters**
            laser: *Laser*
                An object representing the laser with position and velocity.

        **Returns**
            Laser: The laser object with updated position and stopped state.
        '''
        laser.is_block = True
        return laser

    def __call__(self, laser):
        '''
        Allows the object to be called like a function to block a laser.

        **Parameters**
            laser: *Laser*
                The laser object to be blocked.

        **Returns**
            Laser: The updated laser object.
        '''
        return self.opaque(laser)


class C_Block:
    '''
    Refractive block that allows part of the laser to pass while reflecting another part.
    '''
    def __init__(self, position):
        '''
        Initialize a RefractBlock object with its position.

        **Parameters**
            position: *tuple*
                A tuple (x, y) representing the block's position on the grid.
        '''
        if isinstance(position, tuple) or isinstance(position, list):
            self.x, self.y = position
        else:
            self.x, self.y = position[0], position[1]
        self.position = (self.x, self.y)
        self.type = 'C'  # Add type attribute

    def refract(self, laser):
        '''
        Refracts the laser based on its impact on the block.

        **Parameters**
            laser: *Laser*
                An object representing the laser with position and velocity.

        **Returns**
            tuple: containing (new_laser, original_laser)
                new_laser: The refracted laser
                original_laser: The original laser with updated position
        '''
        # Create a new laser for refraction (starts at the same position)
        new_laser = Laser(laser.x, laser.y, laser.vx, laser.vy)
        
        # Determine the approach direction and adjust velocities accordingly
        # Horizontal approach
        if (self.x - 1, self.y) == (laser.x, laser.y) or (self.x + 1, self.y) == (laser.x, laser.y):
            # Reflected laser changes horizontal direction
            new_laser.vx = -laser.vx
            # Original laser continues with unchanged direction
        # Vertical approach
        elif (self.x, self.y - 1) == (laser.x, laser.y) or (self.x, self.y + 1) == (laser.x, laser.y):
            # Reflected laser changes vertical direction
            new_laser.vy = -laser.vy
            # Original laser continues with unchanged direction
            
        # Move both lasers forward once
        new_laser.move()
        laser.move()
        
        return new_laser, laser

    def __call__(self, laser):
        '''
        Allows the object to be called like a function to refract a laser.

        **Parameters**
            laser: *Laser*
                The laser object to be refracted.

        **Returns**
            tuple: containing (new_laser, original_laser)
        '''
        return self.refract(laser)