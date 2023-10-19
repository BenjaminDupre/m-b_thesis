def creating_close_trial(data):
    # Creating Close Index 
    num_rows = data.shape[0]
    C = np.zeros((num_rows - 1, 1))
    for r in range(num_rows - 1):
        C[r, 0] = data['levelCounter'].iloc[r + 1] != data['levelCounter'].iloc[r]
    # Assuming 'indx' is a numpy array of indices
    row_close = np.where(C[:, 0] == 1)[0]
    levelCounter_values = data.iloc[row_close]['levelCounter']
    trial_set_values = data.iloc[row_close]['trial_set']

    # Creating a new DataFrame to store the extracted values
    close_df = pd.DataFrame({
        'row_close': row_close,
        'levelCounter': levelCounter_values,
        'trial_set': trial_set_values
    })
    close_df.reset_index(drop=True, inplace=True)
    return close_df 

def get_one_feedback_per_trail(dataf,close_df):
    # Group the data and extract unique feedbackType values per participant, set, and levelCounter
    unique_feedback_types = dataf.groupby(['ptcp', 'trial_set', 'levelCounter'])['feedbackType'].unique()

    # Remove duplicate feedback types based on the specified conditions
    for index, feedback_types in unique_feedback_types.items():
        ptcp, set_val, level_counter = index
        feedback_types = feedback_types[np.isin(feedback_types, ['incongruent', 'none', 'congruent'])]
        #print(f'Going Through Level {level_counter} and Set {set_val}')
        if level_counter != 0 and feedback_types.size > 1:
            previous_level_counter = level_counter - 1
            previous_feedback_types = unique_feedback_types.get((ptcp, set_val, previous_level_counter))
            if previous_feedback_types is not None :
                if previous_feedback_types.size==1:
                    last_element = previous_feedback_types
                elif previous_feedback_types.size > 1:
                    last_element = np.asarray(previous_feedback_types)[-1]
                else:
                    last_element = None
            if last_element is not None and feedback_types[0] == last_element :
                feedback_types = feedback_types[1:]
        elif level_counter == 0  and feedback_types.size > 1:
            feedback_types = feedback_types[feedback_types != 'none']
        # WARNING: Last resource condition. Not too Pro but effective 
        if  feedback_types.size > 1:
            print(f'WAS TRIGGERED LAST CASE FEEDBACKTYPE in level {level_counter} and set {set_val}')
            row_n = close_df[(close_df['levelCounter'] == level_counter) & (close_df['trial_set'] == set_val)]['row_close']
            #row_n = close_df[(close_df['levelCounter'] == level_counter) & (close_df['trial_set'] == set_val)]['row_close']
            feedback_types = np.asarray(dataf.loc[row_n]['feedbackType'])
            #feedback_types = dataf[dataf['index'] == row_n]['feedbackType']   
        unique_feedback_types[index] = feedback_types
    feedback_df=unique_feedback_types.reset_index()
    feedback_df= pd.DataFrame(feedback_df) 

    return  feedback_df

close_df = creating_close_trial(f_ptcp_df)
payasadaoe = get_one_feedback_per_trail(f_ptcp_df,close_df)
unique_feedback_types.to_csv('delete_after_read.csv')
payasadaoe.to_csv('clean_merged.csv')

#---------------------------------------------------------
# using correct counter 
# Referencing code from Rolf Ulrich and Chatgpt adaptation. 
import numpy as np
import matplotlib.pyplot as plt

