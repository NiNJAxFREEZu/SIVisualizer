class Config:
    class Window:
        # Size of the window
        side = 1000
        size = (side, side)

        # Window caption
        caption = "Free flow"

        # Window logo
        iconPath = "img/icon.jpg"

        # RGB background colour
        backgroundColour = (255, 255, 255)

    class Grid:
        # Determines the THICCNESS of the grid
        thickness = 10

        # RGB grid colour
        colour = (20, 20, 20)


    class Circle:
        borderColour = (10, 10, 10)
