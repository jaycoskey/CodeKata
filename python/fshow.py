#!/usr/bin/env python3

import re


def fshow(fmt, *args):
    pattern = "(\{(?:0|[1-9]\d*)\})"
    prog = re.compile(pattern)
    matches = re.findall(prog, fmt)
    if matches is None:
        return fmt
    try:
        str2id = lambda s: int(s[1: len(s) - 1])
        grp2id = { matches[k]: str2id(matches[k])
                   for k in range(len(matches))
                 }
    except Exception as ex:
        raise ex

    maxid = max(grp2id.values())
    if maxid > len(args) - 1:
        return ValueError(f'Error: printf max index of {maxid} exceeds argument count')
    result = prog.sub(lambda m: str(args[grp2id[m.group(0)]]), fmt)
    return result


def test_fshow():
    result = fshow("{1} {0} {2}", 17, "YoYoYo!", 3.14159)
    print(result)
    assert(result == 'YoYoYo! 17 3.14159')


if __name__ == '__main__':
    test_fshow()
