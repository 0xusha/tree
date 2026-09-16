import cv2
import numpy as np
import math
import sys

# Setup the canvas (800x600, dark background)
width, height = 800, 600
canvas = np.zeros((height, width, 3), dtype=np.uint8)
canvas[:] = (30, 15, 30)  # Dark purple background

def draw_blossom_tree(img, x, y, angle, length):
    # Base case
    if length < 10:
        return

    x_end = int(x + length * math.cos(angle))
    y_end = int(y + length * math.sin(angle))

    # Draw the brown branch
    thickness = max(1, int(length / 12))
    cv2.line(img, (x, y), (x_end, y_end), (60, 80, 110), thickness) # BGR Brown

    # Randomly choose between Red and Orange for the blossoms
    if np.random.rand() > 0.5:
        base_color = (30, 30, 230)   # BGR for Red
        highlight_color = (130, 130, 255) # Lighter Red highlight
    else:
        base_color = (30, 140, 255)  # BGR for Orange
        highlight_color = (130, 200, 255) # Lighter Orange highlight

    blossom_radius = max(2, int(length / 10))
    cv2.circle(img, (x_end, y_end), blossom_radius, base_color, -1)
    
    # Add a "shiny" highlight (Smaller, brighter circle offset to the top-left)
    if blossom_radius > 1:
        highlight_radius = max(1, int(blossom_radius * 0.4))
        cv2.circle(img, (x_end - 1, y_end - 1), highlight_radius, highlight_color, -1)

    # Animate - Updating for every single branch (Original slow speed)
    cv2.imshow("OpenCV Blossom Tree", img)
    if cv2.waitKey(1) & 0xFF == 27:
        sys.exit()

    # Next branches
    new_length = length * 0.8
    angle_offset = math.radians(20)

    draw_blossom_tree(img, x_end, y_end, angle - angle_offset, new_length)
    draw_blossom_tree(img, x_end, y_end, angle + angle_offset, new_length)

