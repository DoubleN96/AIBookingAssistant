import gradio as gr
import openai
from pathlib import Path

# openai.api_key = os.environ.get('OPEN_API_KEY')
openai.api_key = "sk-"


def transcribe(audio):
    print(audio)
    
    myfile=Path(audio)
    myfile=myfile.rename(myfile.with_suffix('.wav'))

    audio_file= open(myfile, "rb")
 
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript)

    return transcript["text"]


demo = gr.Interface(fn=transcribe, inputs=gr.Audio(source="microphone", type="filepath"), outputs="text")

demo.launch()
#demo.launch(share=True)
