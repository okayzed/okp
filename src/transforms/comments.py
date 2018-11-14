from util import *

def skip_comments(lines):
    return comment_remover(''.join(lines)).split('\n')

