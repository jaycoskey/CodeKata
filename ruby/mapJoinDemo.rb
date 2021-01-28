#!/usr/bin/env ruby

# See the Java version of an interpretation of the data and functions

AMY = 'Amy'
BOB = 'Bob'
CAT = 'Cat'
DAN = 'Dan'

DEV = 'Dev'
OPS = 'Ops'

member_availabilities = {
    AMY => [1,0,0,0,0,0,1],
    BOB => [1,1,1,0,0,0,0],
    CAT => [0,0,0,0,1,1,1],
    DAN => [1,1,0,0,0,1,1]
    }

team_members = {
    DEV => [AMY, BOB],
    OPS => [CAT, DAN]
    }

def get_team_avail(member_availabilities, team_members)
    mem2avail = lambda { | b | member_availabilities[b] }
    unify_n = lambda { |xss, n | (xss.map {|xs| xs[n] == 1}).any? }
    unify = lambda { | xss | (0..6).map {|n| unify_n.call(xss, n) ? 1 : 0} }
    result = team_members.map { |k, v| [k, unify.call(v.map {|b| mem2avail.call(b)})] }
    result
end

# if $PROGRAM_NAME == __FILE__
# end

items = get_team_avail(member_availabilities, team_members)
# print(k + ": " + items[v].map(lambda {|i| i.to_s}).join(', '))
items.sort.each do |k, v|
    print(k + ": [")
    have_started_loop = false
    v.each do |x|
        if have_started_loop
	    print(", ")
	else
	    have_started_loop = true
	end
        print(x)
    end
    puts "]"
end

