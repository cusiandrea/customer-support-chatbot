from app.routing.router import route_query
from app.rag.retriever import PolicyRetriever
from app.rag.generator import generate_response
from app.escalation.handoff import generate_handoff_message


retriever = PolicyRetriever()


def handle_user_query(user_query: str):
    routing_result = route_query(user_query)

    if routing_result["route"] == "simple":
        chunks = retriever.retrieve(user_query, top_k=2)
        response = generate_response(user_query, chunks)

        return {
            "type": "auto_response",
            "category": routing_result["category"],
            "reason": routing_result["reason"],
            "response": response,
            "documents": chunks
        }

    handoff = generate_handoff_message(
        user_query=user_query,
        category=routing_result["category"],
        reason=routing_result["reason"]
    )

    return {
        "type": "handoff",
        "category": routing_result["category"],
        "reason": routing_result["reason"],
        "response": handoff["customer_message"],
        "ticket": handoff["ticket"],
        "documents": []
    }