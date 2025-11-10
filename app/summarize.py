from transformers import pipeline
import os


def get_summary_engine(allow_download: bool = True):
    """Return a text-generation pipeline. If allow_download is True the function
    will attempt to download the model if it's not cached. If False it will run
    in offline-only mode and return None on failure.
    """
    # First try in whatever environment mode is currently set (may be offline)
    try:
        generator = pipeline("text-generation", model="distilgpt2")
        return generator
    except Exception as e:
        # If downloads are disallowed, bail out with a clear message
        if not allow_download:
            print("Warning: could not load model in offline mode. Summaries will be text-only.", e)
            return None

        # Otherwise, attempt to enable downloads and retry once
        print("Info: model not available locally; attempting to download the model...")
        # Unset TRANSFORMERS_OFFLINE in this process so transformers can fetch files
        os.environ.pop("TRANSFORMERS_OFFLINE", None)
        try:
            generator = pipeline("text-generation", model="distilgpt2")
            return generator
        except Exception as e2:
            print("Warning: failed to download/load the model. Summaries will be text-only.", e2)
            return None


def generate_summary(generator, user_id, avg_usage, current_plan, rec_plan):
    if generator:
        prompt = f"User {user_id} uses about {avg_usage:.1f} GB/month on {current_plan}. Recommend switching to {rec_plan} to save cost."
        # Keep generation short and deterministic: explicit truncation and limited new tokens
        result = generator(
            prompt,
            max_new_tokens=40,
            do_sample=False,
            truncation=True,
            num_return_sequences=1,
        )
        text = result[0].get('generated_text', '')
        return text.strip()  # remove excessive whitespace/newlines
    else:
        return f"User {user_id} uses {avg_usage:.1f} GB/month. Recommend {rec_plan} for better savings."
