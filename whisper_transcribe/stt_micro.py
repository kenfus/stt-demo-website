import torch
import gradio as gr
from transcribe import AudioTranscriber
from faster_whisper.audio import decode_audio
from faster_whisper import WhisperModel
from faster_whisper.transcribe import Segment


THEME = gr.themes.Soft()
MODEL = "i4ds/whisper4sg-srg-v2-full-mc-de-sg-corpus-v2"


device = "cuda" if torch.cuda.is_available() else "cpu"
model = WhisperModel(MODEL, device=device, compute_type="int8")


def transcribe(inputs) -> tuple[str, list[Segment]]:
    print(inputs)
    print(type(inputs))
    with torch.inference_mode():
        segments, _ = model.transcribe(
            inputs, language="de", without_timestamps=True, vad_filter=False
        )
        segments = fw_segments_to_text(segments)
        return


def fw_segments_to_text(segments: list[Segment]) -> str:

    return " ".join(segment.text for segment in segments)


app = gr.Blocks(theme=THEME)

with app:
    # Include custom CSS for styling
    gr.HTML(
        """
    <style>
    .info-box {
        border: 1px solid #ccc;
        padding: 15px;
        border-radius: 5px;
        font-size: 16px;
    }
    .instructions-box {
        border: 1px solid #007bff;
        padding: 15px;
        border-radius: 5px;
        font-size: 16px;
    }
    </style>
    """
    )

    # Title
    gr.Markdown("# Swiss German Whisper")

    # Information Box
    gr.HTML(
        """
    <div class="info-box">
        <p><strong>Transcribe Swiss German audio files of up to 500MB!</strong></p>
        <p>This demo uses a model trained on Swiss German data by the 
        <a href="https://stt4sg.fhnw.ch/" target="_blank">NLP Team at i4ds</a>, supervised by Prof. Dr. Manfred Vogel.</p>
        <p>It combines:</p>
        <ul>
            <li><a href="https://github.com/guillaumekln/faster-whisper" target="_blank">SYSTRAN/faster-whisper</a> for fast transcription</li>
        </ul>
        <p><strong>Note:</strong> The int8-quantized model is currently running on a CPU.<p>
    </div>
    """
    )

    # Instructions Box
    gr.HTML(
        """
    <div class="instructions-box">
        <p><strong>Instructions:</strong></p>
        <ol>
            <li>Click on "Record from microphone" to start recording.</li>
            <li>Stop recording.</li>
            <li>Click on <em>'Submit'</em>.</li>
            <li>Wait for the transcription to complete.</li>
        </ol>
    </div>
    """
    )
    gr.Interface(
        fn=transcribe,
        inputs=[
            gr.Audio(sources="microphone", type="numpy"),
        ],
        outputs="text",
        theme=THEME,
        allow_flagging="never",
    )

app.launch(server_name="127.0.0.1", server_port=7863, root_path="/stt")
