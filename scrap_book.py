# mistakes = []  # this creates instrumental matrix
mistakesf = []  # this creates goal matrix
behavioral_b = []  # this creates the behavioral with times+mistakes
A=[]
for line in range(f_ptcp_df.shape[0]):  # this indicates to go over every row
    A[line, 2] = f_ptcp_df['correctCounter'][line + 1] != f_ptcp_df['correctCounter'][line]  # this looks for differences in correct counter
    A[line, 0] = f_ptcp_df['trial_set'][line]  # this adds to A the set number
    A[line, 1] = f_ptcp_df['levelCounter'][line]  # this adds the level counter