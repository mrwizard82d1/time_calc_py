%% @doc Summarize a set of activities in a file.


-module(summarize).
-compile(export_all).


%% @doc Converts a list of events to a list of activities.
%%
%% @spec events_to_activites(events()) -> activities()
events_to_activities(Events) ->
		Activities = events_to_activities(Events, []),
		lists:reverse(Activities).

events_to_activities([Start, End | RestEvents], Activities) ->
		Activity = make_activity(Start, End),
		events_to_activities([End | RestEvents], [Activity | Activities]);
events_to_activities([_], Activities) ->
		Activities.


%% @doc Summarizes a file of events.
execute(FileOrFilename) ->
		AllLines = read_all_lines(FileOrFilename),
		summarize_lines(AllLines).

execute() ->
		AllLines = read_all_lines(),
		summarize_lines(AllLines).


%% @doc Converts a string to a date.
list_to_date(Text) ->
		Year = string:substr(Text, 1, 4),
		Month = string:substr(Text, 5, 2),
		Day = string:substr(Text, 7, 2),
		{list_to_integer(Year), list_to_integer(Month), list_to_integer(Day)}.


%% @doc Converts a string to an event.
list_to_event(Text) ->
		Tokens = string:tokens(Text, [$ ]),
		Date = list_to_date(lists:nth(1, Tokens)),
		Time = list_to_time(lists:nth(2, Tokens)),
		Tag = lists:nth(3, Tokens),
		{Date, Time, Tag}.


%% @doc Converts a string to a time.
list_to_time(Text) ->
		Hour = string:substr(Text, 1, 2),
		Min = string:substr(Text, 3, 2),
		{list_to_integer(Hour), list_to_integer(Min)}.


%% @doc "main" function.
main([InFilename]) ->
		Summary = execute(InFilename),
		write_summary(Summary).

main() ->
		Summary = execute(),
		write_summary(Summary).

		
%% @doc Makes an activity between two events.
%%
%% @spec make_activity(Start::event(), End::event())
make_activity({{Year, Month, Day}, {StartHour, StartMin}, Tag},
							{{Year, Month, Day}, {EndHour, EndMin}, _}) 
	when EndMin > StartMin ->
		Duration = (EndHour - StartHour) + ((EndMin - StartMin) / 60),
		{Tag, Duration};
make_activity({{Year, Month, Day}, {StartHour, StartMin}, Tag},
						  {{Year, Month, Day}, {EndHour, EndMin}, _})
	when EndHour > StartHour ->
		Duration =
				if
						EndMin >= StartMin ->
								(EndHour - StartHour) +
										((EndMin - StartMin) / 60);
						true ->
								(EndHour - StartHour - 1) +
										((EndMin - StartMin + 60) / 60)
				end,
		{Tag, Duration}.

%% @doc Read all lines from a named file.
read_all_lines(Filename) when is_list(Filename) ->
		{ok, File} = file:open(Filename, read),
		read_all_lines(File);
read_all_lines(File) when is_pid(File) ->
		AllLines = read_all_lines(File, []),
		lists:reverse(AllLines).

read_all_lines() ->
		AllLines = read_all_lines(standard_io, []),
		lists:reverse(AllLines).

read_all_lines(File, Result) ->
		case io:get_line(File, '') of
				eof ->
						Result;
				NextLine ->
						StrippedLine = string:strip(NextLine, right, $\n),
						read_all_lines(File, [StrippedLine | Result])
		end.


%% @doc Summarize a list of activities.
summarize_activities(Activities) ->
		summarize_activities(Activities, dict:new()).

summarize_activities([{Tag, Duration} | RestActivities], Summary) ->
		NewSummary = dict:update(Tag, fun(Value) -> Value + Duration end,
														 Duration, Summary),
		summarize_activities(RestActivities, NewSummary);
summarize_activities([], Summary) ->
		Summary.


%% @doc Summarize a list of lines.
summarize_lines(AllLines) ->
		Events = lists:map(fun(Line) -> list_to_event(Line) end, AllLines),
		Activities = events_to_activities(Events),
		summarize_activities(Activities).


%% @doc Writes a summary to standard output.
write_summary(Summary) ->
		AllTags = dict:fetch_keys(Summary),
		lists:foreach(fun(Tag) ->
													Value = dict:fetch(Tag, Summary),
													io:format("~-16s\t~.2f~n", [Tag, Value]) end,
									AllTags).
