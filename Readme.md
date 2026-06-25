# AI Customer Support Assistant

This is my project for the AI take-home assignment they gave me. It's a customer support chatbot that works fully offline, no internet, no cloud APIs, everything runs on my own laptop.

## What it does

You type something like "show hotels in dubai" or "where is my order" and the app figures out what category your message belongs to, then shows you a result. If you ask something like "show cheaper ones" after that, it remembers what you asked before and adjusts the answer based on that.

## How I built it

**Backend:** I used FastAPI (Python) for this. It takes the message you send, passes it to a small AI model running locally through Ollama, and that model decides what category the message falls into — things like order tracking, refund request, complaint, hotel search, flight search, etc.

**AI model:** I'm using Ollama with the llama3.2:1b model. It's a small model that runs completely on my own machine, no internet needed once it's downloaded once.

**Fallback:** If the AI model takes too long or isn't running, the backend just falls back to checking for keywords instead, so the app never breaks or crashes, it just keeps working either way.

**Memory:** The backend keeps track of the last few messages in a conversation, so if I say "show cheaper ones" right after asking about hotels, it knows what I'm talking about without me repeating the whole question again.

**Frontend:** I built the frontend in Flutter. It's a simple chat screen, you type your message and based on what category it is, it shows you a different kind of result on screen — hotel cards, flight cards, order status, refund status, and so on.

## How to run it

**1. Start Ollama**

    ollama pull llama3.2:1b
    ollama serve

**2. Start the backend**

    cd backend
    pip install -r requirements.txt
    set OLLAMA_MODEL=llama3.2:1b
    uvicorn app.main:app --reload --port 8000

**3. Start the frontend**

    cd frontend
    flutter pub get
    flutter run -d chrome

Then just start typing in the chat box.

## Things worth knowing

The AI model only decides what category a message belongs to. The actual data that gets shown (hotel names, prices, order status) comes from fixed sample data I wrote myself, not from the AI. I did it this way so the results stay consistent every time instead of the AI making up random data.

Since it's a small model running locally, sometimes it gets confused by short messages or typos. That's normal for a lightweight local model, that's exactly why I added the keyword fallback as backup.

This whole thing works with zero internet connection once the model is downloaded the first time.

## What's in this project

- `backend/` — FastAPI app, intent classification, memory, the tools that return sample data
- `frontend/` — Flutter chat app
