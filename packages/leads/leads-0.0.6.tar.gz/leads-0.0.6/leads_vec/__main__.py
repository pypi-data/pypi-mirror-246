from sys import argv as _argv, exit as _exit

if __name__ == '__main__':
    try:
        from leads_emulation import SRWRandom as Controller
    except ImportError:
        raise EnvironmentError("At least one adapter has to be installed")
    if "remote" in _argv:
        from leads_vec.remote import remote as _main

        _exit(_main())
    else:
        from leads_vec.cli import main as _main

        _exit(_main(Controller("main")))
