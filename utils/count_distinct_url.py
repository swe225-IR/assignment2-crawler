if __name__ == '__main__':
    l = set()
    error_code = set()
    with open(r"../Logs/Worker.log", 'r') as f:
        while True:
            i = f.readline()
            if i:
                try:
                    if i.split(", status <")[1][0:3] == "200":
                        l.add(i.split(", status")[0].split("Downloaded ")[1])
                    else:
                        error_code.add(i.split(", status <")[1][0:3])
                except Exception:
                    pass
            else:
                break
    print(len(l))
    print(error_code)
