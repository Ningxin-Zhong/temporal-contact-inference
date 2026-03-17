#!/usr/bin/env python3
"""Analyse a vampire infiltration.
   Vampire Hunting v1.5.1

   Student number: 23016518
"""

import sys
import os.path
from format_list import format_list, format_list_or, str_time, is_initial, period_of_time, day_of_time, time_of_day


# Section 2
def file_exists(file_name):
    """Verify that the file exists.

    Args:
        file_name (str): name of the file

    Returns:
        boolean: returns True if the file exists and False otherwise.
    """
    return os.path.isfile(file_name)


# Section 3
def parse_file(file_name):
    """Read the input file, parse the contents and return some data structures
    that contain the associated data for the vampire infiltration.

    Args:
        file_name (str): Contains the name of the file.

    Returns:
        participants: list of participants.
        days: list of pairs; the first element of a pair is the result of tests
          (dictionary from participants to "H"/"V"); the second is a list of
          contact groups (list of lists of participants)
    """
    f = open(file_name, "r")

    line1 = f.readline().strip()   # read participants in the first line
    participants = [name.strip() for name in line1.split(",")]

    line2 = f.readline().strip()
    if not line2.isdigit():
        print("Error found in file, aborting.")
        sys.exit()
    num_days = int(line2)

    days = []

    for i in range(num_days):
        test_line = f.readline().strip()
        tests = {}

        if test_line != "##":
            entries = test_line.split(",")
            for entry in entries:
                if ":" not in entry:
                    print("Error found in file, aborting.")
                    sys.exit()

                # val represents the test result for each participant, V or H
                name, val = entry.split(":")
                name = name.strip()
                val = val.strip()
                if name not in participants:
                    print("Error found in file, aborting.")
                    sys.exit()
                tests[name] = (val == "V")   # gives the boolean value

        # number of groups 
        line = f.readline().strip()
        if not line.isdigit():
            print("Error found in file, aborting.")
            sys.exit()
        num_groups = int(line)

        # groups 
        groups = []
        for j in range(num_groups):
            line = f.readline().strip()
            lst = [n.strip() for n in line.split(",")]     # lst represents the group list
            groups.append(lst)

        days.append((tests, groups))

    f.close()
    return (participants, days)


# Section 4
def pretty_print_infiltration_data(data):
    """ In this section we print in a more human-readable format than the Python default shown """
    participants, days = data
    num_days = len(days)

    print("Vampire Infiltration Data")

    # Line: "... days with the following participants: ..."
    participant_str = format_list(sorted(participants))
    print(f"{num_days} days with the following participants: {participant_str}.")

    # For each day
    for i, (tests_dict, groups) in enumerate(days, start=1):

        num_tests = len(tests_dict)
        num_groups = len(groups)

        test_word = "test" if num_tests == 1 else "tests"
        contact_group_word = "contact group" if num_groups == 1 else "contact groups"
        group_word_short = "group" if num_groups == 1 else "groups"

        print(f"Day {i} has {num_tests} vampire {test_word} and {num_groups} {contact_group_word}.")

        # Print tests
        print(f"  {num_tests} {test_word}")

        # alphabetical order of test subjects
        for name in sorted(tests_dict.keys()):
            result = tests_dict[name]
            if result:
                print(f"    {name} is a vampire!")
            else:
                print(f"    {name} is human.")

        # Print groups
        print(f"  {num_groups} {group_word_short}")
        for g in groups:
            print(f"    {format_list(sorted(g))}")

    print("End of Days")





# Section 5
def contacts_by_time(participant, time, contacts_daily):
    """ return the contact people for the participant at specific time unit """
    day = day_of_time(time)

    if day < 1 or day > len(contacts_daily):    # checking for valid days
        return []

    groups = contacts_daily[day-1]

    for g in groups:
        if participant in g:
            return sorted(g)
    return []   # participant with no contact on that day


# Section 6
def create_initial_vk(participants):
    """ Initially everyone's status is unknown. """
    knowledge = {}
    for p in participants:
        knowledge[p] = 'U'
    return knowledge


