def import_txt_file(filename: str) -> list[list[int]]:
  report_list = []
  with open(filename, 'r') as file:
    for line in file:
      report = [int(x) for x in line.strip().split()]
      report_list.append(report)
  return report_list

def is_safe(report: list[int]) -> tuple[bool, int | None]:
  # Returns whether report is safe with an optional int giving first
  # problematic index.
  assert len(report) > 0
  # First check whether report is increasing or decreasing
  diff = report[1] - report[0]
  if diff > 0:
    # Report is increasing
    for i in range(1, len(report)):
      diff = report[i] - report[i - 1]
      if diff < 1 or diff > 3:
        return False, i
  elif diff < 0:
    # Report is decreasing
    for i in range(1, len(report)):
      diff = report[i - 1] - report[i]
      if diff < 1 or diff > 3:
        return False, i
  else:
    # diff = 0 so return False
    return False, 1

  return True, None

report_list = import_txt_file('inputs/day02.txt')

# Part 1: Compute number of "safe" reports.
# For each report, determine whether it is "safe".
# "safe" means that report is increasing or decreasing by between 1 and 3.
# Test with sample data:
# report_list = [
#   [7, 6, 4, 2, 1],
#   [1, 2, 7, 8, 9],
#   [9, 7, 6, 2, 1],
#   [1, 3, 2, 4, 5],
#   [8, 6, 4, 4, 1],
#   [1, 3, 6, 7, 9],
# ]
total_result = [is_safe(report) for report in report_list]
report_result, problematic_indices = zip(*total_result)
# print(report_result)
# print(problematic_indices)
init_num_safe_reports = sum(report_result)
print('Part 1:', init_num_safe_reports)

# Part 2: Compute number of safe reports with problem dampener.
# Problem dampener allows one to remove a number from the report,
# and if then it is safe, the report is considered safe.
second_report_result = []
for report, ind in zip(report_list, problematic_indices):
  # First check whether report is safe without removing any number
  if ind is None:
    second_report_safe = True
  else:
    assert ind >= 1
    # Report is not safe, so try removing the problematic index if it is > 2.
    if ind > 2:
      del report[ind]
      second_report_safe, _ = is_safe(report)
    else:
      second_report_safe = False
      # If problematic index is 1, then try removing 0 or 1.
      # If problematic index is 2, then try removing 0 or 1 or 2.
      if ind == 1:
        candidate_indices = [0, 1]
      if ind == 2:
        candidate_indices = [0, 1, 2]
      for i in candidate_indices:
        # Make a copy of the report
        report_copy = report.copy()
        del report_copy[i]
        safe, _ = is_safe(report_copy)
        if safe:
          second_report_safe = True
          break
  second_report_result.append(second_report_safe)
# print(second_report_result)
print('Part 2:', sum(second_report_result))


  
