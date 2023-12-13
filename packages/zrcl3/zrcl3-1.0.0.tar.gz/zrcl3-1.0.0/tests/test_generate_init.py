import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zrcl3.init_generator import generate_init # noqa

def test_generate():
    generate_init("zrcl3", safe=True)