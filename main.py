import numpy as np
import nashpy as nash
from PIL import Image, ImageDraw


x=499
y=0
#Revards
r1=0.9
r2=0.9
b1=0.45
b2=0.45
e1=1
e2=1
my_array = np.full((500, 500),"")

for i in range(1, 501, 1):
    p=i/500
    for j in range(1, 501, 1):
        q=j/500
#Determining the values of different strategies
        r11 = p*r1*b1 #SS
        r12 = -pow(p,2) + 2*p*r1*b1 +2*p - pow(p,2)*r1*b1 -1 #SA
        r21 = pow(p,2)*e1 #AS
        r22 = pow(p,2)*e1 + 2*p*e1*q + 2*p*q -2*pow(p,2)*q -2*pow(p,2)*e1*q + pow(p,2)-1 #AA

        c11 = (1-p)*r2*b2 #SS
        c21 = -pow(p,2)-pow(p,2)*r2*b2+r2*b2 #AS
        c12 = pow(1-p,2)*e2 #SA
        c22 = -pow(p,2) -2*p*q + 2*pow(p,2)*q - pow(p,2)*e2-2*p*q*e2 +2*pow(p,2)*q*e2 + e2 #AA

        payoff_matrix_player1 = np.array([[r11, r12], [r21, r22]])
        payoff_matrix_player2 = np.array([[c11, c12], [c21, c22]])
#Creating a game and calculating Nash equilibria
        game = nash.Game(payoff_matrix_player1, payoff_matrix_player2)
        eqs = game.support_enumeration()

        for eq in eqs:

            S1=eq[0][0]
            A1=eq[0][1]
            S2=eq[1][0]
            A2=eq[1][1]
#Each character defines a strategic profile. Based on the characters stored in the matrix, the image can be generated later on.
            if S1>A1 and S2>A2:
                my_array[x][y]= str('X')
            elif S1<A1 and S2>A2:
                my_array[x][y] = str('Y')
            elif S1>A1 and S2<A2:
                my_array[x][y] = str('Z')
            elif S1<A1 and S2<A2:
                my_array[x][y] = str('W')

            if S1>0 and A1>0 and S2>0 and A2>0:
                my_array[x][y] = str('D')
        x=x-1
    y=y+1
    print(y)
    x=499

#Color mapping on strategy profiles
print(my_array)
color_mapping = {
    'X': (0, 0, 255),  # Blue SS
    'Y': (255, 0, 0),  # Red AS 
    'Z': (0, 255, 0),  # Green SA 
    'W': (255, 255, 0),  # Yellow AA 
    'D': (255, 140, 0)  # Orange SA AS 
}

# Create a blank white image
img = Image.new('RGB', (500, 500), 'white')
draw = ImageDraw.Draw(img)

# Assuming 'matrix' is your 500x500 matrix
for i in range(len(my_array)):
    for j in range(len(my_array[i])):
        cell_value = my_array[i][j]
        color = color_mapping.get(cell_value, (255, 255, 255))  # Default to white if not found
        img.putpixel((j,i),color_mapping[my_array[i][j]])

# Save the image
img.save('output.png')

# Display the image
img.show()
# Find the Nash Equilibria

