import toml
from pathlib import Path
from typing import Union
import streamlit as st


def fix_email_prompt():
    # * this is a fix for the streamlit prompt for your email to subscribe to their newsletter
    streamlit_config_dir: Path = Path.home() / ".streamlit"
    streamlit_credentials_file: Path = streamlit_config_dir / "credentials.toml"
    if not streamlit_credentials_file.exists():
        streamlit_config_dir.mkdir(exist_ok=True)
        with open(streamlit_credentials_file, "w") as scf:
            toml.dump({"general": {"email": ""}}, scf)
        scf.close()


def get_url_query_parameters() -> dict[str, str]:
    query_params = st.experimental_get_query_params()
    for key, val in query_params.items():
        query_params[key] = val[0]
    return query_params


def redirect(url: str):
    nav_script = """
        <meta http-equiv="refresh" content="0; url='%s'">
    """ % (
        url
    )
    st.write(nav_script, unsafe_allow_html=True)


def inject_css(css: str) -> None:
    """
    Inject CSS into streamlit application.

    Args:
        css (str): css style string
    """
    st.markdown(f"<style>\n{css}\n</style>", unsafe_allow_html=True)


# todo: implement development mode
def make_app_start_command(
    app_path: Union[str, Path],
    open_browser: bool = False,
    development_mode: bool = False,
) -> list[str]:
    """
    subprocess start command for app

    Args:
        _open (bool, optional): open the GUI in the default browser window. Defaults to False.

    Returns:
        list[str]: the start command

    look into:
    --client.caching
    --client.displayEnabled
    --runner.installTracer
    --runner.postScriptGC
    --runner.fastReruns < this seems intuitively like there could be a security vulnerability
    --server.scriptHealthCheckEnabled
    --server.baseUrlPath
    --server.maxMessageSize
    --server.enableWebsocketCompression
    --server.enableStaticServing
    --magic.displayRootDocString
    --magic.displayLastExprIfNoSemicolon
    --deprecation.showfileUploaderEncoding
    --deprecation.showImageFormat
    --deprecation.showPyplotGlobalUse
    --global.showWarningOnDirectExecution False

    look into, but don't use:
    --server.sslCertFile * excerpt from CLI docs: DO NOT USE THIS OPTION IN A PRODUCTION ENVIRONMENT.
    --server.sslKeyFile * excerpt from CLI docs: DO NOT USE THIS OPTION IN A PRODUCTION ENVIRONMENT.

    maybe use:
    --server.maxUploadSize < not currently relevant

    added, but look into in more detail:
    --server.enableCORS
    --server.enableXsrfProtection

    ui, test differences:
    --ui.hideSidebarNav
    --theme.primaryColor
    --theme.backgroundColor
    --theme.secondaryBackgroundColor
    --theme.textColor
    --theme.font

    INFO
    --global.developmentMode > seems to be mostly used for developing streamlit components

    show text
    --theme.textColor "#0F5555"
    """

    return [
        "streamlit",
        "run",
        app_path,
        "--global.developmentMode=False",
        "--global.suppressDeprecationWarnings=False",
        "--logger.enableRich=True",
        "--client.showErrorDetails=True",
        "--client.toolbarMode=minimal",
        "--runner.magicEnabled=False",
        f"--server.headless={str(not open_browser)}",
        "--server.runOnSave=True",
        "--server.allowRunOnSave=True",
        "--server.enableCORS=True",
        "--server.enableXsrfProtection=True",
        "--browser.gatherUsageStats=False",
        # "--theme.base=dark",
        "--ui.hideTopBar=True",
        # "--theme.textColor=#0F1116",
        # "--theme.secondaryBackgroundColor=#0F1116",
        "--server.address=localhost",
        "--server.port=31415",
    ]


# ! temp archive


# def get_url_auth_code(query_params: dict[str, str]) -> Union[str, None]:
#     if not len(query_params):
#         return None
#     elif "code" not in query_params.keys():
#         return None
#     else:
#         return query_params["code"]
