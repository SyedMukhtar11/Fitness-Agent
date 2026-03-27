class PoseHandler:
    def __init__(self, agent, rep_counter, exercise_detector):
        self.agent = agent
        self.rep_counter = rep_counter
        self.exercise_detector = exercise_detector
        self.current_exercise = None
        self.last_feedback = ""

    async def handle(self, data):
        keypoints = data.get("keypoints")

        if keypoints is None:
            return

        # 🔍 Detect exercise
        detected = self.exercise_detector.detect(keypoints)
        if detected:
            self.current_exercise = detected

        # 🏋️ Rep counting
        if self.current_exercise == "squat":
            reps, feedback = self.rep_counter.update_squat(keypoints)

        elif self.current_exercise == "pushup":
            reps, feedback = self.rep_counter.update_pushup(keypoints)

        else:
            return

        print(f"{self.current_exercise} | Reps: {reps}")

        # 🔊 Voice feedback
        if feedback and feedback != self.last_feedback:
            await self.agent.llm.simple_response(text=feedback)
            self.last_feedback = feedback