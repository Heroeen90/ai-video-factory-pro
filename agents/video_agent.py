import os
import json
from pathlib import Path
from datetime import datetime
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips, CompositeVideoClip, TextClip, ColorClip, clips_array
from utils.logger import setup_logger
from core.script_generator import ScriptGenerator
from core.visual_generator import VisualGenerator

logger = setup_logger(__name__)

class VideoAgent:
    """Main agent for video generation orchestration."""
    
    def __init__(self):
        self.script_generator = ScriptGenerator()
        self.visual_generator = VisualGenerator()
        self.output_dir = Path('data/videos')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info("VideoAgent initialized")
    
    def generate_script(self, topic: str, duration: int) -> str:
        """Generate a video script based on topic and duration."""
        try:
            logger.info(f"Generating script for topic: {topic}, duration: {duration}s")
            script = self.script_generator.create_script(topic, duration)
            logger.info(f"Script generated successfully (length: {len(script)} chars)")
            return script
        except Exception as e:
            logger.error(f"Script generation failed: {str(e)}", exc_info=True)
            raise
    
    def generate_voice(self, script: str, language: str = 'en') -> str:
        """Generate voice narration from script using gTTS."""
        try:
            logger.info(f"Generating voice for script (language: {language})")
            audio_dir = Path('data/audio')
            audio_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            audio_path = audio_dir / f'narration_{timestamp}.mp3'
            
            tts = gTTS(script, lang=language, slow=False)
            tts.save(str(audio_path))
            
            logger.info(f"Voice generated successfully: {audio_path}")
            return str(audio_path)
        except Exception as e:
            logger.error(f"Voice generation failed: {str(e)}", exc_info=True)
            raise
    
    def generate_visuals(self, topic: str, duration: int) -> str:
        """Generate visual elements for the video."""
        try:
            logger.info(f"Generating visuals for topic: {topic}")
            visuals_path = self.visual_generator.create_visuals(topic, duration)
            logger.info(f"Visuals generated successfully: {visuals_path}")
            return visuals_path
        except Exception as e:
            logger.error(f"Visual generation failed: {str(e)}", exc_info=True)
            raise
    
    def compose_video(self, visuals_path: str, audio_path: str = None, duration: int = 60) -> str:
        """Compose final video from visuals and audio."""
        try:
            logger.info(f"Composing video: visuals={visuals_path}, audio={audio_path}")
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = self.output_dir / f'video_{timestamp}.mp4'
            
            if os.path.exists(visuals_path):
                video = VideoFileClip(visuals_path)
            else:
                logger.warning(f"Visuals file not found: {visuals_path}, creating fallback video")
                video = self._create_fallback_video(duration)
            
            if audio_path and os.path.exists(audio_path):
                audio = AudioFileClip(audio_path)
                video = video.set_audio(audio)
            
            video.write_videofile(
                str(output_path),
                verbose=False,
                logger=None,
                codec='libx264',
                audio_codec='aac',
                fps=30
            )
            
            video.close()
            if audio_path and os.path.exists(audio_path):
                audio.close()
            
            logger.info(f"Video composition completed: {output_path}")
            return str(output_path)
        except Exception as e:
            logger.error(f"Video composition failed: {str(e)}", exc_info=True)
            raise
    
    def _create_fallback_video(self, duration: int):
        """Create a fallback video when visuals generation fails."""
        try:
            logger.info(f"Creating fallback video (duration: {duration}s)")
            
            background = ColorClip(size=(1920, 1080), color=(20, 20, 40))
            background = background.set_duration(duration)
            
            txt_clip = TextClip(
                "AI Video Factory Pro",
                fontsize=70,
                color='white',
                font='Arial-Bold',
                method='caption',
                size=(1800, None)
            )
            txt_clip = txt_clip.set_duration(duration)
            txt_clip = txt_clip.set_position('center')
            
            video = CompositeVideoClip([background, txt_clip])
            logger.info("Fallback video created successfully")
            return video
        except Exception as e:
            logger.error(f"Fallback video creation failed: {str(e)}", exc_info=True)
            raise
