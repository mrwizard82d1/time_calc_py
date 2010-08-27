#! env ruby


# Module to summarize the time taken for at-work activities.


require 'time'


class Activity
  attr_accessor :start, :details, :duration
  def initialize(*args)
    self.from_text(args[0]) if args.length == 1
    self.from_state(args[0], args[1]) if args.length == 2
  end

  def end
    @start + duration if duration != nil
    @start
  end

  def end=(arg)
    @duration = arg
    if arg.methods.any? { |m| m == 'start' }
      @duration = arg.start - @start
    end
    self
  end

  def from_text(aLine)
    # split into start time text and details
    date_text, @details =
      aLine.match(/(\d{4}-?\d{2}-?\d{2}\s+\d{2}:?\d{2})\s+(.+)$/)[1..2]

    # replace separators
    date_text.gsub!(/-/, '')
    date_text.gsub!(/:/, '')

    # convert to a start time
    @start = Time.parse(date_text)
  end

  def from_state(start, details)
    @start = start
    @details = details
  end

  def to_s
    duration_text = "nil "
    if ! @duration.nil?
      equivalent_time = Time.at(@duration).gmtime
      duration_text = equivalent_time.strftime("%H:%M")
    end

    "%s %s %s" % [@start.strftime("%Y%m%d %H%M"), duration_text, @details]
  end

end


class ConsecutiveActivities
  include Enumerable
  
  def initialize(lines)
    @activities = lines.collect { | l | Activity.new l }
    (0...@activities.length - 1).each do
      | i |
      @activities[i].end = @activities[i+1]
    end
  end
  
  def each(&b)
    @activities.each(&b)
  end
  
end


class Summarizer
  def initialize(activities)
    @summary = Hash.new 0
    activities.each do
      | activity |
      @summary[activity.details] += activity.duration if activity.duration
    end
  end

  def to_s
    @summary.keys.sort.collect do
      | detail |
      "%-12s\t%.02f\n" % ["%s:" % [detail], @summary[detail] / 3600]
    end
  end

end


all_lines = ARGF.collect
as = ConsecutiveActivities.new(all_lines)
puts Summarizer.new(as.collect).to_s