def draw_proposal(img):
    skin_color = (172, 212, 255) # BGR for pale peach
    
    # Add a little patch of grass first so they stand on it
    cv2.ellipse(img, (width // 2, 600), (160, 25), 0, 180, 360, (70, 150, 70), -1)

    # --- GIRL (Right side, facing left, surprised) ---
    gx, gy = 420, 470 
    
    # Legs
    cv2.line(img, (gx - 8, 550), (gx - 8, 590), skin_color, 5)
    cv2.line(img, (gx + 8, 550), (gx + 8, 590), skin_color, 5)
    
    # Yellow Frock
    yellow_color = (50, 220, 250) 
    dress_points = np.array([[gx + 2, 485], [gx - 25, 560], [gx + 20, 560]], np.int32)
    cv2.fillPoly(img, [dress_points], yellow_color)
    
    # Head and Long Hair
    hair_color = (40, 50, 80)
    cv2.circle(img, (gx, gy), 14, skin_color, -1) # Head
    cv2.circle(img, (gx + 6, gy - 2), 15, hair_color, -1) # Top volume
    cv2.ellipse(img, (gx + 12, gy + 30), (10, 45), 12, 0, 360, hair_color, -1) # Long hair down back
    
    # Flower in hair (Red to match the tree)
    flower_color = (30, 30, 230)
    cv2.circle(img, (gx + 12, gy - 6), 4, flower_color, -1)
    cv2.circle(img, (gx + 12, gy - 6), 1, (255, 255, 255), -1) # White center
    
    # Arm (Hands covering mouth in surprise)
    cv2.line(img, (gx - 2, 495), (gx - 12, 515), skin_color, 4) # Upper arm
    cv2.line(img, (gx - 12, 515), (gx - 16, 480), skin_color, 4) # Forearm up to face

    # --- BOY (Left side, facing right, kneeling) ---
    bx, by = 345, 500 
    shirt_color = (245, 245, 245) # White (slightly off-white for depth)
    pants_color = (20, 20, 20)    # Black
    
    # Back Leg (Kneeling on the grass - Black Pants)
    cv2.line(img, (bx, 545), (bx, 585), pants_color, 9) # Thigh
    cv2.line(img, (bx, 585), (bx - 30, 585), pants_color, 9) # Calf
    
    # Front Leg (Planted foot forward - Black Pants)
    cv2.line(img, (bx, 545), (bx + 30, 545), pants_color, 9) # Thigh
    cv2.line(img, (bx + 30, 545), (bx + 30, 590), pants_color, 9) # Calf
    
    # Torso (White Shirt)
    cv2.line(img, (bx - 2, 510), (bx, 545), shirt_color, 16)

    # Head and Hair
    cv2.circle(img, (bx, by), 14, skin_color, -1)
    cv2.ellipse(img, (bx - 3, by - 6), (14, 11), -15, 0, 360, (20, 30, 40), -1) 
    
    # Arm (White sleeve reaching out + skin-colored hand holding the ring)
    cv2.line(img, (bx, 515), (bx + 28, 523), shirt_color, 7) # Sleeve
    cv2.line(img, (bx + 28, 523), (bx + 40, 525), skin_color, 4) # Hand
    
    # --- THE RING BOX ---
    box_x, box_y = bx + 42, 523
    cv2.rectangle(img, (box_x - 3, box_y - 4), (box_x + 3, box_y + 2), (50, 50, 220), -1) # Red box

def main():
    print("Growing blossom tree... Press ESC in the window to stop early.")
    
    start_x = width // 2
    start_y = 600
    initial_length = 120
    initial_angle = -math.pi / 2 

    # 1. Draw the Tree
    draw_blossom_tree(canvas, start_x, start_y, initial_angle, initial_length)
    
    # 2. Draw the Proposal Scene
    draw_proposal(canvas)
    
    # 3. Cinematic Flower Drizzle
    print("Starting cinematic flower drizzle... Press ESC on the image window to close.")
    
    # Save the static background with the tree and couple
    background = canvas.copy()
    
    # Generate random initial positions and physics for petals
    petals = []
    for _ in range(40):
        petals.append([
            np.random.randint(150, 650),      # X bounded roughly to the tree canopy width
            np.random.randint(100, 400),      # Y bounded roughly to the tree canopy height
            np.random.uniform(-1.5, 1.5),     # Initial X velocity
            np.random.uniform(1.5, 3.5),      # Initial Y velocity
            np.random.randint(2, 6),          # Size
            np.random.randint(0, 2)           # Color Flag (0 = Red, 1 = Orange)
        ])
        
    # Animation loop
    while True:
        frame = background.copy()
        
        for p in petals:
            # Move petal
            p[0] += p[2]
            p[1] += p[3]
            
            # Add a slight "wind" sway effect
            p[2] += np.random.uniform(-0.1, 0.1)
            p[2] = max(-2.0, min(2.0, p[2])) # Cap horizontal speed
            
            # Reset petal if it falls below the screen bounds
            if p[1] > height:
                p[0] = np.random.randint(150, 650) # Respawn within the canopy width
                p[1] = np.random.randint(100, 300) # Respawn within the canopy height
                p[2] = np.random.uniform(-1.5, 1.5)
                p[5] = np.random.randint(0, 2)     # Pick a new color upon respawn
                
            # Pick color based on flag
            if p[5] == 0:
                base_color = (30, 30, 230)     # Red
                highlight_color = (130, 130, 255)
            else:
                base_color = (30, 140, 255)    # Orange
                highlight_color = (130, 200, 255)

            # Draw the petal base
            px, py = int(p[0]), int(p[1])
            petal_radius = int(p[4])
            cv2.circle(frame, (px, py), petal_radius, base_color, -1) 
            
            # Add shiny highlight to the falling petals
            if petal_radius > 2:
                highlight_radius = max(1, int(petal_radius * 0.4))
                cv2.circle(frame, (px - 1, py - 1), highlight_radius, highlight_color, -1)
            
        cv2.imshow("OpenCV Blossom Tree", frame)
        
        # 30 ms delay gives ~33 frames per second for smooth falling animation
        if cv2.waitKey(30) & 0xFF == 27:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()