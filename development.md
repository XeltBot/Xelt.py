# Development

You'll need these installed on your machine:

- Python 3 (use 3.10)
- Poetry
- Optional: pyenv

> **Note**
> `uvloop` is used to speed up Xelt internally. uvloop depends on libuv, which is what node.js uses under the hood for its event loop. The maintainers of `uvloop` refuse to add support for Windows (see MagicStack/uvloop/#14 for more details), so Xelt probably will have to be developed on a Unix-like system. If you are using windows, then wsl2 is needed. Note that `uvloop` depends on openssl 1.1, so make sure to installed the headers and shared libs for that on your wsl2 distro.

## Basic setup steps

1. Get an poetry venv up and running (`poetry env use 3.10`)
2. Install the dependencies (`poetry install`)
3. Create a `.env` file in the root of the project with the following contents:

    ```env
    XELT_DEV_TOKEN="your bot token"
    ```

4. Run the bot (`poetry run python xelt.py`). The bot file can be found under the `bot` directory