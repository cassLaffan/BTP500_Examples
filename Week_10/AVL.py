import queue
import random
'''
Augumenting last week's BST such that it will be height balanced,
thus becoming an AVL tree.

A tree is height balanced if for every node within the
tree, the height of its right and left subtrees differ by no
more than one.

In the case of the AVL tree, the balance of a node is calculated:

Node's balance = height of right - height of left
     of node        subtree          subtree
'''

class AVL_Tree:
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None
        self.balance = 0    # Use to check the balance factor...

    def copy(self, other):
        self.data = other.data
        self.left = other.left
        self.right = other.right
        self.balance = other.balance

    def reBalance_helper(self):
        """Helper function to handle re-balancing of the tree"""
        if self.balance == -2:  # Left-heavy :- Need to rotate right.
            if self.left and self.left.balance == 1:  # Left-Right case :- left child is right heavy
                self.left.left_rotate()
            return self.right_rotate()  # Rotate right
        elif self.balance == 2:  # Right-heavy :- need to rotate left.
            if self.right and self.right.balance == -1:  # Right-Left case :- right child is left heavy
                self.right.right_rotate()
            return self.left_rotate()   # Rotate Left
        return self

    def left_rotate(self):
        """Fixed left rotation implementation"""
        if not self.right:  # if there is no right child, rotation not possible
            return self
        new_left = AVL_Tree()
        new_left.copy(self)
        new_left.left = self.left
        new_left.right = self.right.left
        self.copy(self.right)
        self.left = new_left

        # help
        if self.balance == 1 and self.left.balance == 2:
            self.balance = 0
            self.left.balance = 0
        elif self.balance == 1 and self.left.balance == 1:
            self.balance = -1
            self.left.balance = -1
        elif self.balance == 0 and self.left.balance == 1:
            self.balance = -1
            self.left.balance = 0
        elif self.balance == 0 and self.left.balance == 2:
            self.balance = -1
            self.left.balance = 1
        elif self.balance == -1 and self.left.balance == 1:
            self.balance = -2
            self.left.balance = 0
        elif self.balance == 2 and self.left.balance == 2:
            self.balance = 0
            self.left.balance = -1
        else:
            print ("AARG")
            raise "a"
            


    def right_rotate(self):
        """Fixed right rotation implementation"""
        if not self.left:  # If there is no left child, rotation is not possible
            return self
        new_right = AVL_Tree()
        new_right.copy(self)
        new_right.right = self.right
        new_right.left = self.left.right
        self.copy(self.left)
        self.right = new_right

        # help
        if self.balance == -1 and self.right.balance == -2:
            self.balance = 0
            self.right.balance = 0
        elif self.balance == -1 and self.right.balance == -1:
            self.balance = 1
            self.right.balance = 1
        elif self.balance == 0 and self.right.balance == -1:
            self.balance = 1
            self.right.balance = 0
        elif self.balance == 0 and self.right.balance == -2:
            self.balance = 1
            self.right.balance = -1
        elif self.balance == 1 and self.right.balance == -1:
            self.balance = 2
            self.right.balance = 0
        elif self.balance == -2 and self.right.balance == -2:
            self.balance = 0
            self.right.balance = 1
        else:
            print ("AARG")
            raise "a"


    def insert(self, data):
        """Fixed insert implementation with proper balancing"""
        if self.data is None:  # If the current node is empty
            self.data = data
            return self

        # Insert the data into the left or right subtree depending on its value
        if data < self.data:
            if self.left:
                old_bal = self.left.balance
                self.left.insert(data)
                new_bal = self.left.balance
                if old_bal == 0 and abs(new_bal) == 1: # if left side gained a layer
                    self.balance -= 1
            else:
                self.left = AVL_Tree(data)
                self.balance -= 1
        elif data > self.data:
            if self.right:
                old_bal = self.right.balance
                self.right.insert(data)
                new_bal = self.right.balance
                if old_bal == 0 and abs(new_bal) == 1:
                    self.balance += 1
            else:
                self.right = AVL_Tree(data)
                self.balance += 1

        # Re-balance if necessary (the balance factor exceeds the limit)
        if abs(self.balance) > 1:
            self.reBalance_helper()

    def find_balance(self):
        """Calculate balance factor (only for delete atm)
        Time complexity: O(log n)
        """
        return (self.right.find_height() if self.right else 0) - (self.left.find_height() if self.left else 0)

    def find_height(self):
        """Correctly calculate height
        
        Time complexity: O(logn)"""
        return 1 + ((self.left.find_height() if self.left else 0) if self.balance < 0 else (self.right.find_height() if self.right else 0))

    def min_value_node(self):
        """Find minimum value node"""
        current = self
        while current.left:
            current = current.left
        return current

    def delete(self, data):
        """Fixed delete implementation with proper re-balancing"""
        if self.data is None:
            return self

        if data < self.data:   # If the data is smaller than the current node, delete from the left subtree
            if self.left:
                self.left = self.left.delete(data)
        elif data > self.data:  # If the data is larger than the current node, delete from the right subtree
            if self.right:
                self.right = self.right.delete(data)
        else:
            # Node with one child or no child
            if self.left is None:
                return self.right
            elif self.right is None:
                return self.left

            # Node with two children
            temp = self.right.min_value_node()   # Find the inorder successor (min value node in right subtree)
            self.data = temp.data   # Replace the current node's data with the inorder successor's data
            self.right = self.right.delete(temp.data)   # Delete the inorder successor from the right subtree

        # Update balance
        self.balance = self.find_balance()

        # Re-balance if necessary
        if abs(self.balance) > 1:
            self.reBalance_helper()

        return self

    def search(self, data):
        """Search implementation remains the same"""
        if self.data is None:
            return False

        if self.data == data:
            return True
        elif data < self.data and self.left:
            return self.left.search(data)
        elif data > self.data and self.right:
            return self.right.search(data)
        return False

    # Your existing printing methods remain unchanged
    def inorder_print(self):
        if self.data:
            if self.left:
                self.left.inorder_print()
            print(self.data, end=" ")
            if self.right:
                self.right.inorder_print()

    def pre_order_print(self):
        if self.data:
            print(self.data, end=" ")
            if self.left:
                self.left.pre_order_print()
            if self.right:
                self.right.pre_order_print()

    def post_order_print(self):
        if self.data:
            if self.left:
                self.left.post_order_print()
            if self.right:
                self.right.post_order_print()
            print(self.data, end=" ")

    def breadth_first_print(self):
        the_nodes = queue.Queue()
        if self.data:
            the_nodes.put(self)
        while not the_nodes.empty():
            curr = the_nodes.get()
            if curr.left:
                the_nodes.put(curr.left)
            if curr.right:
                the_nodes.put(curr.right)
            print(curr.data, end=" ")

    def breadth_first_print_2(self):
        """tehe xd
        perhaps a helper function for string formatting would've been helpful"""
        max_digits = 5

        overall_spacing = (int)((max_digits + 3)/2)
        height = self.find_height()
        dummy = AVL_Tree(None)
        cur_row = queue.Queue()
        next_row = queue.Queue()
        print(" " * int(overall_spacing*2 * (2**(height - 2)) - overall_spacing), end="") # wacky maths
        print ('{:>{max_digits}}'.format(self.data, max_digits=max_digits), '{:>2}'.format(self.balance), end="")
        if self.data:
            cur_row.put(self)
        next_row_empty = not self.left and not self.right
        while not next_row_empty:
            height -= 1
            next_row_empty = True
            print()
            print(" " * int(overall_spacing*2 * (2**(height - 2)) - overall_spacing), end="") # wacky maths
            while not cur_row.empty():
                element = cur_row.get()

                if element.left:
                    print ('{:>{max_digits}}'.format(element.left.data, max_digits=max_digits), '{:>2}'.format(element.left.balance), end="")
                    next_row.put(element.left)
                    if element.left.left or element.left.right:
                        next_row_empty = False
                else:
                    print('{:>{max_digits}}'.format("_", max_digits=max_digits), '{:>2}'.format("_"), end="")
                    next_row.put(dummy)
                
                # spacing
                print(" " * int(overall_spacing*2 * (2**(height - 1) - 1)), end="")

                if element.right:
                    print ('{:>{max_digits}}'.format(element.right.data, max_digits=max_digits), '{:>2}'.format(element.right.balance), end="")
                    next_row.put(element.right)
                    if element.right.left or element.right.right:
                        next_row_empty = False
                else:
                    print('{:>{max_digits}}'.format("_", max_digits=max_digits), '{:>2}'.format("_"), end="")
                    next_row.put(dummy)
                    
                # spacing
                print(" " * int(overall_spacing*2 * (2**(height - 1) - 1)), end="")
            cur_row = next_row
            next_row = queue.Queue()
        print()



    def print_tree(self, prefix="", is_left=False):
        if self.data:
            print(prefix, end="")
            print("|__" if is_left else "|---", end="")
            print(f"{self.data} (b={self.balance})")
            if self.left:
                self.left.print_tree(prefix + ("|   " if is_left else "    "), True)
            if self.right:
                self.right.print_tree(prefix + ("|   " if is_left else "    "))


if __name__ == "__main__":
    # Create a new AVL tree
    avl = AVL_Tree(6)

    # Test multiple insertions
    values = [7, 10, 1, 3, -4, 8]
    for val in values:
        avl.insert(val)

    print("Initial tree:")
    print ("height:", avl.find_height())
    avl.print_tree()
    avl.breadth_first_print_2()

    # Test search
    print(f"\nIs 10 in the AVL Tree? {avl.search(10)}")
    print(f"Is -1 in the AVL Tree? {avl.search(-1)}")

    # Test height and balance
    #print(f"\nTree height: {avl.find_height()}")
    print(f"Root balance: {avl.balance}")

    # Test deletion
    print("\nDeleting 7...")
    avl.delete(7)
    avl.breadth_first_print_2()

    print(f"\nNew root balance: {avl.balance}")

    avl = AVL_Tree()
    vals = [_ for _ in range(30)]
    random.shuffle(vals)
    print ("randomized insertion order:", vals)
    for val in vals:
        avl.insert(val)
    avl.breadth_first_print_2()
    print("deleting 15")
    avl.delete(15)
    avl.breadth_first_print_2()
    for val in vals:
        if not avl.search(val):
            print(val, "not found~")