def pretty_print_vampire_knowledge(vk):
    """ Print the status for current vampire knowledge in a desirable way """
    humans = []
    vampires = []
    unclear = []

    for person in sorted(vk.keys()):
        status = vk[person]
        if status == 'H':
            humans.append(person)
        elif status == 'V':
            vampires.append(person)
        else:
            unclear.append(person)

    print("  Humans: " + format_list(humans))
    print("  Unclear individuals: " + format_list(unclear))
    print("  Vampires: " + format_list(vampires))


# Done by professors
def pretty_print_vks(vks):
    print(f'Vampire Knowledge Tables')
    for i in range(len(vks)):
        print(f'Day {str_time(i)}:')
        pretty_print_vampire_knowledge(vks[i])
    print(f'End Vampire Knowledge Tables')


# Section 7
def update_vk_with_tests(vk, tests):
    """ Update the vk based on today's test results """
    for name in tests:
        if name not in vk:
            print('Error found in data: test subject is not a participant; aborting.')
            sys.exit()

    for name, result in tests.items():
        status_set = vk[name]    # status set is U, V, or H
        status = list(status_set)[0]

        if status == 'U':
            vk[name] = 'V' if result else 'H'

        elif status == 'H':
            if result:
                print('Error found in data: humans cannot be vampires; aborting.')
                sys.exit()

        elif status == 'V':
            if not result:
                print('Error found in data: vampires cannot be humans; aborting.')
                sys.exit()

    return vk    # anyone not in test remains in their original status


# Section 8
def update_vk_with_vampires_forward(vk_pre, vk_post):
    """ If someone is V in vk_pre, then they must be V in vk_post.

        If vk_post[p] == "U", update it to "V".

        If vk_post[p] == "H", this is an error """
    for p in vk_pre:
        if vk_pre[p] == "V":
            if vk_post[p] == "H":
                print('Error found in data: vampires cannot be humans; aborting.')
                sys.exit()
            elif vk_post[p] == "U":
                vk_post[p] = 'V'
    return vk_post


# Section 9
def update_vk_with_humans_backward(vk_pre, vk_post):
    """ If a participant is:
    H in vk_post, then they must be H in vk_pre.

    If vk_pre[p] == "U", update it to "H".

    If vk_pre[p] == "V", this is an error """

    for p in vk_post:
        if vk_post[p] == "H":
            if vk_pre[p] == "V":
                print('Error found in data: humans cannot be vampires; aborting.')
                sys.exit()
            elif vk_pre[p] == "U":
                vk_pre[p] = 'H'
    return vk_pre


# Section 10
def update_vk_overnight(vk_pre, vk_post):
    """ There's no hunting during the night,
        so the status remain unchanged after one night """
    for p in vk_pre:
        pre_status = vk_pre[p]
        post_status = vk_post[p]

        # If prior was vampire
        if pre_status == "V":
            if post_status == "H":
                print("Error found in data: vampires cannot be humans; aborting.")
                sys.exit()
            elif post_status == "U":
                vk_post[p] = "V"

        # If prior was human
        elif pre_status == "H":
            if post_status == "V":
                print("Error found in data: humans cannot be vampires; aborting.")
                sys.exit()
            elif post_status == "U":
                vk_post[p] = "H"
    return vk_post


