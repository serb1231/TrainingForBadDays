import json
import logging

from flask import Blueprint, request, abort, jsonify

from app.AI.AIMock import AIMock
from app.memory.ContextManager import ContextManager
from app.memory.ConversationHistories import ConversationHistories

chat_bp = Blueprint('chat', __name__)

SECRET_PASSWORD = 'BCG-X-SECRET-KEY'

conversations : ConversationHistories = ConversationHistories()

context_manager = ContextManager(5)
llm = AIMock()

logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

def authenticate():

    authentication_header = request.headers.get('Authorization')
    # Validate the token (you can hard-code a secret like BCG-X-SECRET-KEY).
    # Return 401 Unauthorized if invalid/missing.
    if not authentication_header or authentication_header.split()[-1] != SECRET_PASSWORD:
        abort(401, "Authorization Failed: Incorrect Token")



@chat_bp.post('/api/v1/chat/completions')
def completions():
    data = request.get_json()
    session_id = data.get("session_id")
    message = data.get('message')
    logger.debug(f"received request: session id: {session_id}; message: {message}")

    authenticate()

    conversations.verify_existence_and_insert(session_id)

    # Append the new user message to the history.
    conversations.append(session_id, {"role" : "user",  "content" : message})

    # Retrieve the conversation history for session_id from memory.
    conversation_history = conversations.get_all(session_id)

    # Pass the history through the Context Manager (details below).
    truncated_history : list[dict[str, str]] = context_manager.truncate(conversation_history)
    # Send the truncated history to the Mock LLM.
    llm_response : str = llm.acceptMessage(truncated_history)
    # Save the LLM's response to the history and return it to the client.
    conversations.append(session_id, {"role" : "assistant",  "content" :llm_response})

    return jsonify({
              "session_id": session_id,
              "response": {"role" : "assistant",  "content" :llm_response},
              "total_messages_in_context": len(conversations.get_all(session_id))
            })

@chat_bp.get('/api/v1/chat/history/<session_id>')
def get_memory(session_id):
    logger.debug(f"received get history request from: {session_id}")
    if not session_id or not conversations.verify_existence(session_id):
        abort(400, "User not found")
    authenticate()

    # fetch history
    history = conversations.get_all(session_id)
    # Returns the full, un-truncated conversation history for that session.
    return jsonify({"session_id": session_id, "history": history})


@chat_bp.delete('/api/v1/chat/history/<session_id>')
def clear_memory(session_id):
    logger.debug(f"received delete history request from: {session_id}")
    if not session_id or not conversations.verify_existence(session_id):
        abort(400, "User not found")
    authenticate()
    # Clears the memory for that specific session.
    conversations.pop(session_id)

    # Returns a 204 No Content status.
    return '', 204