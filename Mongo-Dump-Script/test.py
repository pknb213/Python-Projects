import datetime, time


src = 0
ff = [i for i in range(0, 1000)]
while len(ff) > src:
    fname = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    with open("./{}.log".format(fname), "w") as f:
        for l in ff[src:]:
            print(l)
            src += 1
            f.write(str(l).strip()+"\n")
            # f.write("\n")
            f.flush()
            if src % 100 == 0 and src != 0:
                print("~ {} ~".format(src))
                f.close()
                time.sleep(3)
                break
                # continue