def race_model(X, Y, Z, P, Plot):
    # X, Y, Z are arrays with RTs for conditions Cx, Cy, Cz, respectively.
    # P is an array which contains the probabilities for computing percentiles.
    # If Plot is True, a plot of the result is generated.
    
    # Check for ties and get maximum t value
    Ux, Rx, Cx = ties(X)
    Uy, Ry, Cy = ties(Y)
    Uz, Rz, Cz = ties(Z)
    tmax = int(np.ceil(max(max(X), max(Y), max(Z))))
    T = np.arange(1, tmax + 1)
    
    # Get function values of G
    Gx = CDF(Ux, Rx, Cx, tmax)
    Gy = CDF(Uy, Ry, Cy, tmax)
    Gz = CDF(Uz, Rz, Cz, tmax)
    
    # Compute B = Gx plus Gy
    B = [Gx[t] + Gy[t] for t in range(tmax)]
    
    # Check whether requested percentiles can be computed
    OKx = check(Ux[0], P[0], Gx)
    if not OKx:
        print('Not enough X values to compute requested percentiles')
        return [None, None, None, None]
    
    OKy = check(Uy[0], P[0], Gy)
    if not OKy:
        print('Not enough Y values to compute requested percentiles')
        return [None, None, None, None]
    
    OKz = check(Uz[0], P[0], Gz)
    if not OKz:
        print('Not enough Z values to compute requested percentiles')
        return [None, None, None, None]
    
    # Determine percentiles
    Xp = get_percentile(P, Gx, tmax)
    Yp = get_percentile(P, Gy, tmax)
    Zp = get_percentile(P, Gz, tmax)
    Bp = get_percentile(P, B, tmax)
    
    # Generate a plot if requested
    if Plot:
        plt.plot(Xp, P, 'o-', label='G_x(t)')
        plt.plot(Yp, P, 'o-', label='G_y(t)')
        plt.plot(Zp, P, 'o-', label='G_z(t)')
        plt.plot(Bp, P, 'o-', label='G_x(t)+G_y(t)')
        plt.axis([min(Ux + Uy + Uz) - 10, tmax + 10, -0.03, 1.03])
        plt.grid()
        plt.title('Test of the Race Model Inequality', fontsize=16)
        plt.xlabel('Time t (ms)', fontsize=14)
        plt.ylabel('Probability', fontsize=14)
        plt.legend(loc=4)
        plt.show()
    
    return Xp, Yp, Zp, Bp

def check(U1, P1, G):
    for t in range(U1 - 2, U1 + 3):
        if G[t] > P1 and G[t - 1] == 0:
            return False
    return True

def get_percentile(P, G, tmax):
    Tp = []
    for p in P:
        cc = 100
        c = 0
        for t in range(tmax):
            if abs(G[t] - p) < cc:
                c = t
                cc = abs(G[t] - p)
        
        if p > G[c]:
            Tp.append(c + (p - G[c]) / (G[c + 1] - G[c]))
        else:
            Tp.append(c + (p - G[c]) / (G[c] - G[c - 1]))
    return Tp

def ties(W):
    # Count the number k of unique values and store these values in U.
    W = sorted(W)
    n = len(W)
    k = 1
    U = [W[0]]
    
    for i in range(1, n):
        if W[i] != W[i - 1]:
            k += 1
            U.append(W[i])
    
    # Determine the number of replications R
    R = [0] * k
    
    for i in range(k):
        for j in range(n):
            if U[i] == W[j]:
                R[i] += 1
    
    # Determine the cumulative frequency
    C = [0] * k
    C[0] = R[0]
    
    for i in range(1, k):
        C[i] = C[i - 1] + R[i]
    
    return U, R, C

def CDF(U, R, C, maximum):
    G = [0] * maximum
    k = len(U)
    n = C[k - 1]
    
    for i in range(k):
        U[i] = round(U[i])
    
    for t in range(U[0]):
        G[t] = 0
    
    for t in range(U[0], U[1]):
        G[t] = (R[0] / 2 + (R[0] + R[1]) / 2 * (t - U[0]) / (U[1] - U[0])) / n
    
    for i in range(1, k - 1):
        for t in range(U[i], U[i + 1]):
            G[t] = (C[i - 1] + R[i] / 2 + (R[i] + R[i + 1]) / 2 * (t - U[i]) / (U[i + 1] - U[i])) / n
    
    for t in range(U[k - 1], maximum):
        G[t] = 1
    
    return G

# Example usage:
X = [10, 15, 20, 25]
Y = [12, 16, 18, 24]
Z = [9, 14, 21, 27]
P = [0.5, 0.7]
Plot = True

Xp, Yp, Zp, Bp = race_model(X, Y, Z, P, Plot)
