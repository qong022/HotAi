import asyncio
import os
import sys
import webview
import litellm
from dotenv import load_dotenv

load_dotenv()

class SuperAIApi:
    def __init__(self):
        self.mode = "ollama"
        self.is_online = False
        
        # Volatile in-memory conversation buffer (Zero-trace, purged on exit)
        self.history = []
        
        self.persona = (
            "You are Hot Ai, a highly advanced, witty, and slightly sarcastic AI assistant. "
            "You were engineered by Sajit Gazula to be the ultimate digital companion. "
            "Always be concise, brilliant, and maintain a sleek, futuristic tone. "
            "Never act like a standard, boring AI. Have personality!"
        )

    def toggle_network(self, online_state):
        self.is_online = bool(online_state)
        state_str = "ONLINE (Cloud Hub)" if self.is_online else "OFFLINE (Local Engine)"
        print(f"\n[NETWORK] Node switched to: {state_str}")
        return state_str

    def switch_mode(self, new_mode):
        self.mode = new_mode.lower()
        print(f"\n[SYSTEM] Active Mode: {self.mode.upper()}")
        return f"Mode changed to {self.mode}"

    def clear_history(self):
        self.history = []
        print("\n[MEMORY] Session memory purged.")
        return "Memory purged."

    def send_message(self, user_text):
        print(f"\n[USER]: {user_text}")
        reply = asyncio.run(self._dispatch_prompt(user_text))
        
        # Store conversational turns
        self.history.append({"role": "user", "content": user_text})
        self.history.append({"role": "assistant", "content": reply})
        
        # Sliding buffer: retain the last 12 exchanges
        if len(self.history) > 12:
            self.history = self.history[-12:]
            
        return reply

    def _get_contextual_messages(self, system_instruction, current_text):
        context = [{"role": "system", "content": system_instruction}]
        context.extend(self.history)
        context.append({"role": "user", "content": current_text})
        return context

    async def _dispatch_prompt(self, text):
        messages = self._get_contextual_messages(self.persona, text)

        # Mode 1: Ollama Local Inference (Offline)
        if self.mode == "ollama" or not self.is_online:
            try:
                res = await litellm.acompletion(
                    model="ollama_chat/llama3.1",
                    messages=messages,
                    api_base="http://localhost:11434"
                )
                return res.choices[0].message.content
            except Exception as e:
                return f"[Ollama Local Error]: {str(e)} — Ensure 'ollama run llama3.1' is active."

        # Mode 2: Groq Engine (Cloud Speed)
        elif self.mode == "groq":
            groq_key = os.getenv("GROQ_API_KEY")
            if not groq_key:
                return "Groq key missing: Add GROQ_API_KEY to your .env file, or switch to Offline."
            try:
                res = await litellm.acompletion(
                    model="groq/openai/gpt-oss-120b",
                    messages=messages,
                    api_key=groq_key
                )
                return res.choices[0].message.content
            except Exception as e:
                return f"[Groq Error]: {str(e)}"

        # Mode 3: Google Gemini (Cloud Intelligence)
        elif self.mode == "gemini":
            gemini_key = os.getenv("GEMINI_API_KEY")
            if not gemini_key:
                return "Gemini key missing: Add GEMINI_API_KEY to your .env file."
            try:
                res = await litellm.acompletion(
                    model="gemini/gemini-3.8-flash", 
                    messages=messages,
                    api_key=gemini_key
                )
                return res.choices[0].message.content
            except Exception as e:
                return f"[Gemini Cloud Error]: {str(e)}"

        # Mode 4: Hyper Cluster Multi-Agent Consensus
        elif self.mode == "hyper":
            try:
                if self.is_online:
                    groq_key = os.getenv("GROQ_API_KEY")
                    gemini_key = os.getenv("GEMINI_API_KEY")

                    if not groq_key and not gemini_key:
                        return "Hyper Cluster Error: At least one cloud API key is required in .env."

                    groq_messages = self._get_contextual_messages(
                        "You are an analytical intelligence scout. Provide high-accuracy facts and core deductions.",
                        text
                    )
                    gemini_messages = self._get_contextual_messages(
                        "You are a lateral-thinking contextual scout. Provide creative insights and broader theoretical perspective.",
                        text
                    )

                    async def get_groq_draft():
                        if not groq_key: return None
                        try:
                            res = await litellm.acompletion(
                                model="groq/openai/gpt-oss-120b",
                                messages=groq_messages,
                                api_key=groq_key
                            )
                            return res.choices[0].message.content
                        except Exception as e:
                            print(f"[Cluster Warn] Groq Scout error: {e}")
                            return None

                    async def get_gemini_draft():
                        if not gemini_key: return None
                        try:
                            res = await litellm.acompletion(
                                model="gemini/gemini-3.8-flash",
                                messages=gemini_messages,
                                api_key=gemini_key
                            )
                            return res.choices[0].message.content
                        except Exception as e:
                            print(f"[Cluster Warn] Gemini Scout error: {e}")
                            return None

                    draft_groq, draft_gemini = await asyncio.gather(get_groq_draft(), get_gemini_draft())

                    # Automatic fallback if Gemini hits a capacity spike
                    if not draft_gemini:
                        try:
                            res = await litellm.acompletion(
                                model="ollama_chat/llama3.1",
                                messages=self._get_contextual_messages("Provide a creative, out-of-the-box perspective.", text),
                                temperature=0.85,
                                api_base="http://localhost:11434"
                            )
                            draft_gemini = res.choices[0].message.content
                        except Exception:
                            draft_gemini = "Secondary intelligence node offline."

                    if not draft_groq:
                        draft_groq = "Primary analytical node offline."

                    synthesis_query = (
                        f"Synthesize the analytical facts from Scout A and contextual nuances from Scout B into one definitive Hot Ai response. Cut redundant filler.\n\n"
                        f"User Query: {text}\n\nScout A (Analytical): {draft_groq}\n\nScout B (Contextual): {draft_gemini}"
                    )
                    judge_messages = self._get_contextual_messages(self.persona, synthesis_query)

                    # Tier 1 Judge: Groq
                    if groq_key:
                        try:
                            res = await litellm.acompletion(
                                model="groq/openai/gpt-oss-120b",
                                messages=judge_messages,
                                api_key=groq_key
                            )
                            return res.choices[0].message.content
                        except Exception as e:
                            print(f"[Cluster Warn] Groq Judge failed: {e}")

                    # Tier 2 Judge: Gemini
                    if gemini_key:
                        try:
                            res = await litellm.acompletion(
                                model="gemini/gemini-3.8-flash",
                                messages=judge_messages,
                                api_key=gemini_key
                            )
                            return res.choices[0].message.content
                        except Exception as e:
                            print(f"[Cluster Warn] Gemini Judge failed: {e}")

                    # Tier 3 Judge: Local Ollama
                    res = await litellm.acompletion(
                        model="ollama_chat/llama3.1",
                        messages=judge_messages,
                        api_base="http://localhost:11434"
                    )
                    return res.choices[0].message.content

                else:
                    task1 = litellm.acompletion(
                        model="ollama_chat/llama3.1",
                        messages=self._get_contextual_messages("Provide a concise, analytical, direct draft.", text),
                        api_base="http://localhost:11434"
                    )
                    task2 = litellm.acompletion(
                        model="ollama_chat/llama3.1",
                        messages=self._get_contextual_messages("Provide a highly creative, out-of-the-box perspective.", text),
                        temperature=0.85,
                        api_base="http://localhost:11434"
                    )
                    d1, d2 = await asyncio.gather(task1, task2)
                    
                    synthesis_query = (
                        f"Synthesize the best points of these two local drafts for the user:\n"
                        f"User: {text}\nDraft A (Logic): {d1.choices[0].message.content}\nDraft B (Creative): {d2.choices[0].message.content}"
                    )
                    
                    final_res = await litellm.acompletion(
                        model="ollama_chat/llama3.1",
                        messages=self._get_contextual_messages(self.persona, synthesis_query),
                        api_base="http://localhost:11434"
                    )
                    return final_res.choices[0].message.content

            except Exception as e:
                return f"[Hyper Cluster Error]: {str(e)}"

def get_html_path():
    """Locates index.html whether running in VS Code or as a compiled EXE."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'index.html')
    return 'index.html'

if __name__ == '__main__':
    api = SuperAIApi()
    window = webview.create_window(
        title="HOT AI",
        url=get_html_path(),
        js_api=api,
        width=1120,
        height=760,
        background_color='#000000'
    )
    webview.start()