from copy import deepcopy
from colorama import Fore, Back, Style

#direction matrix
DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}
#target matrix
#END = [[1, 2, 3], [0, 8, 4], [7, 6, 5]]
END = []
initial_state_matrix = []


# unicode for draw puzzle in command promt or terminal
left_down_angle = '\u2514'
right_down_angle = '\u2518'
right_up_angle = '\u2510'
left_up_angle = '\u250C'

middle_junction = '\u253C'
top_junction = '\u252C'
bottom_junction = '\u2534'
right_junction = '\u2524'
left_junction = '\u251C'

#bar color
bar = Style.BRIGHT + Fore.CYAN + '\u2502' + Fore.RESET + Style.RESET_ALL
dash = '\u2500'

#Line draw code
first_line = Style.BRIGHT + Fore.CYAN + left_up_angle + dash + dash + dash + top_junction + dash + dash + dash + top_junction + dash + dash + dash + right_up_angle + Fore.RESET + Style.RESET_ALL
middle_line = Style.BRIGHT + Fore.CYAN + left_junction + dash + dash + dash + middle_junction + dash + dash + dash + middle_junction + dash + dash + dash + right_junction + Fore.RESET + Style.RESET_ALL
last_line = Style.BRIGHT + Fore.CYAN + left_down_angle + dash + dash + dash + bottom_junction + dash + dash + dash + bottom_junction + dash + dash + dash + right_down_angle + Fore.RESET + Style.RESET_ALL

#Khởi tạo ma trận
def read_input_matrices():
    """Reads the input matrices from the user."""

    #initial_state_matrix = []
    #END = []

    print("Nhập vào ma trận ban đầu:")
    for row in range(3):
        initial_state_matrix.append([int(x) for x in input().split()])

    print("Nhập vào ma trận đích:")
    for row in range(3):
        END.append([int(x) for x in input().split()])

    return initial_state_matrix, END
#puzzle print function
def print_puzzle(array):
    print(first_line)
    for a in range(len(array)):
        for i in array[a]:
            if i == 0:
                print(bar, Back.RED + ' ' + Back.RESET, end=' ')
            else:
                print(bar, i, end=' ')
        print(bar)
        if a == 2:
            print(last_line)
        else:
            print(middle_line)

#Đây là node lưu trữ các trạng thái của puzzle
class Node:
    def __init__(self, current_node, previous_node, g, h, dir):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h


def get_pos(current_state, element):
    for row in range(len(current_state)):
        if element in current_state[row]:
            return (row, current_state[row].index(element))

