"""Just some examples of lang configs"""


cpp = {
    "extension": "cpp",

    "compilation": {
        "need": True,
        "cmd": "g++ -o {filename}.o {filename}",
        "executable": "{filename}.o",
        "limits": {
            "time": 1000,
            "vms": 104857600
        }
    },

    "execution": {
        "cmd": "./{filename}",
        "limits": {
            "time": 1000,
            "vms": 104857600
        }
    },

    "info": {
        "lang": "C++"
    }
}

py = {
    "extension": "py",

    "compilation": {
        "need": False
    },

    "execution": {
        "cmd": "python3 ./{filename}",
        "limits": {
            "time": 1000,
            "vms": 104857600
        }
    },

    "info": {
        "lang": "Python 3.4"
    }
}
