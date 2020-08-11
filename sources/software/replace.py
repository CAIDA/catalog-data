filename = "artemis.json"

output = []
with open(filename,"r") as f:
    
    for line in f:
        line = line.replace("presentation", "media")
        # if line.count('\"to\"')>0:
        #     line = line.lower()
        #     # print(line)
        #     for i in range(len(line)):
        #         # if line[i:i+5] == '\"to\": ':
        #         if line[i] == "t":
        #             # print(line)

        #             # replace space with underline
        #             line = line[:i+5] + line[i+5:].replace(" ", "_")
        #             line = line.replace("presemtatopm", "presentation")
        #             # print(line)
        #             # input("press")
        #             break

        #     # print(line[:6])
            

        output.append(line)
        # print(line)    
    
with open(filename, "w") as f:

    f.writelines(output)