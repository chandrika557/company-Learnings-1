"""Agent helpers: use Ollama when available, otherwise fallback to Gemini or a stub.

This module intentionally tolerates missing optional runtimes so the Streamlit
UI can load during development. Prefer installing the `ollama` Python client
and the Ollama app/daemon if you want local LLM inference.
"""

import os
try:
    import ollama
    OLLAMA_AVAILABLE = True
except Exception:
    ollama = None
    OLLAMA_AVAILABLE = False

try:
    from google import generativeai as genai
    GOOGLE_GENAI_AVAILABLE = True
except Exception:
    genai = None
    GOOGLE_GENAI_AVAILABLE = False


def gemini_ai(prompt):
    """Yield chunks from Google Gemini if available; otherwise yield a stub message.

    This generator yields strings to preserve the streaming interface used by
    the Streamlit frontend.
    """
    if not GOOGLE_GENAI_AVAILABLE:
        yield "[Gemini client not installed. Set up the `google-generative-ai` package and $env:gemini_API4 to use Gemini.]"
        return

    API_KEY = os.environ.get("gemini_API4")
    if not API_KEY:
        yield "[Gemini API key not set. Please set environment variable 'gemini_API4'.]"
        return

    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-pro")
    try:
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            # The gemini client yields objects with .text for each chunk
            yield getattr(chunk, "text", str(chunk))
    except Exception as e:
        yield f"[Gemini error: {e}]"


def chat_with_llama(prompt):
    """Stream responses from Ollama if available; otherwise fall back to Gemini or a helpful message.

    Yields string chunks to match the original interface.
    """
    if OLLAMA_AVAILABLE:
        try:
            model = "llama3.2"
            stream = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )
            for chunk in stream:
                # Ollama returns dict-like chunks with nested message content
                try:
                    yield chunk["message"]["content"]
                except Exception:
                    # Fallback to str representation
                    yield str(chunk)
            return
        except Exception as e:
            # If the Ollama client/daemon fails at runtime, fall through to Gemini
            yield f"[Ollama runtime error: {e}]"

    # Ollama not available — try Gemini
    for piece in gemini_ai(prompt):
        yield piece


def chat_with_llama_direct(prompt):
    """Return a single string response. Prefer Ollama, else Gemini, else explanatory text."""
    if OLLAMA_AVAILABLE:
        try:
            model = "llama3.2"
            response = ollama.chat(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.get("message", {}).get("content", str(response))
        except Exception as e:
            return f"[Ollama runtime error: {e}]"

    # If Ollama is not available, try Gemini (accumulate streaming chunks)
    if GOOGLE_GENAI_AVAILABLE:
        parts = []
        for chunk in gemini_ai(prompt):
            parts.append(chunk)
        return "".join(parts)

    return "[No LLM runtime available: install Ollama or configure Google Gemini (set gemini_API4).]"


if __name__ == "__main__":
    # Quick diagnostic output
    print(f"OLLAMA_AVAILABLE={OLLAMA_AVAILABLE}")
    print(f"GOOGLE_GENAI_AVAILABLE={GOOGLE_GENAI_AVAILABLE}")
    

