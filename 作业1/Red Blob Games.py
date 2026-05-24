import heapq
from collections import defaultdict

def a_star_search(graph, start, goal):
    """
    Red Blob Games 风格的 A* 核心算法实现
    graph: 包含节点和邻居关系的图结构对象
    start: 起点
    goal: 终点
    """
    # 优先队列 (Frontier)，存储 (优先级, 节点)
    frontier = []
    heapq.heappush(frontier, (0, start))
    
    # came_from 用于记录路径，方便最后回溯
    came_from = {}
    came_from[start] = None
    
    # cost_so_far 相当于 g_score，记录从起点到当前节点的实际代价
    cost_so_far = {}
    cost_so_far[start] = 0
    
    while frontier:
        # 弹出当前 f(n) 最小（优先级最高）的节点
        _, current = heapq.heappop(frontier)
        
        # 如果到达终点，结束搜索
        if current == goal:
            break
            
        # 遍历当前节点的所有邻居
        for next_node in graph.neighbors(current):
            # 计算新的实际代价 (g(n))，假设每步基础代价为1
            new_cost = cost_so_far[current] + graph.cost(current, next_node)
            
            # 如果发现了一条到达该邻居的更短路径，就更新它
            if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                cost_so_far[next_node] = new_cost
                
                # 计算总预估代价 f(n) = g(n) + h(n)
                # heuristic 是 Red Blob Games 强调的启发式函数（如曼哈顿距离）
                priority = new_cost + graph.heuristic(next_node, goal)
                
                heapq.heappush(frontier, (priority, next_node))
                came_from[next_node] = current
    
    return came_from, cost_so_far

# --- 辅助函数：根据 came_from 字典重建完整路径 ---
def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    if goal not in came_from: 
        return [] # 没有找到路径
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


# --- 网格图类：用于演示 A* 在二维网格上的寻路 ---
class SimpleGrid:
    def __init__(self, width, height, obstacles=None):
        self.width = width
        self.height = height
        self.obstacles = set(obstacles) if obstacles else set()

    def in_bounds(self, pos):
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, pos):
        return pos not in self.obstacles

    def neighbors(self, pos):
        x, y = pos
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        result = []
        for dx, dy in directions:
            next_pos = (x + dx, y + dy)
            if self.in_bounds(next_pos) and self.passable(next_pos):
                result.append(next_pos)
        return result

    def cost(self, current, next_node):
        return 1

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


if __name__ == "__main__":
    # 定义障碍物
    obstacles = [(1, 1), (3, 0), (3, 1), (4, 0), (5, 2), (6, 0)]
    grid = SimpleGrid(8, 8, obstacles)

    start = (0, 0)
    goal = (7, 5)

    print("=" * 50)
    print(f"Red Blob Games 风格 A* 算法演示")
    print(f"起点: {start}, 终点: {goal}")
    print(f"障碍物: {obstacles}")
    print("=" * 50)

    came_from, cost_so_far = a_star_search(grid, start, goal)
    path = reconstruct_path(came_from, start, goal)

    if path:
        print(f"\n找到路径！共 {len(path)} 步")
        print(f"路径坐标: {path}")
        print(f"总代价: {cost_so_far.get(goal, 'N/A')}")
    else:
        print("\n未找到路径！")

    # 可视化地图
    print("\n地图可视化 (@=起点, $=终点, *=路径, X=障碍, .=空地):")
    path_set = set(path)
    for y in range(grid.height):
        row = ""
        for x in range(grid.width):
            pos = (x, y)
            if pos == start:
                row += " @ "
            elif pos == goal:
                row += " $ "
            elif pos in path_set:
                row += " * "
            elif pos in grid.obstacles:
                row += " X "
            else:
                row += " . "
        print(row)