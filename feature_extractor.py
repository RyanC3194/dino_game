class FirstObstacleExtractor:
    def get_features(self, state, action):
        new_state = state.get_next(action)
        return (f"First_Obstacle {round(new_state.obstacles[0].x / 10, 0) * 10}", f"Height: {round(new_state.dino.y, 0)}")