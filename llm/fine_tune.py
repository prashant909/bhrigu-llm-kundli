# llm/fine_tune.py

from unsloth import FastLanguageModel
from datasets import load_dataset
import torch

# ✅ 1. Load Base Model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/mistral-7b-bnb-4bit",
    max_seq_length = 2048,
    dtype = torch.float16,
    load_in_4bit = True,
)

# ✅ 2. Load Your JSONL Dataset
# Format: [{"prompt": "...", "completion": "..."}]
dataset = load_dataset("json", data_files="data/bhrigu_dataset.jsonl")

# ✅ 3. Preprocess Dataset
def format(example):
    return {
        "input": example["prompt"],
        "output": example["completion"]
    }

dataset = dataset.map(format)

# ✅ 4. Apply SFT (Supervised Fine-Tuning)
FastLanguageModel.prepare_for_training(model)

from trl import SFTTrainer
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset["train"],
    dataset_text_field = "input",
    max_seq_length = 2048,
    packing = False,
    args = {
        "output_dir": "llm/mistral-bhrigu",
        "num_train_epochs": 3,
        "per_device_train_batch_size": 2,
        "gradient_accumulation_steps": 2,
        "logging_steps": 10,
        "save_steps": 50,
        "learning_rate": 2e-4,
        "lr_scheduler_type": "cosine",
        "warmup_ratio": 0.1,
        "bf16": False,
        "fp16": True,
        "optim": "paged_adamw_8bit",
        "save_total_limit": 2,
    },
)

trainer.train()

# ✅ 5. Save Model
model.save_pretrained("llm/mistral-bhrigu")
tokenizer.save_pretrained("llm/mistral-bhrigu")
