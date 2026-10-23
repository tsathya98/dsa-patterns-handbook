# BFS vs. DFS Cheat Sheet

## 1. The Difference in One Line
- **BFS (Breadth-First Search):** Explores layer by layer (all distance-1 neighbors, then distance-2). Uses a **Queue (`collections.deque`)**.
- **DFS (Depth-First Search):** Plunges all the way down one branch until it hits a dead end, then backtracks. Uses the **Call Stack (recursion)** or an explicit stack.

---

## 2. Which one should you pick?

| Problem Goal | Pick | Why |
| :--- | :--- | :--- |
| **Shortest path / minimum steps** in an unweighted graph or grid | **BFS** | First time you reach the target, you are guaranteed it took the fewest steps. |
| **Level-by-level** tree traversal | **BFS** | Queue naturally groups nodes by depth level. |
| **Max depth / path sum / subtree property** | **DFS** | Clean 3-line recursion (`1 + max(dfs(l), dfs(r))`). |
| **Count connected components / islands** | **DFS** (or BFS) | Recursive flood-fill is shorter to write. |
| **Detect cycles or topological sort** | **DFS** (or Kahn's BFS) | Tracks recursion stack ancestors easily. |

### Decision rules:
* **1. Shortest path or level-order exploration:** Choose BFS using a double-ended queue (`collections.deque`). Mark visited nodes immediately when pushing onto the queue to prevent redundant explorations, guaranteeing shortest unweighted distance in $\mathcal{O}(V + E)$ time.
* **2. Tree depth, exhaustive paths, or topological sorting:** Choose DFS using recursion or an explicit stack. Explore branch depth completely before backtracking, marking nodes visited on function entry.
* **3. Connected components and flood-fill:** Use either BFS or DFS. Prefer recursive DFS for conciseness or iterative BFS if call stack depth risks exceeding recursion limits.


---

## 3. Core Templates

### BFS Template (Level-by-Level Queue)
Always use `collections.deque` so `popleft()` is $\mathcal{O}(1)$. Never use `list.pop(0)`, which shifts the entire list in $\mathcal{O}(n)$ time.

```python
from collections import deque

def bfs_levels(root):
    if not root:
        return []

    queue = deque([root])
    levels = []

    while queue:
        level_size = len(queue)  # Snapshot current level width
        cur_level = []

        for _ in range(level_size):
            node = queue.popleft()
            cur_level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        levels.append(cur_level)

    return levels
```

### DFS Template (Grid Flood-Fill, LC 200 Number of Islands)
```python
def numIslands(grid: list[list[str]]) -> int:
    rows, cols = len(grid), len(grid[0])
    islands = 0

    def dfs(r: int, c: int) -> None:
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'  # Mark visited immediately
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                islands += 1

    return islands
```

---

## 4. Common Traps
1. **Forgetting to mark `visited` in graphs/grids:** Trees have no cycles, so you don't need a `visited` set. Graphs and 2D grids have cycles (`A <-> B`), so forgetting `visited` causes an infinite loop or `RecursionError`.
2. **Marking `visited` too late in BFS:** In grid/graph BFS, add nodes to `visited` **at the moment you push them into the queue**, not when you pop them. Waiting until `popleft()` lets multiple neighbors push the same node into the queue dozens of times and causes TLE.
