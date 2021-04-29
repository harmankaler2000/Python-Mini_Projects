from sample_madlibs import code,hp,hunger_games,zombie
import random

if __name__ == "__main__":
    mad = random.choice([hp,code,zombie,hunger_games])
    mad.madlib()