import cv2
import numpy as np
import math
import sys

width, height = 800, 600
screen_w, screen_h = 1920, 1200
canvas = np.zeros((height, width, 3), dtype=np.uint8)
canvas[:] = (30, 15, 30)

def draw_blossom_tree(img, x, y, angle, length):
    if length < 10:
        return

    x_end = int(x + length * math.cos(angle))
    y_end = int(y + length * math.sin(angle))
    
    thickness = max(1, int(length / 12))
    cv2.line(img, (x, y), (x_end, y_end), (60, 80, 110), thickness)

    if np.random.rand() > 0.5:
        base_color = (30, 30, 230)
        highlight_color = (130, 130, 255)
    else:
        base_color = (30, 140, 255)
        highlight_color = (130, 200, 255)

    blossom_radius = max(2, int(length / 10))
    cv2.circle(img, (x_end, y_end), blossom_radius, base_color, -1)
    
    if blossom_radius > 1:
        highlight_radius = max(1, int(blossom_radius * 0.4))
        cv2.circle(img, (x_end - 1, y_end - 1), highlight_radius, highlight_color, -1)

    cv2.imshow("OpenCV", cv2.resize(img, (screen_w, screen_h)))
    if cv2.waitKey(1) & 0xFF == 27:
        sys.exit()

    new_length = length * 0.8
    angle_offset = math.radians(20)

    draw_blossom_tree(img, x_end, y_end, angle - angle_offset, new_length)
    draw_blossom_tree(img, x_end, y_end, angle + angle_offset, new_length)

def draw_proposal(img):
    skin_color = (172, 212, 255)
    cv2.ellipse(img, (width // 2, 600), (160, 25), 0, 180, 360, (70, 150, 70), -1)

    gx, gy = 420, 470 
    
    cv2.line(img, (gx - 8, 550), (gx - 8, 590), skin_color, 5)
    cv2.line(img, (gx + 8, 550), (gx + 8, 590), skin_color, 5)
    
    yellow_color = (50, 220, 250) 
    dress_points = np.array([[gx + 2, 485], [gx - 25, 560], [gx + 20, 560]], np.int32)
    cv2.fillPoly(img, [dress_points], yellow_color)
    
    hair_color = (40, 50, 80)
    cv2.circle(img, (gx, gy), 14, skin_color, -1)
    cv2.circle(img, (gx + 6, gy - 2), 15, hair_color, -1)
    cv2.ellipse(img, (gx + 12, gy + 30), (10, 45), 12, 0, 360, hair_color, -1)
    
    flower_color = (30, 30, 230)
    cv2.circle(img, (gx + 12, gy - 6), 4, flower_color, -1)
    cv2.circle(img, (gx + 12, gy - 6), 1, (255, 255, 255), -1)
    
    cv2.line(img, (gx - 2, 495), (gx - 12, 515), skin_color, 4)
    cv2.line(img, (gx - 12, 515), (gx - 16, 480), skin_color, 4)

    bx, by = 345, 500 
    shirt_color = (245, 245, 245)
    pants_color = (20, 20, 20)
    
    cv2.line(img, (bx, 545), (bx, 585), pants_color, 9)
    cv2.line(img, (bx, 585), (bx - 30, 585), pants_color, 9)
    
    cv2.line(img, (bx, 545), (bx + 30, 545), pants_color, 9)
    cv2.line(img, (bx + 30, 545), (bx + 30, 590), pants_color, 9)
    
    cv2.line(img, (bx - 2, 510), (bx, 545), shirt_color, 16)

    cv2.circle(img, (bx, by), 14, skin_color, -1)
    cv2.ellipse(img, (bx - 3, by - 6), (14, 11), -15, 0, 360, (20, 30, 40), -1) 
    
    cv2.line(img, (bx, 515), (bx + 28, 523), shirt_color, 7)
    cv2.line(img, (bx + 28, 523), (bx + 40, 525), skin_color, 4)
    
    box_x, box_y = bx + 42, 523
    cv2.rectangle(img, (box_x - 3, box_y - 4), (box_x + 3, box_y + 2), (50, 50, 220), -1)

def main():
    cv2.namedWindow("OpenCV", cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
    cv2.setWindowProperty("OpenCV", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    draw_blossom_tree(canvas, width // 2, 600, -math.pi / 2, 120)
    draw_proposal(canvas)
    
    background = canvas.copy()
    
    petals = []
    for _ in range(40):
        petals.append([
            np.random.randint(150, 650),
            np.random.randint(100, 400),
            np.random.uniform(-1.5, 1.5),
            np.random.uniform(1.5, 3.5),
            np.random.randint(2, 6),
            np.random.randint(0, 2)
        ])
        
    while True:
        frame = background.copy()
        
        for p in petals:
            p[0] += p[2]
            p[1] += p[3]
            
            p[2] += np.random.uniform(-0.1, 0.1)
            p[2] = max(-2.0, min(2.0, p[2]))
            
            if p[1] > height:
                p[0] = np.random.randint(150, 650)
                p[1] = np.random.randint(100, 300)
                p[2] = np.random.uniform(-1.5, 1.5)
                p[5] = np.random.randint(0, 2)
                
            if p[5] == 0:
                base_color = (30, 30, 230)
                highlight_color = (130, 130, 255)
            else:
                base_color = (30, 140, 255)
                highlight_color = (130, 200, 255)

            px, py = int(p[0]), int(p[1])
            petal_radius = int(p[4])
            cv2.circle(frame, (px, py), petal_radius, base_color, -1) 
            
            if petal_radius > 2:
                highlight_radius = max(1, int(petal_radius * 0.4))
                cv2.circle(frame, (px - 1, py - 1), highlight_radius, highlight_color, -1)
            
        cv2.imshow("OpenCV", cv2.resize(frame, (screen_w, screen_h)))
        
        if cv2.waitKey(30) & 0xFF == 27:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()