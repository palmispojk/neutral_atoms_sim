import pylcp
import .constants as constants
import numpy as np
import concurrent.futures
import pickle

def simulate_single_atom(seed):
    """ Worker function to simulate a single atom. """
    # 1. Explicitly seed the random generator for THIS specific atom
    # This replaces the hacky `np.random.rand(256*x)` method
    np.random.seed(seed)
    
    # 2. Generate the random starting position and velocity internally
    r0 = constants.rscale * np.random.randn(3) + constants.roffset
    v0 = constants.vscale * np.random.randn(3) + constants.voffset
    
    # 3. Build the trap components
    laserBeams = pylcp.conventional3DMOTBeams(
        k=constants.kmag, s=constants.s, delta=0., beam_type=pylcp.infinitePlaneWaveBeam
    )
    magField = pylcp.quadrupoleMagneticField(constants.alpha)
    
    H_g, muq_g = pylcp.hamiltonians.singleF(F=2, gF=1.5, muB=constants.muB)
    H_e, muq_e = pylcp.hamiltonians.singleF(F=3, gF=1+1/3, muB=constants.muB)
    d_q = pylcp.hamiltonians.dqij_two_bare_hyperfine(2, 3)
    hamiltonian = pylcp.hamiltonian(
        H_g, -constants.det*np.eye(7)+H_e, muq_g, muq_e, d_q, 
        mass=constants.mass, muB=constants.muB, gamma=constants.gamma, k=constants.kmag
    )
    
    obe = pylcp.obe(laserBeams, magField, hamiltonian, transform_into_re_im=True)
    
    # Pre-calculate initial density matrix
    obe.set_initial_rho_from_rateeq()
    
    # 4. Evolve motion with your kwargs
    tmax = 1e5
    kwargs = {
        't_eval': np.linspace(0, tmax, 5001),
        'random_recoil': True,
        'progress_bar': False,
        'max_scatter_probability': 0.5
    }
    
    sol = obe.evolve_motion([0, tmax], r0, v0, **kwargs)
    
    return sol.t, sol.r, sol.v

if __name__ == '__main__':
    Natoms = 96
    
    # Generate an array of highly random integer seeds
    seeds = np.random.randint(0, 2**32 - 1, size=Natoms)
    
    print(f"Starting parallel simulation of {Natoms} atoms...")
    
    results = []
    
    # concurrent.futures automatically handles chunking and load balancing across all CPU cores!
    # We no longer need the manual `chunksize = 4` loop or `pathos`.
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # We simply pass the array of seeds to the executor
        for res in executor.map(simulate_single_atom, seeds):
            results.append(res)
            
    print("Simulation complete! Saving data...")
    
    with open('mot_simulation_data.pkl', 'wb') as file:
        pickle.dump(results, file, protocol=pickle.HIGHEST_PROTOCOL)
        
    print("Data saved successfully.")