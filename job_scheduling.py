from ortools.sat.python import cp_model
jobs = {
    'J1': {'duration': 2, 'machines': ['M1', 'M2', 'M3']},
    'J2': {'duration': 3, 'machines': ['M1', 'M3']},
    'J3': {'duration': 1, 'machines': ['M2', 'M3']},
    'J4': {'duration': 4, 'machines': ['M1', 'M2']},
}

jobpost = {job: {'duration': jobs[job]['duration'], 'machines': jobs[job]['machines']} for job in jobs}

jobpost_jobs = list(jobs.keys())

    def (your_jobs, jobpost):
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

    # Each pair of tasks in a job must be executed sequentially on the same machine.
    for i in range(num_jobs):
        for j in range(num_machines):
            model.Add(task_starts[(i, j)] == task_ends[(i-1, j)]).OnlyEnforceIf(task_ends[(i-1, j)] >= 0)
            model.Add(task_ends[(i, j)] == task_starts[(i+1, j)]).OnlyEnforceIf(task_starts[(i+1, j)] >= 0)

    # Objective
    obj_var = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(obj_var, [task_ends[(i, j)] for i in range(num_jobs) for j in range(num_machines)])
    model.Minimize(obj_var)

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Output
    if status == cp_model.OPTIMAL:
        print(f'Optimal Schedule Found with Makespan = {solver.ObjectiveValue()}')
        for i in range(num_jobs):
            print(f'Job {i}:')
            for j in range(num_machines):
                start_time = solver.Value(task_starts[(i, j)])
                end_time = solver.Value(task_ends[(i, j)])
                print(f'Machine {j}: Start Time = {start_time}, End Time = {end_time}')
    else:
        print('No feasible solution found.')
result = job_scheduling_forward_selection(your_jobs, jobpost)
print(result)
