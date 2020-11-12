# -*- coding: utf-8 -*-
import time
import traceback


def main():
    try:
        from utils.server import Server
        server = Server()
    except:
        traceback.print_exc()
        time.sleep(0)
        input('Exception occurred, press Enter to exit')
    else:
        server.start()


if __name__ == '__main__':
    main()