# Section 11
def update_vk_with_contact_group(vk_pre, contacts, vk_post):
    """ In this section we update the vk with more sophisticated contacts information"""

    # vampires in pre cannot be human in post
    for p in vk_pre:
        if vk_pre[p] == "V" and vk_post[p] == "H":
            print('Error found in data: vampires cannot be human; aborting.')
            sys.exit()

    # propagate definite vampires from pre → post
    for p in vk_pre:
        if vk_pre[p] == "V" and vk_post[p] == "U":
            vk_post[p] = 'V'

    # error when participants not in contact groups
    in_group = set()
    for group in contacts:
        for x in group:
            in_group.add(x)

    for p in vk_pre:
        if p not in in_group:
            if vk_pre[p] == "H" and vk_post[p] == "V":
                print('Error found in data: humans cannot be vampires; aborting.')
                sys.exit()

            if vk_pre[p] == "H" and vk_post[p] == "U":
                vk_post[p] = 'H'

    # processing contact groups
    for groups in contacts:
        for x in groups:    # non-participants appearing
            if x not in vk_pre:
                print('Error found in data: contact subject is not a participant; aborting.')
                sys.exit()

        # checking if group is all-human in pre
        pre_statuses = [vk_pre[x] for x in groups]
        all_human = all(s == 'H' for s in pre_statuses)

        # propagating human if all human
        if all_human:
            for x in groups:
                if vk_post[x] == "V":
                    print('Error found in data: humans cannot be vampires; aborting.')
                    sys.exit()
                if vk_post[x] == "U":
                    vk_post[x] = 'H'

        # doing nothing if unknown or vampire in groups

    return vk_post


# Section 12
def find_infection_windows(vks):
    """ recording the time period when a human turns to a vampire """
    iw = {}        # infection window
    last_time = len(vks)-1

    # determine the definite vampires at last time
    final_vampires = [p for p in vks[last_time] if vks[last_time][p] == "V"]

    for p in sorted(final_vampires):
        end = None   # first end time, that is, first t when p is V
        for t in range(len(vks)):
            if vks[t][p] == "V":
                end = t
                break

        start = 0   # first start time: that is, last t < end when p is H
        for t in range(end -1, -1, -1):
            if vks[t][p] == "H":
                start = t
                break

        iw[p] = (start, end)

    return iw


def pretty_print_infection_windows(iw):
    """ Print the infection window in a desired way"""

    for p in sorted(iw.keys()):
        start, end = iw[p]
        print(f"  {p} was turned between day {str_time(start)} and day {str_time(end)}.")


# Section 13
def find_potential_sires(iw, groups):
    """ In this section we look at every PM time inside the infection window for each vampire.
        If they had contact that afternoon, we collect the group they are in.
        Then store the result in a dictionary, with ps[vamp] = [ (time, group), … ].
    """
    ps = {}     # potential sire
    for vampire in iw:
        start, end = iw[vampire]
        lst = []
        # infection happens after the last 'definitely human' time, so start + 1
        # including the end time
        for t in range(start + 1, end + 1):
            if period_of_time(t) == False:  # PM is false
                contacts = contacts_by_time(vampire, t, groups)
                lst.append((t, contacts))
        ps[vampire] = lst
    return ps


def pretty_print_potential_sires(ps):
    """ Print out the ps structure in a desired way """
    for vampire in sorted(ps.keys()):
        print(f'  {vampire}:')
        lst = ps[vampire]

        if len(lst) == 0:
            print('    ' + format_list([]))
        else:
            for (t, contacts) in lst:
                day = day_of_time(t)
                contacts_readable_way = format_list(contacts)
                print(f"    On day {day} (PM), met with {contacts_readable_way}.")



# Section 14
def trim_potential_sires(ps, vks):
    """ remove vampires
        remove definite humans
    """
    for vamp in ps:
        new_days = []
        for (t, contacts) in ps[vamp]:
            temp_lst = []
            for p in contacts:
                if p != vamp and vks[t][p] != "H":
                    temp_lst.append(p)
            if len(temp_lst) > 0:
                new_days.append((t, temp_lst))
        ps[vamp] = new_days
    return ps


# Section 15
def trim_infection_windows(iw, ps):
    """ If a vampire has no potential sire entries,
        they must have been a vampire from the very beginning,
        Otherwise, their infection must have occurred on one of the PM times
        when they had contacts with eligible sires.
    """
    new_iw = {}
    for vampire, (start, end) in iw.items():
        entries = ps.get(vampire, [])

        if not entries:     # no possible sires
           new_iw[vampire] = (0, 0)
        else:
            pm_times = [t for (t, c) in entries]
            if start == 0:
                new_start = 0
            else:
                # ensure all times are pm and using the latest time
                new_start = min(pm_times)
            new_end = max(pm_times)
            new_iw[vampire] = (new_start, new_end)

    return new_iw



