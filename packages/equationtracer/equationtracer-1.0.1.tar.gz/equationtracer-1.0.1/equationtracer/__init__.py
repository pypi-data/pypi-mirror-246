if __name__ == '__main__':
    try:
        from main import main
    except ModuleNotFoundError:
        from equationtracer.main import main

    main()
