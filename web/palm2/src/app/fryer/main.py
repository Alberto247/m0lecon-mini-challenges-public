from PIL import Image

import fryer, sys

'''
    Quick meme thrown together with the help of StackOverflow and some GitHub repos found online
'''


def load():
    print(sys.argv[1])
    image = Image.open(sys.argv[1])
    layers = int(sys.argv[2])
    emote_amount = int(sys.argv[3])
    noise = float(sys.argv[4])
    contrast = int(sys.argv[5])
    return image, layers, emote_amount, noise, contrast


if __name__ == '__main__':
    image, layers, emote_amount, noise, contrast = load()

    fried = fryer.fry(image, emote_amount, 0, contrast)
    for layer in range(layers - 1):
        fried = fryer.fry(fried, emote_amount, noise, contrast)

    print(f"saving {sys.argv[6]}")
    fried.save(sys.argv[6])
