from big_sleep import Imagine

import torch
torch.cuda.empty_cache()

def draw_journal_picture():
    dream = Imagine(
        text = "victory against combatant|forest path|rocky terrain",
        image_size=256,
        save_every = 25,
        epochs=5,
        iterations=500,
        num_cutouts=32,
        save_progress = False
    )
    dream()
    pass

if __name__ == "__main__":
    draw_journal_picture()