# Section 16
def update_vks_with_windows(vks, iw):
    """ deduce certain human times and certain vampire times,
        then updates the vk tables accordingly;
        count and return the number of changes
    """
    changes = 0
    for vamp in iw:
        (start, end) = iw[vamp]

        # Times strictly before start must be human & count changes accordingly
        for t in range(0,start):
            if vks[t][vamp] == "V":
                print("Error found in data: humans cannot be vampires; aborting.")
                sys.exit()
            if vks[t][vamp] == "U":
                vks[t][vamp] = "H"
                changes += 1

        # Times strictly after end must be vampire & count changes accordingly
        for t in range(end, len(vks)):
            if vks[t][vamp] == "H":
                print("Error found in data: vampires cannot be human; aborting.")
                sys.exit()
            if vks[t][vamp] == "U":
                vks[t][vamp] = "V"
                changes += 1

    return (vks, changes)


# Section 17; done by professors
def cyclic_analysis(vks, iw, ps):
    count = 0
    changes = 1
    while (changes != 0):
        ps = trim_potential_sires(ps, vks)
        iw = trim_infection_windows(iw, ps)
        (vks, changes) = update_vks_with_windows(vks, iw)
        count = count + 1
    return (vks, iw, ps, count)


# Section 18: vampire strata
def vampire_strata(iw):
    """ We divide the vampires into three sets:
        the original one:  iw = (0,0)
        newborn: iw is a single PM time
        unclear: turned into vampire, but we can't determine exactly when.
    """
    originals = set()
    unclear_vamps = set()
    newborns = set()

    for vamp, (start, end) in iw.items():
        # original vampires
        if start == 0 and end == 0:
            originals.add(vamp)

        # newborn vampires
        elif start > 0:
            newborns.add(vamp)

        # unclear vampires
        else:
            unclear_vamps.add(vamp)

    return (originals, unclear_vamps, newborns)


def pretty_print_vampire_strata(originals, unclear_vamps, newborns):
    """ Print out these three sets in a desired way. """
    print("  Original vampires: " + format_list(sorted(originals)))
    print("  Unknown strata vampires: " + format_list(sorted(unclear_vamps)))
    print("  Newborn vampires: " + format_list(sorted(newborns)))


# Section 19: vampire sire sets
def calculate_sire_sets(ps):
    """ In this section we map each vampire to the set of all potential sires. """
    ss = {}   # sire set
    for vamp, entries in ps.items():
        sire_set = set()
        for (t, contacts) in entries:
            for person in contacts:
                sire_set.add(person)
        ss[vamp] = sire_set
    return ss


def pretty_print_sire_sets(ss, iw, vamps, newb):
    """ Print out the updated sire sets. """
    if newb:
        print("Newborn vampires:")
    else:
        print("Vampires of unknown strata:")

    if not vamps:
        print("  (None)")
        return

    for v in sorted(vamps):
        sires = sorted(ss.get(v, set()))
        sire_str = format_list_or(sires) if sires else "(None)"

        start, end = iw[v]

        # Format start
        if start == 0:
            start_str = "day 0"
        else:
            start_str = f"day {day_of_time(start)} (PM)"

        # Format end
        if end == 0:
            end_str = "day 0"
        else:
            end_str = f"day {day_of_time(end)} (PM)"

        # UNKNOWN STRATA (always print a window)
        if not newb:
            print(f"  {v} could have been sired by {sire_str} between {start_str} and {end_str}.")
            continue

        # NEWBORN VAMPIRES
        if start == end:
            print(f"  {v} was sired by {sire_str} on day {day_of_time(end)} (PM).")
        else:
            print(f"  {v} was sired by {sire_str} between {start_str} and {end_str}.")


