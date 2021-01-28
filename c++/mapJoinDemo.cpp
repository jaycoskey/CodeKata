#include <algorithm>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

using std::cout;
using std::endl;
using std::map;
using std::string;
using std::vector;

using Ints = vector<int>;
using Intss = vector<vector<int>>;
using Strings = vector<string>;
using String2Ints = map<string, Ints>;
using String2Strings = map<string, Strings>;


struct MapJoinDemo {
    static String2Ints
    getTeamAvails(String2Ints &memberAvails, String2Strings &teamMembers)
    {
        auto mem2avails = [&](string &mem) { return memberAvails[mem]; };
        auto unifyN = [](Intss &xss, int n) {
	    Ints acc(7, 0);
            std::transform(xss.begin(), xss.end(), acc.begin()
                , [=](Ints &xs) { return xs[n] == 1; }
                );
	    return std::any_of(acc.begin(), acc.end(), [](bool b) { return b; }); 
            };
        auto unify = [&](Intss &xss) {
	    Ints days{0, 1, 2, 3, 4, 5, 6};
	    Ints result(7, 0);
            std::transform(days.begin(), days.end(), result.begin()
                , [&](int n) { int x = unifyN(xss, n) ? 1 : 0; return x; }
		);
	    return result;
            };

        String2Ints result{ };
	for (auto &[teamName, memberNames] : teamMembers) {
	    Intss availss{ };
	    std::for_each(memberNames.begin(), memberNames.end()
                , [&](string &memberName) { availss.push_back(mem2avails(memberName)); }
		);
	    result.insert(std::pair<string, Ints>(teamName, unify(availss)));
	}
        return result;
    }
};

string join(vector<int> xs, string (*mapfunc)(int)
    , const char *pre, const char *delim, const char *post)
{
    std::stringstream ss;
    ss << pre;
    bool isLaterIteration = false;
    for (auto &x : xs) {
        if (isLaterIteration) { ss << delim; }
	else { isLaterIteration = true; }
        ss << mapfunc(x);
    }
    ss << post;
    return ss.str();
}

int main(int argc, char **argv) {
    static constexpr auto AMY = "Amy";
    static constexpr auto BOB = "Bob";
    static constexpr auto CAT = "Cat";
    static constexpr auto DAN = "Dan";

    static constexpr auto DEV = "Dev";
    static constexpr auto OPS = "Ops";

    String2Ints memberAvails = {
        { AMY, {1,0,0,0,0,0,1} }
        ,{ BOB, {1,1,1,0,0,0,0} }
        ,{ CAT, {0,0,0,0,1,1,1} }
        ,{ DAN, {1,1,0,0,0,1,1} }
    };
    
    String2Strings teamMembers = {
        { DEV, { AMY, BOB } }
        ,{ OPS, { CAT, DAN } }
    };

    for (auto &kv : MapJoinDemo::getTeamAvails(memberAvails, teamMembers)) {
        cout << kv.first << ": " << join(kv.second, std::to_string, "[", ", ", "]") << endl;
    }
}