#Tính chi phí (khoảng cách) tới vị trí đích
def euclidianCost(current_state):
    cost = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            pos = get_pos(END, current_state[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost

#Lấy các Nodes kề
def getAdjNode(node):
    listNode = []
    emptyPos = get_pos(node.current_node, 0)

    for dir in DIRECTIONS.keys():
        newPos = (emptyPos[0] + DIRECTIONS[dir][0], emptyPos[1] + DIRECTIONS[dir][1])
        if 0 <= newPos[0] < len(node.current_node) and 0 <= newPos[1] < len(node.current_node[0]):
            newState = deepcopy(node.current_node)
            newState[emptyPos[0]][emptyPos[1]] = node.current_node[newPos[0]][newPos[1]]
            newState[newPos[0]][newPos[1]] = 0
            # listNode += [Node(newState, node.current_node, node.g + 1, euclidianCost(newState), dir)]
            listNode.append(Node(newState, node.current_node, node.g + 1, euclidianCost(newState), dir))

    return listNode

#Tìm nodes tốt nhất trong danh sách listNodes
def getBestNode(openSet):
    firstIter = True

    for node in openSet.values():
        if firstIter or node.f() < bestF:
            firstIter = False
            bestNode = node
            bestF = bestNode.f()
    return bestNode

#Hàm tạo đường đi ngắn nhất cho bài toán
def buildPath(closedSet):
    node = closedSet[str(END)]
    branch = list()

    while node.dir:
        branch.append({
            'dir': node.dir,
            'node': node.current_node
        })
        node = closedSet[str(node.previous_node)]
    branch.append({
        'dir': '',
        'node': node.current_node
    })
    branch.reverse()

    return branch

#Hàm main để thực hiện thuật toán
def main(puzzle):
    open_set = {str(puzzle): Node(puzzle, puzzle, 0, euclidianCost(puzzle), "")}
    closed_set = {}

    while True:
        test_node = getBestNode(open_set)
        closed_set[str(test_node.current_node)] = test_node

        if test_node.current_node == END:
            return buildPath(closed_set)

        adj_node = getAdjNode(test_node)
        for node in adj_node:
            if str(node.current_node) in closed_set.keys() or str(node.current_node) in open_set.keys() and open_set[
                str(node.current_node)].f() < node.f():
                continue
            open_set[str(node.current_node)] = node

        del open_set[str(test_node.current_node)]

# Convert ma trận sang array, đếm số lượng đảo chiều
def getInvCount(arr):
    inv_count = 0
    empty_value = -1
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if arr[j] != empty_value and arr[i] != empty_value and arr[j] < arr[i]: #Ô trước lớn hơn thì là tính 1 cặp đảo chiều
                inv_count += 1
    return inv_count
 
     

def isSolvable(puzzle) :
 
    # Đếm số lượng đảo chiều
    inv_count = getInvCount([j for sub in puzzle for j in sub])
 
    # Chia hết cho 2, tức là số lượng đảo chiều chẵn thì quay lui về trạng thái đích thành công!
    return (inv_count % 2 == 0)
     

# Convert ma trận để kiểm tra trạng thái đầu có thể tiến tới trạng thái đích được hay không
def process_matrix(TEST, INIT):
    n = len(TEST)
    
    # Khởi tạo mảng TMP với giá trị từ 1 đến n-1
    #TMP = [0] * (n * n)
    
    # Khởi tạo từ điển để lưu trữ chỉ số của mỗi giá trị trong TMP
    index_dict = {}
    
    cnt = 1
    
    # Duyệt qua ma trận TEST và gán giá trị vào mảng TMP và từ điển
    for row in range(n):
        for col in range(n):
            value = TEST[row][col]
            #TMP[cnt - 1] = value  # Chỉ số của TMP giảm đi 1
            index_dict[value] = cnt  # Lưu chỉ số vào từ điển
            cnt += 1
    
    index_dict[TEST[2][2]] = 0
    
    # Khởi tạo ma trận CHECK với các phần tử ban đầu là 0
    CHECK = [[0 for _ in range(n)] for _ in range(n)]
    
    for row in range(n):
        for col in range(n):
            value = INIT[row][col]
            CHECK[row][col] = index_dict[value]  # Sử dụng từ điển để lấy chỉ số
          
    return CHECK

def simple_check(start_matrix):
    for direction in DIRECTIONS:
        new_matrix = move_tile(deepcopy(start_matrix), direction)
        if new_matrix == END:
           return True
    return False

def move_tile(matrix, direction):
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] == 0:
                new_row = row + DIRECTIONS[direction][0]
                new_col = col + DIRECTIONS[direction][1]
                if 0 <= new_row < len(matrix) and 0 <= new_col < len(matrix[0]):
                    matrix[row][col], matrix[new_row][new_col] = matrix[new_row][new_col], matrix[row][col]
                return matrix
# Ma trận TEST mẫu


if __name__ == '__main__':
    #it is start matrix
    puzzle = read_input_matrices()
    CHECK = process_matrix(END, initial_state_matrix)
    if(simple_check(initial_state_matrix)):
      print("Ma trận khởi tạo có thể trở thành ma trận đích!")
    elif(isSolvable(CHECK)) :
      print("Ma trận khởi tạo có thể trở thành ma trận đích!")
    else :
      print("Ma trận khởi tạo không thể trở thành ma trận đích!")
      exit()
         
    br = main(puzzle[0])
    print('Tổng số bước di chuyển : ', len(br) - 1)
    print()
    print(dash + dash + right_junction, "INPUT", left_junction + dash + dash)
    for b in br:
        if b['dir'] != '':
            letter = ''
            if b['dir'] == 'U':
                letter = 'UP'
            elif b['dir'] == 'R':
                letter = "RIGHT"
            elif b['dir'] == 'L':
                letter = 'LEFT'
            elif b['dir'] == 'D':
                letter = 'DOWN'
            print(dash + dash + right_junction, letter, left_junction + dash + dash)
        print_puzzle(b['node'])
        print()

    print(dash + dash + right_junction, 'ABOVE IS THE OUTPUT', left_junction + dash + dash)
    

