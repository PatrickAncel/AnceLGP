with open(F"results1/final.txt", "w") as final:
    for function_number in range(3):
        for condition_number in range(1,10):
            total = 0.0
            for replicate_number in range(1,6):
                with open(F"results1/{function_number}-{condition_number}-{replicate_number}-result.txt", "r") as file:
                    total += float(file.read())
            avg = round(total/5, 3)
        final.write(F"Function {function_number}, Condition {condition_number}: {avg}\n")
