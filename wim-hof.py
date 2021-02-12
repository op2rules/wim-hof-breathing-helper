#!/usr/bin/env python3
from logmanager import LogManager
from wimhofbreather import WimHofBreather

wim_hof_class = WimHofBreather()
wim_hof_class.lets_do_some_breathing()

log_manager = LogManager('breathing_log.tsv')
log_manager.save_breathing_time_to_today(wim_hof_class.get_breathing_times())
log_manager.output_breathing_log(5)

print("\nWim would be proud :)")
