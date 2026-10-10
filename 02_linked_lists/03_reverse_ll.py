class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head: ListNode) -> ListNode:
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev        

def print_list(head: ListNode) -> None:
    curr = head
    while curr:
        print(curr.val, end=" -> ")
        curr = curr.next
    print("None")
    
if __name__ == "__main__":
    # creating a linked list 1->2->3->4->5
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    head.next.next.next = ListNode(4)
    head.next.next.next.next = ListNode(5)
    
    # printing the linked list
    print_list(head)
    
    # reversing the linked list
    head = reverse_list(head)
    
    # printing the reversed linked list
    print_list(head)