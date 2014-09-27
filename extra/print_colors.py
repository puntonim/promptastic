import subprocess


def foreground(color):
    return '$(tput setaf {})'.format(color)


def background(color):
    return '$(tput setab {})'.format(color)


def reset():
    return '$(tput sgr0)'


if __name__ == '__main__':
    for i in range(256):
        subprocess.call(
            'echo "{}{}user_name@localhost{} background={}"'.format(
                foreground(15),
                background(i),
                reset(),
                i
            ),
            shell=True
        )