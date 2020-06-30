class Config:
    class Window:
        # Buttons
        buttonHeight = 50
        buttonColour = (100, 200, 200) # Grey
        buttonColour_01 = (255, 213, 0)  # Grey
        buttonColour_02 = (255, 97, 129)  # Grey
        buttonColour_03 = (50, 50, 102)  # Grey
        buttonText = "Solve"
        buttonText_01 = "3 x 3"
        buttonText_02 = "5 x 5"
        buttonText_03 = "10 x 10"

        # Size of the window
        side = 500
        size = (side, side + 4*buttonHeight)

        # Window caption
        caption = "Free flow"

        # Window logo
        iconPath = "img/icon.jpg"

        # RGB background colour
        backgroundColour = (255, 255, 255) # White

    class Grid:
        # Determines the THICCNESS of the grid
        thickness = 7

        # RGB grid colour
        colour = (211, 211, 211)


    class Circle:
        borderColour = (211, 211, 211)
