import os, sys, time, hash, metadata, logging, download

def main(args: list) -> int:
    try: os.mkdir("logs")
    except: pass

    logging.basicConfig(
        filename=f"logs/{time.strftime('%F_%T', time.localtime()).replace(':', '-')}.log",
        format=f"[%(levelname)s]%(message)s",
        level=logging.INFO
    )
    logger = logging.getLogger()

    logger.info("Starting automated download")
    exit_code_download = download.main(args, debug_verify=False, logger=logger)

    logger.info("Starting hash pre-computer")
    exit_code_hash = hash.main(logger=logger)

    logger.info("Starting metadata extractor")
    exit_code_meta = metadata.main(logger=logger)

    return max(exit_code_download, exit_code_hash, exit_code_meta)
    
if __name__ == "__main__":
    exit_code = main(sys.argv)
    sys.exit(exit_code)