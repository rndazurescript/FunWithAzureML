def init():
    print("Load model here")


def run(mini_batch):
    output = []
    print('Batch call')
    for file_path in mini_batch:
        print(f'Processing file {file_path}')
        output.append([file_path, 0])
    return output