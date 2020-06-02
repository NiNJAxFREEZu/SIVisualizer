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
        # Determines how far the base grid will be drawn from the window border
        # TODO
        padding = 20

        # Determines the THICCNESS of the grid
        thickness = 10

        # RGB grid colour
        colour = (185, 185, 185)
