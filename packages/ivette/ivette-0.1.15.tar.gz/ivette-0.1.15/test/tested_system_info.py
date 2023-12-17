import platform

def system_info():
    unique_identifier = f"{platform.system()}_{platform.node()}_{platform.processor()}"
    
    info = {
        'Unique Identifier': unique_identifier,
        'System': platform.system(),
        'Node': platform.node(),
        'Release': platform.release(),
        'Version': platform.version(),
        'Machine': platform.machine(),
        'Processor': platform.processor()
    }
    return info

# Example usage
if __name__ == "__main__":
    system_data = system_info()
    for key, value in system_data.items():
        print(f"{key}: {value}")
