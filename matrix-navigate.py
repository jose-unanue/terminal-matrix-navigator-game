import pynput, os, random, time

os.system('clear')
size = -1

try:
    while not 4 <= size <= 20: size = int(input('How big do you want the board to be? (4 - 20): '))

except ValueError:
    print(f'You have to input numbers.')
    os.abort()

move_board = [[0 for _ in range(size)] for _ in range(size)]

moves = {
    'd': (1, 0),
    's': (0, 1),
    'a': (-1, 0),
    'w': (0, -1)
}

messages = {
    range(0, 2): 'You are very close to the goal.',
    range(2, 4): 'You are close to the goal.',
    range(4, 7): 'You are far from the goal.',
    range(7, 11): 'You are very far from the goal.'
}

pos = [random.randint(0, size - 1), random.randint(0, size - 1)]
end_pos = [random.randint(0, size - 1), random.randint(0, size - 1)]
move_board[pos[1]][pos[0]] = 2
key_press = None
not_moved = 0
hint = False
score = 0

def print_m(m):
    if m == None or len(m) != 0:
        print('Matrix cannot be empty.')
        os.abort()
        
    else:
        print('')
        for i in range(len(m)):
            for r in range(len(m)):
                print(move_board[i][r], end=' ')
            print('')
            

def handleKeyPress(key):
    global key_press
    if isinstance(key, pynput.keyboard.KeyCode): key_press = key.char
    return False


def waitForKeyInput():
    with pynput.keyboard.Listener(
        on_press=handleKeyPress) as listener:
        listener.join()
        

print('Press H to show end position, press any other key to continue.')
waitForKeyInput()

if key_press == 'h':
    hint = True
    
while True:
    if hint == True: move_board[end_pos[1]][end_pos[0]] = 'X'
    
    if not_moved != 0: print(f'You have not moved {not_moved} time(s).')
    if key_press != None: print(f'Last key pressed is {key_press.capitalize()}')
    
    for _, goal_range in enumerate(messages):
        if max(abs(pos[0] - end_pos[0]), abs(pos[1] - end_pos[1])) in goal_range and hint != 'hint':
            print(messages[goal_range])
    
    print_m(move_board)
    
    waitForKeyInput()
    
    move_board[pos[1]][pos[0]] = 0
    
    last_pos = [pos[0], pos[1]]
    for _, move in enumerate(moves):
        if key_press == move and pos[0] + moves[move][0] in range(0, size) and pos[1] + moves[move][1] in range(0, size) and (move_board[pos[1] + moves[move][1]][pos[0] + moves[move][0]] == 0 or move_board[pos[1] + moves[move][1]][pos[0] + moves[move][0]] == 'X'):
            pos[0] += moves[move][0]
            pos[1] += moves[move][1]
    
    move_board[pos[1]][pos[0]] = 2
    
    if last_pos == [pos[0], pos[1]]:
        not_moved += 1
    
    if [pos[0], pos[1]] == end_pos:
        score += 1
        while move_board[pos[1]][pos[0]] != 0: pos = [random.randint(0, size - 1), random.randint(0, size - 1)]
        while move_board[end_pos[1]][end_pos[0]] != 0: end_pos = [random.randint(0, size - 1), random.randint(0, size - 1)]
        move_board[pos[1]][pos[0]] = 2
        os.system('clear')
        print(f'You have reached the goal! Next round begins in')
        for i in range(3):
            print(f'{3 - i}...')
            time.sleep(1)
    
    os.system('clear')
    
    if not_moved > 5:
        break

print(f'Your score was {score} point(s).')
