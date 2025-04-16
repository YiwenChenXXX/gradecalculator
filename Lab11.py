import os
import matplotlib.pyplot as plt
DATA_DIR = 'data'
def read_students(path):
    students = {}
    with open(path, 'r') as f:
        for i in f:
            i = i.rstrip()
            if not i:
                continue
            s = i[:3]
            name = i[3:].strip()
            students[name] = s
    return students
def read_assignments(path):
    assigns = {}
    with open(path, 'r') as f:
        lines = [l.rstrip() for l in f if l.strip()]
    for i in range(0, len(lines), 3):
        name = lines[i]
        aid = lines[i+1]
        points = float(lines[i+2])
        assigns[name] = (aid, points)
    return assigns
def read_submissions_file(path):
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            sid, aid, pct = line.split('|')
            return sid, aid, float(pct)
    return None
def load_data():
    base = os.path.join(os.path.dirname(__file__), DATA_DIR)
    students = read_students(os.path.join(base, 'students.txt'))
    assignments = read_assignments(os.path.join(base, 'assignments.txt'))
    subs = []
    subs_dir = os.path.join(base, 'submissions')
    for fn in os.listdir(subs_dir):
        if fn.startswith('.'):
            continue
        path = os.path.join(subs_dir, fn)
        if not os.path.isfile(path) or not fn.lower().endswith('.txt'):
            continue
        rec = read_submissions_file(path)
        if rec:
            subs.append(rec)
    return students, assignments, subs
def student_grade(name, students, assignments, submissions):
    sid = students.get(name)
    if not sid:
        print("Student not found")
        return
    aid_to_pts = {aid: pts for (_n, (aid, pts)) in assignments.items()}
    total_earned = 0.0
    for sub_sid, sub_aid, pct in submissions:
        if sub_sid == sid:
            pts = aid_to_pts.get(sub_aid)
            if pts is not None:
                total_earned += pts * (pct / 100.0)
    overall_pct = round((total_earned / 1000.0) * 100)
    print(f"{overall_pct}%")
def get_assignment_scores(name, assignments, submissions):
    info = assignments.get(name)
    if not info:
        print("Assignment not found")
        return None
    aid, _pts = info
    scores = [pct for (_sid, sub_aid, pct) in submissions if sub_aid == aid]
    if not scores:
        print("Assignment not found")
        return None
    return scores
def assignment_stats(name, assignments, submissions):
    scores = get_assignment_scores(name, assignments, submissions)
    if scores is None:
        return
    mn  = round(min(scores))
    avg = round(sum(scores) // len(scores))
    mx  = round(max(scores))
    print(f"Min: {mn}%")
    print(f"Avg: {avg}%")
    print(f"Max: {mx}%")
def assignment_graph(name, assignments, submissions):
    scores = get_assignment_scores(name, assignments, submissions)
    if scores is None:
        return
    bin_edges = list(range(50, 101, 5))
    counts, edges, patches = plt.hist(
        scores,
        bins=bin_edges,
        rwidth=1.0,
        edgecolor=None
    )
    plt.xticks(bin_edges[::2])
    maxc = int(counts.max())
    top_even = maxc - (maxc % 2)
    plt.yticks(range(0, top_even + 1, 2))
    plt.show()
def main():
    students, assignments, submissions = load_data()
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph\n")
    choice = input("Enter your selection: ").strip()
    if choice == '1':
        name = input("What is the student's name: ").strip()
        student_grade(name, students, assignments, submissions)
    elif choice == '2':
        assignment_name = input("What is the assignment name: ").strip()
        assignment_stats(assignment_name, assignments, submissions)
    elif choice == '3':
        assignment_name = input("What is the assignment name: ").strip()
        assignment_graph(assignment_name, assignments, submissions)
if __name__ == "__main__":
    main()
