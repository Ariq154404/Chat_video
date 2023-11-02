<h1 align="center" style="font-size: 68px;">Chat Video</h1>

<p align="center">
  <img src="https://github.com/Ariq154404/Chat_video/blob/main/assets/proj_logo.png" alt="Project Logo">
</p>
logo created with DALL-E-3

## Description

In this project , I used llamaindex with gpt-3.5 to interact with video and ask queiries. LlamaIndex significantly enhances the capabilities of Large Language Models (LLMs) by integrating specific user data, ensuring tailored and relevant responses. It streamlines the Retrieval Augmented Generation (RAG) process, enabling efficient data retrieval and handling through advanced indexing, querying, and storage solutions.
## Demo

![Demo GIF](https://github.com/Ariq154404/Chat_video/blob/main/assets/project_demo.gif)

## Concept Diagram

Here below it shows the conceptual diagram:

![Concept Diagram](https://github.com/Ariq154404/Chat_video/blob/main/assets/system_diagram.png)

## Run Locally

Clone the project
```bash
   git clone https://github.com/Ariq154404/data-engineering
```
Change  to project directory
```bash
   cd Chat_video
```
Change to model directory to download vosk speech recognizing model
Make sure you have .env file with "OPENAI_API_KEY" Key
```bash
   cd models
   curl -L -O https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
   unzip vosk-model-small-en-us-0.15.zip
   rm vosk-model-small-en-us-0.15.zip
   cd .. 
```
Create virtual environment and download all dependencies
```bash
   cd Chat_video
   python3 -m venv myenv
   source myenv/bin/activate
   pip install -r requirements.txt
```

Start the project
```bash
   chainlit run app.py -w 
```
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file. 
Create .env file with the following command

```bash
  touch .env
```
`OPENAI_API_KEY`




## References

 - [Chainlit with llama index documentation](https://docs.chainlit.io/integrations/llama-index)

- [Open AI api ](https://platform.openai.com/docs/introduction)
- [ Kurzgesakt video sample ](https://www.youtube.com/watch?v=JOiGEI9pQBs)

## Tech Stack

**LLAMAIndex:**  

**Chatgpt:**  

**Chainlit**  