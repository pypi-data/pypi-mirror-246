import streamlit as st
from fuzzywuzzy import fuzz, process
from streamlit_searchbox import st_searchbox
from ci import env
from ci import system
from ci.use import streamlit
from ci.gui.node import testing


st.set_page_config(
    page_title=env.PACKAGE_NAME_TITLE,
    page_icon=env.CFG_PAGE_ICON,
    layout=env.CFG_LAYOUT,
    initial_sidebar_state=env.CFG_INITIAL_SIDEBAR_STATE,
)

streamlit.inject_css(env.OBJ_THEME)


def auth_instructions() -> None:
    _, logo_col, _ = st.columns([4, 1, 4])
    with logo_col:
        st.markdown("# ")
        st.image(env.OBJ_LOGO)
    _, main_col, _ = st.columns([1, 1, 1])
    with main_col:
        st.markdown("# ")
        st.write("To create an account, run the following command in your terminal:")
        st.code("ci register", language="bash")
        st.write("To login to an account, run the following command in your terminal:")
        st.code("ci login", language="bash")
        st.write("To reset your password, run the following command in your terminal:")
        st.code("ci password", language="bash")
        st.write("# ")
        refresh_button = st.button("Refresh", use_container_width=True)
        if refresh_button:
            st.rerun()


nodes = {
    "page/testing": testing,
}


def search_nodes(query: str) -> list[str]:
    matches = process.extract(query, nodes.keys(), scorer=fuzz.token_sort_ratio)
    sorted_matches = sorted(matches, key=lambda x: x[1], reverse=True)
    result = [match[0] for match in sorted_matches]
    return result


def home() -> None:
    with st.sidebar:
        _, lc, _ = st.columns([1, 2, 1])
        with lc:
            st.image(env.OBJ_LOGO)
        st.markdown(f"# Cephalon Interface :blue[{env.PACKAGE_VERSION}]")
        selected_value = st_searchbox(
            search_function=search_nodes,
            key="searchbox",
            placeholder="Search...",
            default_options=list(nodes.keys()),
        )
    if selected_value:
        nodes[selected_value].render()
    else:
        st.write("Search for a tool in the sidebar.")


def main() -> None:
    if not system.account.authenticated:
        auth_instructions()
    else:
        home()


if __name__ == "__main__":
    main()
