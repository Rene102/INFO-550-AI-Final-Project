from ortools.sat.python import cp_model
import random

# Define the jobs and their properties
jobs = {
    'J1': {'duration': 2, 'machines': ['M1', 'M2', 'M3']},
    'J2': {'duration': 3, 'machines': ['M1', 'M3']},
    'J3': {'duration': 1, 'machines': ['M2', 'M3']},
    'J4': {'duration': 4, 'machines': ['M1', 'M2']},
}

# Convert the job dictionary to a list of dictionaries, for convenience
job_properties = [job_info for job_info in jobs.values()]

# Get a list of job names
job_names = list(jobs.keys())

def job_scheduling_forward_selection(jobs):
    # Get the number of jobs and machines
    num_jobs = len(jobs)
    num_machines = len(job_properties)

    # Create the CP-SAT model
    model = cp_model.CpModel()

    # Define the horizon, i.e. the latest possible end time for all tasks
    horizon = sum(job['duration'] for job in job_properties)

    # Create the decision variables for start and end times for each task
    task_start_vars = {}
    task_end_vars = {}
    for i, job_info in enumerate(job_properties):
        for j in range(num_machines):
            task_start_vars[(i, j)] = model.NewIntVar(0, horizon, f'start_{i}_{j}')
            task_end_vars[(i, j)] = model.NewIntVar(0, horizon, f'end_{i}_{j}')

    # Define the constraints
    # Each job must be assigned to exactly one machine
    for i in range(num_jobs):
        model.Add(sum(task_start_vars[(i, j)] >= 0 for j in range(num_machines)) == 1)

    # No two tasks assigned to the same machine can overlap
    for j in range(num_machines):
        for k in range(num_jobs):
            for l in range(k+1, num_jobs):
                model.AddNoOverlap2(
                    [
                        (task_start_vars[(k, j)], task_end_vars[(k, j)]),
                        (task_start_vars[(l, j)], task_end_vars[(l, j)])
                    ]
                )

    # Define the objective function
    obj_var = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(obj_var, [task_end_vars[(i, j)] for i in range(num_jobs) for j in range(num_machines)])
    model.Minimize(obj_var)

    # Solve the problem using forward selection
    solver = cp_model.CpSolver()
    sequence = [i for i in range(num_jobs)]
    while True:
        # Solve the problem with the current sequence
        model.AddMinEquality(task_start_vars[(sequence[-1], 0)], max(solver.Value(task_end_vars[(i, num_machines-1)]) for i in sequence[:-1]))
        solver.Solve(model)

        # If we have found an optimal solution, stop searching
        if solver.StatusName(solver.Status()) != 'OPTIMAL':
            break

        # Search for a better solution by swapping tasks between jobs
        best_solution = solver.ObjectiveValue()
        best_sequence = sequence
        for i in range(num_jobs):
            for j in range(i+1, num_jobs):
                # Swap tasks from different jobs
                new_job_properties = job_properties.copy()
                temp = new_job_properties[i]['
