"""
Red-Black Tree Visualizer
A Python implementation of Red-Black Tree with graphical visualization.

Author: Your Name
GitHub: https://github.com/YOUR_USERNAME/red-black-tree-visualizer
License: MIT
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import sys
import argparse


class Node:
    """Node class for Red-Black Tree"""
    
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.color = 'RED'
        self.parent = None
    
    def __str__(self):
        return f"Node({self.key}, {self.color})"


class RedBlackTree:
    """Red-Black Tree implementation with self-balancing properties"""
    
    def __init__(self):
        self.NIL = Node(None)
        self.NIL.color = 'BLACK'
        self.root = self.NIL
    
    def insert(self, key):
        """Insert a new key into the tree"""
        node = Node(key)
        node.left = self.NIL
        node.right = self.NIL
        
        parent = None
        current = self.root
        
        while current != self.NIL:
            parent = current
            if node.key < current.key:
                current = current.left
            else:
                current = current.right
        
        node.parent = parent
        
        if parent is None:
            self.root = node
        elif node.key < parent.key:
            parent.left = node
        else:
            parent.right = node
        
        node.color = 'RED'
        self.fix_insert(node)
    
    def fix_insert(self, node):
        """Fix Red-Black Tree properties after insertion"""
        while node.parent and node.parent.color == 'RED':
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                
                if uncle.color == 'RED':
                    node.parent.color = 'BLACK'
                    uncle.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    
                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    self.right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                
                if uncle.color == 'RED':
                    node.parent.color = 'BLACK'
                    uncle.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    
                    node.parent.color = 'BLACK'
                    node.parent.parent.color = 'RED'
                    self.left_rotate(node.parent.parent)
        
        self.root.color = 'BLACK'
    
    def left_rotate(self, x):
        """Perform left rotation"""
        y = x.right
        x.right = y.left
        
        if y.left != self.NIL:
            y.left.parent = x
        
        y.parent = x.parent
        
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        y.left = x
        x.parent = y
    
    def right_rotate(self, y):
        """Perform right rotation"""
        x = y.left
        y.left = x.right
        
        if x.right != self.NIL:
            x.right.parent = y
        
        x.parent = y.parent
        
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        
        x.right = y
        y.parent = x
    
    def inorder_traversal(self):
        """Return in-order traversal of the tree"""
        result = []
        self._inorder_helper(self.root, result)
        return result
    
    def _inorder_helper(self, node, result):
        """Helper function for in-order traversal"""
        if node != self.NIL:
            self._inorder_helper(node.left, result)
            result.append((node.key, node.color))
            self._inorder_helper(node.right, result)


def parse_parenthetic(s):
    """
    Parse parenthetic notation like: (5(3(1)(4))(8(7)(9)))
    Returns list of values
    """
    s = s.strip()
    if not s or s == '()':
        return []
    
    values = []
    current_num = ''
    
    for char in s:
        if char.isdigit() or char == '-':
            current_num += char
        elif char in '()':
            if current_num:
                values.append(int(current_num))
                current_num = ''
    
    if current_num:
        values.append(int(current_num))
    
    return values


def get_tree_positions(node, x=0, y=0, layer=1, pos_dict=None, x_offset=None):
    """Calculate positions for each node in the tree"""
    if pos_dict is None:
        pos_dict = {}
    
    if x_offset is None:
        x_offset = {'offset': 0}
    
    if node and node.key is not None:
        if node.left and node.left.key is not None:
            get_tree_positions(node.left, x, y - 1, layer + 1, pos_dict, x_offset)
        
        pos_dict[node.key] = (x_offset['offset'], y)
        x_offset['offset'] += 1
        
        if node.right and node.right.key is not None:
            get_tree_positions(node.right, x, y - 1, layer + 1, pos_dict, x_offset)
    
    return pos_dict


def draw_tree(rb_tree, save_path=None):
    """
    Draw the Red-Black tree graphically
    
    Args:
        rb_tree: RedBlackTree instance
        save_path: Optional path to save the image
    """
    if rb_tree.root == rb_tree.NIL:
        print("Tree is empty!")
        return
    
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_aspect('equal')
    
    positions = get_tree_positions(rb_tree.root)
    
    def draw_node(node, pos_dict):
        """Recursively draw nodes and edges"""
        if node and node.key is not None:
            x, y = pos_dict[node.key]
            
            color = '#FF4444' if node.color == 'RED' else '#333333'
            text_color = 'white'
            
            circle = plt.Circle((x, y), 0.3, color=color, ec='black', 
                              linewidth=2, zorder=3)
            ax.add_patch(circle)
            
            ax.text(x, y, str(node.key), ha='center', va='center', 
                   fontsize=12, fontweight='bold', color=text_color, zorder=4)
            
            if node.left and node.left.key is not None:
                x_left, y_left = pos_dict[node.left.key]
                ax.plot([x, x_left], [y, y_left], 'k-', linewidth=2, zorder=1)
                draw_node(node.left, pos_dict)
            
            if node.right and node.right.key is not None:
                x_right, y_right = pos_dict[node.right.key]
                ax.plot([x, x_right], [y, y_right], 'k-', linewidth=2, zorder=1)
                draw_node(node.right, pos_dict)
    
    draw_node(rb_tree.root, positions)
    
    red_patch = mpatches.Patch(color='#FF4444', label='RED')
    black_patch = mpatches.Patch(color='#333333', label='BLACK')
    ax.legend(handles=[red_patch, black_patch], loc='upper right', fontsize=12)
    
    ax.set_xlim(min(x for x, y in positions.values()) - 1, 
                max(x for x, y in positions.values()) + 1)
    ax.set_ylim(min(y for x, y in positions.values()) - 1, 
                max(y for x, y in positions.values()) + 1)
    
    ax.axis('off')
    ax.set_title('Red-Black Tree Visualization', fontsize=16, 
                fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\n✓ Image saved to: {save_path}")
    
    plt.show()


def print_header():
    """Print program header"""
    print("=" * 70)
    print(" " * 15 + "Red-Black Tree Visualizer")
    print("=" * 70)


def print_tree_structure(rb_tree):
    """Print tree structure in console"""
    print("\n" + "=" * 70)
    print("Tree Structure (In-order Traversal):")
    print("=" * 70)
    
    traversal = rb_tree.inorder_traversal()
    for key, color in traversal:
        color_symbol = '🔴' if color == 'RED' else '⚫'
        print(f"  {color_symbol} {key:4d} ({color})")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Red-Black Tree Visualizer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python red_black_tree.py
  python red_black_tree.py --input "5,3,8,1,4,7,9"
  python red_black_tree.py --input "(5(3(1)(4))(8(7)(9)))"
  python red_black_tree.py --input "5,3,8" --save output.png
        """
    )
    
    parser.add_argument('--input', '-i', type=str,
                       help='Input values (parenthetic or comma-separated)')
    parser.add_argument('--save', '-s', type=str,
                       help='Save visualization to file')
    
    args = parser.parse_args()
    
    print_header()
    
    if args.input:
        user_input = args.input
    else:
        print("\nEnter tree in one of these formats:")
        print("  1. Parenthetic notation: (5(3(1)(4))(8(7)(9)))")
        print("  2. Comma-separated: 5,3,8,1,4,7,9")
        print("=" * 70)
        user_input = input("\nInput: ").strip()
    
    if not user_input:
        print("❌ No input provided!")
        return
    
    # Parse input
    if '(' in user_input:
        values = parse_parenthetic(user_input)
    else:
        try:
            values = [int(x.strip()) for x in user_input.split(',') if x.strip()]
        except ValueError:
            print("❌ Invalid input format!")
            return
    
    if not values:
        print("❌ No valid values found!")
        return
    
    print(f"\n✓ Extracted values: {values}")
    
    # Build tree
    rb_tree = RedBlackTree()
    
    print("\nBuilding Red-Black Tree...")
    for value in values:
        rb_tree.insert(value)
        print(f"  ✓ Inserted: {value}")
    
    # Print structure
    print_tree_structure(rb_tree)
    
    # Visualize
    print("\n" + "=" * 70)
    print("Generating graphical visualization...")
    print("=" * 70)
    
    draw_tree(rb_tree, save_path=args.save)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Program interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)