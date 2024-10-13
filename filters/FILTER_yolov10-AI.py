import os
import subprocess

def initialize_filter():
    path = os.getcwd()
    filter_list = [f for f in os.listdir(f"{path}/submodules/yolov10/") if f.startswith("FILTER_") and f.endswith(".py")]
    print("Available files:")
    for i, file in enumerate(filter_list):
        print(f"{i + 1}. {file}")


    while True:
        try:
            choice = int(input("Select a filter by number: "))
            if 1 <= choice <= len(filter_list):
                selected_file = filter_list[choice - 1]
                print(f"You selected: {selected_file}")
                os.system(f"python {path}/submodules/yolov10/{selected_file}")
                break
            else:
                print(f"Invalid choice. Please select a number between 1 and {len(filter_list)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")



def main():
    initialize_filter()


if __name__ == "__main__":
    main()