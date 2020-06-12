class Config:
    class Window:
        # Window side and button props
        side = 600
        buttonHeight = int(side / 8)
        buttonColour = (100, 200, 200) # Grey
        size = (side, side + buttonHeight)

        # Window caption
        caption = "Free flow"

        # Window logo
        iconPath = "img/icon.jpg"

        # RGB background colour
        backgroundColour = (255, 255, 255) # White

    class Grid:
        # Determines the THICCNESS of the grid
        thickness = 10

        # RGB grid colour
        colour = (20, 20, 20)


    class Circle:
        borderColour = (10, 10, 10)
