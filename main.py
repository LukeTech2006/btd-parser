import os, sys, parse, download

def main(args: list) -> int:
    return download.main(args)
    
if __name__ == "__main__":
    exit_code = main(sys.argv)
    os._exit(exit_code)