# Section 20: vampire sire sets
def find_hidden_vampires(ss, iw, vamps, vks):
    """ Get the sire set from ss and infection time from iw
        Set the sire status
        Count the change
    """
    changes = 0
    last_t = len(vks) - 1

    for v in vamps:
        sires = ss.get(v, set())

        # Only singleton sire sets allow deductions
        if len(sires) != 1:
            continue

        s = next(iter(sires))  # the only sire
        (start, end) = iw[v]  # only using the end time
        t = end  # The infection moment must be at or before end

        # UPDATE t-1 IF EXISTS
        if t > 0:
            status = vks[t - 1][s]      # Sire already vampire before infecting
            if status == 'H':
                print("Error found in data: vampires cannot be humans; aborting.")
                sys.exit()
            if status == 'U':
                vks[t - 1][s] = 'V'
                changes += 1

        # UPDATE t AND ALL FUTURE TIMES
        for k in range(t, last_t + 1):     # Once vampire, always vampire
            status = vks[k][s]
            if status == 'H':
                print("Error found in data: vampires cannot be humans; aborting.")
                sys.exit()
            if status == 'U':
                vks[k][s] = 'V'
                changes += 1
    return (vks, changes)


# Section 21; done by professor
def cyclic_analysis2(vks, groups):
    count = 0
    changes = 1
    while (changes != 0):
        iw = find_infection_windows(vks)
        ps = find_potential_sires(iw, groups)
        vks, iw, ps, countz = cyclic_analysis(vks, iw, ps)
        o, u, n = vampire_strata(iw)
        ss = calculate_sire_sets(ps)
        vks, changes = find_hidden_vampires(ss, iw, n, vks)
        count = count + 1
    return (vks, iw, ps, ss, o, u, n, count)


