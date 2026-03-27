import numpy as np

class RepCounter:
    def __init__(self, exercise="squat"):
        self.exercise = exercise
        self.count = 0
        self.stage = None  # "up" or "down"

    def calculate_angle(self, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
                  np.arctan2(a[1]-b[1], a[0]-b[0])

        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180:
            angle = 360 - angle

        return angle

    def update(self, landmarks):
        """
        landmarks should include:
        shoulder, elbow, wrist, hip, knee, ankle
        """

        if self.exercise == "squat":
            return self._count_squat(landmarks)

        elif self.exercise == "pushup":
            return self._count_pushup(landmarks)

        return False

    # ---------------- SQUAT ----------------
    def _count_squat(self, landmarks):
        hip = landmarks["hip"]
        knee = landmarks["knee"]
        ankle = landmarks["ankle"]

        angle = self.calculate_angle(hip, knee, ankle)

        # Going DOWN
        if angle < 90:
            self.stage = "down"

        # Coming UP → count rep
        if angle > 160 and self.stage == "down":
            self.stage = "up"
            self.count += 1
            return True

        return False

    # ---------------- PUSH-UP ----------------
    def _count_pushup(self, landmarks):
        shoulder = landmarks["shoulder"]
        elbow = landmarks["elbow"]
        wrist = landmarks["wrist"]

        angle = self.calculate_angle(shoulder, elbow, wrist)

        # Going DOWN
        if angle < 90:
            self.stage = "down"

        # Coming UP → count rep
        if angle > 160 and self.stage == "down":
            self.stage = "up"
            self.count += 1
            return True

        return False