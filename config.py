class Config:
    class Window:
        # Buttons
        buttonHeight = 50
        buttonColour = (100, 200, 200) # Grey
        buttonText = "Solve"

        # Size of the window
        side = 500
        size = (side, side + buttonHeight)

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
