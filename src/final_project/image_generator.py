from big_sleep import Imagine

import torch
torch.cuda.empty_cache()

def draw_journal_picture():
    dream = Imagine(
        text = "mountain view",
        image_size=128,
        save_every = 1,
        epochs=1,
        iterations=200,
        save_progress = False
    )
    dream()
    pass

if __name__ == "__main__":
    draw_journal_picture()