;;;
;;; Clojure script to summarize how I spend my time.
;;;


(require 'clojure.string)


(defn lines [in-stream]
  "Returns all the lines in-stream."
  (filter #(not (empty? %1)) (line-seq (java.io.BufferedReader. in-stream))))


(defn extract-int
  "Extracts an integer from-text starting at start for length.

  If length is not supplied, the extracted integer extends from start to
  the end of from-text." 
  ([from-text start length]
     (Integer/parseInt (.substring from-text start (+ start length))))
  ([from-text start]
     (Integer/parseInt (.substring from-text start))))


(defn make-task [line]
  "Create a task from a line."
  (let [[date-text time-text category] (clojure.string/split line
							     #"\s" 3)
	year (extract-int date-text 0 4)
	month (dec (extract-int date-text 4 2))
	date (extract-int date-text 6)
	hour (extract-int time-text 0 2)
	min (extract-int time-text 2)
	date-time (java.util.Calendar/getInstance)]
    (.set date-time year month date hour min)
    {:start date-time
     :end date-time
     :category category}))


(defn task-duration [task]
  (- (.getTimeInMillis (:end task))
     (.getTimeInMillis (:start task))))


(defn make-contiguous [before after]
  "Return a new task from before that is contiguous with after."
  (merge before {:end (:start after)}))

	
(defn make-tasks-contiguous [tasks]
  "Make a sequence of tasks contiguous. In other words, the start of
  the next task is the end of the first."
  (map #(make-contiguous %1 %2) tasks (rest tasks)))


(defn summarize-task [a-task]
  "Summarize a single task."
  {(:category a-task) (task-duration a-task)})


(defn summarize-tasks [in-stream]
  "Summarize all the tasks in-stream."
  (reduce #(merge-with + %1 %2)
	  (map summarize-task
	       (make-tasks-contiguous (map make-task (lines
						      in-stream))))))


(defn decimal-duration [duration-in-millis]
  "Convert a duration in milliseconds to a decimal duration of hours."
  (let [seconds (/ duration-in-millis 1000)]
    (/ seconds 3600)))


(defn write-summary [summary]
  (doseq [key (sort (keys summary))]
    (printf "%-16s%.2f\n" key (double (decimal-duration (summary key))))))


(defn main []
  (let [in-stream (java.io.FileReader.
		   (if *command-line-args*
		     (first *command-line-args*)
		     "time.txt"))]
    (write-summary (summarize-tasks in-stream))))

		    
(def tasks (make-tasks-contiguous
	    (map make-task (lines (java.io.FileReader. "time.txt")))))


(main)