def main():
    """Main logic for the program.  Do not change this (although if
       you do so for debugging purposes that's ok if you later change
       it back...)
    """
    filename = ""
    # Get the file name from the command line or ask the user for a file name
    args = sys.argv[1:]
    if len(args) == 0:
        filename = input("Please enter the name of the file: ")
    elif len(args) == 1:
        filename = args[0]
    else:
        print("""\n\nUsage\n\tTo run the program type:
        \tpython contact.py infile
        where infile is the name of the file containing the data.\n""")
        sys.exit()

    # Section 2. Check that the file exists
    if not file_exists(filename):
        print("File does not exist, ending program.")
        sys.exit()

    # Section 3. Create contacts dictionary from the file
    # Complete function parse_file().
    data = parse_file(filename)
    participants, days = data
    tests_by_day = [d[0] for d in days]
    groups_by_day = [d[1] for d in days]

    # Section 4. Print contact records
    pretty_print_infiltration_data(data)


    # Section 5. Create helper function for time analysis.
    print("********\nSection 5: Lookup helper function")
    if len(participants) == 0:
        print("  No participants.")
    else:
        p = participants[0]
        if len(days) > 1:
            d = 2
        elif len(days) == 1:
            d = 1
        else:
            d = 0
        t = time_of_day(d, True)
        t2 = time_of_day(d, False)
        print(
            f"  {p}'s contacts for time unit {t} (day {day_of_time(t)}) are {format_list(contacts_by_time(p, t, groups_by_day))}.")
        print(
            f"  {p}'s contacts for time unit {t2} (day {day_of_time(t2)}) are {format_list(contacts_by_time(p, t2, groups_by_day))}.")

    # Section 6.  Create the initial data structure and pretty-print it.
    print("********\nSection 6: create initial vampire knowledge tables")
    vks = [create_initial_vk(participants) for i in range(1 + (2 * len(days)))]
    pretty_print_vks(vks)


    # Section 7.  Update the VKs with test results.
    print("********\nSection 7: update the vampire knowledge tables with test results")
    for t in range(1, len(vks), 2):
        vks[t] = update_vk_with_tests(vks[t], tests_by_day[day_of_time(t) - 1])
    pretty_print_vks(vks)

    # Section 8.  Update the VKs to push vampirism forwards in time.
    print("********\nSection 8: update the vampire knowledge tables by forward propagation of vampire status")
    for t in range(1, len(vks)):
        vks[t] = update_vk_with_vampires_forward(vks[t - 1], vks[t])
    pretty_print_vks(vks)

    # Section 9.  Update the VKs to push humanism backwards in time.
    print("********\nSection 9: update the vampire knowledge tables by backward propagation of human status")
    for t in range(len(vks) - 1, 0, -1):
        vks[t - 1] = update_vk_with_humans_backward(vks[t - 1], vks[t])
    pretty_print_vks(vks)

    # Sections 10 and 11.  Update the VKs to account for contact groups and safety at night.
    print(
        "********\nSections 10 and 11: update the vampire knowledge tables by forward propagation of contact results and overnight")
    for t in range(1, len(vks), 2):
        vks[t + 1] = update_vk_with_contact_group(vks[t], groups_by_day[day_of_time(t) - 1], vks[t + 1])
        if t + 2 < len(vks):
            vks[t + 2] = update_vk_overnight(vks[t + 1], vks[t + 2])
    pretty_print_vks(vks)

    # Section 12. Find infection windows for vampires.
    print("********\nSection 12: Vampire infection windows")
    iw = find_infection_windows(vks)
    pretty_print_infection_windows(iw)

    # Section 13. Find possible vampire sires.
    print("********\nSection 13: Find possible vampire sires")
    ps = find_potential_sires(iw, groups_by_day)
    pretty_print_potential_sires(ps)

    # Section 14. Trim the potential sire structure.
    print("********\nSection 14: Trim potential sire structure")
    ps = trim_potential_sires(ps, vks)
    pretty_print_potential_sires(ps)

    # Section 15. Trim the infection windows.
    print("********\nSection 15: Trim infection windows")
    iw = trim_infection_windows(iw, ps)
    pretty_print_infection_windows(iw)

    # Section 16. Update the vk structures with infection windows.
    print("********\nSection 16: Update vampire information tables with infection window data")
    (vks, changes) = update_vks_with_windows(vks, iw)
    pretty_print_vks(vks)
    str_s = "" if changes == 1 else "s"
    print(f'({changes} change{str_s})')

    # Section 17.  Cyclic analysis for sections 14-16
    print("********\nSection 17: Cyclic analysis for sections 14-16")
    vks, iw, ps, count = cyclic_analysis(vks, iw, ps)
    str_s = "" if count == 1 else "s"
    print(f'Detected fixed point after {count} iteration{str_s}.')
    print('Potential sires:')
    pretty_print_potential_sires(ps)
    print('Infection windows:')
    pretty_print_infection_windows(iw)
    pretty_print_vks(vks)

    # Section 18.  Calculate vampire strata
    print("********\nSection 18: Calculate vampire strata")
    (origs, unkns, newbs) = vampire_strata(iw)
    pretty_print_vampire_strata(origs, unkns, newbs)

    # Section 19.  Calculate definite sires
    print("********\nSection 19: Calculate definite vampire sires")
    ss = calculate_sire_sets(ps)
    pretty_print_sire_sets(ss, iw, unkns, False)
    pretty_print_sire_sets(ss, iw, newbs, True)

    # Section 20.  Find hidden vampires
    print("********\nSection 20: Find hidden vampires")
    (vks, changes) = find_hidden_vampires(ss, iw, newbs, vks)
    pretty_print_vks(vks)
    str_s = "" if changes == 1 else "s"
    print(f'({changes} change{str_s})')

    # Section 21.  Cyclic analysis for sections 14-20
    print("********\nSection 21: Cyclic analysis for sections 14-20")
    (vks, iw, ps, ss, o, u, n, count) = cyclic_analysis2(vks, groups_by_day)
    str_s = "" if count == 1 else "s"
    print(f'Detected fixed point after {count} iteration{str_s}.')
    print("Infection windows:")
    pretty_print_infection_windows(iw)
    print("Vampire potential sires:")
    pretty_print_potential_sires(ps)
    print("Vampire strata:")
    pretty_print_vampire_strata(o, u, n)
    print("Vampire sire sets:")
    pretty_print_sire_sets(ss, iw, u, False)
    pretty_print_sire_sets(ss, iw, n, True)
    pretty_print_vks(vks)


if __name__ == "__main__":
    main()
