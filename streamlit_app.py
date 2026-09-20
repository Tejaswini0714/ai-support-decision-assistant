import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Support Ticket Assistant")

st.title("AI Support Ticket Decision Assistant")


# -------------------------
# Login / Register
# -------------------------

if "token" not in st.session_state:
    st.session_state["token"] = None


if st.session_state["token"] is None:

    st.sidebar.header("Account")

    option = st.sidebar.selectbox(
        "Choose an option",
        ["Login", "Register"]
    )

    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input(
        "Password",
        type="password"
    )

    button = st.sidebar.button(option)

    if button and option == "Register":

        response = requests.post(
            f"{API_URL}/register",
            json={
                "email": email,
                "password": password
            }
        )

        if response.status_code == 200:
            st.sidebar.success(
                "Registration successful. Please login."
            )
        else:
            st.sidebar.error(
                f"Registration failed: {response.text}"
            )

    if button and option == "Login":

        response = requests.post(
            f"{API_URL}/login",
            json={
                "email": email,
                "password": password
            }
        )

        if response.status_code == 200:
            st.session_state["token"] = response.json()[
                "access_token"
            ]
            st.rerun()
        else:
            st.sidebar.error(
                f"Login failed: {response.text}"
            )

    st.info("Please login to use the support ticket assistant.")


# -------------------------
# Authenticated application
# -------------------------

else:

    token = st.session_state["token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    st.sidebar.header("Menu")

    page = st.sidebar.radio(
        "Select page",
        ["New Decision", "History"]
    )

    if st.sidebar.button("Logout"):
        st.session_state["token"] = None
        st.rerun()


    # -------------------------
    # New Decision
    # -------------------------

    if page == "New Decision":

        st.header("New Decision")

        message = st.text_area(
            "Support Ticket",
            placeholder="Enter the customer support ticket..."
        )

        if st.button("Get AI Decision"):

            if not message.strip():
                st.warning("Please enter a support ticket.")

            else:

                with st.spinner("Analyzing ticket..."):

                    response = requests.post(
                        f"{API_URL}/tickets",
                        headers=headers,
                        json={
                            "message": message
                        }
                    )

                if response.status_code == 200:

                    data = response.json()
                    decision = data["decision"]

                    st.success("Decision generated")

                    st.subheader("Recommendation")
                    st.write(decision["action"])

                    st.subheader("Confidence")
                    st.write(
                        f'{decision["confidence"] * 100:.1f}%'
                    )

                    st.subheader("Reasoning")
                    st.write(decision["reason"])

                    st.subheader("Sources")

                    for source in decision["sources"]:
                        st.write(f"- {source}")

                else:

                    st.error(
                        f"Failed to create decision: {response.text}"
                    )


    # -------------------------
    # History
    # -------------------------

    if page == "History":

        st.header("Decision History")

        response = requests.get(
            f"{API_URL}/tickets",
            headers=headers
        )

        if response.status_code == 200:

            tickets = response.json()

            if not tickets:
                st.info("No previous tickets found.")

            else:

                for ticket in tickets:

                    st.subheader(
                        f'Ticket #{ticket["id"]}'
                    )

                    st.write(ticket["message"])

                    if ticket["decision"]:

                        st.write(
                            f'Action: '
                            f'{ticket["decision"]["action"]}'
                        )

                        st.write(
                            f'Confidence: '
                            f'{ticket["decision"]["confidence"] * 100:.1f}%'
                        )

                        if st.button(
                            f'View Result #{ticket["id"]}',
                            key=f'view_{ticket["id"]}'
                        ):

                            detail_response = requests.get(
                                f'{API_URL}/tickets/{ticket["id"]}',
                                headers=headers
                            )

                            if detail_response.status_code == 200:

                                detail = detail_response.json()
                                decision = detail["decision"]

                                st.write(
                                    f'**Action:** {decision["action"]}'
                                )

                                st.write(
                                    f'**Confidence:** '
                                    f'{decision["confidence"] * 100:.1f}%'
                                )

                                st.write(
                                    f'**Reason:** {decision["reason"]}'
                                )

                                st.write("**Sources:**")

                                for source in decision["sources"]:
                                    st.write(f"- {source}")

                            else:

                                st.error(
                                    f"Unable to retrieve ticket: "
                                    f"{detail_response.text}"
                                )

                    st.divider()

        else:

            st.error(
                f"Unable to load history: {response.text}"
            )