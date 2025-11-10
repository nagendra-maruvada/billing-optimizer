packages = [
    ("pandas", "pd"),
    ("numpy", "np"),
    ("scikit-learn", "sklearn"),
    ("transformers", "transformers"),
    ("torch", "torch"),
    ("tqdm", "tqdm"),
]

for name, module in packages:
    try:
        m = __import__(module)
        version = getattr(m, "__version__", "(no __version__)")
        print(f"{name}: OK — {version}")
    except Exception as e:
        print(f"{name}: FAILED — {e}")
