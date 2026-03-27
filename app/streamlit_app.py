import streamlit as st

from app.main import handle_user_query


st.set_page_config(page_title="Customer Support Chatbot", layout="wide")

st.title("Customer support RAG chatbot")
st.write("Demo of a rule-based routing, LLM powered chatbot, that retrieves chunks of an e-commerce company policies in order to answer simple customer support question. If the customer request is too complex, it simulates a handoff to a human operator with a ticketing system")

user_query = st.text_area("Enter a customer support request:")

if st.button("Submit") and user_query.strip():
    try:
        result = handle_user_query(user_query)

        st.subheader("Assistant Response")
        st.write(result["response"])

        with st.sidebar:
            st.header("Routing Info")
            st.write(f"**Type:** {result['type']}")
            st.write(f"**Category:** {result['category']}")
            st.write(f"**Reason:** {result['reason']}")

            if result["type"] == "auto_response" and result["documents"]:
                st.header("Retrieved Chunks")
                for doc in result["documents"]:
                    st.write(f"**Source:** {doc['source']}")
                    st.write(f"**Chunk ID:** {doc['chunk_id']}")
                    if "distance" in doc:
                        st.write(f"**Distance:** {doc['distance']:.4f}")
                    st.caption(doc["text"][:400] + "...")
                    st.markdown("---")

            elif result["type"] == "handoff":
                ticket = result["ticket"]

                st.header("Opened Ticket")
                st.write(f"**Ticket ID:** {ticket['ticket_id']}")
                st.write(f"**Created at:** {ticket['created_at']}")
                st.write(f"**Category:** {ticket['category']}")
                st.write(f"**Status:** {ticket['status']}")
                st.write(f"**Reason for handoff:** {ticket['reason_for_handoff']}")

                # with st.expander("Customer request summary"):
                #     st.write(ticket["customer_request"])

    except FileNotFoundError as e:
        st.error(str(e))
        st.info("Run the ingestion step first: python -m app.rag.ingest")

    except Exception as e:
        st.error(f"Unexpected error: {e}")