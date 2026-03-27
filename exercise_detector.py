import numpy as np

class ExerciseDetector:
    def __init__(self):
        self.current_exercise = None

    def angle(self, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
                  np.arctan2(a[1]-b[1], a[0]-b[0])

        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180:
            angle = 360 - angle

        return angle

    def detect(self, landmarks):
        """
        landmarks must include:
        shoulder, elbow, wrist, hip, knee, ankle
        """

        shoulder = landmarks["shoulder"]
        elbow = landmarks["elbow"]
        wrist = landmarks["wrist"]
        hip = landmarks["hip"]
        knee = landmarks["knee"]
        ankle = landmarks["ankle"]

        knee_angle = self.angle(hip, knee, ankle)
        elbow_angle = self.angle(shoulder, elbow, wrist)

        # 🟢 Detect Squat
        if knee_angle < 100:
            return "squat"

        # 🔵 Detect Push-up
        if elbow_angle < 100:
            return "pushup"

        # 🟡 Detect Standing / Idle
        if knee_angle > 150 and elbow_angle > 150:
            return "standing"

        return "unknown"