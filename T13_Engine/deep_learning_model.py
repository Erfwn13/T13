import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer


class DeepConversationalModel:
    def __init__(self, model_name="auto", device="cpu", lang="fa"):
        """
        اگر model_name='auto' باشد، مدل فارسی برای fa و مدل انگلیسی برای en بارگذاری می‌شود.
        """
        if model_name == "auto":
            model_name = "HooshvareLab/gpt2-fa" if lang == "fa" else "gpt2"
        try:
            self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
            self.model = GPT2LMHeadModel.from_pretrained(model_name)
            self.device = torch.device(device)
            self.model.to(device=self.device)  # type: ignore
        except Exception as e:
            self.tokenizer = None
            self.model = None
            self.device = torch.device(device)
            self.error = str(e)

    def generate_response(
        self, prompt, max_length=100, temperature=1.0, top_k=50, top_p=0.95
    ):
        if not self.model or not self.tokenizer:
            return f"مدل عمیق بارگذاری نشد: {getattr(self, 'error', 'نامشخص')}"
        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt")
            # ساخت attention_mask برای رفع هشدار
            attention_mask = torch.ones_like(inputs)
            if hasattr(inputs, 'to'):
                inputs = inputs.to(self.device)
                attention_mask = attention_mask.to(self.device)
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    attention_mask=attention_mask,
                    max_length=max_length,
                    do_sample=True,
                    temperature=temperature,
                    top_k=top_k,
                    top_p=top_p,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            return f"Error: {str(e)}"


if __name__ == "__main__":
    model = DeepConversationalModel(
        device="cuda" if torch.cuda.is_available() else "cpu"
    )
    prompt = "گفتگوی خودکار: جلسه یادگیری جدید"
    print("پاسخ مدل:", model.generate_response(prompt, max_length=150))
