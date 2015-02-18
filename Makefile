default: test-pahole

test-pahole: test-pahole.cc
	g++ -ggdb -std=c++11 $< -o $@
