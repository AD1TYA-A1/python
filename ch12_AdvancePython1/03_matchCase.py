def http_status(status):
    match status:
        case 200:
            print("OK Nice")
            return "Last line of 200"

        case 404:
            print("Not Found")
            print("I am insidde case 404")
            return "This is last Line of 404"
        case 500:
            print("Internal Server Error")
            return "This is last Line of 500"

        case _:     # Default Case 
            print("Unknown Status")

a = http_status(500)
print(f'I am value of "a" {a}')