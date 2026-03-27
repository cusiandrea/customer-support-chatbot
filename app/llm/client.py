import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from app.config import MODEL_NAME, MAX_NEW_TOKENS, TEMPERATURE, TOP_P


@st.cache_resource
def load_llm_resources():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True
    )

    dtype = torch.float16 if device.type == "cuda" else torch.float32

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=dtype,
        trust_remote_code=True
    )

    model.to(device)
    model.eval()

    return tokenizer, model, device


class LocalLLM:
    def __init__(self):
        self.tokenizer, self.model, self.device = load_llm_resources()

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True
        )

        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        generated_ids = outputs[0][inputs["input_ids"].shape[1]:]
        response = self.tokenizer.decode(
            generated_ids,
            skip_special_tokens=True
        )

        return response.strip()