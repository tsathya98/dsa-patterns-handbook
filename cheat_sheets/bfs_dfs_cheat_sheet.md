# 🌲 BFS vs. DFS Master Cheat Sheet & Decision Guide

> **Pattern:** Tree & Graph Traversal (Breadth-First Search vs. Depth-First Search)  
> **Audience:** Complete Beginner / 1st-Year CS Student  
> **Analogies:** The Water Ripple (BFS) vs. The Maze Runner (DFS)

---

## 💡 1. What Are Trees and Graphs in Plain English?

* A **Node (Vertex)** = A city, a webpage, or a number in a circle.
* An **Edge** = A road or link connecting two nodes.
* A **Tree** = A graph with no cycles (it branches out like an upside-down family tree from the `root`).

When you want to visit every room in a building, there are two distinct strategies:
1. **BFS (Breadth-First Search):** Explore all immediate neighboring rooms on your current floor before going up to the next floor.
2. **DFS (Depth-First Search):** Pick one hallway and walk as far as you can until you hit a dead end, then backtrack and try the next hallway.

---

## 🌊 2. BFS: The Breadth-First Search

```text
               ( 1 )              Level 0 (Start)
             /       \
          ( 2 )     ( 3 )         Level 1 (Neighbors of 1)
          /   \     /   \
        (4)   (5) (6)   (7)       Level 2 (Neighbors of 2 & 3)

BFS Visit Order: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 (Layer by Layer!)
```

### 💡 The Big Superpower of BFS
> **In unweighted graphs or grids, BFS GUARANTEES the SHORTEST path!**  
> Why? Because it checks everything at distance 1, then distance 2, then distance 3. The first time you reach your target, you are 100% guaranteed it took the fewest possible steps.

### ⚙️ Data Structure: **Queue (`collections.deque`)** — First In, First Out (FIFO)

#### ⚙️ BFS Template (Level-by-Level)
```python
from collections import deque

def bfs(root):
    if not root:
        return []
    
    queue = deque([root])
    results = []
    
    while queue:
        level_size = len(queue)
        current_level = []
        
        # Process every node at the CURRENT level
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
                
        results.append(current_level)
        
    return results
```

---

## 🌲 3. DFS: The Depth-First Search

```text
               ( 1 )
             /       \
          ( 2 )     ( 5 )
          /   \
        (3)   (4)

DFS Visit Order: 1 -> 2 -> 3 (hits dead end, backtracks) -> 4 -> 5
```

### 💡 The Big Superpower of DFS
> **DFS is great for exploring complete paths, checking connectivity, and counting regions.**  
> It uses almost no extra memory for shallow branches and writes very elegantly using **Recursion**.

### ⚙️ Data Structure: **Call Stack (Recursion)**

#### ⚙️ DFS Template (e.g. *Number of Islands* - LC 200)
```python
def numIslands(grid: list[list[str]]) -> int:
    if not grid:
        return 0
        
    rows, cols = len(grid), len(grid[0])
    islands = 0
    
    def dfs(r, c):
        # 1. Base case: out of bounds or water ('0')
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
            
        # 2. Sink the land (mark visited so we don't re-visit!)
        grid[r][c] = '0'
        
        # 3. Explore 4 directions: Up, Down, Left, Right
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)      # Sinks the whole connected island
                islands += 1   # Count 1 island
                
    return islands
```

---

## 🏆 4. When to Use BFS vs. DFS (The Decision Table)

| Problem Clue | Which to Pick? | Why? |
|---|---|---|
| *"Find the **shortest** path / minimum steps"* | **BFS** | BFS explores by distance layer-by-layer; first arrival is shortest. |
| *"Traverse level-by-level"* | **BFS** | Natural fit for a queue. |
| *"Find if **any** path exists from A to B"* | **DFS** | Just dive deep until you find it; less queue overhead. |
| *"Find maximum depth of binary tree"* | **DFS** | 3 lines of recursion: `1 + max(dfs(left), dfs(right))`. |
| *"Count connected components / islands"* | **DFS** (or BFS) | DFS flood-fill is simpler to write. |

---

## ⚠️ 5. The #1 Beginner Trap: The Infinite Loop

In a graph or grid, nodes can point back to each other: `A -> B -> A -> B...`
* **Always maintain a `visited` set (or mark visited in-place like `grid[r][c] = '0'`).**
* If you forget to record visited nodes, your BFS/DFS will loop infinitely and crash!
