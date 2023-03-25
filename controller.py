class Controller:
    def __init__(self):
        self.mouse_sensitivity = 0.05
        self.mouse_selection = False
        self.mouse_position = (0, 0)

        # Tuple does not support item assignment.
        self.mouse_movement = [0.0, 0.0]

    def get_frame_update(self) -> tuple[float, float]:
        movement = self.mouse_movement
        self.mouse_movement = [0.0, 0.0]
        return movement

    def mouse_button_down(self, screen_position: tuple[int, int]) -> None:
        self.mouse_selection = True
        self.mouse_position = screen_position
    
    def mouse_button_up(self) -> None:
        self.mouse_selection = False
        self.mouse_position = (0, 0)

    def mouse_motion(self, screen_position: tuple[int, int], time: int) -> None:
        if self.mouse_selection:
            pixel_x = self.mouse_position[0] - screen_position[0]
            pixel_y = self.mouse_position[1] - screen_position[1]

            # Rotating around X axis moves a point along Y axis.
            self.mouse_movement[0] += pixel_y * time * self.mouse_sensitivity
            self.mouse_movement[1] += pixel_x * time * self.mouse_sensitivity

            self.mouse_position = screen_position
