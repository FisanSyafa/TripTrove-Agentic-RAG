"""
Fine-tune Llama 3.1 dengan LoRA untuk TripTrove
Menggunakan unsloth untuk efisiensi maksimal
"""
print("="*60)
print("🎓 TripTrove Fine-Tuning dengan LoRA")
print("="*60)

print("\n⚠️  CATATAN PENTING:")
print("Fine-tuning memerlukan library tambahan yang cukup besar.")
print("Estimasi download: 2-5 GB")
print("Estimasi waktu training: 30-60 menit (tergantung hardware)")
print("\nApakah Anda ingin melanjutkan? (y/n): ", end="")

response = input().lower()
if response != 'y':
    print("❌ Fine-tuning dibatalkan")
    exit()

print("\n📦 Installing required packages...")
print("Ini mungkin memakan waktu beberapa menit...")

import subprocess
import sys

# Install dependencies
packages = [
    "torch",
    "transformers",
    "peft",
    "accelerate",
    "bitsandbytes",
    "datasets",
    "trl"
]

for package in packages:
    print(f"   Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])

print("✅ Packages installed!\n")

# Now import
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from datasets import load_dataset
from trl import SFTTrainer
import torch
from pathlib import Path

print("="*60)
print("🚀 Starting Fine-Tuning Process")
print("="*60)

# Configuration
MODEL_NAME = "meta-llama/Llama-3.1-8B"  # Atau path ke model lokal Anda
OUTPUT_DIR = "./models/triptrove-llama"
TRAINING_DATA = "./training_data.jsonl"

print(f"\n📋 Configuration:")
print(f"   Base Model: {MODEL_NAME}")
print(f"   Output: {OUTPUT_DIR}")
print(f"   Training Data: {TRAINING_DATA}")

# Check if training data exists
if not Path(TRAINING_DATA).exists():
    print(f"\n❌ Training data not found: {TRAINING_DATA}")
    print("   Run: python prepare_training_data.py first")
    exit()

print("\n1️⃣ Loading base model...")
print("   (This may take a few minutes...)")

# Load model with 4-bit quantization for efficiency
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    load_in_4bit=True,
    device_map="auto",
    trust_remote_code=True
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token

print("✅ Model loaded!")

print("\n2️⃣ Preparing model for LoRA...")

# LoRA configuration
lora_config = LoraConfig(
    r=16,  # LoRA rank
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, lora_config)

print("✅ LoRA configured!")
print(f"   Trainable parameters: {model.print_trainable_parameters()}")

print("\n3️⃣ Loading training data...")

# Load dataset
dataset = load_dataset('json', data_files=TRAINING_DATA, split='train')

print(f"✅ Loaded {len(dataset)} training examples")

print("\n4️⃣ Setting up training...")

# Training arguments
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    save_steps=50,
    logging_steps=10,
    save_total_limit=2,
    report_to="none"
)

# Trainer
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=training_args,
    tokenizer=tokenizer,
    max_seq_length=512,
    dataset_text_field="text"  # Will be formatted
)

print("✅ Trainer ready!")

print("\n5️⃣ Starting training...")
print("   This will take 30-60 minutes depending on your hardware")
print("   You can monitor progress below:\n")

# Train!
trainer.train()

print("\n✅ Training complete!")

print("\n6️⃣ Saving fine-tuned model...")

# Save model
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"✅ Model saved to {OUTPUT_DIR}")

print("\n" + "="*60)
print("🎉 Fine-Tuning Complete!")
print("="*60)
print(f"\nYour fine-tuned model is ready at: {OUTPUT_DIR}")
print("\nNext steps:")
print("1. Update .env: FINETUNED_MODEL_PATH=./fine_tuning/models/triptrove-llama")
print("2. Restart application: streamlit run app.py")
print("3. Test the improved responses!")
print("="*60)
