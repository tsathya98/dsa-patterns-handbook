# Linked list fundamentals

If linked lists feel slippery, the confusion usually comes down to two things: how nodes sit in memory and what a pointer assignment actually changes.

## Array vs. linked list in memory

In an array `[10, 20, 30]`, memory is allocated in one contiguous block:
- Address 101: `10`
- Address 102: `20`
- Address 103: `30`

Because the items sit side by side, jumping to index `2` is instant math (`101 + 2 = 103`) in $\mathcal{O}(1)$ time. Inserting a new item at the front, however, forces every element to shift one spot to the right in $\mathcal{O}(n)$ time.

In a linked list, nodes can live anywhere in memory. Each node holds its own value and the memory address of the next node:
- Address `0x100`: value is `10`, next node is at `0x850`.
- Address `0x850`: value is `20`, next node is at `0x320`.
- Address `0x320`: value is `30`, next node is `None`.

```text
[ Address: 0x100 ]        [ Address: 0x850 ]        [ Address: 0x320 ]
┌────────┬───────┐        ┌────────┬───────┐        ┌────────┬───────┐
│ val: 10│ 0x850 ├───────►│ val: 20│ 0x320 ├───────►│ val: 30│ None  │
└────────┴───────┘        └────────┴───────┘        └────────┴───────┘
```

A singly linked node has no idea what came before it. It only knows its own `val` and its `.next` pointer.

## Node anatomy in Python

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val     # The data stored in this node
        self.next = next   # Reference to the next ListNode (or None)
```

When you write:
```python
node_a = ListNode(10)
node_b = ListNode(20)
node_a.next = node_b
```
you are wiring `node_a`'s pointer so it leads to `node_b`.

## The two pointer operations

Most linked list bugs happen when these two lines get mixed up:

### 1. Mutating the wire (`curr.next = ...`)
When `.next` is on the left side of `=`, you are physically changing where a node's outgoing arrow points in memory. For example, `curr.next = ListNode(5)` attaches a new node right after `curr`.

### 2. Moving your finger (`curr = curr.next`)
When a variable name is on the left side of `=`, no nodes in memory change. You are just moving your `curr` label one step forward along the existing chain.

```text
Before:
  [ Node 1 ] ────► [ Node 2 ]
      ▲
      │
     curr

Operation: curr = curr.next

After:
  [ Node 1 ] ────► [ Node 2 ]
                       ▲
                       │
                      curr   (The list did not change; only the label moved)
```

## Why losing the head loses the list

Variables in Python are labels pointing to objects in memory. Given `head -> [1] -> [2] -> [3] -> None`, if you run `head = head.next` without saving another reference to `[1]`, nothing points to `[1]` anymore. Since arrows only go forward, you can never walk back to `[1]`, and garbage collection reclaims it.

## The dummy node pattern

Whenever you build a new linked list or might delete/replace the original head node, start with a dummy node.

Think of `dummy` as a wooden stake hammered into the ground at the start of a train track, and `curr` as the worker walking down the track attaching new cars:
1. `dummy` stays at the front forever so you never lose the start of the list.
2. `curr` starts at `dummy`, hooks on each new node (`curr.next = ...`), and steps onto it (`curr = curr.next`).

```python
dummy = ListNode(0)  # Anchor at the front
curr = dummy         # Worker starts at the anchor

for val in [10, 20, 30]:
    curr.next = ListNode(val)  # 1. Attach new node
    curr = curr.next           # 2. Step onto the new node

return dummy.next              # Real head sits right after the dummy stake
```
