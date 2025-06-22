def convert_to_qa(text_file, output_file="data/bhrigu_dataset.jsonl"):
    with open(text_file, "r", encoding="utf-8") as f:
        content = f.read()

    qa_pairs = []
    for line in content.split('\n'):
        if "house" in line.lower() or "planet" in line.lower():
            qa = {
                "context": line.strip(),
                "question": f"What does this say about a person?",
                "answer": line.strip()
            }
            qa_pairs.append(qa)

    os.makedirs("data", exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        for qa in qa_pairs:
            f.write(f"{qa}\n")

    print("✅ Saved QA dataset:", output_file)
