
import math


def read_file():
    result = []
    f = open("house-votes-84.data", "r")
    for line in f:
        clear_line = line.rstrip()
        result.append(clear_line.split(","))
    return result

def split_in_chunks(people):
    chunks_people = []
    len_chunk = int(len(people) / 10)

    for i in range(0, len(people), len_chunk):
        chunks_people.append(people[i:i+len_chunk])
    
    left_people = chunks_people.pop()
    for i in range(len(left_people)):
        chunks_people[i].append(left_people[i])

    return chunks_people

def count_classes(chunks):
    republicans = {
        'y': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'n': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        '?': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    democrats = {
        'y': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'n': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        '?': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    num_republicans = 0
    num_democrats = 0
    for chunk in chunks:
        for person in chunk:
            if person[0] == "republican":
                num_republicans += 1
                for question in range(1, len(person)):
                    republicans[person[question]][question - 1] += 1
            else:
                num_democrats += 1
                for question in range(1, len(person)):
                    democrats[person[question]][question - 1] += 1

    return republicans, democrats, num_republicans, num_democrats


def test_person(republicans, democrats, num_republicans, num_democrats, person):
    prob_rep_log = 0
    prob_dem_log = 0
    lambda_ = 1
    A = 2 # two classes, rep and dem

    for question in range(1, len(person)):
        prob_rep_log += math.log(republicans[person[question]][question - 1] + lambda_) / math.log(num_republicans + lambda_ * A)
        prob_dem_log += math.log(democrats[person[question]][question - 1] + lambda_) / math.log(num_democrats + lambda_ * A)

    prob_rep_log += math.log((num_republicans + lambda_) / (num_republicans + num_democrats + lambda_ * A))
    prob_dem_log += math.log((num_democrats + lambda_) / (num_republicans + num_democrats + lambda_ * A))

    if person[0] == "republican":
        return int(prob_dem_log <= prob_rep_log)
    else:
        return int(prob_dem_log >= prob_rep_log)
    

def beyes_classifier(chunks):
    sum_accuracy = 0
    for i in range(len(chunks)):
        republicans, democrats, num_republicans, num_democrats = count_classes(chunks[:i] + chunks[i + 1:])
        
        right_predictions = 0
        
        for person in chunks[i]:
            right_predictions += test_person(republicans, democrats, num_republicans, num_democrats, person)
        accuracy = (right_predictions / len(chunks[i])) * 100
        print("Accuracy for", i, ": ", round(accuracy,2), "%")
        sum_accuracy += accuracy
    
    print("Final accuracy: ", round(sum_accuracy / 10, 2), "%")    



def main():
    people = read_file()
    chunks = split_in_chunks(people)
    beyes_classifier(chunks)

if __name__ == "__main__":
    main()