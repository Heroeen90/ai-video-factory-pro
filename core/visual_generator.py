from pathlib import Path
from datetime import datetime
from moviepy.editor import ColorClip, TextClip, concatenate_videoclips, CompositeVideoClip
from utils.logger import setup_logger

logger = setup_logger(__name__)

class VisualGenerator:
    def __init__(self):
        self.output_dir = Path('data/visuals')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.width = 1920
        self.height = 1080
        logger.info("VisualGenerator initialized")
    
    def create_visuals(self, topic: str, duration: int) -> str:
        try:
            logger.info(f"Creating visuals for topic: {topic}, duration: {duration}s")
            
            scenes = []
            scene_duration = max(5, duration // 3)
            
            scene1 = self._create_title_scene(topic, scene_duration)
            scenes.append(scene1)
            
            scene2 = self._create_content_scene(topic, scene_duration)
            scenes.append(scene2)
            
            scene3 = self._create_closing_scene(topic, scene_duration)
            scenes.append(scene3)
            
            video = concatenate_videoclips(scenes)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = self.output_dir / f'visuals_{timestamp}.mp4'
            
            video.write_videofile(str(output_path), verbose=False, logger=None, fps=30)
            video.close()
            
            logger.info(f"Visuals created: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Visual creation failed: {str(e)}", exc_info=True)
            raise
    
    def _create_title_scene(self, topic: str, duration: int):
        try:
            background = ColorClip(size=(self.width, self.height), color=(30, 30, 60))
            background = background.set_duration(duration)
            
            title_clip = TextClip(topic, fontsize=80, color='white', font='Arial-Bold', method='caption', size=(1800, None))
            title_clip = title_clip.set_duration(duration).set_position('center')
            
            subtitle_clip = TextClip("AI Video Factory", fontsize=40, color='#FFD700', font='Arial', method='caption', size=(1800, None))
            subtitle_clip = subtitle_clip.set_duration(duration).set_position(('center', 0.7))
            
            return CompositeVideoClip([background, title_clip, subtitle_clip])
        except Exception as e:
            logger.error(f"Title scene failed: {str(e)}", exc_info=True)
            raise
    
    def _create_content_scene(self, topic: str, duration: int):
        try:
            background = ColorClip(size=(self.width, self.height), color=(40, 40, 80))
            background = background.set_duration(duration)
            
            content_text = f"Exploring {topic}\n\nKey Points:\n• Important aspect 1\n• Important aspect 2\n• Important aspect 3"
            content_clip = TextClip(content_text, fontsize=50, color='white', font='Arial', method='caption', size=(1600, None))
            content_clip = content_clip.set_duration(duration).set_position('center')
            
            return CompositeVideoClip([background, content_clip])
        except Exception as e:
            logger.error(f"Content scene failed: {str(e)}", exc_info=True)
            raise
    
    def _create_closing_scene(self, topic: str, duration: int):
        try:
            background = ColorClip(size=(self.width, self.height), color=(50, 30, 70))
            background = background.set_duration(duration)
            
            title_clip = TextClip("Thank You!", fontsize=80, color='white', font='Arial-Bold', method='caption', size=(1800, None))
            title_clip = title_clip.set_duration(duration).set_position(('center', 0.3))
            
            subtitle_clip = TextClip(f"Learn more about {topic}", fontsize=40, color='#FFD700', font='Arial', method='caption', size=(1800, None))
            subtitle_clip = subtitle_clip.set_duration(duration).set_position(('center', 0.7))
            
            return CompositeVideoClip([background, title_clip, subtitle_clip])
        except Exception as e:
            logger.error(f"Closing scene failed: {str(e)}", exc_info=True)
            raise
