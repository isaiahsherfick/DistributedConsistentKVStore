My attempt at a distributed KV store with multiple different consistency models



files:
	src/eventual
		client_eventual.py: the client
		logical_clock.py: lamport clock
		server_eventual.py: messy, messy but working eventual server
		config: configfile
		message.py: message class with clocks, barely used for eventual implementation
		RUN_ME.py: test suite for eventual
		top_level_controller.py: driver/middleware thing that spawns server processes

	src/sequential
		alice,bob,etc.py: test processes, needed to be different files for unique pids

		client_sequential.py: sequential client. much cleaner than eventual
		server_sequential.py: sequential server. much cleaner than eventual
		logical_clock.py: identical lamport clock implementation
		message.py: identical timestamped message implementation
		sequential_test.py: deprecated, non-functional test suite
				    left behind to demonstrate that I did 
				    spend a lot of time running tests
		middleware_sequential.py: middleware to intercept and re-order messages
					  to achieve total order broadcasts
		RUN_ME.py: test suite for sequential

I used the built-in dictionary class for Python as it is very simple to use
and I was already familiar with it.

