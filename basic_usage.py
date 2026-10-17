#!/usr/bin/env python3
from context_engineering_kit import PointerStore, compress_text, select_relevant, isolate_context

def main():
    # Externalize
    store = PointerStore(root="/tmp/demo_pointers")
    big = "A" * 5000 + " important error code 0xDEADBEEF " + "B" * 5000
    ptr = store.store(big, summary="Large log containing error 0xDEADBEEF")
    print("Pointer for agent context:", ptr)

    # Compress
    long_text = "Sentence one. Sentence two is longer and has more words. Short. Another detailed sentence with many terms. Final."
    print("Compressed:", compress_text(long_text, max_sentences=3))

    # Select
    docs = ["cats are fluffy", "dogs bark loudly", "the weather is rainy today"]
    print("Relevant to 'dog':", select_relevant("dog bark", docs))

    # Isolate
    full = {"agent_a_plan": "do X", "agent_b_plan": "do Y", "shared_ptr": "ptr_123"}
    print("Isolated for agent_a:", isolate_context(full, "agent_a"))

    print("Done — all local, zero lag.")

if __name__ == "__main__":
    main()
