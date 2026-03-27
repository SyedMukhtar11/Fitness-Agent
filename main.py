import asyncio
import logging
from uuid import uuid4
from dotenv import load_dotenv

from vision_agents.core.edge.types import User
from vision_agents.core import agents
from vision_agents.plugins import getstream, ultralytics, gemini

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

import math

def angle(a, b, c):
    ang = math.degrees(
        math.atan2(c[1]-b[1], c[0]-b[0]) -
        math.atan2(a[1]-b[1], a[0]-b[0])
    )
    return abs(ang)

async def start_yoga_instructor():

    logger.info("Starting Yoga AI Instructor...")

    agent = agents.Agent(
        edge=getstream.Edge(),
        agent_user=User(name="AI Yoga Instructor", id="yoga_agent"),
        instructions="Read @yoga_instructor_guide.md",

        llm=gemini.Realtime(),

        processors=[
            ultralytics.YOLOPoseProcessor(
                model_path="yolo11n-pose.pt",
                conf_threshold=0.5,
                enable_hand_tracking=True,
            )
        ],
    )

    await agent.create_user()

    call_id = str(uuid4())
    call = agent.edge.client.video.call("default", call_id)

    await agent.edge.open_demo(call)

    async with agent.join(call):

        await agent.llm.simple_response(
            text="Namaste! I will guide your yoga using your camera. Please stand in front of the camera."
        )

        await agent.finish()

if __name__ == "__main__":
    asyncio.run(start_yoga_instructor())
