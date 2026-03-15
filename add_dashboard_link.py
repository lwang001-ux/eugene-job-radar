import fileinput

dashboard = "View the live job dashboard:\\nhttps://lwang001-ux.github.io/eugene-job-radar/\\n\\n"

for line in fileinput.input("jobs_daily.py", inplace=True):
    if "body =" in line:
        print(line.rstrip())
        print(f'    body = "{dashboard}" + body')
    else:
        print(line.rstrip())
