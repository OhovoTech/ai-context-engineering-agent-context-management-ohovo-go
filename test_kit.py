from context_engineering_kit import PointerStore, compress_text, select_relevant, isolate_context

def test_pointer():
    s = PointerStore("/tmp/test_ptrs")
    ptr = s.store("hello world" * 100)
    assert "pointer" in ptr
    loaded = s.load(ptr["pointer"])
    assert loaded and "hello world" in loaded

def test_compress():
    t = "One. Two is longer sentence here. Three. Four also long enough. Five."
    c = compress_text(t, max_sentences=3)
    assert len(c) < len(t)

def test_select():
    res = select_relevant("python code", ["python is great", "java rocks", "code in python"])
    assert res[0][1] > 0

def test_isolate():
    full = {"a_x": 1, "b_y": 2, "shared_z": 3}
    iso = isolate_context(full, "a")
    assert "a_x" in iso and "b_y" not in iso
