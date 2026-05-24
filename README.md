# 搜索算法与机器学习 - 作业合集

> 本仓库包含《搜索算法与机器学习》课程的四次作业，涵盖图搜索、监督学习与无监督学习。

---

## 目录

| 作业 | 主题 | 核心算法 |
|:---:|------|------|
| [1](#作业1--a-启发式搜索) | A\* 启发式搜索 | f(n) = g(n) + h(n) |
| [2](#作业2--多元线性回归与正则化) | 多元线性回归与正则化 | 梯度下降 / L2 岭回归 |
| [3](#作业3--svm-鸢尾花分类) | SVM 鸢尾花分类 | 支持向量机 (线性核) |
| [4](#作业4--k-means-聚类) | K-Means 聚类 | 无监督聚类 / 肘部法则 |

---

## 作业1 · A\* 启发式搜索

### 文件

| 文件 | 说明 |
|------|------|
| `astar_self.py` | 在 8x7 障碍地图上寻路，每步打印当前节点和 g/h/f 值，直观展示决策过程 |
| `Red Blob Games.py` | 通用 A\* 框架，将算法与图结构解耦，附带 SimpleGrid 演示 |

### 代码来源

- [Introduction to the A\* Algorithm](https://www.redblobgames.com/pathfinding/a-star/introduction.html) — 经典 A\* 伪代码参考 (Wikipedia / Red Blob Games)
- [CSDN: A\*算法详解](https://blog.csdn.net/)
- [GitHub: python-astar](https://github.com/)
- [GitHub: brean/python-pathfinding](https://github.com/brean/python-pathfinding) — 类似思路参考
- Python 标准库参考：`heapq` — Heap queue algorithm

### 算法简介 & 运行方法

A\* 搜索算法，结合 Dijkstra 算法的全局最优性和贪心最佳优先搜索的高效性，通过评估函数 **f(n) = g(n) + h(n)** 来指导搜索方向。

| 项 | 说明 |
|:---|------|
| 语言 | Python 3.x |
| 运行 | `python astar_self.py` |
| 输出 | 控制台打印坐标路径 + 字符画地图（障碍物、路径可视化） |

### 脚本结构

```
astar_self.py (主程序入口)
│
├── a_star()              ← 核心算法
│   ├── heuristic()       计算 h 值 (曼哈顿距离)
│   ├── get_neighbors()   获取四方向合法邻居
│   └── reconstruct_path()回溯前驱节点生成最终路径
│
├── reconstruct_path()    ← 路径回溯工具
├── get_neighbors()       ← 地图交互工具
└── heuristic()           ← 数学计算工具
```

### 解决什么问题

在带障碍物的网格地图上，找一条从起点到终点的最短路径。

BFS 按层均匀扩散，Dijkstra 按已走距离均匀扩散——两者都不"看向"终点。在无障碍的开阔地图上，Dijkstra 会探索一个以起点为圆心的圆，直到碰巧撞上终点为止。大量算力浪费在背离目标的方向上。

### 算法关键函数实现

| 函数 | 输入 | 输出 | 职责 |
|------|:---:|:---:|------|
| `heuristic(a, b)` | 两个坐标 | 曼哈顿距离 | 估算剩余距离，A\* 区别于 Dijkstra 的唯一之处 |
| `get_neighbors(current, grid)` | 节点 + 地图 | 邻居列表 | 检查边界和障碍物，返回合法邻居 |
| `reconstruct_path(came_from, current)` | 前驱字典 + 终点 | 完整路径 | 从终点回溯到起点 |
| `a_star(start, goal, grid)` | 起点 + 终点 + 地图 | 路径 / None | 主循环：弹出→判终→扩展→更新→入队 |

### 学习收获

A\* 算法通过评估函数 f(n) = g(n) + h(n)，融合 Dijkstra 算法的严谨和贪心最佳优先搜索的高效，A*算法通过评估函数f(n) = g(n) + h(n)，融合 Dijkstra 算法的严谨和贪心最佳优先搜索的高效，其中Dijkstra的部分对应g_score代表从起点到current节点的实际已经发生的代价，而heuristic(current, goal)会输出距离终点的值h（n），两者相加获得f（n）从而获得一个相对的平衡，关键的算法函数实现模块a_star()， reconstruct_path()， get_neighbors()， heuristic()
同时依赖字典存放并理清每一个节点的前驱节点，用二维网格数组实现二维点阵街区地图，建立neighbors列表存放满足条件的邻居节点，open_set用于作为优先队列存放需要探索的节点，在循环中遍历open_set中的邻居节点的函数值，不断更新g_score和f_score的函数启发值，total_path在一个一个循环判断分支之后遍历到goal目标点之后开始回溯reconstruct路径，这时候就需要字典存放的遍历的每一个节点的前驱节点构成路径：

- **g(n)** — Dijkstra 的部分，对应 `g_score`，代表从起点到当前节点实际已经发生的代价
- **h(n)** — `heuristic(current, goal)` 输出到终点的估计距离
- **f(n)** — 两者相加，获得相对平衡的搜索方向

核心数据结构：
- `came_from` 字典存放每个节点的前驱节点，用于最终回溯
- 二维网格数组实现街区地图
- `neighbors` 列表存放满足条件的邻居节点
- `open_set` 优先队列存放待探索节点
- 循环中遍历邻居节点，不断更新 `g_score` 和 `f_score`
- 到达 goal 后通过 `came_from` 回溯，构成完整路径

---

## 作业2 · 多元线性回归与正则化

### 
作业要求是手搓带L2正则化的线性回归（岭回归）和基础线性回归对加州房价数据集进行回归分析，其中这两个由class MyLinearRegression封装实现
Base_MLR.ipynb：手写 MyLinearRegression，梯度下降拟合
Regularized_MLR.ipynb：手写 MyRidgeRegression，加入 L2 惩罚项
包含
init（初始化方法）：learning_rate（学习率就是每次学习自变量变化的步长，太大的话可能会错过梯度下降的最优，太小学习速度比较慢）,n_iterations（迭代的次数）,lambda_param（岭回归的核心，决定对过大的权重施加多大的惩罚）,weights(存放经过学习调整后的特征权重）
fit（拟合）：首先随机初始化权重（在开始学习前，先给权重赋一些极小的随机值作为起点，减少初始偏移），然后进入训练循环，循环iterations次，前向传播通过矩阵乘法计算出预测值，和真实值作差得到残差，运用损失函数对权重求导的公式计算并更新参数，训练完毕
predict（self， x）返回的是测试数据点乘权重矩阵得到预测结果

### 文件

| 文件 | 说明 |
|------|------|
| `Base_MLR.ipynb` | 手写 `MyLinearRegression`，梯度下降拟合 |
| `Regularized_MLR.ipynb` | 手写 `MyRidgeRegression`，加入 L2 惩罚项 |

### 代码来源

- [scikit-learn: Linear Models](https://scikit-learn.org/stable/modules/linear_model.html)

### 数据来源

- California Housing 数据集：`sklearn.datasets.fetch_california_housing()`

### 损失函数 — MSE

从概率视角：假设 ε 服从正态分布，**最大似然估计 ⇔ 最小化均方误差**。

MSE = (1/n) Σ(ŷᵢ - yᵢ)²

凸性保证：MSE 对 w 是二次函数，只有一个全局最小值，梯度下降一定收敛（步长合适的前提下）。

### 梯度下降的推导

```
损失:    J(w) = (1/n) · (Xw - y)ᵀ (Xw - y)
梯度:    ∇J  = (2/n) · Xᵀ (Xw - y)
更新:    w   := w - α · ∇J
```

### L2 正则化 (Ridge)

在损失函数上加一项：

```
J_ridge = J + (λ/2n) · Σ wⱼ²    (不含偏置项 w₀)
∇J_ridge = (2/n) · Xᵀ (Xw - y) + (λ/n) · w
```

效果：每次更新时，权重额外减去 (αλ/n)w，即按比例缩小。λ 越小约束越弱。

### 手写类结构

两个类均由 `class` 封装实现：

```
MyLinearRegression / MyRidgeRegression
│
├── __init__()    ← 初始化超参数
│   ├── learning_rate    学习率 (步长: 太大错过最优, 太小收敛慢)
│   ├── n_iterations     迭代次数
│   ├── lambda_param     岭回归核心参数 (仅 Ridge)
│   └── weights          特征权重 (训练后存储)
│
├── fit(X, y)     ← 训练
│   ├── 随机初始化权重 (极小随机值, 减少初始偏移)
│   ├── 循环 n_iterations 次:
│   │   ├── 前向传播: y_pred = X·weights
│   │   ├── 残差: error = y_pred - y
│   │   ├── 梯度计算 (MSE 求导 / Ridge 额外加 λ/n·w)
│   │   └── 权重更新: weights -= α · gradient
│   └── 训练完毕
│
└── predict(X)    ← 预测: return X · weights
```

### 模块职责

| 模块 | 职责 |
|------|------|
| `StandardScaler` | 使每个特征均值为 0、标准差为 1，消除量纲差异 |
| `MyLinearRegression.fit()` | 梯度下降循环：预测 → 算误差 → 算梯度 → 更新权重 |
| `MyLinearRegression.predict()` | 矩阵乘法 X·w |
| `MyRidgeRegression.fit()` | 同上，梯度中额外加 (λ/n)·w（偏置项除外） |
| MSE / R² | MSE 越小越好，R² 越接近 1 越好 |

### 运行结果

| 模型 | MSE | R² |
|------|:---:|:---:|
| 基础线性回归 | 0.5559 | 0.5758 |
| 岭回归 (λ=1.0) | 0.5559 | 0.5758 |

> 两者 MSE 与 R² 完全一致。数据本身没有严重的过拟合或多重共线性，加入轻微 L2 惩罚不会对预测能力产生肉眼可见的影响。但基础回归权重和岭回归权重有轻微区别——L2 让权重整体变小并保持平滑，模型不再对某个单一特征过度敏感。

### 为什么偏置项不参与正则化？

如果连截距 b 也一起惩罚（强制接近 0），就相当于要求拟合直线必须经过原点 (0,0)，会导致严重欠拟合。偏置 w₀ 只控制预测基准线，不应被惩罚。

---

## 作业3 · SVM 鸢尾花分类

### 文件

| 文件 | 说明 |
|------|------|
| `Iris_SVM_Classifier.py` | 带 StandardScaler + 决策边界可视化，准确率 73.33% |
| `svm_3d.py` | 不做标准化，纯控制台输出，准确率 80.00% |

### 数据来源

- Iris 数据集：`sklearn.datasets.load_iris()`

### 线性可分情况下的最优分类器

给定两个类别的点，存在无穷多条线能把它们分开。**SVM 选择的是到最近点的距离（margin）最大的那条。**

### 算法流程

1. `sklearn.datasets.load_iris()` 获取 Iris 数据集
2. 取前两个特征：花萼长度和花萼宽度
3. 按比例划分训练集和测试集（通常 7:3 或 8:2）
4. 可选：`StandardScaler` 特征缩放
5. 实例化 `SVC(kernel='linear', C=1.0, random_state=42)` — 线性核
6. 训练完毕后预测测试集并输出分类报告

> 在工程项目中，通常还会插入超参数调优环节：用网格搜索 (Grid Search) + 交叉验证自动尝试参数组合（调整 C 值、尝试 RBF 核），找到最优配置。

### 运行结果对比

#### Iris_SVM_Classifier.py (有标准化)

```
Accuracy: 0.7333

              precision    recall  f1-score   support
      setosa       1.00      1.00      1.00        19
  versicolor       0.54      0.54      0.54        13
   virginica       0.54      0.54      0.54        13
    accuracy                           0.73        45
```

#### svm_3d.py (无标准化)

```
Accuracy: 0.8000

              precision    recall  f1-score   support
      setosa       1.00      1.00      1.00        19
  versicolor       0.70      0.54      0.61        13
   virginica       0.62      0.77      0.69        13
    accuracy                           0.80        45
```

### 结果分析：为什么不做标准化反而更准？

| 原因 | 说明 |
|------|------|
| 天然可比特征 | 花萼长度和宽度都是厘米级（4~8 范围），没必要做标准化 |
| 小样本偏差 | 测试集经过"带偏差的变换"后，分布与训练集不完全一致，导致泛化变差 |

> **启示：标准化不是默认必做的。当特征量纲已经一致时，先跑无标准化 baseline 对比。**

### 冷知识：random_state=42 为什么是 42？

在科幻名著《银河系漫游指南》中，42 被设定为"生命、宇宙以及一切终极问题的答案"。

---

## 作业4 · K-Means 聚类

### 文件

| 文件 | 说明 |
|------|------|
| `Kmeans_Exp.ipynb` | 手写完整 K-Means 各组件 + 肘部法则 k-cost 曲线 |
| `cluster_dataset.mat` | MATLAB 格式聚类数据集 |

### 数据来源

- `cluster_dataset.mat` — MATLAB 格式，课程提供

### 算法原理

监督学习有 y 告诉你"分得对不对"，聚类没有。K-Means 的突破口是：**定义一个"内部紧凑度"的量化指标，然后优化它。**

目标函数：

```
J = (1/n) · Σᵢ ||xᵢ - μ_{c(i)}||²
```

其中 μ_{c(i)} 是点 xᵢ 所属簇的中心。这个函数衡量"每个点到它所属中心的平均距离"。

### 算法流程

```
给定 k → 选 k 个初始质心
  │
  ▼
将每个点分配到距离最近的质心，形成 K 个簇
  │
  ▼
对每个簇计算均值，得到新的聚类中心
  │
  ▼
重复上面两步，直到所有质心不再变化 (收敛)
```

无监督学习代表算法。通过"分配 → 更新中心 → 再分配"迭代，收敛到局部最优簇划分。

### 运行结果

- k=3 设定下约 10 轮收敛
- k-cost 曲线肘部落在 k=3，验证预设合理性

---

## 学习总结：从规则到数据

```
作业1 (A*)
  │  输入：地图规则 + 确定的代价函数
  │  输出：确定性最优路径
  │  本质：人给出完整规则，算法执行搜索
  │
  ▼
作业2 (线性回归 & 岭回归)
  │  输入：特征 + 标签（数据）
  │  输出：拟合数据的权重
  │  本质：从数据中学规则，正则化 = "不完全相信数据"
  │
  ▼
作业3 (SVM)
  │  输入：特征 + 标签
  │  输出：最大化 margin 的分类面
  │  本质：主动放弃完美拟合，换取泛化——"不信任数据的每一个细节"
  │
  ▼
作业4 (K-Means)
  │  输入：只有特征，没有标签
  │  输出：数据的内在分组结构
  │  本质：连标签都不要，让数据自己说话
```

> 从"人规定一切"到"数据驱动"再到"无监督自主发现"——每一步都在减少人对模型的直接控制，增加数据自身的话语权。这也正是机器学习作为一个领域的核心进化方向。

---

## 通用工具与框架

- [NumPy 官方文档](https://numpy.org/doc/) — 所有作业的基础数值计算库
- [Matplotlib 官方文档](https://matplotlib.org/stable/) — 可视化绘图基础库
- [scikit-learn 官方文档](https://scikit-learn.org/stable/) — 作业 2/3/4 的数据加载、预处理和对比实现
- [Python 官方教程](https://docs.python.org/zh-cn/3/tutorial/) — 代码语言限制为 C++/Python 的参考基础
