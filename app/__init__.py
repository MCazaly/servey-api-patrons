from flask import Flask

name = "Flask App"

app = Flask(name)


def main():
    app.run()


if __name__ == "__main__":
    main()
