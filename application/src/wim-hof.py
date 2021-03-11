#!/usr/bin/env python3
from logmanager import LogManager
from wimhofbreather import WimHofBreather

wim_hof_class = WimHofBreather()
wim_hof_class.lets_do_some_breathing()

log_manager = LogManager('breathing-log.tsv')
journal_entry = log_manager.ask_for_journal_entry()
log_manager.save_entry(journal_entry, wim_hof_class.get_breathing_times())
log_manager.output_breathing_log(5)

print("\nWim would be proud :)")
