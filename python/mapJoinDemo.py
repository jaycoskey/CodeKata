#!/usr/bin/env python

# See the Java version of an interpretation of the data and functions

AMY = 'Amy'
BOB = 'Bob'
CAT = 'Cat'
DAN = 'Dan'

DEV = 'Dev'
OPS = 'Ops'

member_availabilities = {
    AMY: [1,0,0,0,0,0,1]
    , BOB: [1,1,1,0,0,0,0]
    , CAT: [0,0,0,0,1,1,1]
    , DAN: [1,1,0,0,0,1,1]
    }

team_members = {
    DEV: [AMY, BOB]
    , OPS: [CAT, DAN]
    }

def get_team_avail(member_availabilities, team_members):
    mem2avail = lambda b: member_availabilities[b]
    unify_n = lambda xss, n: any([xs[n] == 1 for xs in xss])
    unify = lambda xss: [1 if unify_n(xss, n) else 0 for n in range(7)]
    result = {k: unify(list(map(mem2avail, v))) for k, v in team_members.items()}
    return result

if __name__ == '__main__':
    for k, v in sorted(get_team_avail(member_availabilities, team_members).items()):
        print(f'{k}: {v}')
