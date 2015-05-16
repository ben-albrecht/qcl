""" Figs sub module to generate figures"""
#!/usr/bin/env python3
# encoding: utf-8

FIGS = True

try:
    import cclib
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
except ImportError:
    FIGS = False


def figs(opts):
    """
    Determine type of output from opts or file
    Call appropriate function
    """

    if type(opts.fname) == str:
        # Assuming ccinput is a filename
        data = cclib.parser.ccopen(opts.fname).parse()
    else:
        data = opts.fname
        assert type(data) == cclib.parser.data.ccData_optdone_bool \
            or type(data) == cclib.parser.data.ccData

    # TODO: determine what kind of job (opt, sp, freq)
        # auto = automatically determine
        # or get from opts.job
    if opts.job == 'auto':
        #print opts.job, "not yet implemented"
        _opt(data)
    elif opts.job == 'opt':
        _opt(data)
    elif opts.job == 'sp':
        _sp(data)
    elif opts.job == 'vib':
        print(opts.job, "not yet implemented")
    else:
        print(opts.job, "not yet implemented")


def _sp(data):
    """
    Generate plots of convergence criteria, and energy vs. optimization cycles

    :job: ccdata object, or file
    :returns: TODO

    """
    # TODO scfenergies, scfvalues, scftargets vs. scf cycles
    print("\n\n")
    #print("Optimization Converged: ", data.optdone)
    criteria = [0, 0, 0]
    criteria[0] = [x[0] for x in data.scfvalues]
    criteria[1] = [x[1] for x in data.scfvalues]
    criteria[2] = [x[2] for x in data.scfvalues]
    idx = np.arange(len(criteria[0]))

    # Plot Geometry Optimization Criteria for Convergence over opt cycles
    plt.plot(idx, criteria[0], label='Criteria 1')
    plt.plot(idx, criteria[1], label='Criteria 2')
    plt.plot(idx, criteria[2], label='Criteria 3')

    # Plot target criteria for convergence
    plt.axhline(y=data.scftargets[0])
    plt.yscale('log')

    plt.title("SCF Convergence Analysis")
    plt.xlabel("SCF Cycle")
    plt.legend()

    plt.show()

   # idx = np.arange(len(data.scfenergies))
   # plt.plot(idx, data.scfenergies, label='SCF Energy (eV)')
   # plt.show


def _opt(data):
    """ Generate plots of convergence criteria,
        and energy vs. optimization cycles

    :job: ccdata object, or file
    :returns: TODO
    """
    print("\n\n")
    print("Optimization Converged: ", data.optdone)
    print("Optimization Targets:")
    print("Gradient: ", data.geotargets[0])
    print("Displacement: ", data.geotargets[1])
    print("Energy Change: ", data.geotargets[2])

    criteria = [0, 0, 0]
    criteria[0] = [x[0] for x in data.geovalues]
    criteria[1] = [x[1] for x in data.geovalues]
    criteria[2] = [x[2] for x in data.geovalues]
    idx = np.arange(len(criteria[0]))

    print("Optimization Final Values:")
    print("Gradient: ", criteria[0][-1])
    print("Displacement: ", criteria[1][-1])
    print("Energy Change: ", criteria[2][-1])

    # Plot Geometry Optimization Criteria for Convergence over opt cycles
    plt.plot(idx, criteria[0], label='Gradient', color='red')
    plt.plot(idx, criteria[1], label='Displacement', color='green')
    plt.plot(idx, criteria[2], label='Energy Change', color='blue')

    # Plot target criteria for convergence
    plt.axhline(y=data.geotargets[0], color='red')
    plt.axhline(y=data.geotargets[1], color='green')
    plt.axhline(y=data.geotargets[2], color='blue')
    plt.yscale('log')

    plt.title("Optimization Convergence Analysis")
    plt.xlabel("Optimization Cycle")
    plt.legend()

    plt.show()

    idx = np.arange(len(data.scfenergies))
    plt.plot(idx, data.scfenergies, label='SCF Energy (eV)')
    plt.show

    # TODO plot scfenergies vs. cycles


def main(opts):
    """ Main function for figs """
    if FIGS:
        figs(opts)
    else:
        raise ImportError("""Unable to import all libraries for figs
                       numpy
                       matplotlib
                       cclib""")
