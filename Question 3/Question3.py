#import turtle module
import turtle


def draw_tree(t, branch_length, angle_left, angle_right, depth, reduction_factor, total_depth):
    
    
    # Base case - stop when depth is 0
    if depth == 0:
        return
    
    # Set trunk color and thickness
    if depth == total_depth:
        t.color("brown")
        t.pensize(10) 
        
    # Set branch color and varying thickness
    else:
        t.color("green")
        t.pensize(max(1, depth)) 
    
    # Draw current branch
    t.forward(branch_length)
    
    # Create left branch recursively
    t.left(angle_left)
    draw_tree(t, branch_length * reduction_factor,  
              angle_left, angle_right, depth - 1,
              reduction_factor, total_depth)
    t.right(angle_left)
    
    # Create right branch recursively
    t.right(angle_right)
    draw_tree(t, branch_length * reduction_factor, 
              angle_left, angle_right, depth - 1,
              reduction_factor, total_depth)
    t.left(angle_right)
    
    # Return to branch start position
    t.backward(branch_length)


def draw_trunk(t, length):
    # Draw the main trunk of the tree
    t.color("brown")
    t.pensize(5)  
    t.penup()
    t.goto(0, -200) 
    t.pendown()
    t.setheading(90) 
    t.forward(length) 

# Get user input for tree parameters
def main():
    angle_left = int(input("Enter the left branch angle (degrees): "))     
    angle_right = int(input("Enter the right branch angle (degrees): "))    
    branch_length = int(input("Enter the starting branch length (pixels): ")) 
    depth = int(input("Enter the recursion depth: "))                        

    # Validate reduction factor input    
    while True:
        reduction_factor = float(input("Enter the branch length reduction factor (e.g., 0.7): ").strip())
        if 0 < reduction_factor < 1:
            break
        print("Reduction factor must be between 0 and 1. Try again.")

    # Setup drawing window    
    screen = turtle.Screen()
    screen.title("Recursive Tree")
    screen.bgcolor("white")

    # Initialize turtle settings    
    t = turtle.Turtle()
    t.speed(5)      
    t.penup()
    t.goto(0, -200) 
    t.left(90)      
    t.pendown()

    # Draw tree branches    
    draw_tree(t, branch_length, angle_left, angle_right,
              depth, reduction_factor, depth)
    
    # Draw main trunk
    draw_trunk(t, branch_length)
    
    # Keep window open
    screen.mainloop()
    
# Start program if run directly
if __name__ == "__main__":
    main()