import heapq

def heuristic(node_a, node_b):                      #通过x,y坐标之间的绝对值的差值获得两个节点之间的曼哈顿距离（也可以是欧式距离）
    
    dx = abs(node_a[0] - node_b[0])                 #dx, dy分别表示两个节点在x轴和y轴上的距离差，用于求得街区距离
    dy = abs(node_a[1] - node_b[1])                 #如果是欧式距离则需要使用sqrt(dx^2 + dy^2)，但在网格地图中通常使用曼哈顿距离更合适，因为只能沿着网格移动
   
    return dx + dy
    
def get_neighbors(current, grid):                   #定义当前位置上下左右的邻居
    neighbors = []                                  #定义一个空列表来存储邻居节点的坐标
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] # 右、下、左、上
    rows, cols = len(grid), len(grid[0])            #获取地图的行数和列数

    for dx, dy in directions:                       #通过for循环遍历四个方向
        new_x = current[0] + dx                     #计算邻居节点的坐标
        new_y = current[1] + dy

        if 0 <= new_x < cols and 0 <= new_y < rows and grid[new_y][new_x] == 0:         #检查是否在地图范围内且不是障碍物（==0）
            neighbors.append((new_x, new_y))                                            #如果满足条件则将邻居节点添加到列表中
  
    return neighbors

def reconstruct_path(came_from, current):                      #算法找到目标节点，通过回溯重建路径。函数接受一个字典came_from和当前节点current作为参数
    total_path = [current]                                     #初始化路径列表total_path，首先将当前节点添加到路径中
    while current in came_from:                                #当前节点在came_from字典中时，继续回溯
        current = came_from[current]                           #获取当前节点的前驱节点
        total_path.insert(0, current)                          #将前驱节点插入到路径列表的开头
    return total_path                                          #返回从起点到目标节点的完整路径列表

def a_star(start, goal, grid):                                 #A*算法的核心函数，输入起点、终点和地图作为参数，输出从起点到终点的路径列表
    open_set = []                                              #使用open_set作为优先队列来存放待探索的节点
    heapq.heappush(open_set, (0, start))                       #开始的时候将（0, 0）push到openset

    came_from = {}                                             #定义字典came_from来存放每个节点的前驱节点，便于理清每一个节点是从哪个节点过来的
    g_score = {start: 0}                                       #定义字典g_score来存放从起点到每个节点的实际代价，初始时只有起点的g_score为0，其他节点默认为无穷大
    f_score = {start: heuristic(start, goal)}                  #定义字典f_score来存放从起点到每个节点的估计总代价，初始时只有起点的f_score为启发式函数值，其他节点默认为无穷大

    step_count = 1                                             #给A*探索的每一步计数，直观体现算法的执行过程和效率

    while open_set:                                            #当open_set不为空时，继续探索

        current_f, current = heapq.heappop(open_set)           #从open_set中弹出f_score最低的节点作为当前节点current，同时获取其f_score值current_f


        print(f"第 {step_count} 步->选中当前节点: {current}, "
              f"g={g_score[current]}, h={heuristic(current, goal)}, f={current_f}")             #打印当前步骤数、选中的节点坐标以及其g_score、h_score和f_score值，体现算法的决策过程
        step_count += 1

        if current == goal:
            print("\n到达终点！展示路径...\n")                                                     #如果当前节点是目标节点，打印提示信息并调用reconstruct_path函数重建路径，返回完整路径列表
            return reconstruct_path(came_from, current)

        neighbors = get_neighbors(current, grid)                                                #获取当前节点的邻居节点列表，通过get_neighbors函数检查地图边界和障碍物，确保只返回有效的邻居节点坐标

        for neighbor in neighbors:                                                              #遍历每个邻居节点
            tentative_g_score = g_score[current] + 1                                            #计算从起点到邻居节点的临时g_score值，等于当前节点的g_score加上从当前节点到邻居节点的代价（这里假设每一步的代价为1）

            if tentative_g_score < g_score.get(neighbor, float('inf')):                         #如果计算得到的临时g_score值小于邻居节点当前的g_score值（如果邻居节点不在g_score字典中，则默认为无穷大），说明找到了一条更优的路径到达邻居节点
                came_from[neighbor] = current                                                   #更新came_from字典，记录邻居节点的前驱节点为当前节点
                g_score[neighbor] = tentative_g_score                                           #更新g_score字典，记录邻居节点的g_score值为计算得到的临时g_score值
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)               #更新f_score字典，记录邻居节点的f_score值为g_score值加上从邻居节点到目标节点的启发式估计值

                if neighbor not in [node[1] for node in open_set]:                              #如果邻居节点不在open_set中，说明这是第一次发现这个节点，将其添加到open_set中以便后续探索
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

if __name__ == "__main__":
    grid_map = [
        [0, 0, 0, 1, 0, 0, 1],
        [0, 1, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0],                      #建立一个二维地图张量，0代表空地，1代表障碍物
        [0, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
    ]

    start_point = (0, 0)                            #定义起点和终点坐标
    end_point = (6, 7)

    print(f"正在使用 A* 算法寻找从 {start_point} 到 {end_point} 的路径...\n")
    path = a_star(start_point, end_point, grid_map) #调用A*算法函数，传入起点、终点和地图，获取路径

    if path:                                        #如果找到路径，打印路径坐标和地图可视化展示
        print("最终完整路径坐标如下：")
        print(path)
        print("\n地图可视化展示 (@=起点, *=路径, X=障碍, .=空地):")
        for y in range(len(grid_map)):
            row_str = ""
            for x in range(len(grid_map[0])):
                if (x, y) == start_point:
                    row_str += " @ "
                elif (x, y) in path and (x, y) != start_point and (x, y) != end_point:
                    row_str += " * "
                elif (x, y) == end_point:
                    row_str += " $ "
                elif grid_map[y][x] == 1:
                    row_str += " X "
                else:
                    row_str += " . "
            print(row_str)
    else:
        print(" 未找到可行路径。")
