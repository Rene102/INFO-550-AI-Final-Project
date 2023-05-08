from ortools.sat.python import cp_model

jobs = {
    'J1': {'duration': 2, 'machines': ['M1', 'M2', 'M3']},
    'J2': {'duration': 3, 'machines': ['M1', 'M3']},
    'J3': {'duration': 1, 'machines': ['M2', 'M3']},
    'J4': {'duration': 4, 'machines': ['M1', 'M2']},
}

jobpost = {job: {'duration': jobs[job]['duration'], 'machines': jobs[job]['machines']} for job in jobs}

jobpost_jobs = list(jobs.keys())

def job_scheduling_forward_selection(your_jobs, jobpost):
    num_jobs = len(your_jobs)
    num_machines = len(jobpost)

    model = cp_model.CpModel()

    # Variables
    horizon = sum(job[1] for job in your_jobs)
    task_starts = {}
    task_ends = {}
    for i in range(num_jobs):
        for j in range(num_machines):
            task_starts[(i, j)] = model.NewIntVar(0, horizon, f'start_{i}_{j}')
            task_ends[(i, j)] = model.NewIntVar(0, horizon, f'end_{i}_{j}')

    # Constraints
    # Each job must be assigned to exactly one machine.
    for i in range(num_jobs):
        model.Add(sum(task_starts[(i, j)] >= 0 for j in range(num_machines)) == 1)

    # No two tasks assigned to the same machine can overlap.
    for j in range(num_machines):
        for k in range(num_jobs):
            for l in range(k+1, num_jobs):
                model.AddNoOverlap2(
                    [
                        (task_starts[(k, j)], task_ends[(k, j)]),
                        (task_starts[(l, j)], task_ends[(l, j)])
                    ]
                )

    # Objective
    obj_var = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(obj_var, [task_ends[(i, j)] for i in range(num_jobs) for j in range(num_machines)])

    # Solve with forward selection
    solver = cp_model.CpSolver()
    solution_printer = cp_model.ObjectiveSolutionPrinter(obj_var)
    sequence = [i for i in range(num_jobs)]
    while True:
        # Solve with current sequence
        model.AddMinEquality(task_starts[(sequence[-1], 0)], max(solver.Value(task_ends[(i, num_machines-1)]) for i in sequence[:-1]))  
        solver.SolveWithSolutionCallback(model, solution_printer)
        if solver.StatusName(solver.Status()) != 'OPTIMAL':
            break

        # Find best next job to add to sequence
        best_next_job = None
        best_next_makespan = float('inf')
        for job in range(num_jobs):
            if job in sequence:
                continue

            sequence_try = sequence + [job]
            model_tmp = cp_model.CpModel()
            task_starts_tmp = {}
            task_ends_tmp = {}
            for i in sequence_try:
                for j in range(num_machines):
                    task_starts_tmp[(i, j)] = task_starts[(i, j)]
                    task_ends_tmp[(i, j)] = task_ends[(i, j)]
            for j in range(num_machines):
                for k in range(len(sequence_try)-1):
                    for l in range(k+1
result = job_scheduling_forward_selection(jobpost)
print(result)

#I would choose the job with the shortest duration and allocate it to the machine with the earliest available time slot as a starting point for solving the job scheduling challenge. Then, after checking that the constraints are met, I would go through the remaining jobs one by one and allocate each one to the machine with the earliest available time window. 
# This strategy may be more effective than the conventional strategy since it minimizes the amount of variables and restrictions that must be taken into account at each stage, which could result in shorter search durations and a more effective timetable.
