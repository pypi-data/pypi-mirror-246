import rich_click as click

from pycooltext import cooltext
from pick import pick
from ci.utility import terminal, validation
from ci import system
from ci import env

# import subprocess
# from ci.api import system
# from ci.gui import APP_PATH
# from ci.utility import terminal, validation
# from ci.auth import status, LocalAccountStatus

# todo: add terms/TOS
# todo: add plugins (extra open source packages with in built tools)


class ConsoleSequence:
    @staticmethod
    def run_account_register():
        first_name = terminal.first_name_input()
        last_name = terminal.last_name_input()
        email = terminal.email_input()
        while not validation.check_email_format(email=email, verbose=True):
            email = terminal.email_input()
        result = system.account.register(
            email=email, first_name=first_name, last_name=last_name
        )
        print()
        if result.is_ok():
            terminal.success_output(result.ok_value)
            terminal.info_output("Please check your email for a temporary password.")
        else:
            terminal.failure_output(result.err_value)

    @staticmethod
    def run_account_confirm():
        temporary_password = terminal.secure_input(
            "\nPlease enter the temporary password emailed to you.\n"
        )
        new_password = terminal.set_new_password_input()
        while not validation.check_password(new_password, verbose=True):
            new_password = terminal.set_new_password_input()
        # result = nexus.account.confirm(email=#todo
        #     temporary_password=temporary_password, new_password=new_password
        # )

    @staticmethod
    def run_account_login():
        # todo: check if already logged in (tokens cached), warn logging in again overrides previous
        email = terminal.email_input()
        while not validation.check_email_format(email=email, verbose=True):
            email = terminal.email_input()
        password = terminal.password_input()
        result = system.account.login(email=email, password=password)
        print()
        if result.is_ok():
            terminal.success_output(result.ok_value)
        else:
            terminal.failure_output(result.err_value)


@click.group(name="ci", invoke_without_command=True, help="Cephalon Interface CLI.")
@click.version_option(env.VERSION, prog_name=env.NAME)
@click.pass_context
def entry(ctx):
    if ctx.invoked_subcommand is None:
        cooltext("CI")
        terminal.write(f"[deep_sky_blue3]version [dark_orange]{env.VERSION}")
        if system.account.authenticated:
            terminal.write("authenticated", color="light_green")
        else:
            terminal.write("not logged in", color="red")


@entry.command(name="register", help="Register a new account.")
@click.option(
    "--confirm/--no-confirm",
    "-c/-nc",
    type=bool,
    default=True,
    help="Include the email confirmation step",
)
def account_register(confirm: bool) -> None:
    ConsoleSequence.run_account_register()
    if confirm:
        ConsoleSequence.run_account_confirm()


@entry.command(name="confirm", help="Confirm your email address.")
def account_confirm():
    ConsoleSequence.run_account_confirm()


@entry.command(name="login", help="Login to an existing account.")
def account_login():
    ConsoleSequence.run_account_login()


# @account.command(name="info", help="View account information.")
# def account_info():
#     pass


# @account.command(name="password", help="Request a password reset.")
# def account_password():
#     pass


# @account.command(name="resources", help="View table of available resources.")
# def account_resources():
#     pass


# @account.command(name="enable", help="Request access to a particular resource.")
# def account_enable():
#     pass


# @entry.group(name="system", help="System interface utilities.")
# def system():
#     pass


# @system.command(name="start", help="Start the local graphical user interface.")
# def system_start():
#     pass


# @account.command(name="status")
# def account_status() -> None:
#     _status = status()
#     terminal.write(f"\nAccount Status: {_status.value.upper()}\n")
#     if _status == LocalAccountStatus.UNINITIALIZED:
#         terminal.info_output("To register, run the following command:")
#         terminal.command_output("ci account register\n")
#         terminal.info_output("To login, run the following command:")
#         terminal.command_output("ci account login")
#     elif _status == LocalAccountStatus.EMAIL_UNVERIFIED:
#         pass


# @account.command(name="register", help="Register a new account.")
# def register():


# # @entry.group(name="account", invoke_without_command=True, help="todo")
# # def account():
# #     pass


# # @entry.command(name="signup", help="Sign up for an account.")


# # @entry.command(name="login", help="Log in to an existing account.")
# # def login():


# # @entry.command(name="logout", help="Log out of currently logged in account.")
# # def logout():
# #     pass


# # @entry.group(name="")
# # @entry.command(name="start")
# # @click.option(
# #     "--open-browser/--no-open-browser",
# #     "-o/-no",
# #     type=bool,
# #     default=False,
# #     required=True,
# #     help="Open the app automatically in a browser window.",
# # )
# # def start(open_browser: bool):
# #     subprocess.run(
# #         util.make_streamlit_app_start_command(
# #             app_path=str(APP_PATH),
# #             open_browser=open_browser,
# #         )
# #     )


# # @entry.group(invoke_without_command=True)
# # def account():
# #     pass
