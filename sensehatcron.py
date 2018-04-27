import datetime

from sense_hat import SenseHat

from nakama import get_latest_one_piece_chapter_jb, get_latest_one_piece_chapter_ms

if __name__ == "__main__":
    print(get_latest_one_piece_chapter_jb())
    print(get_latest_one_piece_chapter_ms())
    
