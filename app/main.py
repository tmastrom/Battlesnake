import json
import os
import random
import bottle
import time

from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    #print(json.dumps(data))

    color = "#8935B9"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json
    start = time.time()
    print 'turn ', data['turn']

    head = [int(data["you"]["body"][0]["x"]), int(data["you"]["body"][0]["y"])]
    # food location
    # change to make this the closest food!!
    # account for 'no food on board' case 

    width = data['board']['width'] - 1
    height = data['board']['height'] - 1
    directions = ['up', 'down', 'left', 'right']
    direction = ''
    dont = []
    other_snake_heads = []    # not ideal positions
    direc = [0, 0] # direction vector

    # handle no food on the board case
    if data["board"]["food"]:   # no food on the board
        food = [data["board"]["food"][0]["x"], data["board"]["food"][0]["y"]]       # error index out of range if no food on board  
        print "no food on board"
    else:   
        food = [width/2, height/2]  # go to the middle 
        

    # Todo list 
    # avoid other snake heads
    # prioritize moving towards middle 
   
    #print(json.dumps(data))

    def check_next_pos(direc, dont, head, directions):
        next_pos = [sum(x) for x in zip(head, direc)]
        print 'next position', next_pos
        
        for i in next_pos:
            if i not in range(0,15):
                print 'not in the boundary'
                return False

        if next_pos in dont:
            print 'dont go here'
            return False
        else: 

            print 'go here'
            return True

    def prioritize(dont, head, directions, other_snake_heads):
        # prioritize the list of directions 
        # 
        # if othersnakeheads in 3x3
        # get dist 
        # move that dir to  

        threeby = [[head[0], head[1]-1],
        [head[0], head[1]+1],
        [head[0]-1, head[1]],
        [head[0]-1, head[1]-1],
        [head[0]-1, head[1]+1],
        [head[0]+1, head[1]],
        [head[0]+1, head[1]-1],
        [head[0]+1, head[1]+1]]

        for i in other_snake_heads:
            if i in threeby:
                print "DANGER"
                direc = get_dist(head, i, 'away')
                if vec_to_word(direc) in directions:
                    directions.insert(0, vec_to_word(direc))
                print "move away in direction", directions[0]
                return directions

        return directions

        # check for snake heads
        # make a list of snake heads in a 3x3 grid
        # prioritize away from them if bigger 
        # prioritize middle of the board 
        # return new directions list
        return False

    def get_dist(head, thing, going):  # returns direction to move towards the thing
        direc = [0, 0]

        if len(thing) != 2:
            print 'not a 2 coord list'
            return direc

        # find direction
        neg = [-x for x in thing]   # takes the negative the thing position
        dist = [sum(x) for x in zip(head, neg)] # distance to thing
                
        distabs = [abs(x) for x in dist]
        ind = distabs.index(max(distabs))   # which direction is the furthest

        # set the direction vector
        if going == 'to':       # if you want to go to the thing
            if dist[ind] < 0:
                direc[ind] = 1
            else: direc[ind] = -1

        if going == 'away':      # if you want to go away 
            if dist[ind] < 0:
                direc[ind] = -1
            else: direc[ind] = 1
        
        return direc

    def vec_to_word(direction):
        up = [0, -1]
        down = [0, 1]
        left = [-1, 0]
        right = [1, 0]

        if direction == up:
            return 'up'
        if direction == down:
            return 'down'
        if direction == left:
            return 'left'
        if direction == right:
            return 'right'

    def word_to_vec(direction):
        up = [0, -1]
        down = [0, 1]
        left = [-1, 0]
        right = [1, 0]

        if direction == 'up':
            return up
        if direction == 'down':
            return down
        if direction == 'left':
            return left
        if direction == 'right':
            return right

    # grow the list of coordinates not to go
    # populate the list with snakes on the board including myself
    # differentiate between me and others??
    # save the head/tail location to see where they are moving??
    for i in data["board"]["snakes"]:
        for j in i['body']:
            pos = [j['x'],j['y']]
            dont.append(pos)
    #print dont, 'DONT'

    for i in data["board"]["snakes"]:
        pos = [i['body'][0]['x'],i['body'][0]['y']]
        other_snake_heads.append(pos)      
    
    # account for 'no food on board' case 
    # make a closest food function
    # order the directions based on priority

    direc = get_dist(head, food, 'to')    # direction to food 

    while len(directions) != 0:

        #print 'directions list after check_border()', directions
        isValid = check_next_pos(direc, dont, head, directions)
        
        if isValid == True:
            print 'position is valid'
            validDir = direc
            direction = vec_to_word(validDir)
            print 'direction ', direction
            
            # execution time 
            end = time.time()
            print(end - start)
            return move_response(direction)
        
        invalidDir = vec_to_word(direc)
        print 'invalidDir', invalidDir
        print 'directions list', directions
        directions.remove(invalidDir)
        # change the direction vector to something else 
        #directions = prioritize(dont, head, directions, other_snake_heads)
        direc = word_to_vec(directions[0])


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    #print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )


