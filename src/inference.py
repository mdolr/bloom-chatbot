from huggingface_hub import notebook_login
from huggingface_hub import HfFolder
from huggingface_hub.inference_api import InferenceApi

inference = InferenceApi("bigscience/bloom", token=HfFolder.get_token())


def infer(prompt,
          seed=0,
          max_length=32,
          top_k=0,
          num_beams=0,
          no_repeat_ngram_size=2,
          top_p=0.9,
          temperature=0.7,
          greedy_decoding=False,
          return_full_text=False):
    """
    Inference function taken from sentdex example
    <https://github.com/Sentdex/BLOOM_Examples/blob/main/BLOOM_api_example.ipynb>
    """

    top_k = None if top_k == 0 else top_k
    do_sample = False if num_beams > 0 else not greedy_decoding
    num_beams = None if (greedy_decoding or num_beams == 0) else num_beams
    no_repeat_ngram_size = None if num_beams is None else no_repeat_ngram_size
    top_p = None if num_beams else top_p
    early_stopping = None if num_beams is None else num_beams > 0

    params = {
        "max_new_tokens": max_length,
        "top_k": top_k,
        "top_p": top_p,
        "temperature": temperature,
        "do_sample": do_sample,
        "seed": seed,
        "early_stopping": early_stopping,
        "no_repeat_ngram_size": no_repeat_ngram_size,
        "num_beams": num_beams,
        "return_full_text": return_full_text
    }

    response = inference(prompt, params=params)
    return response
