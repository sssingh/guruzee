import base64
import requests
from app_config import config
import gradio as gr
import mongo_utils as mongo


def clear():
    return None, ""


# Function to encode the local image into base64 to be send over HTTP
def __encode_image(image_path: str) -> bytes:
    """
    Encodes the passed image to base64 byte-stream.
    This is required for passing the image over a HTTP get/post call.
    """
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    return base64_image


def solve(image_path: str):
    """
    Invokes the GuruZee API passing the raw image bytes and returns the response
    to client
    """
    image_data = __encode_image(image_path=image_path)
    headers = {"Content-Type": "application/json"}
    payload = {"data": image_data}
    end_point = config.GURUZEE_API_ENDPOINT + "/solve"
    response = requests.post(end_point, headers=headers, json=payload)
    # increment the openai access counter and compute count stats
    mongo.increment_curr_access_count()
    max_count = config.openai_max_access_count
    curr_count = config.openai_curr_access_count
    available_count = max_count - curr_count
    return response.json(), max_count, curr_count, available_count


def create_interface():
    js_enable_darkmode = """() => 
    {
        document.querySelector('body').classList.add('dark');
    }"""
    js_toggle_darkmode = """() => 
    {
        if (document.querySelectorAll('.dark').length) {
            document.querySelector('body').classList.remove('dark');
        } else {
            document.querySelector('body').classList.add('dark');
        }
    }"""

    with gr.Blocks(title=config.title, theme=config.theme, css=config.css) as app:
        # enable darkmode
        app.load(fn=None, inputs=None, outputs=None, _js=js_enable_darkmode)
        with gr.Row():
            darkmode_checkbox = gr.Checkbox(
                label="Dark Mode", value=True, interactive=True
            )
            # toggle darkmode on/off when checkbox is checked/unchecked
            darkmode_checkbox.change(
                None, None, None, _js=js_toggle_darkmode, api_name=False
            )
        with gr.Row():
            with gr.Column():
                gr.Markdown(
                    """
                    # GuruZee
                    ***Where Math Meets Marvel with AI Wizardry for Primary School 
                    Prowess! 🧙♂📚✨***
                    **GuruZee whips up question papers with answers and detailed 
                    explanations, all based on those elusive course chapter images. 
                    Not just that, it's a math-solving maestro, tackling problems 
                    presented as images with ease..  
                    <br>
                    Select/upload an `Image` containing the problem Then hit 
                    `GO!` button.
                    Alternatively, just select one of the pre-configured `Example` image 
                    from the Example section at the bottom**  
                    <br>
                    Visit the [project's repo](https://github.com/sssingh/GuruZee)  
                    <br>
                    ***Please exercise patience, as the models employed are extensive 
                    and may require a few seconds to load. If you encounter an unrelated 
                    response, it is likely still loading; wait a moment and try again.***
                    """
                )
            with gr.Column():
                max_count = gr.Textbox(
                    label="Max allowed OpenAI requests:",
                    value=config.openai_max_access_count,
                )
                curr_count = gr.Textbox(
                    label="Used up OpenAI requests:",
                    value=config.openai_curr_access_count,
                )
                available_count = gr.Textbox(
                    label="Available OpenAI requests:",
                    value=config.openai_max_access_count
                    - config.openai_curr_access_count,
                )
        with gr.Row():
            with gr.Column():
                image = gr.Image(
                    type="filepath",
                )
                with gr.Row():
                    submit_button = gr.Button(value="GO!", elem_classes="orange-button")
                    clear_button = gr.ClearButton(elem_classes="gray-button")
            with gr.Column():
                answer = gr.Textbox(
                    label="Answer:",
                    placeholder="Answer will appear here.",
                    lines=20,
                )
        with gr.Row():
            with gr.Accordion("Expand for examples:", open=False):
                gr.Examples(
                    examples=[
                        [
                            "assets/examples/1.png",
                        ],
                        [
                            "assets/examples/2.png",
                        ],
                        [
                            "assets/examples/3.png",
                        ],
                        [
                            "assets/examples/4.png",
                        ],
                        [
                            "assets/examples/5.png",
                        ],
                        [
                            "assets/examples/6.png",
                        ],
                        [
                            "assets/examples/7.png",
                        ],
                        [
                            "assets/examples/8.png",
                        ],
                        [
                            "assets/examples/9.png",
                        ],
                        [
                            "assets/examples/10.png",
                        ],
                    ],
                    fn=solve,
                    inputs=[image],
                    outputs=[answer, max_count, curr_count, available_count],
                    run_on_click=True,
                )
        submit_button.click(
            fn=solve,
            inputs=[image],
            outputs=[answer, max_count, curr_count, available_count],
        )
        clear_button.click(fn=clear, inputs=[], outputs=[image, answer])
        image.clear(fn=clear, inputs=[], outputs=[image, answer])

    return app


if __name__ == "__main__":
    mongo.fetch_curr_access_count()
    app = create_interface()
    app.launch()
