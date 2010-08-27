-module(summarize_time).
-compile(export_all).

for_each_line_in_file(Name, Proc, Mode, Accum) ->
	{ ok, Device } = file:open(Name, Mode),
	Result = for_each_line( Device, Proc, Accum ),
	file:close( Device),
	Result.

for_each_line(Device, Proc, Accum) ->
	case io:get_line(Device, "") of
		eof -> Accum;
		Line ->
			NewAccum = Proc(Line, Accum),
			for_each_line(Device, Proc, NewAccum)
	end.

read_lines(Filename) ->
	{ ok, Device } = file:open( Filename, [read] ),
	Result = collect_lines( Device ),
	file:close( Device),
	Result.

collect_lines(Device) ->
	case io:get_line(Device, "") of
		eof -> [];
		Line -> [ Line | collect_lines(Device) ]
	end.

parse_time_line( Line ) ->
	{ ok, [ DateText, TimeText | DetailsStrings ] } = regexp:split( Line, "\s"),
	{ DateText, TimeText, join_strings(DetailsStrings) }.

join_strings([]) ->
	[];
join_strings( [ HeadString | Tail ] ) ->
	string:strip( string:concat( string:concat( HeadString, " " ), 
			join_strings( Tail ) ) ).
